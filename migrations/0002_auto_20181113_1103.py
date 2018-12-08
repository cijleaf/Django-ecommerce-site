from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(max_length=200, null=True, verbose_name='SKU'),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.IntegerField(null=True, verbose_name='weight'),
        ),
    ]
