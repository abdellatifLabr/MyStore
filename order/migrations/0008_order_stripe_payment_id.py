# Generated by Django 3.1 on 2020-08-21 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20200818_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stripe_payment_id',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
    ]
