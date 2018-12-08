from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20181113_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='csv_file',
            field=models.FileField(blank=True, null=True, upload_to='csv/'),
        ),
    ]
