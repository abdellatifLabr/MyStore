# Generated by Django 3.1 on 2020-08-24 14:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0025_cartproduct_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartproduct',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]