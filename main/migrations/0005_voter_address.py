# Generated by Django 3.2.7 on 2021-09-14 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_voter_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='voter',
            name='address',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
