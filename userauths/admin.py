from typing import Any
from django.contrib import admin
from userauths.models import User
from django.contrib.auth.hashers import make_password

class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]  # To display certain information in the user info bar

    def save_form(self, request: Any,form: Any, change: Any) -> Any:
        if "password" in request.POST:
            password = request.POST["password"]
            form.instance.password = make_password(password)
        return super().save_form(request, form, change)

# Register the customized user model in the admin page
admin.site.register(User, UserAdmin)
