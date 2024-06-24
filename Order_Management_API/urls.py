
from django.contrib import admin
from django.urls import path ,include
from .views import new_order

app_name = "order"
urlpatterns = [
path('create_order/',new_order, name='order-create'),
# path('create_update/<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
# path('list/', OrderListView.as_view(), name='order-list'),
# path('create_delete/<int:pk>/', OrderDeleteView.as_view(), name='order-delete'),

]

