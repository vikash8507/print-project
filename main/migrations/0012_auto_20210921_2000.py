# Generated by Django 3.2.7 on 2021-09-21 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20210921_1950'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voter',
            old_name='partname',
            new_name='partname1',
        ),
        migrations.AddField(
            model_name='voter',
            name='partname2',
            field=models.CharField(default='', max_length=100),
        ),
    ]
