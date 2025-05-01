# -*- coding: UTF-8 -*-
# Copyright 2008-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

from lino_xl.lib.excerpts.mixins import Certifiable
from lino_xl.lib.accounting.utils import HUNDRED
from lino_xl.lib.accounting.choicelists import TradeTypes
from lino_xl.lib.vat.mixins import QtyVatItemBase, VatVoucher
from lino_xl.lib.vat.utils import add_vat, remove_vat
from lino_xl.lib.vat.mixins import get_default_vat_regime, myround
from lino_xl.lib.contacts.mixins import PartnerPrintable
from lino_xl.lib.vat.choicelists import VatAreas, VatRules

from lino.api import dd, rt, _


class SalesPrintable(PartnerPrintable, Certifiable):

    class Meta:
        abstract = True

    subject = models.CharField(_("Subject"), max_length=200, blank=True)
    paper_type = dd.ForeignKey('trading.PaperType', null=True, blank=True)

    # channel = Channels.field(default='paper')

    def get_excerpt_templates(self, bm):
        # Overrides lino_xl.lib.excerpts.mixins.Certifiable.get_excerpt_templates

        pt = self.paper_type or get_paper_type(self.get_partner())
        if pt and pt.template:
            # print(20190506, pt.template)
            return [pt.template]

    def get_printable_context(self, ar):
        context = super().get_printable_context(ar)
        context.update(
            site_company=settings.SITE.get_config_value('site_company'))
        return context


class TradingVoucher(SalesPrintable, VatVoucher):

    class Meta:
        abstract = True

    edit_totals = False

    intro = models.TextField(_("Introductive text"), blank=True)
    default_discount = dd.PercentageField(_("Discount"), blank=True, null=True)

    def get_trade_type(self):
        return TradeTypes.sales

    def add_voucher_item(self, product=None, qty=None, **kw):
        if product is not None:
            Product = rt.models.products.Product
            if not isinstance(product, Product):
                product = Product.objects.get(pk=product)
            # if qty is None:
            # qty = Duration(1)
        kw['product'] = product
        kw['qty'] = qty
        i = super().add_voucher_item(**kw)
        return i


dd.update_field(TradingVoucher, 'total_base', editable=False)
dd.update_field(TradingVoucher, 'total_vat', editable=False)
dd.update_field(TradingVoucher, 'total_incl', editable=False)


def get_paper_type(obj):
    sr = getattr(obj, 'salesrule', None)
    if sr:
        return sr.paper_type


class TradingVoucherItem(QtyVatItemBase):

    class Meta:
        abstract = True

    product = dd.ForeignKey('products.Product', blank=True, null=True)
    description = dd.RichTextField(_("Description"),
                                   blank=True,
                                   null=True,
                                   bleached=True)
    discount = dd.PercentageField(_("Discount"), blank=True, null=True)

    def get_base_account(self, tt, ar=None):
        # if self.product is None:
        #     return tt.get_base_account(ar)
        return tt.get_product_base_account(self.product, ar)
        # return self.voucher.journal.chart.get_account_by_ref(ref)

    def get_default_vat_class(self, tt):
        if self.product and self.product.vat_class:
            return self.product.vat_class
        return super().get_default_vat_class(tt)

    def discount_changed(self, ar=None):
        if not self.product:
            return

        tt = self.voucher.get_trade_type()
        catalog_price = tt.get_catalog_price(self.product)
        # catalog_price = self.product.get_catalog_price(tt, self.voucher.partner)

        if catalog_price is None:
            return
        # assert self.vat_class == self.product.vat_class
        rule = self.get_vat_rule(tt)
        if rule is None:
            return
        va = VatAreas.get_for_country()
        cat_rule = VatRules.get_vat_rule(
            va, tt, get_default_vat_regime(), self.vat_class, dd.today())
        if cat_rule is None:
            return
        if rule.rate != cat_rule.rate:
            catalog_price = remove_vat(catalog_price, cat_rule.rate)
            catalog_price = add_vat(catalog_price, cat_rule.rate)

        if self.discount is None:
            dsc = self.voucher.default_discount
        else:
            dsc = self.discount
        if dsc is None:
            self.unit_price = myround(catalog_price)
        else:
            self.unit_price = myround(catalog_price * (HUNDRED - dsc) / HUNDRED)
        self.unit_price_changed(ar)

    def product_changed(self, ar=None):
        if self.product:
            self.title = dd.babelattr(self.product, 'name')
            self.body = dd.babelattr(self.product, 'body')
            if self.qty is None:
                self.qty = Decimal("1")
            self.discount_changed(ar)

    def full_clean(self):
        super().full_clean()
        if self.total_incl and not self.product:
            tt = self.voucher.get_trade_type()
            if self.get_base_account(tt) is None:
                raise ValidationError(
                    _("You must specify a product if there is an amount."))
