from django.urls import include, path
from . import views

app_name = "Accounts"
urlpatterns = [
path ( "register/" , views.register , name="register"),
path ( "admin_info/" , views.admin_info , name="admin_info"),
path ( "vendor_info/" , views.vendor_info , name="vendor_info"),
path ( "customer_info/" , views.customer_info , name="customer_info"),
path ( "vendor/profile/update/" , views.update_vendor , name="update_vendor"),
path ( "customer/profile/update/" , views.update_customer , name="update_customer"),
path ( "delete_account/" , views.delete_account , name="delete_account"),




]
