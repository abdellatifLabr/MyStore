# Generated by Django 3.1 on 2020-08-29 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0027_auto_20200829_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_products', to='shopping.product'),
        ),
    ]
