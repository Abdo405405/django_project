# order management app
from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import connection, models
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from Product_Management_API.models import Product
from Accounts.models import Customer  ,Address
from Payment_Management_API.models import User_Payment_Method
# Create your models here.

STATUS_CHOICE=(# lowercase for writing and uppercase one  to show to user
('new', 'New'), 
('old', 'Old'), 
)
class PaymentStatus (models.TextChoices):
    PAID="Paid"
    UNPAID="Unpaid"
class PaymentMode (models.TextChoices): 
    COD="Cod"
    CARD="Card"
class OrderStatus(models.TextChoices):
    PROCESSING="Processing"
    SHIPPED="Shipped"
    DELIVERED="Delivered"
    CANCELLED="Cancelled"


class CartOrder (models.Model): # represents an entire order placed by a user
    id=models.AutoField(primary_key=True)
    customer= models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ManyToManyField(Product , blank=True)
    total_price = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))],blank=True,default=0.00,null=False)
    order_date=models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=OrderStatus.choices, max_length=20, default=OrderStatus.PROCESSING , null=True)
    payment_status= models.CharField(choices=PaymentStatus.choices , max_length=30 , default=PaymentStatus.UNPAID ,null=True)
    payment_mode=models.CharField(choices=PaymentMode.choices , max_length=30 , default=PaymentMode.COD , null=True)
    payment_type=models.ForeignKey(User_Payment_Method,models.SET_NULL,null=True)
    shipping_address=models.ForeignKey(Address,on_delete=models.SET_NULL,blank=True ,null=True)
    invoice_no=models.CharField(max_length=10,default="Auto-fill")
    SearchableFields=["customer_id",]
    class Meta :
        verbose_name = "Cart Order"
    # Modls methods 
    def get_products (self):
      return ", ".join([product.title for product in self.product.all()])  

    
    def set_invoice_number (self,*args, **kwargs):
       if  self.invoice_no=="Auto-fill":
        current_year = timezone.now().year
        if  CartOrder.objects.filter(order_date__year=current_year).exists():
          order_related_objects = CartOrder.objects.filter(order_date__year=current_year)
          num_of_last_order=order_related_objects.count()
          invoice_number=order_related_objects.last().invoice_no
          flag=True
          num_of_order=""
          for index,count in enumerate(invoice_number) :
              if index>3:
                  if count =="0" and flag:
                      continue
                  else:
                      flag=0
                      num_of_order=num_of_order+count
        else:
            num_of_order="0"
        #num_of_order=int(num_of_order)+1
        num_of_order=int(num_of_order)+1
        # Format the invoice number
        formatted_invoice_number = f"{current_year}{num_of_order:04d}"
        self.invoice_no=formatted_invoice_number
        return None  
    def clean(self):
        if  self.customer.user != self.payment_type.user:  # التحقق مما إذا كانت الطريقة المحددة للدفع مملوكة للمستخدم الحالي
            raise ValidationError('User does not has This Payment Type ')
        shipping_address_id=self.shipping_address.id  # this field that related to Address Table 
        customer_addresses_objects=self.customer.addresses #this field that related to Customer Table that related to Address table 
        if not customer_addresses_objects.filter(id=shipping_address_id).exists(): # if Shipping Address is not Exist in Addresses of this customer it raise Error
            raise ValidationError('Wrong Address')
        return super().clean()
    def save(self, *args,**kwargs) -> None:
        self.set_invoice_number()
        return super().save(*args,**kwargs)      
    def __str__(self):
        return f"{self.customer.user.first_name} {self.customer.user.last_name} - Invoice No: {self.invoice_no}"
    # End of The Class                  
class CartOrderItem (models.Model): # represents the individual items contained within that order
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE , related_name="order_items")
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    image=models.CharField(max_length=200)
    qty =models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))],blank=True,default=0.00,null=False)
    # Model Methods 
    def set_total_price_of_item(self,*args,**kwargs):
        old_total_item_price= Decimal(self.total_price)
        order_total_price=Decimal(self.order.total_price)
        new_total_price_item=self.qty * self.product.price # put new total price when you add more quantity of this item
        self.total_price=new_total_price_item  # put the value to total price of item
        increase_by= new_total_price_item - old_total_item_price # if new total price = 100 and old one = 20 so amount of increase is 80 
        self.order.total_price=order_total_price+increase_by  # here we are save this increase in total price of order
        self.order.save() #If you do not include this line, the object of cartorder table  will not be automatically updated
    def clean(self):
        product_objects_in_cart_order=self.order.product.all()
        if not product_objects_in_cart_order.filter(title=self.product).exists():    
            raise ValidationError('You cannot Add item does not belong order.')
        items=CartOrderItem.objects.filter(order=self.order)
        if not self.pk : # The condition only runs for newly added items that have not been saved yet, so their primary keys do not exist.
         for item in items :
            if self.product.title ==item.product.title:
                raise ValidationError("This Item is Already Exist")
    def save(self, *args,**kwargs) -> None:
        self.set_total_price_of_item()
        return super().save(*args,**kwargs)
    class Meta :
        verbose_name = "Cart Order Item"
    def order_image (self) : 
        return mark_safe('<img src="%s" width=50 height=50 />' % (self.image.url))
    def __str__(self) -> str:
        if self.product:
            return self.product.title
        return "No product"    # End of the Model 
@receiver(pre_delete, sender=CartOrderItem)
def Delete_total_item_price_from_order(sender, instance, **kwargs):
    Deleted_price=instance.total_price
    obj_cardorder=instance.order
    obj_cardorder.total_price-=Deleted_price
    obj_cardorder.save()
@receiver(post_delete)
def reset_primary_key_sequence(sender, instance, **kwargs):
    if not sender.objects.exists():
        table_name = sender._meta.db_table
        engine = connection.vendor
        if engine == 'mysql':
            with connection.cursor() as cursor:
                cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;")
