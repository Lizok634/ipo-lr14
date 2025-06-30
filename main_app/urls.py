from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('about_author', views.about_author, name='about_author'),
    path('about_stationery_store', views.about_stationery_store, name='about_stationery_store'),
    path('spec/', views.speciality, name='speciality'),
    path('speciality_search', views.speciality_search, name='speciality_search'),
    
    path('catalog/', views.product_list, name='product_list'),
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),
]