from django.urls import include, path
from . import views

app_name = "products"
urlpatterns = [
    path("all_products/", views.products_display_all, name="display_all_products"),
    path("product/<str:pk>/", views.product_by_id, name="display_all_products"),
    path("product<str:pk>/<slug:slug>/", views.product_detail, name="product_detail"),
    path("create_product/", views.create_product, name="create_product"),
    path("delete_product<str:pk>/", views.delete_product, name="delete_product"),
    path("update_product<str:pk>/", views.update_product, name="update_product"),
    

    path("all_categories/",views.categories_display_all,name="categories_display_all"),
    path("category<str:pk>/",views.Category_by_id,name="categories_display_all"),
    path("create_category/", views.create_category, name="create_category"),
    path("update_category<str:pk>/", views.update_category, name="update_category"),
    path("delete_category<str:pk>/", views.delete_category, name="delete_category"),


    path("all_feedbacks/product/<str:pk>/", views.Feedbacks_of_Product, name="Feedbacks_of_Product"),
    path("feedback/product/<str:pk>/", views.create_or_update_feedback, name="create_or_update_feedback"),
    path("delete_feedback/product/<str:pk>/", views.delete_feedback, name="delete_feedback"),


    
    
    
    path("next_page/", views.page_next, name="page_next"),
    path("page_display/", views.page_display, name="page_display"),
    path("<slug:category_slug>/", views.category_listPage, name="category_listPage"),
]
