# Generated by Django 3.0.9 on 2020-08-17 19:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shopping', '0018_auto_20200817_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartproduct',
            name='cart',
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='store',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='cart_products', to='shopping.Store'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='cart_products', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
