import json
from django.shortcuts import render

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