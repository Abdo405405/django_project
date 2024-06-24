from django.contrib import admin
from typing import Any
from .models import Payment_Type , User_Payment_Method

# Register your models here.


@admin.register(User_Payment_Method)
class payment_method_Admin (admin.ModelAdmin):
     list_display=("Name","payment_type","provider","account_number","is_default")
     def Name(self,obj):
          return obj.user.first_name+" "+obj.user.last_name
   
     def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
               obj.change_default_user_payment()
               return super().save_model(request, obj, form, change)
  
@admin.register(Payment_Type)
class payment_type_Admin (admin.ModelAdmin):
     list_display=("payment_name","image")