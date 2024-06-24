from django.contrib import admin
from .models import Category , Product , ProductFeedback ,ProductImages , Wishlist
from .forms import ProductForm
from typing import Any
# Register your models here.
@admin.register(Category)
class CategoryAdmin (admin.ModelAdmin):
     list_display = ["title","category_iamge"]
     prepopulated_fields={"slug":("title",)}
     readonly_fields=("url",)

class ProductImagesAdmin (admin.TabularInline):
    model = ProductImages 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form=ProductForm
    inlines = [ProductImagesAdmin]
    list_display = ["vendor", "title","product_image", "price", "instock","is_active", "product_status","rating","category","created_at","qty_in_stock"]
    list_filter = ['instock', 'is_active']
    list_editable=["price", "instock","category","is_active","qty_in_stock"]  # do not forget delete Category from here 
    readonly_fields = ('url',"rating")
    prepopulated_fields={"slug":("title",)}
    auto_fill_field="Shipping_Fee"
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
         if not getattr (obj,self.auto_fill_field):
              setattr(obj,self.auto_fill_field,0.00)
         return super().save_model(request, obj, form, change)

@admin.register(ProductFeedback)
class ProductFeedbackAdmin(admin.ModelAdmin):
    list_display=('customer','product','comment','rating','created_at','updated_at')
@admin.register(Wishlist)
class WishlistAdmin (admin.ModelAdmin):
     list_display=['customer','products','created_at','updated_at']
     def products (self,obj):   # this Function to display Products bcause it has to many to many Relationship and django can not to show it Auto 
          return " , ".join( [product.title for product in obj.product.all()])
