from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
from apps.shop.plugshop.utils import get_categories


class CategoryAbstractManager(TreeManager):
    def get_by_path(self, path):
        path_patterns = path.split('/')
        slug = path_patterns[-1]
        return self.get(slug=slug)


class CategoryAbstract(MPTTModel):

    objects = CategoryAbstractManager()

    class Meta:
        abstract = True
        verbose_name = _(u'category')
        verbose_name_plural = _(u'categories')

    class MPTTMeta:
        ordering = ['pk', 'lft']

    parent = TreeForeignKey('self', null=True, blank=True,
                            verbose_name=_(u'parent node'), on_delete=models.CASCADE)
    name = models.CharField(_(u'name'), blank=False, max_length=80)
    slug = models.SlugField(_(u'slug'), blank=False, unique=True)
    weight = models.IntegerField(_('weight'), null=True)
    sku = models.CharField(_('SKU'), null=True, max_length=200)

    def __str__(self):
        return self.name

    def get_ancestor_list(self):
        categories = get_categories()
        return [n for n in categories if n.lft <= self.lft and
                n.rght >= self.rght and n.tree_id == self.tree_id]

    def get_path(self):
        ancestors = self.get_ancestor_list()
        return "/".join([a.slug for a in ancestors])

    def get_absolute_url(self):
        return reverse('plugshop-category', kwargs={'category_path': self.get_path()})
