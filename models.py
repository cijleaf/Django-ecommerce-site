# encoding: utf-8
import datetime

from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToCover, ResizeToFit, \
    ResizeCanvas, Anchor
from pytils import numeral
import csv

from apps.core.models import MetaPage
from apps.shop.templatetags.plugshop import plugshop_currency
from apps.utils import upload_to
from .plugshop.models.category import CategoryAbstract
from .plugshop.models.order import OrderAbstract
from .plugshop.models.order_products import OrderProductsAbstract
from .plugshop.models.product import ProductAbstract
from .plugshop.settings import STATUS_CHOICES_FINISH
from .plugshop.utils import get_categories


class ShippingType(models.Model):

    class Meta:
        verbose_name = 'delivery method'
        verbose_name_plural = 'delivery methods'
        ordering = ('sort',)

    name = models.CharField('delivery method', blank=False, max_length=100)
    price = models.PositiveIntegerField('price', blank=False, default=0)
    require_address = models.BooleanField('you must specify the address',
                                            default=False)
    require_zip_code = models.BooleanField('index is required',
                                            default=False)
    help = models.TextField('hint', blank=True, null=True)
    sort = models.PositiveSmallIntegerField('sorting', default=1)
    is_active = models.BooleanField('active', default=True)
    
    def has_requirements(self):
        return self.require_address or self.require_zip_code
    
    def __str__(self):
        return self.name


class Order(OrderAbstract):
    
    class Meta:
        verbose_name  = 'order'
        verbose_name_plural = 'orders'
        ordering = ['-created_at']
        
    shipping_type = models.ForeignKey(ShippingType, 
                                        verbose_name='delivery method',
                                        related_name='orders', on_delete=models.CASCADE)
    city = models.CharField('city', blank=True, null=True, max_length=80)
    address = models.TextField('delivery address', blank=True, null=True)
    zip_code = models.CharField('index', blank=True, null=True,
                                max_length=24)
    phone = models.CharField('phone', blank=False, max_length=80)
    ip_address = models.CharField('IP', blank=True, null=True, max_length=80)
    comment = models.TextField('comment', blank=True)
    csv_file = models.FileField(upload_to='csv/', null=True, blank=True)

    def price_without_shipping(self):
        return super(Order, self).price_total()
    
    def price_total(self):
        price = super(Order, self).price_total()
        shipping_price = self.shipping_type.price
        return price + shipping_price


class OrderProducts(OrderProductsAbstract):
    class Meta:
        verbose_name = _('order product')
        verbose_name_plural = _('order product')


class Category(CategoryAbstract):
    short_description = models.TextField('short description', blank=True)
    description = models.TextField('description', blank=True)
    is_active = models.BooleanField('active', default=True)
    sort = models.PositiveSmallIntegerField('sorting', default=1)
    
    def get_first_product(self):
        try:
            return self.products.all()[0]
        except IndexError:
            return None
    
    class Meta:
        ordering = ['sort']
        verbose_name  = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(ProductAbstract, MetaPage):

    class Meta:
        ordering = ('sort', )
        verbose_name  = 'product'
        verbose_name_plural = 'products'
        
    is_active = models.BooleanField('active', default=True)
    short_description = models.TextField('short description', blank=True)
    description = models.TextField(_(u'описание'), blank=True)
    sort = models.PositiveSmallIntegerField('description', default=1)
    
    def get_cover(self):
        coverset = ProductImage.objects.filter(product=self)
        if (len(coverset)):
            return coverset[0]

    def has_video(self):
        return len(ProductVideo.objects.filter(product=self)) > 0
        
    def label_buy(self):
        currency = plugshop_currency(self.price)
        label = numeral.choose_plural(self.price, ('ruble', 'ruble', 'rubles'))
        return 'Buy for %s %s' % (currency, label)


