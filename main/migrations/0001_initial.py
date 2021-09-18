# Generated by Django 3.2.7 on 2021-09-13 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('epic', models.CharField(max_length=20, unique=True)),
                ('name1', models.CharField(max_length=100)),
                ('name2', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('block', models.CharField(max_length=100)),
                ('subblock', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('gname1', models.CharField(max_length=100)),
                ('gname2', models.CharField(max_length=100)),
                ('partno', models.CharField(max_length=100)),
                ('partname', models.CharField(max_length=100)),
                ('serialno', models.CharField(max_length=100)),
                ('polling_station', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='photos/')),
            ],
        ),
    ]
