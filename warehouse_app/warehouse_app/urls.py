from django.urls import path
from .views import warehouse_exists, OrderView

urlpatterns = [
    path('warehouse/exists', warehouse_exists),
    path('warehouse/order', OrderView.as_view({'delete': 'destroy', 'put': 'update', 'get': 'list'})),
]
