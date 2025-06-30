import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category, Manufacturer, ShoppingCart, ShoppingCartElement
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import xlsxwriter
import io
from datetime import datetime

# Create your views here.
def main_page(request):
    return render(request, 'main_page.html')

def about_author(request):
    return render(request, 'about_author.html')

def about_stationery_store(request):
    return render(request, 'about_stationery_store.html')

def speciality(request):
    specialties = []  
    with open("dump.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    for specialty in data:
        if specialty.get("model") == "data.specialty":
            specialty_data = {
                "code": specialty["fields"].get("code"),
                "pk": specialty.get("pk"),
                "title": specialty["fields"].get("title"),
                "c_type": specialty["fields"].get("c_type"),
            }
            specialties.append(specialty_data)  
    return render(request, 'speciality.html',{'specialties': specialties})

def speciality_search(request):
    id = request.GET.get('code') 
    speciality_list = []
    with open("dump.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

        for speciality in data:
            if speciality.get('model') == "data.specialty" and (speciality["fields"].get("code") == id):
                    speciality_data = {
                        "code": speciality["fields"].get("code"),
                        "pk": speciality["pk"],
                        "title": speciality["fields"].get("title"),
                        "c_type": speciality["fields"].get("c_type"),
                    }
                    speciality_list.append(speciality_data)

    return render(request, "speciality_search.html", {'speciality': speciality_list})

def product_list(request):
    products = Product.objects.all()
    category = request.GET.get('category')
    manufacturer = request.GET.get('manufacturer')
    search_query = request.GET.get('search')

    if category:
        products = products.filter(category__id=category)
    if manufacturer:
        products = products.filter(manufacturer__id=manufacturer)
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query))
    
    context = {
        'products': products,
        'categories': Category.objects.all(),
        'manufacturers': Manufacturer.objects.all(),
    }
    return render(request, 'product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    
    cart_item, created = ShoppingCartElement.objects.get_or_create(
        shopping_cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart_view')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(ShoppingCartElement, pk=item_id, shopping_cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= cart_item.product.stock_quantity:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            pass
    return redirect('cart_view')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(ShoppingCartElement, pk=item_id, shopping_cart__user=request.user)
    cart_item.delete()
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart = get_object_or_404(ShoppingCart, user=request.user)
    cart_items = cart.shopping_cart_elements.all()
    total = cart.total_cost()
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('product_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def checkout(request):
    shopping_cart = get_object_or_404(ShoppingCart, user=request.user)
    shopping_cart_elements = shopping_cart.shopping_cart_elements.all()
    
    if request.method == 'POST':
        if not shopping_cart_elements:
            return redirect('cart_view')

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
    
        bold = workbook.add_format({'bold': True})
        money_format = workbook.add_format({'num_format': '#,##0.00'})
        
        worksheet.write('A1', 'Чек заказа', bold)
        worksheet.write('A2', 'Дата:', bold)
        worksheet.write('B2', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        worksheet.write('A3', 'Покупатель:', bold)
        worksheet.write('B3', request.user.username)
        
        worksheet.write('A5', 'Товар', bold)
        worksheet.write('B5', 'Количество', bold)
        worksheet.write('C5', 'Цена', bold)
        worksheet.write('D5', 'Сумма', bold)
        
        row = 6
        for item in shopping_cart_elements:
            worksheet.write(f'A{row}', item.product.name)
            worksheet.write(f'B{row}', item.quantity)
            worksheet.write(f'C{row}', float(item.product.price), money_format)
            worksheet.write(f'D{row}', float(item.element_cost()), money_format)
            row += 1
        
        worksheet.write(f'D{row}', 'Итого:', bold)
        worksheet.write(f'E{row}', float(shopping_cart.total_cost()), money_format)
        
        workbook.close()
        output.seek(0)
        excel_data = output.getvalue()
        
        subject = f'Ваш чек заказа от {datetime.now().strftime("%Y-%m-%d")}'
        message = 'Спасибо за ваш заказ! Во вложении вы найдете чек.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [request.user.email]
        
        email = EmailMessage(
            subject,
            message,
            from_email,
            recipient_list,
        )
        email.attach('order_receipt.xlsx', excel_data, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        
        html_message = render_to_string('order_confirmation.html', {
            'user': request.user,
            'shopping_cart': shopping_cart,
            'shopping_cart_elements': shopping_cart_elements,
            'total_cost': shopping_cart.total_cost(),
        })
        email.content_subtype = "html"
        email.body = html_message
        
        email.send(fail_silently=False)
        
        shopping_cart_elements.delete()
        
        return render(request, 'checkout_success.html')
    
    return render(request, 'checkout.html', {
        'shopping_cart_elements': shopping_cart_elements,
        'total_cost': shopping_cart.total_cost(),
    })