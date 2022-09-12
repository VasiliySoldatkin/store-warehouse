from .views import store_exists, OrderView
from django.urls import path

urlpatterns = [
    path('store/exists', store_exists),
    path('store/order', OrderView.as_view({'delete': 'destroy', 'put': 'update', 'get': 'list'})),
]
