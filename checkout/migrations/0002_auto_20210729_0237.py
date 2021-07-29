# Generated by Django 3.2.4 on 2021-07-29 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlineitem',
            name='item_price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='orderlineitem',
            name='lineitem_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='orderlineitem',
            name='product',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='orderlineitem',
            name='product_id',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='orderlineitem',
            name='product_line',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='orderlineitem',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='orderlineitem',
            name='sub_product_line',
            field=models.CharField(max_length=254),
        ),
    ]