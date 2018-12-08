from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20181113_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='sku',
            field=models.CharField(max_length=200, null=True, verbose_name='SKU'),
        ),
        migrations.AddField(
            model_name='category',
            name='weight',
            field=models.IntegerField(null=True, verbose_name='weight'),
        ),
    ]
