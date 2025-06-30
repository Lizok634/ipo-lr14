from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.

class CustomUser(AbstractUser):
    about_yourself = models.TextField(blank=True, null=True, verbose_name="О себе", max_length=200)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="user",
    )
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Category(models.Model):
    name = models.CharField(max_length = 100, verbose_name = "Название")
    description = models.TextField(blank = True, null = True, verbose_name = "Описание")
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Manufacturer(models.Model):
    name = models.CharField(max_length = 200, verbose_name = "Название")
    country = models.CharField(max_length = 100, verbose_name = "Страна")
    description = models.TextField(blank = True, null = True, verbose_name = "Описание")

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

class Product(models.Model):
    name = models.CharField(max_length = 200, verbose_name = "Название")
    description = models.TextField(verbose_name = "Описание")
    photo = models.ImageField(blank = True, null = True, upload_to = "products/", verbose_name = "Фото товара")
    price = models.DecimalField(
        decimal_places = 2, 
        max_digits = 10,
        validators = [MinValueValidator(0)],
        verbose_name = "Цена"
    )
    stock_quantity = models.IntegerField(
        validators = [MinValueValidator(0)],
        verbose_name = "Количество на складе"
    )
    category = models.ForeignKey(
        Category,
        on_delete = models.CASCADE,
        verbose_name = "Категория"
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete = models.CASCADE,
        verbose_name = "Производитель"
    )

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def clean(self):
        if self.price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        if self.stock_quantity < 0:
            raise ValidationError("Количество на складе не может быть отрицательным")
        
class ShoppingCart(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete = models.CASCADE,
        verbose_name = "Пользователь"
    )
    creation_date = models.DateTimeField(
        auto_now_add = True,
        verbose_name = "Дата создания"
    )

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"
    
    def total_cost(self):
        return sum(item.element_cost() for item in self.shopping_cart_elements.all())
    
    total_cost.short_description = 'Общая стоимость'

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

class ShoppingCartElement(models.Model):
    shopping_cart = models.ForeignKey(
        ShoppingCart,
        on_delete = models.CASCADE,
        verbose_name = "Корзина",
        related_name = 'shopping_cart_elements'
    )
    product = models.ForeignKey(
        Product,
        on_delete = models.CASCADE,
        verbose_name = "Товар"
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"
    
    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
    
    def element_cost(self):
        return self.product.price * self.quantity
    
    element_cost.short_description = 'Стоимость элемента'

    def clean(self):
        if self.quantity > self.product.stock_quantity:
            raise ValidationError(
                f"Недостаточно товара на складе. Доступно: {self.product.stock_quantity}"
            )