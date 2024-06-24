from django import forms 
from .models import CartOrderItem , CartOrder ,Product
class CartOrderItemForm(forms.ModelForm):
     class Meta:
        model = CartOrderItem
        fields = '__all__'
        
        widgets = {
            'total_price': forms.TextInput(attrs={'readonly': True,"placeholder":"Auto-fill"}),  }
    

class CartOrderForm (forms.ModelForm):
     class Meta : 
          model = CartOrder 
          fields="__all__"
          widgets={
               "invoice_no" : forms.TextInput(attrs={'readonly':True , 'placeholder':"Auto-fill",}),
               "total_price":forms.TextInput(attrs={'readonly':True,'placeholder':"Auto-fill",'value':''}),
               "item":forms.TextInput(attrs={'placeholder':"Select"})
          }