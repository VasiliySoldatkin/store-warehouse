# Generated by Django 4.1.1 on 2022-09-11 21:12

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0002_alter_storeaccounts_uri_alter_warehouseaccounts_uri'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='storeorder',
            managers=[
                ('orders', django.db.models.manager.Manager()),
            ],
        ),
    ]
