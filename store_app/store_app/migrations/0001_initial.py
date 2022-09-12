# Generated by Django 4.1.1 on 2022-09-11 19:11

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StoreAccounts',
            fields=[
                ('store_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, unique=True)),
                ('uri', models.CharField(max_length=500, unique=True)),
            ],
            managers=[
                ('stores', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='WarehouseAccounts',
            fields=[
                ('warehouse_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, unique=True)),
                ('uri', models.CharField(max_length=500, unique=True)),
            ],
            managers=[
                ('warehouses', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='StoreOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'New'), (1, 'In Process'), (2, 'Stored'), (3, 'Send')])),
                ('order_number', models.CharField(max_length=250)),
                ('store_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_app.storeaccounts')),
                ('warehouse_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_app.warehouseaccounts')),
            ],
        ),
    ]
