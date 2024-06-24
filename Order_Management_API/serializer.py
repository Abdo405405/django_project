# serializers.py
from rest_framework import serializers
from .models import CartOrder, CartOrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartOrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = CartOrder
        fields = '__all__'

    def get_order_items(self, obj):
        order_items = obj.order_items.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return serializer.data
    
    
