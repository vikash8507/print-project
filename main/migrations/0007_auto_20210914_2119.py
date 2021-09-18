# Generated by Django 3.2.7 on 2021-09-14 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210914_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='address1',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='voter',
            name='address2',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='voter',
            name='barcode',
            field=models.ImageField(blank=True, null=True, upload_to='barcodes/'),
        ),
        migrations.AlterField(
            model_name='voter',
            name='birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]