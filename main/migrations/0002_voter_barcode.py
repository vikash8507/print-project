# Generated by Django 3.2.7 on 2021-09-14 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voter',
            name='barcode',
            field=models.ImageField(default='default.png', upload_to='barcode/'),
        ),
    ]