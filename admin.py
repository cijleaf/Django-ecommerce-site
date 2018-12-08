from django.contrib import admin
from django.utils.translation import ugettext as _
from django.contrib.admin.views.main import ChangeList

from .plugshop.admin import BaseProductAdmin, BaseOrderAdmin

from apps.shop.models import *
from apps.shop.forms import ProductAdminForm, CategoryAdminForm
from imagekit.admin import AdminThumbnail


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    thumbnail = AdminThumbnail(image_field='image_admin')
    readonly_fields = ('thumbnail',)
    min_num = 1
    max_num = 1


class ProductVideoInline(admin.TabularInline):
    model = ProductVideo
    extra = 0


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 0


class ProductAdmin(BaseProductAdmin):
    form = ProductAdminForm
    list_display = (
        'name',
        'price',
        'thumbnail',
        'is_active',
        'sort',
        'weight',
        'sku'
    )
    list_editable = (
        'is_active', 
        'sort',
    )
    inlines = (
        ProductImageInline,
        ProductVideoInline,
        ProductOptionInline,
    )
    
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'slug',
                'category',
                'short_description',
                'description',
                'price',
                'is_active',
                'sort',
                'weight',
                'sku'
            )
        }),
        # ('Extra', {
        #     #'classes': ('collapse',),
        #     'fields': (
        #         'order',
        #         'suggestions',
        #     )
        # }),
        ('Meta', {
            #'classes': ('collapse closed',),
            'fields': (
                'meta_title',
                'meta_keywords',
                'meta_description',
            )
        }),
    )
    thumbnail = AdminThumbnail(image_field=lambda x: x.get_cover().image_admin)
    thumbnail.short_description = 'preview'


class OrderAdminChangeList(ChangeList):

    def get_total_values(self, queryset):
        totals = {}
        for field in self.fields_to_total:
            totals[field] = sum([getattr(p, field) for p in queryset])
        return totals

    def get_results(self, request):
        super(OrderAdminChangeList, self).get_results(request)


class OrderAdmin(BaseOrderAdmin):
    
    fields_to_total = ('price_total',)
    search_fields = (
        'number', 
        'user__email', 
        'user__first_name', 
        'user__last_name',
    )
    list_display = (
        'number',
        'user',
        'get_user_name',
        'status',
        'price_total',
        'created_at',
        'updated_at',
        'delivered_at',
    )
    list_per_page = 15
    readonly_fields = (

    )

    def get_changelist(self, request, **kwargs):
        return OrderAdminChangeList
           
    def get_user_name(self, inst):
        user = inst.user
        return "%s %s" % (user.first_name, user.last_name)
    get_user_name.short_description = 'name'


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = (
        'name', 
        'slug',
        'is_active',
        'sort',
    )
    list_editable = ('is_active','sort',)


class ShippingTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'require_address',
        'require_zip_code',
        'is_active',
        'sort',
    )
    list_editable = (
        'is_active',
        'sort',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingType, ShippingTypeAdmin)
admin.site.register(Option)