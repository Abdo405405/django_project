# core app
from django.db import connection, models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.safestring import mark_safe
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
 # Create your models here.


def productimages_directory_path(instance,filename) :                  #upload_to Function 
    return 'Products by Vendors/vendor_{0}/products/{1}'.format(instance.product.id,filename)
# class ProductManager (models.manager):
#     def get_queryset(self):
#         return super(ProductManager,self).get_queryset().filter(is_active=Tre)
class Advertisement_Board(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='advertisement_images/',blank=True)
    link = models.URLField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    priority = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta : 
        verbose_name="Advertisement Board"
    def get_image (self):
        if self.image:
            return mark_safe('<img src="%s" style="max-height: 100px; max-width: 100px;" />' % self.image.url)

    def __str__(self):
        return self.title
################################# USERS DETAILS  SECTION ######################################
################################# USERS DETAILS  SECTION ######################################
################################# USERS DETAILS  SECTION ######################################
################################# USERS DETAILS  SECTION ######################################


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    country_name=models.CharField(max_length=100 , blank=True , null=True)
    def __str__(self) -> str:
        return self.country_name
    
class Address(models.Model): # this Model  for User 
    contact=models.CharField(max_length=15 , blank=True , null=True)
    unit_number=models.IntegerField(blank=True , null=True)
    street_number=models.IntegerField(blank=True , null=True)
    address_line1=models.CharField(max_length=200,blank=True , null=True)
    address_line2=models.CharField(max_length=200,blank=True , null=True)
    city=models.CharField(max_length=100)
    country=models.ForeignKey(Country,on_delete=models.CASCADE,blank=True , null=True)
    region=models.CharField(max_length=100,blank=True , null=True)
    postal_code=models.IntegerField(blank=True , null=True)
    class Meta : 
        verbose_name= "Address"
    def __str__(self):
            return  f"{self.address_line1}, {self.city}, {self.country}"


class Vendor (models.Model):
    addresses=models.ManyToManyField(Address,blank=True , null=True)
    default_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='default_for_vendor')
    image=models.ImageField(upload_to="All Vendors",blank=True , null=True)
    description=models.TextField(null=True,blank=True)
    chat_resp_time = models.CharField(max_length=100,blank=True , null=True)
    authentic_rating=models.CharField(max_length=100,blank=True , null=True)
    shipping_on_time=models.CharField(max_length=100,blank=True , null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta : 
        verbose_name = "Vendor"
    def  set_default_address(self):
        pass
    def vendor_image (self):
        if self.image:
            return mark_safe('<img src="%s" style="max-height: 100px; max-width: 100px;" />' % self.image.url)
        else:
            return "No Image Available"
    def delete(self, *args, **kwargs):
        # Delete all associated addresses
        self.address.clear()  # Removes all associated addresses from the ManyToManyField
        
        self.default_address.delete()  # Delete the default address
        print("111111")
        super().delete(*args, **kwargs)
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    


class Customer (models.Model):
        id=models.AutoField(primary_key=True)
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        image=models.ImageField(upload_to="Customers",blank=True)
        addresses=models.ManyToManyField(Address,blank=True , null=True)
        default_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='default_for_customer')
        class Meta : 
          verbose_name = "Customer"
        def clean(self) -> None:
            return super().clean()
        def customer_image (self):
             if self.image:
                 return mark_safe('<img src="%s" width=50 height=50 />' % (self.image.url))
             else:
                 return "No Image Available"

        def __str__(self):
            return self.user.username

@receiver(post_delete)
def reset_primary_key_sequence(sender, instance, **kwargs):
    if not sender.objects.exists():
        table_name = sender._meta.db_table
        from django.db import connection
        engine = connection.vendor
        if engine == 'mysql':
            with connection.cursor() as cursor:
                cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;")

@receiver(post_save,sender=User)
def create_vendor_or_customer(sender, instance, created, **kwargs):
    if created:
        if instance.is_vendor:
            Vendor.objects.create(user=instance,default_address=Address.objects.create())
        elif  instance.is_vendor==False and not instance.is_superuser :
            Customer.objects.create(user=instance,default_address=Address.objects.create())

@receiver(post_delete, sender=Vendor)
def delete_related_addresses(sender, instance, **kwargs):
    # Delete all associated addresses
    instance.addresses.clear()  # Removes all associated addresses from the ManyToManyField
    if instance.default_address:
        instance.default_address.delete()  # Delete the default address

@receiver(post_delete, sender=Customer)
def delete_related_addresses(sender, instance, **kwargs):
    # Delete all associated addresses
    instance.addresses.clear()  # Removes all associated addresses from the ManyToManyField
    if instance.default_address:
        instance.default_address.delete()  # Delete the default address
