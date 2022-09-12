from django.db import models, transaction
import requests
from uuid import uuid4

from django.db.models.utils import resolve_callables
from .errors import SyncError


def random_order():
    return str(uuid4())


class WarehouseAccounts(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)
    uri = models.CharField(max_length=500, unique=True)

    warehouses = models.Manager()

    def __str__(self):
        return self.name


class StoreAccounts(models.Model):
    store_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)
    uri = models.CharField(max_length=500, unique=True)

    stores = models.Manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class OrdersQuerySet(models.QuerySet):
    # Initial "update_or_create" method but with sync
    def update_or_create(self, defaults=None, sync=False, **kwargs):
        defaults = defaults or {}
        self._for_write = True
        with transaction.atomic(using=self.db):
            # Lock the row so that a concurrent update is blocked until
            # update_or_create() has performed its save.
            obj, created = self.select_for_update().get_or_create(defaults, **kwargs)
            if created:
                return obj, created
            for k, v in resolve_callables(defaults):
                setattr(obj, k, v)
            obj.save(using=self.db, sync=sync)

        return obj, False


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrdersQuerySet(self.model, using=self._db)

    def update_or_create(self, defaults=None, sync=False, **kwargs):
        return self.get_queryset().update_or_create(defaults=defaults, sync=sync, **kwargs)


class Order(models.Model):
    class Statuses(models.IntegerChoices):
        NEW = 0, 'New'
        IN_PROCESS = 1, 'In Process'
        STORED = 2, 'Stored'
        SEND = 3, 'Send'

    status = models.IntegerField(choices=Statuses.choices)
    store_account = models.ForeignKey(StoreAccounts, on_delete=models.CASCADE)
    warehouse_account = models.ForeignKey(WarehouseAccounts,
                                          on_delete=models.CASCADE)
    order_number = models.CharField(max_length=250, unique=True, primary_key=True,
                                    db_index=True, default=random_order)

    orders = OrderManager()

    def save(self, sync=False, *args, **kwargs):
        # TODO: Serialize data
        update_fields = {'warehouse_account': self.warehouse_account.name,
                         'order_number': self.order_number,
                         'status': self.status,
                         'store_account': self.store_account
                         }

        if sync:
            response = requests.put(f'{self.warehouse_account.uri}/order',
                                    data=update_fields, params={'sync': False})

            if response.status_code != 200:
                raise SyncError()

        super().save(*args, **kwargs)

    def delete(self, sync=False, *args, **kwargs):
        if sync:
            response = requests.delete(f'{self.warehouse_account.uri}/order',
                                       data={'order_number': self.order_number}, params={'sync': False})

            # TODO: handle custom errors
            if response.status_code != 200:
                raise SyncError()

        return super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.order_number} - {self.warehouse_account}'
