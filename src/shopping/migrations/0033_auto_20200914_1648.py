# Generated by Django 3.1.1 on 2020-09-14 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0032_auto_20200914_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]