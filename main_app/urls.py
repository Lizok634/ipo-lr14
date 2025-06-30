from django.urls import path
from .views import about_author, main_page, about_stationery_store, speciality, speciality_search

urlpatterns = [
    path('', main_page, name='main_page'),
    path('about_author', about_author, name='about_author'),
    path('about_stationery_store', about_stationery_store, name='about_stationery_store'),
    path('spec/', speciality, name='speciality'),
    path('speciality_search', speciality_search, name='speciality_search')
]