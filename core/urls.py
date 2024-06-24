from django.urls import path
from core.views import main 
app_name="core"
urlpatterns = [
    path("",main,name='main'),
]