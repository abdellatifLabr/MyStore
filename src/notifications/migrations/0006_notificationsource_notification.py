# Generated by Django 3.1.1 on 2020-09-10 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_auto_20200910_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationsource',
            name='notification',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='source', to='notifications.notification'),
            preserve_default=False,
        ),
    ]
