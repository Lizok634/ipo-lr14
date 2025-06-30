from django.contrib import admin

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Category, Manufacturer, Product, ShoppingCart, ShoppingCartElement
from django.utils.html import format_html

# Register your models here.

@admin.register(Category)
class CategoryAdminModel(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")

@admin.register(Manufacturer)
class MakerAdminModel(admin.ModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name", "country")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_photo', 'price', 'stock_quantity', 'category', 'manufacturer')
    list_filter = ('category', 'manufacturer')
    search_fields = ('name', 'description')
    
    def display_photo(self, obj): 
        if obj.photo: 
            return format_html(                                                                              
                '<img src="{}" width="70" height="70" style="object-fit: contain; background: #f0f0f0;" />', 
                obj.photo.url
            )
        return "—"
    display_photo.short_description = 'Фото'

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email']
    fieldsets = (
        ('Персональная информация', {
            'fields': ('username', 'first_name', 'last_name', 'about_yourself', 'email', 'password')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'creation_date', 'total_cost')
    list_filter = ('creation_date',)
    search_fields = ('user__username',)
    readonly_fields = ('creation_date', 'total_cost') 
    fieldsets = (
        (None, {
            'fields': ('user', 'creation_date', 'total_cost')
        }),
    )

@admin.register(ShoppingCartElement)
class ShoppingCartElementAdmin(admin.ModelAdmin):
    list_display = ('shopping_cart', 'product', 'quantity', 'element_cost')
    list_filter = ('shopping_cart__user', 'product')
    search_fields = ('product__name', 'shopping_cart__user__username')
    readonly_fields = ('element_cost',)
    
    fieldsets = (
        (None, {
            'fields': ('shopping_cart', 'product', 'quantity')
        }),
    )