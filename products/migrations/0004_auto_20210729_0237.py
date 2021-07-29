# Generated by Django 3.2.4 on 2021-07-29 01:37

from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210727_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, help_text='(Optional) Please add an image for this Product.', max_length=2000, null=True, upload_to=products.models.product_image_path),
        ),
        migrations.AlterField(
            model_name='product',
            name='reduced_reason',
            field=models.ForeignKey(blank=True, help_text='Why is this product reduced?', null=True, on_delete=django.db.models.deletion.RESTRICT, to='products.reduced_reason', verbose_name='Reason for Reduction'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock_state',
            field=models.ForeignKey(default=2, help_text='What is the stock status of this product?', null=True, on_delete=django.db.models.deletion.RESTRICT, to='products.stock_state', verbose_name='Stock State'),
        ),
        migrations.AlterField(
            model_name='product_line',
            name='category',
            field=models.ForeignKey(help_text='Please select a category for this Product Line.', on_delete=django.db.models.deletion.RESTRICT, to='products.category'),
        ),
        migrations.AlterField(
            model_name='product_line',
            name='genre',
            field=models.ForeignKey(help_text='Please select a genre for this Product Line.', on_delete=django.db.models.deletion.RESTRICT, to='products.genre'),
        ),
        migrations.AlterField(
            model_name='product_line',
            name='image',
            field=models.ImageField(blank=True, help_text='(Optional) Please add an image for this Product Line.', max_length=2000, null=True, upload_to=products.models.product_line_image_path),
        ),
        migrations.AlterField(
            model_name='sub_product_line',
            name='image',
            field=models.ImageField(blank=True, help_text='(Optional) Please add an image for this Sub Product Line.', max_length=2000, null=True, upload_to=products.models.sub_product_line_image_path),
        ),
    ]