# Generated by Django 3.0.8 on 2020-07-30 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0007_auto_20200730_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='shopping.Store'),
        ),
    ]
