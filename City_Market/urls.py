"""
URL configuration for City_Market project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from . import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views 
from userauths.views import clear_error_message , hide_error_messages 
from rest_framework_simplejwt.views import  TokenObtainPairView , TokenRefreshView
from .views import CustomTokenObtainPairView , logout
app_name = "project"
urlpatterns = [
    path('admin/', admin.site.urls),
    path("" , include("core.urls")),
    path("user/",include("userauths.urls")),
    path("api/" , include("Product_Management_API.urls")),
    path("" , include("Order_Management_API.urls")),
    path('clear-error-message/', clear_error_message, name='clear_error_message'),
    path('hide_error_messages/', hide_error_messages, name='get_first_name'),
    path("" , include("Accounts.urls")),
    path("token/" , CustomTokenObtainPairView.as_view()),
    path("token/refresh/" , TokenRefreshView.as_view(),name="token_refresh"),
    path('logout/', logout, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404="utils.errors_views.handler404"
