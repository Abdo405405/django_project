from rest_framework import serializers
from .models import Product ,Category ,ProductFeedback , Customer ,Wishlist
from django.shortcuts import get_object_or_404
from django.utils import text
from rest_framework.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal
from .models import STATUS

class ProductSerializer(serializers.ModelSerializer):
    vendor = serializers.SerializerMethodField()
    category=serializers.SerializerMethodField()
    subcategory=serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'title', "vendor",'url', "category","subcategory","rating",'price',"old_price", 'image',"color", "description","specifications",'product_status','instock',"is_new", 'qty_in_stock',"Shipping_Fee","created_at"]
    def get_vendor(self, obj):
        return " ".join( [obj.vendor.user.first_name,obj.vendor.user.last_name]  )
    def get_category(self, obj):
        return obj.category.title
    def get_subcategory(self, obj):
         if obj.subcategory:
            return obj.subcategory.title
         else:
             return None


class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [ 'title', "vendor", "category","subcategory",'price',"old_price", 'image',"color", "description","specifications",'product_status','instock',"is_new", 'qty_in_stock',"Shipping_Fee","is_active"]
        
    def to_representation(self, instance):
         data = super().to_representation(instance)
         data["url"]=instance.url
         return data


class CreateProductSerializer (serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)
    description=serializers.CharField()
    price=serializers.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    old_price=serializers.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    product_status = serializers.ChoiceField(choices=STATUS ,default="in_review")
    specifications=serializers.CharField()
    Shipping_Fee= serializers.DecimalField(max_digits=14, decimal_places=2)
    instock = serializers.BooleanField(required=True)
    is_new = serializers.BooleanField(required=True)
    is_active = serializers.BooleanField(required=True)
    qty_in_stock=serializers.IntegerField()
    color=serializers.CharField(max_length=100)
    class Meta : 
        model=Product
        fields = [ 'title', "vendor", "category","subcategory",'price',"old_price", 'image',"color", "description","specifications",'product_status','instock',"is_new", 'qty_in_stock',"Shipping_Fee","is_active"]


class CategorySerializer(serializers.ModelSerializer):
    parent_category=serializers.SerializerMethodField()
    class Meta : 
        model=Category
        fields='__all__'
    def get_parent_category(self,obj):
        if obj.parent_category :
            return obj.parent_category.title
        else:
            return None


class CreateCategorySerializer(serializers.ModelSerializer):
    parent_category = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        parent_category = validated_data.pop("parent_category", None)
        slug=validated_data.pop("slug",None)
        url=validated_data.pop("url",None)
        if slug  :
            raise ValidationError({"slug": "This field cannot be access"})
        elif not slug:
            slug = text.slugify(validated_data['title'])
            validated_data['slug'] = slug
        if url  :
            raise ValidationError({"url": "This field cannot be access"})
        if parent_category:
            parent_category = get_object_or_404(Category,title=parent_category)
            validated_data['parent_category'] = parent_category
        return super().create(validated_data)    


class UpdateCategorySerializer(serializers.ModelSerializer):
    parent_category_name = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    parent_category=serializers.SerializerMethodField()
    title=serializers.CharField(required=False)
    slug=serializers.SlugField(required=False)
    class Meta:
        model = Category
        fields = '__all__'
    def update(self, instance, validated_data):
        parent_category_name=validated_data.pop("parent_category_name",None)
        title=validated_data.pop("title",None)
        slug=validated_data.pop("slug",None)
        url=validated_data.pop("url",None)
        # here is condtions to denay user from modify specific fields 
        if slug  :
            raise ValidationError({"slug": "This field cannot be modified"})
        if url  :
            raise ValidationError({"url": "This field cannot be modified"})
        # here is auto_fill for slug and url fields based on title
        if title :
            slug=text.slugify(title)
            validated_data["slug"]=slug
            validated_data["url"]=f"api/{slug}"
        # to make user change parent_category based on name not id then convert this name to correspond id 
        if parent_category_name:
            validated_data["parent_category"] = get_object_or_404(Category,title=parent_category_name)
        validated_data["title"]=title
        return super().update(instance, validated_data)
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('parent_category_name', None)  # Remove parent_category_name from the output
        return data
    def get_parent_category(self,obj):
        if obj.parent_category :
            return obj.parent_category.title
        else:
            return None
    
class GetFeedbacksOfProduct (serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    class Meta : 
        model=ProductFeedback
        fields = ["comment", "rating", "created_at", "updated_at", "customer", "image","first_name","last_name" ]
    def get_customer (self,obj):
        customer=obj.customer.user.first_name +" "+ obj.customer.user.last_name
        return customer
    def get_first_name (self,obj):
        customer_first_name=obj.customer.user.first_name
        return customer_first_name  
    def get_last_name (self,obj):
        customer_last_name=obj.customer.user.last_name
        return customer_last_name    
    def get_image (self , obj) : 
        customer_image = obj.customer.image.url
        if customer_image :
            return customer_image
        else :
            return  "No Image is Avalible" 
    
class WishlistSerializer (serializers.ModelSerializer):
    class Meta : 
        model=Wishlist
        fields=["product"]

