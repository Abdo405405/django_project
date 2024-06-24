from django.db import models
from Accounts.models import User
from django.dispatch import receiver 
from django.db.models.signals import post_delete
# Create your models here.
class Payment_Type (models.Model):
    id=models.AutoField(primary_key=True)
    payment_name= models.CharField(max_length=100,unique=True)
    image=models.ImageField(upload_to="Payment_methods",blank=True)
    def __str__(self) -> str:
        return self.payment_name
    class Meta :
        verbose_name = "Payment Type"

class User_Payment_Method (models.Model):
    id=models.AutoField(primary_key=True)
    payment_type=models.ForeignKey(Payment_Type,on_delete=models.CASCADE)
    provider=models.CharField(max_length=100)
    account_number=models.CharField(max_length=20,unique=True)
    expiry_date=models.DateField()
    is_default=models.BooleanField(default=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def change_default_user_payment(self,*args,**kwargs):
        if User_Payment_Method.objects.exists():
         if self.is_default==True:
          all_data=User_Payment_Method.objects.filter(user=self.user)
          for data in all_data :
              if data.is_default:
                  data.is_default=False
                  data.save()#  self.save() #  OR super().save(*args,**kwargs)  
    def __str__(self) -> str:
        return self.payment_type.payment_name 
    class Meta :
        verbose_name = "User Payment"



@receiver(post_delete)
def reset_primary_key_sequence(sender, instance, **kwargs):
    if not sender.objects.exists():
        table_name = sender._meta.db_table
        from django.db import connection
        engine = connection.vendor
        if engine == 'mysql':
            with connection.cursor() as cursor:
                cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;")