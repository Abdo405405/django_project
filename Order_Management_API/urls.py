
from django.contrib import admin
from django.urls import path 
from .views import new_order , get_orders , single_order ,change_order_status

app_name = "order"
urlpatterns = [
path('create_order/',new_order, name='order-create'),
path('get_orders/',get_orders , name="get_all_orders"),
path('order/<str:pk>/',single_order , name="get_single_order"),
path('order/<str:pk>/process/',change_order_status , name="change_order_status"),
path('order/<str:pk>/delete/',change_order_status , name="change_order_status"),


# path('create_update/<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
# path('list/', OrderListView.as_view(), name='order-list'),
# path('create_delete/<int:pk>/', OrderDeleteView.as_view(), name='order-delete'),

]

