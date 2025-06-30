from django.shortcuts import render

# Create your views here.
def main_page(request):
    return render(request, 'main_page.html')

def about_author(request):
    return render(request, 'about_author.html')

def about_stationery_store(request):
    return render(request, 'about_stationery_store.html')