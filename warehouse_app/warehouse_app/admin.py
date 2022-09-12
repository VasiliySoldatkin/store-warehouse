import requests
from django.contrib import admin
from django.core.exceptions import ValidationError
from warehouse_app.models import Order, StoreAccounts, WarehouseAccounts


class StoreAdmin(admin.ModelAdmin):
    # TODO: add uri validation (to prevent self-reference)
    def save_model(self, request, obj, form, change):
        if not requests.get(f'{obj.uri}/exists', params={'name': obj.name}).json()['is_exists']:
            raise ValidationError("Store with this name doesn't exists")
        obj.save()

    def delete_model(self, request, obj):
        if requests.get(f'{obj.uri}/exists', params={'name': obj.name}).status_code == 404:
            raise ValidationError("Store with this name doesn't exists")

        obj.delete()


class OrderAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save(sync=True)

    def delete_model(self, request, obj):
        obj.delete(sync=True)


admin.site.register(Order, OrderAdmin)
admin.site.register(StoreAccounts, StoreAdmin)
admin.site.register(WarehouseAccounts)
