# Generated by Django 3.1 on 2020-08-24 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_auto_20200824_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='discount_codes',
            field=models.ManyToManyField(null=True, related_name='orders', to='order.DiscountCode'),
        ),
    ]
