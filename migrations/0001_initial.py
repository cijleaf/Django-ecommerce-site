from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('short_description', models.TextField(blank=True, verbose_name='short_description')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('sort', models.PositiveSmallIntegerField(default=1, verbose_name='sort')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Category', verbose_name='parent node')),
            ],
            options={
                'verbose_name': 'verbose_name',
                'verbose_name_plural': 'verbose_name_plural',
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'verbose_name',
                'verbose_name_plural': 'verbose_name_plural',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(editable=False, max_length=10, unique=True, verbose_name='order number')),
                ('status', models.IntegerField(choices=[(1, 'Created'), (2, 'Confirmed'), (3, 'Denied'), (4, 'Shipped'), (5, 'Completed')], default=1, verbose_name='order status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('delivered_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='delivery date')),
                ('city', models.CharField(blank=True, max_length=80, null=True, verbose_name='city')),
                ('address', models.TextField(blank=True, null=True, verbose_name='address')),
                ('zip_code', models.CharField(blank=True, max_length=24, null=True, verbose_name='zip_code')),
                ('phone', models.CharField(max_length=80, verbose_name='phone')),
                ('ip_address', models.CharField(blank=True, max_length=80, null=True, verbose_name='IP')),
                ('comment', models.TextField(blank=True, verbose_name='comment')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'order',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_items', to='shop.Order', verbose_name='order')),
            ],
            options={
                'verbose_name': 'order product',
                'verbose_name_plural': 'order product',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_title', models.CharField(blank=True, max_length=200, verbose_name='meta_title')),
                ('meta_keywords', models.CharField(blank=True, max_length=300, verbose_name='meta_keywords')),
                ('meta_description', models.TextField(blank=True, verbose_name='meta_description')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('price', models.PositiveIntegerField(verbose_name='price')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('short_description', models.TextField(blank=True, verbose_name='short_description')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('sort', models.PositiveSmallIntegerField(default=1, verbose_name='sort')),
                ('category', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.Category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'verbose_name',
                'verbose_name_plural': 'verbose_name_plural',
                'ordering': ('sort',),
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.PositiveSmallIntegerField(default=1, verbose_name='sort')),
                ('image', models.ImageField(upload_to='uploads/products/', verbose_name='image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.Product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'verbose_name',
                'verbose_name_plural': 'verbose_name_plural',
                'ordering': ('sort',),
            },
        ),
        migrations.CreateModel(
            name='ProductOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(default='', max_length=200, verbose_name='value')),
                ('sort', models.PositiveSmallIntegerField(default=1, verbose_name='sort')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Option', verbose_name='option')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='shop.Product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'verbose_name',
                'verbose_name_plural': 'verbose_name_plural',
                'ordering': ('sort',),
            },
        ),
        migrations.CreateModel(
            name='ProductVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('embeded', models.TextField(verbose_name='embeded')),
                ('sort', models.PositiveSmallIntegerField(default=1, verbose_name='sort')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='shop.Product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'verbose_name',
                'verbose_name_plural': 'verbose_name_plural',
                'ordering': ('sort',),
            },
        ),
        migrations.CreateModel(
            name='ShippingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='price')),
                ('require_address', models.BooleanField(default=False, verbose_name='require_address')),
                ('require_zip_code', models.BooleanField(default=False, verbose_name='require_zip_code')),
                ('help', models.TextField(blank=True, null=True, verbose_name='help')),
                ('sort', models.PositiveSmallIntegerField(default=1, verbose_name='sort')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
            ],
            options={
                'verbose_name': 'verbose_name',
                'verbose_name_plural': 'verbose_name_plural',
                'ordering': ('sort',),
            },
        ),
        migrations.AddField(
            model_name='orderproducts',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product', verbose_name='product'),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='products', through='shop.OrderProducts', to='shop.Product', verbose_name='products'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='shop.ShippingType', verbose_name='shipping_type'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
