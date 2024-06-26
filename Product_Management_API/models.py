# product management app
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import connection, models
from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import text
from django.utils.safestring import mark_safe
from Accounts.models import Customer, Vendor
def productimages_directory_path(instance,filename) :                  #upload_to Function 
    return 'Products by Vendors/vendor_{0}/products/{1}'.format(instance.product.id,filename)
# Create your models here.
class ProductManger(models.Manager):
    def get_queryset (self):
        return super(ProductManger,self).get_queryset().filter(is_active=True)  # self here im not understand it but if you remove it super can not access to get_queryset 


STATUS=(
    ('', ''),
    ('in_review', 'In Review'),
    ('published', 'Published'),
    ('discontinued', 'Discontinued'),
    ('on_sale', 'On Sale'),
    
)
RATING=(
    (0,"☆☆☆☆☆"),
    (1,"★☆☆☆☆"),
    (2,"★★☆☆☆"),
    (3,"★★★☆☆"),
    (4,"★★★★☆"),
    (5,"★★★★★"),
)
class Category (models.Model):
    title = models.CharField(max_length=255  , db_index=True ,unique=True )
    slug=models.SlugField(max_length=255,blank=True)
    url=models.CharField(max_length=255,blank=True)
    image=models.ImageField(upload_to="Categories",blank=True,null=True ,max_length=500)
    description = models.TextField(null=True, blank=True)
    parent_category=models.ForeignKey("self",models.CASCADE,blank=True,null=True,related_name="subcategories")
    class Meta:
        verbose_name="Category"
        verbose_name_plural="Categories"
    def get_absolute_url (self):
        return reverse("products:category_listPage",args=[self.slug])  
    def category_iamge (self):
        if self.image:
            return mark_safe('<img src="%s" style="max-height: 60px; max-width: 60px;" />' % self.image.url)
        else:
            return "No Image Available"
    def __str__(self):
        return self.title
    

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True )
    subcategory=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,related_name="subcategory",blank=True)
    title = models.CharField(max_length=100,blank=False)
    slug = models.SlugField(max_length=255  ,blank=True)
    url= models.CharField(max_length=255 , unique=True , blank=True)
    image = models.ImageField(upload_to="All Products",blank=True,max_length=500,null=True)
    color= models.CharField(null=True, blank=True,max_length=100)
    description = models.TextField(null=True, blank=True, default="This is the product")
    price = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))],default=Decimal('0.00'))
    old_price = models.DecimalField(max_digits=14, decimal_places=2, default=0,blank=True)
    Shipping_Fee= models.DecimalField(max_digits=14, decimal_places=2, default=0.00,blank=True)
    specifications = models.TextField(null=True, blank=True)
    product_status = models.CharField(choices=STATUS, max_length=250, default="")
    is_new=models.BooleanField()
    instock = models.BooleanField()
    is_active = models.BooleanField()
    qty_in_stock = models.PositiveIntegerField()
    rating=models.IntegerField(null=True,blank=True)
    digital = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) #  Sets the value of the field to the current date and time when the object is first created.
    updated_at = models.DateTimeField(auto_now=True)   # Updates the value of the field to the current date and time every time the object is saved
    objects=models.Manager()
    activated_products=ProductManger()
    class Meta :
        verbose_name = "Product"
        ordering=("-created_at",)
    

        # Call the superclass's save() method to save the object
    def get_absolute_url (self):
        return reverse('products:product_detail', args=[self.pk,self.slug])  # Adjust the URL pattern name and parameters accordingly
    def product_image (self) : 
        if self.image:
            return mark_safe('<img src="%s" width=50 height=50 />' % (self.image.url))
        else:
            return "No image is Available"
    def __str__(self):
        return self.title
    def get_precentage(self):
        if self.old_price != 0:
            return (self.price / self.old_price) * 100 
        else :
            return 0
        

class ProductImages (models.Model):
    image=models.ImageField(upload_to=productimages_directory_path) 
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,related_name="product_images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta :
        verbose_name = "Product Images"
class ProductFeedback (models.Model):
    comment=models.TextField(blank=True ,null=True)
    rating=models.IntegerField(choices=RATING,default=None,blank=True ,null=True)
    created_at=models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True)
    customer= models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    product= models.ForeignKey(Product,on_delete=models.CASCADE,null=True,related_name="feedback")
    class Meta :
        verbose_name = "Product Feedback"
    def __str__(self):
        return self.product.title
    def get_rating (self):
        return self.rating
class Wishlist (models.Model):
    customer= models.OneToOneField(Customer,on_delete=models.CASCADE)
    product= models.ManyToManyField(Product)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta :
        verbose_name = "Wishlist"
@receiver(post_delete)
def reset_primary_key_sequence(sender, instance, **kwargs):
    if not sender.objects.exists():
        table_name = sender._meta.db_table
        engine = connection.vendor
        if engine == 'mysql':
            with connection.cursor() as cursor:
                cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;")
@receiver (post_save,sender=Product)
def set_product_url(sender, instance, created,**kwargs):
    sender=sender._meta.db_table
    # Generate a slug based on the title
    if created and not instance.url:
        slug = text.slugify(instance.title)
        instance.slug = slug
        instance.url = instance.get_absolute_url() 
        instance.save()
@receiver (post_save,sender=Category)
def set_product_url(sender, instance, created,**kwargs):
    # Generate a slug based on the title
    if  not instance.url:
        slug = text.slugify(instance.title)
        instance.slug = slug
        instance.url = instance.get_absolute_url() 
        instance.save()

@receiver (post_save,sender=Customer)
def CreateWishlist (sender , instance ,created,**kwargs) : 
    if created : 
        Wishlist.objects.create(customer=instance)