from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class OrderProductsAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('order product')
        verbose_name_plural = _('order product')

    quantity = models.PositiveIntegerField(_('quantity'), blank=False,
                                           null=False, default=1)
    order = models.ForeignKey(settings.ORDER_MODEL, verbose_name=_('order'),
                              related_name='ordered_items', on_delete=models.CASCADE)
    product = models.ForeignKey(settings.PRODUCT_MODEL,
                                verbose_name=_('product'), on_delete=models.CASCADE)

    def price(self):
        return self.product.price * self.quantity
    price.short_description = _('Total price')

