from django.shortcuts import render ,get_object_or_404
from rest_framework.decorators import api_view  , permission_classes
from rest_framework import status
from rest_framework.response import Response
from .models import Product , Category ,ProductFeedback
from Accounts.models import Vendor 
from .serializers import ProductSerializer , UpdateProductSerializer ,CreateProductSerializer, CategorySerializer ,CreateCategorySerializer , UpdateCategorySerializer , GetFeedbacksOfProduct
from . import filters
from rest_framework.pagination import PageNumberPagination
from math import ceil
from django.utils import text
from rest_framework.permissions import IsAuthenticated 
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import Avg
from Accounts.models import Customer
from rest_framework.exceptions import ValidationError

# Create your views here.
def product_detail ( request , pk ,slug) :
    product = get_object_or_404 (Product , slug=slug , pk=pk) 
    product_images=[ image.image.url for image in product.product_images.all()]
    context={
      "product":product,  
      "images":product_images
    }
    return render (request,"core/product_detail.html",context)

def category_listPage (request , category_slug):
    # Categories=list_categories1(request)
    category = get_object_or_404(Category , slug=category_slug)
    num_all_products=Product.activated_products.filter(category=category).count()
    num_pages = ceil(num_all_products/7)
    category_id=category.id           # to get category_id then pass next-page function by hx-get = "url" 
    # page_range = range(1, num_pages + 1)
    context={
        "category_id":category_id,
        "category_title":category.title,
        # "page_range":page_range,
        "Items_found" : num_all_products,
        "num_pages":num_pages
    }
    return render (request ,"core/category_listPage.html",context)

def page_next(request):
        num_page= int(request.GET.get("value"))
        category_id=request.GET.get("category_id")
        all_products=Product.activated_products.filter(category_id=category_id)
        all_products=all_products[::-1]
        start_idx=(7 * (num_page-1))
        end_idx=start_idx + 7
        all_products=all_products[::-1]
        products=all_products[start_idx:end_idx]
        # print(all_products)
        context={
             "products":products
        }
        return render(request,"core/pagination_bar/pages.html",context)
def page_display(request):
     category_id=request.GET.get("category_id")
     action=int(request.GET.get("action"))
     value1= int(request.GET.get("value1"))
     value2= int(request.GET.get("value2"))
     value3= int(request.GET.get("value3"))
     num_pages=int(request.GET.get("num_pages"))
    #  if page2 == num_pages:
    #       return HttpResponse("")
     if action :
          page1=value2
          page2=value3
          page3 = page2+1
     else:                                
          page1=value1-1
          page2=value1
          page3=value2       
     context={
          "page1":page1,
          "page2":page2,
          "page3":page3,
          "category_id":category_id,
          "action":action,
          "num_pages":num_pages
     }
     return render (request,"core/pagination_bar/next_previous_page.html",context)

