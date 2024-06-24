from rest_framework import serializers 
from userauths.models import User , GENDER
from .models import Vendor ,Country , Customer
from django.contrib.auth.hashers import make_password 
class SignUpSerializer (serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False,allow_null=False )
    email = serializers.EmailField(required=True, allow_blank=False,allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False,allow_null=False)
    first_name = serializers.CharField(required=True, allow_blank=False,allow_null=False)
    last_name = serializers.CharField(required=True, allow_blank=False,allow_null=False)
    gender = serializers.ChoiceField(choices=GENDER,required=True, allow_blank=False,allow_null=False)
    birthday = serializers.DateField(required=True)
    is_vendor=serializers.BooleanField(required=True)
    class Meta : 
        model=User 
        fields =["username", "email", "password", "first_name", "last_name", "gender", "birthday","is_vendor"]


class AdminInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UpdateVendorSerializer (serializers.ModelSerializer):
    username = serializers.CharField(max_length=150,required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(max_length=150,required=False)
    first_name = serializers.CharField(max_length=150,required=False)
    last_name = serializers.CharField(max_length=150,required=False)
    birthday = serializers.DateField(required=False)
    contact=serializers.CharField(max_length=15 , required=False)
    unit_number=serializers.IntegerField(required=False)
    street_number=serializers.IntegerField(required=False)
    address_line1=serializers.CharField(max_length=200,required=False)
    address_line2=serializers.CharField(max_length=200,required=False)
    city=serializers.CharField(max_length=100,required=False)
    region=serializers.CharField(max_length=100,required=False)
    postal_code=serializers.IntegerField(required=False)
    image=serializers.ImageField(required=False)
    description=serializers.CharField(required= False)
    country=serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),required=False)
    class Meta : 
        model=Vendor
        fields =["username", "email", "password", "first_name", "last_name","image","description",
                  "birthday","contact","unit_number","country",
                 "street_number","address_line1","address_line2","city","region","postal_code"]

    def update(self, instance, validated_data):
        user_instance = instance.user  # Get the related user instance
        default_address_instance =instance.default_address # Get the related vendor default_address
        copy_validated_data=validated_data.copy()
        # Update user instance fields if provided
        for attr, value in copy_validated_data.items():
            if hasattr(user_instance,attr):
                if attr =="password":
                    setattr(user_instance, attr, make_password(value))
                else:
                    setattr(user_instance, attr, value)
                validated_data.pop(f"{attr}")
        for attr, value in validated_data.items():
            if hasattr(default_address_instance,attr):
                setattr(default_address_instance, attr, value)
        # Save the updated user instance
        user_instance.save() 
        default_address_instance.save()
        # Update the Vendor instance
        instance = super().update(instance, validated_data) 

        return instance  # Return the updated instance
    def to_representation(self, instance):
        data= super().to_representation(instance)
        user_instance = instance.user
        default_address_instance =instance.default_address 
        if default_address_instance.country:
            country_name=default_address_instance.country.country_name
        else:
            country_name=None
        Vendor_data = {
        'username': user_instance.username,
        'email': user_instance.email,
        'password': user_instance.password,  # You might want to exclude this for security reasons
        'first_name': user_instance.first_name,
        'last_name': user_instance.last_name,
        'birthday': user_instance.birthday,
        'contact': default_address_instance.contact,
        'city': default_address_instance.city,
         'Country': country_name,
        'region': default_address_instance.region,
        'address_line1': default_address_instance.address_line1,
        'address_line2': default_address_instance.address_line2,
        'street_number': default_address_instance.street_number,
        'unit_number': default_address_instance.unit_number,
        'postal_code': default_address_instance.postal_code,
        
    }
        return Vendor_data
    

class UpdateCustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150,required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(max_length=150,required=False)
    first_name = serializers.CharField(max_length=150,required=False)
    last_name = serializers.CharField(max_length=150,required=False)
    birthday = serializers.DateField(required=False)
    contact=serializers.CharField(max_length=15 , required=False)
    unit_number=serializers.IntegerField(required=False)
    street_number=serializers.IntegerField(required=False)
    address_line1=serializers.CharField(max_length=200,required=False)
    address_line2=serializers.CharField(max_length=200,required=False)
    city=serializers.CharField(max_length=100,required=False)
    region=serializers.CharField(max_length=100,required=False)
    postal_code=serializers.IntegerField(required=False)
    image=serializers.ImageField(required=False)
    country=serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),required=False)
    class Meta:
        model=Customer 
        fields =["username", "email", "password", "first_name", "last_name","image",
                  "birthday","contact","unit_number","country",
                 "street_number","address_line1","address_line2","city","region","postal_code"]
        
    def update(self, instance, validated_data):
        user_instance = instance.user
        default_address_instance =instance.default_address 
        copy_validated_data=validated_data.copy()
        for attr, value in copy_validated_data.items():
            if hasattr(user_instance,attr):
                if attr =="password":
                    setattr(user_instance, attr, make_password(value))
                else:
                    setattr(user_instance, attr, value)
                validated_data.pop(f"{attr}")
        for attr, value in validated_data.items():
            if hasattr(default_address_instance,attr):
                setattr(default_address_instance, attr, value)

        user_instance.save() 
        default_address_instance.save()

        return super().update(instance, validated_data)
    def to_representation(self, instance):
        data= super().to_representation(instance)
        user_instance = instance.user
        default_address_instance =instance.default_address 
        if default_address_instance.country:
            country_name=default_address_instance.country.country_name
        else:
            country_name=None
        customer_data = {
        'username': user_instance.username,
        'email': user_instance.email,
        'password': user_instance.password,  # You might want to exclude this for security reasons
        'first_name': user_instance.first_name,
        'last_name': user_instance.last_name,
        'birthday': user_instance.birthday,
        'contact': default_address_instance.contact,
        'city': default_address_instance.city,
        'Country': country_name,
        'region': default_address_instance.region,
        'address_line1': default_address_instance.address_line1,
        'address_line2': default_address_instance.address_line2,
        'street_number': default_address_instance.street_number,
        'unit_number': default_address_instance.unit_number,
        'postal_code': default_address_instance.postal_code,
    }
        return customer_data


