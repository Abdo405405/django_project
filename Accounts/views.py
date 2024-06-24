from django.shortcuts import render
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from userauths.models import User 
from .models import Vendor ,Country,Customer
from django.contrib.auth.hashers import make_password 
from rest_framework import status  # status of creation user 
from .serializer import SignUpSerializer , AdminInfoSerializer , UpdateVendorSerializer , UpdateCustomerSerializer,VendorInfoSerializer , CustomerInfoSerializer
from rest_framework.permissions import IsAuthenticated  
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.http import Http404
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
@api_view(["POST"])
def register(request):
    data=request.data.copy()
    gender = data.get("gender",None)
    is_vendor = data.get("is_vendor",None)
    if gender : 
        data["gender"] = gender.lower() 
    if is_vendor : 
     is_vendor = str(data["is_vendor"])  # Convert boolean to string
     is_vendor = is_vendor.lower()  # Convert the rest of the string to lowercase
     is_vendor = is_vendor.capitalize()  # Capitalize first letter
     is_vendor = is_vendor == "True" or is_vendor == "1"
    #  data["is_vendor"]=is_vendor
    user=SignUpSerializer(data=data)
    if user.is_valid():
        if not User.objects.filter(email=data["email"]).exists():
            user=User.objects.create(
                  username = data["username"]
                , email=data["email"]
                , password=make_password(data["password"])
                , first_name=data["first_name"]
                , last_name=data["last_name"]
                , gender=data["gender"]
                , birthday=data["birthday"]
                ,is_vendor=is_vendor
            )
            return Response ( {"Details" : "Your Account registered successfuly"},status=status.HTTP_201_CREATED)
        else:
             return Response ( {"Error" : "This Account is already exist ! "},status=status.HTTP_400_BAD_REQUEST)
    else:
         return Response ( user.errors)


@api_view (["GET"])
@permission_classes ([IsAuthenticated])
def admin_info (request):
    if request.user.is_superuser:
     user = AdminInfoSerializer(request.user,many=False)
     return Response (user.data)
    else:
        return Response ({"Error":"UNAUTHORIZED USER"
                          ,"AUTHORIZED USER":"only superusers"})


@api_view (["GET"])
@permission_classes ([IsAuthenticated])
def vendor_info (request):
    try :
     vendor=Vendor.objects.get(user=request.user)
     serializer = VendorInfoSerializer(vendor,many=False)
     return Response (serializer.data)
    except Vendor.DoesNotExist:
        return Response ( {"Error" : "This Vendor does not exist ! "},status=status.HTTP_400_BAD_REQUEST)
    

@api_view (["GET"])
@permission_classes ([IsAuthenticated])
def customer_info (request):
    try :
     customer=Customer.objects.get(user=request.user)
     serializer = CustomerInfoSerializer(customer,many=False)
     return Response (serializer.data)
    except Customer.DoesNotExist:
        return Response ( {"Error" : "This Customer does not exist ! "},status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
        if request.user == vendor.user or request.user.is_superuser:
         data = request.data.copy()
         country = data.get("country",None)
         if country:
          country=data["country"]
          country_object = Country.objects.get(country_name__icontains=country)
          data["country"] = country_object.pk
         serialzer = UpdateVendorSerializer(vendor, data=data, partial=True)
         if serialzer.is_valid():
             serialzer.save()
             return Response(serialzer.data)
         else:
             # Handle serializer validation errors
             raise ValidationError(serialzer.errors)
        else:
            return Response({"Error":"UNAUTHORIZED USER ","Details":"This user cannot access this account. Please check if this token belongs to this vendor."
                           ,"AUTHORIZED USERS ":"Superusers and The account Owner"}, status=status.HTTP_401_UNAUTHORIZED)
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
    except Country.DoesNotExist:
                return Response({"country": "not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_customer(request):
     try: 
        cutomer= Customer.objects.get(user=request.user)
        if request.user == cutomer.user or request.user.is_superuser:
         data = request.data.copy()
         country = data.get("country",None)
         if country:
          country=data["country"]
          country_object = Country.objects.get(country_name__icontains=country)
          data["country"] = country_object.pk
         serializer=UpdateCustomerSerializer(cutomer,data=data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data)
         else:
             # Handle serializer validation errors
             raise ValidationError(serializer.errors)
        else:
            return Response({"Error":"UNAUTHORIZED USER ","Details":"This user cannot access this account. Please check if this token belongs to this vendor."
                           ,"AUTHORIZED USERS ":"Superusers and The account Owner"}, status=status.HTTP_401_UNAUTHORIZED)
     except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
     except Country.DoesNotExist:
                return Response({"country": "not found"}, status=status.HTTP_404_NOT_FOUND)               

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_account(request):
    try:
     user = User.objects.get(pk=request.user.pk)
     user.delete()
     return Response({"Success":" The Account deleted successfully"})
    except User.DoesNotExist:
             return Response({"Error":"This Account does not exist"})
    


