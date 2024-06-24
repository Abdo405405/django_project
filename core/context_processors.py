from Accounts.models import Advertisement_Board
from Product_Management_API.models import Category
def categories(request):

    categories = Category.objects.all()
    return {
       "categories": categories}

def list_advertisements(request):
    advertisements = Advertisement_Board.objects.filter(is_active=True)
    return {
        'advertisements': advertisements
    }