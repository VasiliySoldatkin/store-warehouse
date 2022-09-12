from django.contrib import admin
from store_app.models import Order, WarehouseAccounts, StoreAccounts
from django.core.exceptions import ValidationError
import requests


class WarehouseAdmin(admin.ModelAdmin):
    # TODO: add uri validation (to prevent self-reference)
    def save_model(self, request, obj, form, change):
        if requests.get(f'{obj.uri}/exists', params={'name': obj.name}).status_code == 404:
            raise ValidationError("Warehouse with this name doesn't exists")

        obj.save()

    def delete_model(self, request, obj):
        if requests.get(f'{obj.uri}/exists', params={'name': obj.name}).status_code == 404:
            raise ValidationError("Warehouse with this name doesn't exists")

        obj.delete()


class OrderAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save(sync=True)

    def delete_model(self, request, obj):
        obj.delete(sync=True)


admin.site.register(WarehouseAccounts, WarehouseAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(StoreAccounts)
# Register your models here.