##############################################################################
############################## Products APIs #################################
##############################################################################

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def products_display_all (request):
     try:
        products = Product.activated_products.all().order_by("id")
        filter_set = filters.ProductsFilter(request.GET , queryset=products)
        count = filter_set.qs.count()
        max_products_per_page= 10 
        total_pages=ceil(count/max_products_per_page)
        paginator = PageNumberPagination()
        paginator.page_size = max_products_per_page
        queryset = paginator.paginate_queryset(filter_set.qs,request)
        print(filter_set.qs)
        serializer= ProductSerializer(queryset, many=True )
        context={
              "max_products_per_page":max_products_per_page ,
              "total_pages":total_pages ,
              "total products found":count,
             "products":serializer.data ,
        }
        return Response(context ,status=status.HTTP_200_OK) 
       
     except ValidationError as e:
        error_message = e.args[0] if e.args else 'Unknown error'
        return Response({"Error": error_message}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def product_by_id (request,pk):
     products=get_object_or_404 (Product , pk = pk)
     # if products.vendor.user == request.user or request.user.is_superuser:
     serializer= ProductSerializer(products,many=False)
     return Response({"products":serializer.data}) 
     # else:
     #      return Response({"Error":"UNAUTHORIZED USER ","Details":"This vendor cannot access this product. Please check if this token belongs to this vendor."
     #                       ,"AUTHORIZED USERS ":"Superusers and The Product Owner"}, status=status.HTTP_401_UNAUTHORIZED)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_product(request):
    try:
            vendor = Vendor.objects.get(user = request.user) 
            data = request.data.copy()  # Create a mutable copy of request data
            product_status = data.get("product_status", None)
            category = data.get("category", None)
            data["vendor"] = vendor.id
            if not category : 
                return Response({"category":"This field is required"})
            if product_status:
                data["product_status"] = product_status.lower()  # Convert to lowercase
            
            category_name = data.get("category")  # Corrected from "caegory" to "category_name"
            category = Category.objects.get(title__icontains=category_name)  # Use icontains for partial matching

            data["category"] = category.id
            if "subcategory" in data:
             sub_category_name = data.get("subcategory")
             if sub_category_name:
                 sub_category = get_object_or_404(Category, title__icontains=sub_category_name)
                 data["subcategory"] = sub_category.id
            serializer = CreateProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    except Vendor.DoesNotExist:
        return Response({"error": "This vendor does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    except Category.DoesNotExist:
        return Response({"Error":"This category does not exist "})

      
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_product(request,pk):
     product=get_object_or_404(Product ,pk=pk)
     if product.vendor.user == request.user or request.user.is_superuser:
          data = request.data.copy()  # Create a mutable copy of request data
          product_status = data.get("product_status", None)
          if product_status:
            data["product_status"] = product_status.lower()  # Convert to lowercase
          serializer = UpdateProductSerializer(product,data=data,partial=True)
          if serializer.is_valid():
                if 'title' in serializer.validated_data:
                     slug = text.slugify(serializer.validated_data['title'])
                     serializer.validated_data['slug'] = slug
                     serializer.validated_data["url"]=f"/api/product{product.id}/{slug}"
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
          else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     else:
          return Response({"Error":"UNAUTHORIZED USER ","Details":"This vendor cannot access this product. Please check if this token belongs to this vendor."
                           ,"AUTHORIZED USERS ":"Superusers and The Product Owner"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_product(request,pk):
    product = get_object_or_404(Product, pk=pk)
    if product.vendor.user == request.user or request.user.is_superuser:
     product.delete()
     return Response({f"product:{product}":"is deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    else:
          return Response({"Error":"UNAUTHORIZED USER ","Details":"This vendor cannot access this product. Please check if this token belongs to this vendor.",
"AUTHORIZED USERS ":"Superusers and The Product Owner"}, status=status.HTTP_401_UNAUTHORIZED)

# Category API
     
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def categories_display_all(request):
     if request.user.is_superuser:
      Categories = Category.objects.all()
      max_category_per_page = 10
      count= Categories.count()
      total_pages=ceil(count/max_category_per_page)
      paginator=PageNumberPagination()
      paginator.page_size = max_category_per_page
      querset=paginator.paginate_queryset(Categories,request)
      serializer=CategorySerializer(querset,many=True)
      context={
           "max_category_per_page" : max_category_per_page,
           "total_pages" : total_pages , 
           "total_categories":count ,
           "categories":serializer.data
      }
      return Response(context,status=status.HTTP_202_ACCEPTED)
     else: 
          return Response({"Error":"UNAUTHORIZED USER ","AUTHORIZED USERS ":" Only Superusers"}, status=status.HTTP_401_UNAUTHORIZED)
     
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def Category_by_id(request,pk):
     if request.user.is_superuser:
      category = get_object_or_404(Category,pk=pk)
      serializer=CategorySerializer(category,many=False)
      return Response({"category":serializer.data},status=status.HTTP_202_ACCEPTED)
     else: 
          return Response({"Error":"UNAUTHORIZED USER ","AUTHORIZED USERS ":" Only Superusers"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_category(request):
     if request.user.is_superuser:
      serializer=CreateCategorySerializer(data=request.data)
      if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     else: 
          return Response({"Error":"UNAUTHORIZED USER ","AUTHORIZED USERS ":" Only Superusers"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_category(request,pk):
     if request.user.is_superuser:
       category=get_object_or_404(Category,pk=pk)
       serializer=UpdateCategorySerializer(category,data=request.data)
       if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     else: 
         return Response({"Error":"UNAUTHORIZED USER ","AUTHORIZED USERS ":" Only Superusers"}, status=status.HTTP_401_UNAUTHORIZED)
           
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_category(request,pk):
     if request.user.is_superuser:
          category = get_object_or_404(Category,pk=pk)
          category.delete()
          return Response ({f"category:{category}":"Deleted successfully"},status=status.HTTP_204_NO_CONTENT)
     else: 
          return Response({"Error":"UNAUTHORIZED USER ","AUTHORIZED USERS ":" Only Superusers"}, status=status.HTTP_401_UNAUTHORIZED)
     
     # Category API

# Feedback API
@api_view(["GET"])
def Feedbacks_of_Product (request , pk) : 
    try:
     product=Product.objects.get(pk=pk)
     print(product)
     feedbacks=product.feedback.all()
     filter_set_feedbacks = filters.FeedbackFilter(request.GET , queryset=feedbacks)
     count=filter_set_feedbacks.qs.count()
     num_feedbacks_per_page=20
     total_pages=ceil(count/num_feedbacks_per_page)
     paginator=PageNumberPagination()
     paginator.page_size=num_feedbacks_per_page
     feedbacks=paginator.paginate_queryset(filter_set_feedbacks.qs,request)
     serializer=GetFeedbacksOfProduct(feedbacks , many=True)
     context={
         "Num_feedbacks":count,
         "num_feedbacks_per_page":num_feedbacks_per_page,
         "num_total_pages":total_pages,
         "Feedbacks":serializer.data,
     }
     return Response (context)
    except Product.DoesNotExist:
        return Response({"Error":" This Product does not exist"})
    except ValidationError as e:
        error_message = e.args[0] if e.args else 'Unknown error'
        return Response({"Error": error_message}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def create_or_update_feedback(request,pk):
   try: 
    user=request.user
    customer=Customer.objects.get(user=user)
    product=Product.objects.get(pk=pk)     
    feedback = product.feedback.filter(customer=customer) #get only feedback related to this product from registred customer
    data=request.data.copy()
    customer_rating = int(data.get("rating" , None))
    print(type(customer_rating))
    customer_comment = data.get("comment" , None)
    if not (customer_rating >=0 and customer_rating<=5) :
        return Response({"Error":" Reating Should be from 1 to 5"})
    elif feedback.exists():                           # if it exist then update it 
        new_feedback = {f"{field}": value for field , value in data.items()} # this dynamic feedback user can submit eather comment or rating
        feedback.update(**new_feedback)   
        if  customer_rating:      
         rating=product.feedback.aggregate(avg_rating = Avg("rating")) # avarge of all ratings(this customer and others) of this product  
         product.rating=rating["avg_rating"]                           # update rating of the product
         product.save()
        return Response({"details":" Feedback updated successfully"})
    else:                                          # else created new feedback if it does not exist
         ProductFeedback.objects.create(
             product=product,
             customer=customer,
             rating=customer_rating,
             comment=customer_comment
         )     
         rating=product.feedback.aggregate(avg_rating = Avg("rating"))        # avarge of all ratings(this customer and others) of this product
         if  customer_rating:
          product.rating=rating["avg_rating"]                                  # update rating of the product
          product.save()    
         return Response({"details":" Feedback created successfully"})
   except Customer.DoesNotExist :
       return Response({"Error":" This Customer does not exist"})
   except Product.DoesNotExist:
       return Response({"Error":" This Product does not exist"})

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_feedback(request,pk):
    try:
      user=request.user
      customer=Customer.objects.get(user=user)
      product=Product.objects.get(pk=pk)     
      feedback = product.feedback.filter(customer=customer) #get only feedback related to this product from registred customer
      feedback.delete()
      rating = product.feedback.aggregate(avg_rating=Avg("rating"))
      product.rating=rating["avg_rating"]
      product.save()
      return Response({"details":" This Feedback deleted successfully"})
    except Customer.DoesNotExist:
        return Response({"Error":" This Customer does not exist"})
    except Product.DoesNotExist:
        return Response({"Error":" This Product does not exist"})

        

        
     
        

