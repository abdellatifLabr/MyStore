# Generated by Django 3.1.1 on 2020-09-10 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0008_remove_notification_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='source',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='notifications.notificationsource'),
            preserve_default=False,
        ),
    ]