class Option(models.Model):

    name = models.CharField('Name', blank=False, max_length=200,
                            unique=True)
                            
    class Meta:
        verbose_name = 'option'
        verbose_name_plural = 'product options'
        
    def __str__(self):
        return self.name


class ProductImage(models.Model):

    product = models.ForeignKey(Product, verbose_name='product',
                                        related_name='images', on_delete=models.CASCADE)
    sort = models.PositiveSmallIntegerField('sorting', default=1)
    image = models.ImageField('picture',
                              upload_to=upload_to('products'))

    image_admin = ImageSpecField(source='image', 
                                    processors=[ResizeToCover(100, 100)], 
                                    format='JPEG', options={'quality': 90})

    image_banner = ImageSpecField(source='image', 
                                    processors=[ResizeToFit(250, 250),
                                                ResizeCanvas(250, 250, 
                                                        anchor=Anchor.CENTER)], 
                                    format='PNG')
                                
    image_product = ImageSpecField(source='image', 
                                    processors=[ResizeToFit(280, 280),
                                                ResizeCanvas(280, 280, 
                                                    anchor=Anchor.CENTER)], 
                                    format='PNG')
                                
    image_category = ImageSpecField(source='image', 
                                    processors=[ResizeToFit(160, 160),
                                                ResizeCanvas(160, 160, 
                                                        anchor=Anchor.CENTER)], 
                                    format='PNG')
                                
    image_list = ImageSpecField(source='image', 
                                processors=[ResizeToFit(160, 160),
                                            ResizeCanvas(160, 160, 
                                                anchor=Anchor.CENTER)], 
                                 format='PNG')

    image_cart = ImageSpecField(source='image', 
                                processors=[ResizeToFit(86, 86),
                                            ResizeCanvas(86, 86, 
                                                        anchor=Anchor.CENTER)], 
                                format='PNG')

    class Meta:
        verbose_name = 'product image'
        verbose_name_plural = 'product images'
        ordering = ('sort', )


class ProductVideo(models.Model):
    class Meta:
        verbose_name = 'product video'
        verbose_name_plural = 'product video'
        ordering = ('sort', )
        
    product = models.ForeignKey(Product, verbose_name='product',
                                        related_name='videos', on_delete=models.CASCADE)
    embeded = models.TextField('Code for video', blank=False)
    sort = models.PositiveSmallIntegerField('sorting', default=1)


class ProductOption(models.Model):
    class Meta:
        ordering = ('sort',)
        verbose_name = 'Product Detail'
        verbose_name_plural = 'product characteristics'
        
    product = models.ForeignKey(Product, verbose_name='product',
                                        related_name='options', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, verbose_name='option', on_delete=models.CASCADE)
    value = models.CharField('value', blank=False, max_length=200,
                            default="")
    sort = models.PositiveSmallIntegerField('sorting', default=1)

    def __str__(self):
        o = self.option
        return "%s = %s" % (o.name, self.value)
        

@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    pass

@receiver(pre_save, sender=Order)
def set_delivered(sender, instance, **kwargs):
    if instance.status == STATUS_CHOICES_FINISH:
        instance.delivered_at = datetime.datetime.now()
    else:
        instance.delivered_at = None


@receiver(pre_save, sender=Order)
def generate_number(sender, instance, **kwargs):
    if instance.id is None:
        now = datetime.datetime.now()
        hour_from = datetime.datetime(now.year, now.month, now.day, now.hour)
        hour_till = hour_from + datetime.timedelta(hours=1)

        today_orders = Order.objects.filter(Q(created_at__gte=hour_from),
                                                  Q(created_at__lt=hour_till))

        today_orders_nums = [0]
        for o in today_orders:
            num = str(o.number)[8:]
            try:
                today_orders_nums.append(int(num))
            except ValueError:
                today_orders_nums.append(max(today_orders_nums))

        num = max(today_orders_nums) + 1
        instance.number = u"%s%s" % (now.strftime('%y%m%d%H'), num)

post_save.connect(get_categories, sender=Category)