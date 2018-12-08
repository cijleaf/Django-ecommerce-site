from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.fields import TreeForeignKey
from apps.shop.plugshop.utils import get_categories
from django.urls import reverse, reverse_lazy


class ProductAbstract(models.Model):

    category = TreeForeignKey(settings.CATEGORY_MODEL, blank=True, null=True,
                              verbose_name=_('category'),
                              related_name='products', on_delete=models.CASCADE)
    name = models.CharField(_('name'), blank=False, max_length=200)
    slug = models.SlugField(_('slug'), blank=False, unique=True)
    price = models.PositiveIntegerField(_('price'), blank=False)
    weight = models.IntegerField(_('weight'), null=True)
    sku = models.CharField(_('SKU'), null=True, max_length=200)

    class Meta:
        abstract = True
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        categories = get_categories()
        try:
            category = list(filter(lambda x: x.pk == self.category_id, categories))[0]
            category_path = category.get_path()

        except IndexError:
            category_path = "-"

        return reverse('plugshop-product', kwargs={
            'category_path': category_path,
            'slug': self.slug,
        })
