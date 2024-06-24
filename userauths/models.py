from django.contrib.auth.models import AbstractUser
from django.db import models
GENDER=[('male', 'Male'), ('female', 'Female')]
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100,unique=True)
    birthday=models.DateField(blank=True,null=True)
    gender=models.CharField(choices=GENDER,null=True , blank=True,max_length=10)
    is_vendor=models.BooleanField(null=True)
    first_name=models.CharField(blank=True, max_length=150, verbose_name='first name' , default="Missing")
    last_name=models.CharField(blank=True, max_length=150, verbose_name='last name' , default="Missing")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="Groups",
        related_name="custome_user_groups",   #  related name attribute for custome  reverse accessors so take care when you use it type name_of_model.custome_user_groups instead user
        related_query_name="user" ,           # .................................. but for query 
        blank=True,
    )
    user_permissions=models.ManyToManyField(
        "auth.Permission",
        verbose_name="User Permission",
        related_name="custome_user_permission",
        related_query_name="user",
        blank=True ,
        help_text="Specific permissions for this user",
    )

    def __str__(self):
        return self.username


