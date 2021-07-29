# Generated by Django 3.2.4 on 2021-07-26 13:12

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(editable=False, max_length=32)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('street_address1', models.CharField(max_length=80)),
                ('street_address2', models.CharField(blank=True, max_length=80, null=True)),
                ('town_or_city', models.CharField(max_length=40)),
                ('county', models.CharField(blank=True, max_length=80, null=True)),
                ('postcode', models.CharField(max_length=20)),
                ('country', django_countries.fields.CountryField(default='GB', max_length=2)),
                ('delivery_first_name', models.CharField(max_length=25)),
                ('delivery_last_name', models.CharField(max_length=25)),
                ('delivery_address1', models.CharField(max_length=80)),
                ('delivery_address2', models.CharField(blank=True, max_length=80, null=True)),
                ('delivery_town_or_city', models.CharField(max_length=40)),
                ('delivery_county', models.CharField(blank=True, max_length=80, null=True)),
                ('delivery_postcode', models.CharField(max_length=20)),
                ('delivery_country', django_countries.fields.CountryField(default='GB', max_length=2)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('delivery_cost', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('order_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('original_basket', models.TextField(default='')),
                ('stripe_pid', models.CharField(default='', max_length=254)),
                ('user_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='profiles.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='OrderLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(editable=False, max_length=254)),
                ('product', models.CharField(editable=False, max_length=254)),
                ('sub_product_line', models.CharField(editable=False, max_length=254)),
                ('product_line', models.CharField(editable=False, max_length=254)),
                ('quantity', models.IntegerField(default=0, editable=False)),
                ('item_price', models.DecimalField(decimal_places=2, editable=False, max_digits=6)),
                ('lineitem_total', models.DecimalField(decimal_places=2, editable=False, max_digits=6)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineitems', to='checkout.order')),
            ],
        ),
    ]