# Generated by Django 3.1.1 on 2020-09-10 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('notifications', '0004_notification_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='source',
        ),
        migrations.CreateModel(
            name='NotificationSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
    ]