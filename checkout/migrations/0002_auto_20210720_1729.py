# Generated by Django 3.2.4 on 2021-07-20 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_first_name',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_last_name',
            field=models.CharField(max_length=25),
        ),
    ]
