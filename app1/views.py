from django.shortcuts import render, redirect 
from django.http import HttpResponse
from .models import Contact
from django.core.mail import send_mail
from django.conf import settings




# Create your views here.
def index(request): 
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        description = request.POST.get('description')
        contact = Contact(name=name, email=email, phone=phone, desc=description)
        contact.save()
    
    return render(request, 'contact.html')

def product(request):
    return render(request, 'product.html')


