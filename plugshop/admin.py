from django.contrib import admin
from django.apps import apps
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from mptt.admin import MPTTModelAdmin


class BaseProductAdmin(admin.ModelAdmin):
    inlines = ()
    search_fields = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }
    list_display = (
        'name',
        'slug',
        'price',
    )
    list_filter = (
        'category',
    )

    def changelist_view(self, request, extra_context=None):
        ctx = {}
        return super(BaseProductAdmin, self).changelist_view(request,
                                                             extra_context=ctx)


class BaseCategoryAdmin(MPTTModelAdmin):
    change_list_template = 'admin/category/change_list.html'
    mptt_level_indent = 20
    prepopulated_fields = {
        'slug': ('name', )
    }
    list_display = (
        'name',
        'get_products',
        'slug',
    )

    def get_products(self, instance):
        return "<br/>".join(p.name for p in instance.products.all())
    get_products.allow_tags = True
    get_products.short_description = _(u'products')



class BaseOrderProductsInline(admin.TabularInline):
    model = apps.get_model(settings.ORDER_PRODUCTS_MODEL)
    extra = 0


class BaseOrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    inlines = (
        BaseOrderProductsInline,
    )
    search_fields = ('number', 'user',)
    list_display = (
        'number',
        'user',
        'status',
        'price_total',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'status',
        'created_at',
    )

