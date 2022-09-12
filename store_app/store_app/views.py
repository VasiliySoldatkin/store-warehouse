from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet

from .models import StoreAccounts, Order, WarehouseAccounts
from .serializers import OrderSerializer, BaseParamsSerializer, \
    DestroyParamsSerializer, StoreSerializer, WarehouseSerializer


class OrderView(ModelViewSet):
    queryset = Order.orders.all()
    serializer_class = OrderSerializer

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        serializer: OrderSerializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response({'success': False, 'error_message': {'data': serializer.errors}},
                            status=status.HTTP_400_BAD_REQUEST)

        params_serializer = BaseParamsSerializer(data=request.query_params)
        if not params_serializer.is_valid(raise_exception=False):
            return Response({'success': False, 'error_message': {'params': params_serializer.errors}},
                            status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data
        params = params_serializer.data

        store = StoreAccounts.stores.filter(name=data['store_account']).first()
        if not store:
            return Response({'success': False,
                             'error_message': {'internal': "Store with this name doesn't exists"}},
                            status=status.HTTP_404_NOT_FOUND)
        warehouse = WarehouseAccounts.warehouses.filter(name=data['warehouse_account']).first()

        # TODO: Create warehouse instance automatically if warehouse doesn't exist
        if not warehouse:
            return Response({'success': False,
                             'error_message': {'internal': "Warehouse with this name doesn't exists"}},
                            status=status.HTTP_404_NOT_FOUND)

        updates_data = {
            'status': data['status'],
            'store_account': store,
            'warehouse_account': warehouse
        }

        order, created = Order.orders.update_or_create(order_number=data['order_number'],
                                                       defaults=updates_data, sync=params['sync'])
        serializer = self.get_serializer(order)

        return Response({'success': True, 'created': created, 'result': serializer.data})

    @transaction.atomic()
    def destroy(self, request, *args, **kwargs):
        params_serializer = DestroyParamsSerializer(data=request.query_params)

        if not params_serializer.is_valid(raise_exception=False):
            return Response({'success': False, 'error_message': {'params': params_serializer.errors}},
                            status=status.HTTP_400_BAD_REQUEST)
        params = params_serializer.data

        Order.orders.get(order_number=params['order_number']).delete(sync=params['sync'])
        return Response({'success': True})


@api_view(['GET'])
def store_exists(request):
    print(request.query_params)
    store = StoreAccounts.stores.filter(name=request.query_params['name']).first()
    print(store)
    return Response({'is_exists': bool(store)},
                    status=status.HTTP_404_NOT_FOUND if not store else status.HTTP_200_OK)
