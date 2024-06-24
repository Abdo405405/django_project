from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CartOrder , CartOrderItem , PaymentStatus ,PaymentMode,OrderStatus
from Product_Management_API.models import Product
from Accounts.models import Customer  
from Payment_Management_API.models import   User_Payment_Method
from rest_framework import status  # status of creation user 
from .serializer import OrderSerializer
from rest_framework.decorators import permission_classes 
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@permission_classes(IsAuthenticated)
@api_view(["POST"])
def new_order (request):
    try:
      user = request.user 
      data=request.data 
      customer = Customer.objects.get(user=user)
      customer_id= customer.id
      order_items=data.get("order_items",None)
      order_status=data.get("order_status",None)
      payment_status=data.get("payment_status",None)
      payment_mode=data.get("payment_mode",None)
      payment_id=data.get("payment_id",None)
      if (order_status not in OrderStatus.values and  order_status) or order_status=="" : 
           return Response({'error': f"Invalid order_status. Choices are: {', '.join(OrderStatus.labels)}"}, status=status.HTTP_400_BAD_REQUEST)
      if (payment_status not in PaymentStatus.values and payment_status) or payment_status==""   : 
           return Response({'error': f"Invalid payment_status. Choices are: {', '.join(PaymentStatus.labels)}"}, status=status.HTTP_400_BAD_REQUEST)
      if (payment_mode not in PaymentMode.values and payment_mode)  or payment_mode=="": 
           return Response({'error': f"Invalid payment_mode. Choices are: {', '.join(PaymentMode.labels)}"}, status=status.HTTP_400_BAD_REQUEST)
      

      if not order_items or  len(order_items)==0 :
          return Response ({'error': "No order recived" }, status=status.HTTP_400_BAD_REQUEST)
      else:
        for item in order_items : 
                  if "qty"  not in item : 
                     return Response({'qty': f"this field is required "}, status=status.HTTP_400_BAD_REQUEST)
                  if "product_id" not in item : 
                     return Response({'product_id': f"this field is required "}, status=status.HTTP_400_BAD_REQUEST)    
        payment_type = User_Payment_Method.objects.get(user = user , id = data["payment_id"])
        shipping_address = customer.default_address

        order=CartOrder.objects.create(
              customer = Customer.objects.get(id=customer_id),
              order_status=order_status,
              payment_status=payment_status,
              payment_mode=payment_mode,
              payment_type= payment_type,
              shipping_address=shipping_address,
          )
        for item in order_items : 
              id_of_product = item["product_id"]
              try : 
                   product = Product.objects.get(id = id_of_product)
              except Product.DoesNotExist: 
                       return Response({'error': f" Product with id {id_of_product } does not exist"}, status=status.HTTP_400_BAD_REQUEST)
  
              item = CartOrderItem.objects.create(
                  order = order, 
                  product=product,
                  image=product.image,
                  qty=item["qty"],
              )
  
              new_qty=product.qty_in_stock-item.qty
              if new_qty < 0 :
                  return Response({'error': f'Insufficient stock for product {product.title}'}, status=status.HTTP_400_BAD_REQUEST)
              else:
                  product.qty_in_stock=new_qty
                  product.save()
              order.product.add(product)
        serializer = OrderSerializer(order , many=False)
        return Response(serializer.data)
    except User_Payment_Method.DoesNotExist:
              return Response({'error': f" Payment_Method with id {payment_id} does not exist For this customer"}, status=status.HTTP_400_BAD_REQUEST)
    except Customer.DoesNotExist:
              return Response({'error': "this Customer with does not exist"}, status=status.HTTP_400_BAD_REQUEST)
  
@api_view(["GET"])
def get_orders (request):
     orders = CartOrder.objects.all()
     serializer = OrderSerializer(orders,many=True)
     return Response ({"orders":serializer.data})

@api_view(["GET"])
def single_order (request ,pk):
    try:
      order = CartOrder.objects.get(id = pk )
      serializer = OrderSerializer(order,many=False)
      return Response ({"order":serializer.data})
    except CartOrder.DoesNotExist:
         return Response({"Error":"This order does not Exist"},status=status.HTTP_404_NOT_FOUND)

@permission_classes(IsAuthenticated)   
@api_view(["PUT"])
def change_order_status (request ,pk):
    try:
      order = CartOrder.objects.get(id = pk )
      order_staus = request.data.get("order_status")
      if order_staus not in OrderStatus.values :
           return Response({'Error': f"Invalid order_status. Choices are: {', '.join(OrderStatus.labels)}"}, status=status.HTTP_400_BAD_REQUEST)
      order.order_status = order_staus
      order.save()
      serializer = OrderSerializer(order,many=False)
      return Response ({"order":serializer.data})
    except CartOrder.DoesNotExist:
         return Response({"Error":"This order does not Exist"},status=status.HTTP_404_NOT_FOUND)

@api_view(["DELETE"])
def delete_order (request ,pk):
    try:
      order = CartOrder.objects.get(id = pk )
      order.delete()
      return Response({"details":"order is deleted successfully"})
    except CartOrder.DoesNotExist:
         return Response({"Error":"This order does not Exist"},status=status.HTTP_404_NOT_FOUND)