class VendorInfoSerializer (serializers.ModelSerializer):
        username = serializers.CharField(source="user.username",max_length=150,required=False)
        email = serializers.EmailField(source="user.email",required=False)
        password = serializers.CharField(source="user.password",max_length=150,required=False)
        first_name = serializers.CharField(source="user.first_name",max_length=150,required=False)
        last_name = serializers.CharField(source="user.last_name",max_length=150,required=False)
        birthday = serializers.DateField(source="user.birthday",required=False)
        contact = serializers.SerializerMethodField()
        unit_number = serializers.SerializerMethodField()
        street_number = serializers.SerializerMethodField()
        address_line1 = serializers.SerializerMethodField()
        address_line2 = serializers.SerializerMethodField()
        city = serializers.SerializerMethodField()
        region = serializers.SerializerMethodField()
        postal_code = serializers.SerializerMethodField()
        country = serializers.SerializerMethodField()
        class Meta:
            model=Vendor 
            fields =["username", "email", "password", "first_name", "last_name","image",
                    "birthday","contact","unit_number",
                    "street_number","address_line1","address_line2","country","city","region","postal_code",
                    "description", "chat_resp_time","authentic_rating","shipping_on_time"]
        def get_contact(self, obj):
             if obj.default_address:
                 return obj.default_address.contact
             return None
     
        def get_unit_number(self, obj):
             if obj.default_address:
                 return obj.default_address.unit_number
             return None
     
        def get_street_number(self, obj):
             if obj.default_address:
                 return obj.default_address.street_number
             return None
     
        def get_address_line1(self, obj):
             if obj.default_address:
                 return obj.default_address.address_line1
             return None
     
        def get_address_line2(self, obj):
             if obj.default_address:
                 return obj.default_address.address_line2
             return None
     
        def get_city(self, obj):
             if obj.default_address:
                 return obj.default_address.city
             return None
     
        def get_region(self, obj):
             if obj.default_address:
                 return obj.default_address.region
             return None
     
        def get_postal_code(self, obj):
             if obj.default_address:
                 return obj.default_address.postal_code
             return None
     
     
        def get_country(self, obj):
             if obj.default_address and obj.default_address.country:
                 return obj.default_address.country.country_name
             return None


class CustomerInfoSerializer (serializers.ModelSerializer):
        username = serializers.CharField(source="user.username",max_length=150,required=False)
        email = serializers.EmailField(source="user.email",required=False)
        password = serializers.CharField(source="user.password",max_length=150,required=False)
        first_name = serializers.CharField(source="user.first_name",max_length=150,required=False)
        last_name = serializers.CharField(source="user.last_name",max_length=150,required=False)
        birthday = serializers.DateField(source="user.birthday",required=False)
        contact = serializers.SerializerMethodField()
        unit_number = serializers.SerializerMethodField()
        street_number = serializers.SerializerMethodField()
        address_line1 = serializers.SerializerMethodField()
        address_line2 = serializers.SerializerMethodField()
        city = serializers.SerializerMethodField()
        region = serializers.SerializerMethodField()
        postal_code = serializers.SerializerMethodField()
        country = serializers.SerializerMethodField()
        class Meta:
            model=Customer
            fields =["username", "email", "password", "first_name", "last_name","image",
                    "birthday","contact","unit_number",
                    "street_number","address_line1","address_line2","country","city","region","postal_code"]
        def get_contact(self, obj):
             if obj.default_address:
                 return obj.default_address.contact
             return None
     
        def get_unit_number(self, obj):
             if obj.default_address:
                 return obj.default_address.unit_number
             return None
     
        def get_street_number(self, obj):
             if obj.default_address:
                 return obj.default_address.street_number
             return None
     
        def get_address_line1(self, obj):
             if obj.default_address:
                 return obj.default_address.address_line1
             return None
     
        def get_address_line2(self, obj):
             if obj.default_address:
                 return obj.default_address.address_line2
             return None
     
        def get_city(self, obj):
             if obj.default_address:
                 return obj.default_address.city
             return None
     
        def get_region(self, obj):
             if obj.default_address:
                 return obj.default_address.region
             return None
     
        def get_postal_code(self, obj):
             if obj.default_address:
                 return obj.default_address.postal_code
             return None
     
     
        def get_country(self, obj):
             if obj.default_address and obj.default_address.country:
                 return obj.default_address.country.country_name
             return None
     