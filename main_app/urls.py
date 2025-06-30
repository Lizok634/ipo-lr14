from django.urls import path
from .views import about_author, main_page, about_stationery_store

urlpatterns = [
    path('', main_page, name='main_page'),
    path('about_author', about_author, name='about_author'),
    path('about_stationery_store', about_stationery_store, name='about_stationery_store')
]