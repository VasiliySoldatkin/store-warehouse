from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    store_account = serializers.CharField(max_length=250)
    warehouse_account = serializers.CharField(max_length=250)
    order_number = serializers.CharField(max_length=250)
    status = serializers.IntegerField()


class BaseParamsSerializer(serializers.Serializer):
    sync = serializers.BooleanField(default=True)


class DestroyParamsSerializer(BaseParamsSerializer):
    order_number = serializers.CharField(max_length=250)


class WarehouseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    uri = serializers.URLField(max_length=500)

    # TODO: override save method to check unique


class StoreSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    uri = serializers.URLField(max_length=500)

    # TODO: override save method to check unique
