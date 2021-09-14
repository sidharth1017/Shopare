from django.shortcuts import render, redirect
from app1.models import Product
from app1.models import Order
from app1.models import Customer
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User, auth
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import View

#html email reqiured stuff
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags




# Create your views here.

class register(View):
    def get(delf, request):
        return render(request, 'register.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email').lower()
        password = postData.get('password')

        error_message = None

        customer = Customer(first_name=first_name,
                                last_name=last_name,
                                phone=phone,
                                email=email,
                                password=password)
        #Validation

        value = {
            'first_name' : first_name,
            'last_name' : last_name,
            'phone' : phone,
            'email' : email,

        }

        if len(phone) <= 10:
            error_message = 'Enter valid number'
        elif len(email) < 4:
            error_message = 'Email must be 4 character'
        elif len(password) < 6:
            error_message = 'Password must be 6 character'
        elif customer.isExists():
            error_message = 'Email Address Already Taken'
        

        #Saving
        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect ('login')
        else:
            data = {
                'error': error_message,
                'values' : value
            }
            return render(request, 'register.html', data)


class login(View):
    return_url = None
    def get(self, request):
        login.return_url = request.GET.get('return_url')
        return render(request, 'login.html') 
    
    def post(self, request):
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password , customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['customer_name'] = customer.first_name
                request.session['email'] = customer.email
                if login.return_url:
                    return HttpResponseRedirect(login.return_url)
                else:
                    login.return_url = None
                    return redirect("/accounts/")
            else:
                error_message = 'Email or Password invalid !!'

        else:
            error_message = 'Email or Password invalid !!'
        return render(request, 'login.html', {'error' : error_message})
        

        
def logout(request):
    request.session.clear()
    return redirect("/")

def home(request):
    return render(request, 'home.html')
    

def grocery(request):
    return render(request, 'grocery.html')
def bakery(request):
    return render(request, 'bakery.html')
def medical(request):
    return render(request, 'medical.html')
def electronic(request):
    return render(request, 'electronic.html')
def hospital(request):
    return render(request, 'hospital.html')
def clothing(request):
    return render(request, 'clothing.html')
def comingsoon(request):
    return render(request, 'comingsoon.html')

class Shiv(View):
    def post(self, request):
        Product = request.POST.get('product')
        cart = request.session.get('cart')
        remove = request.POST.get('remove')
        if cart:
            quantity = cart.get(Product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(Product)
                    else:
                        cart[Product] = quantity-1
                else:
                    cart[Product] = quantity+1
            else:
                cart[Product] = 1
        else:
            cart = {}
            cart[Product] = 1

        request.session['cart'] = cart
        return redirect('shiv')
        
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
        products = None
        products = Product.get_all_products_by_id(1)
        return render(request, 'shiv.html' , {'products' : products})

class Indianbakery(View):
    def post(self, request):
        Product = request.POST.get('product')
        cart = request.session.get('cart')
        remove = request.POST.get('remove')
        if cart:
            quantity = cart.get(Product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(Product)
                    else:
                        cart[Product] = quantity-1
                else:
                    cart[Product] = quantity+1
            else:
                cart[Product] = 1
        else:
            cart = {}
            cart[Product] = 1

        request.session['cart'] = cart
        return redirect('indianbakery')

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
        products = None
        products = Product.get_all_products_by_id(2)
        return render(request, 'indianbakery.html', {'products' : products})

    
class cart(View):
    def post(self, request):
        Product = request.POST.get('product')
        cart = request.session.get('cart')
        remove = request.POST.get('remove')
        if cart:
            quantity = cart.get(Product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(Product)
                    else:
                        cart[Product] = quantity-1
                else:
                    cart[Product] = quantity+1
            else:
                cart[Product] = 1
        else:
            cart = {}
            cart[Product] = 1

        request.session['cart'] = cart
        return redirect('cart')

    def get(self, request):
        cart = request.session.get('cart') 
        if not cart:
            request.session['cart'] = {}
            Products = None
        else:    
            ids = list(request.session.get('cart').keys())
            Products = Product.get_products_by_id(ids) 
        return render(request, 'cart.html',{'products' : Products})


 
class checkout(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        cart = request.session.get('cart')
        payment = request.POST.get('payment_method')
        customer = request.session.get('customer')
        mail = request.session.get('email')
        name = request.session.get('customer_name')
        products = Product.get_products_by_id(list(cart.keys()))
        total = request.POST.get('total')
        #send the html mail
        html_content = render_to_string('emailtemplate.html',{'products' : products,'name':name,'total':total,'payment':payment})
        text_content = strip_tags(html_content)
        emailsend = EmailMultiAlternatives(
            #subject
            "Order Confirmation!",
            #content
            text_content,
            #from email
            settings.EMAIL_HOST_USER,
            #to 
            [mail], 
        )
        emailsend.attach_alternative(html_content,"text/html")
        emailsend.send()        

        # for product in products:
        #     order = Order(customers = Customer(id = customer),
        #                   product = product,
        #                   price = product.price,
        #                   quantity = cart.get(str(product.id)),
        #                   address = address,
        #                   phone = phone,
        #                   payment_choice = payment
        #     )
            
        #     order.placeOrder()
        
        request.session['cart'] = {}
        return redirect('confirmation')


def confirmation(request):
    return render(request, 'confirmation.html')

class search1(View):
    def get(self, request):
        q = request.GET.get('search')
        if q:
            products = Product.objects.filter(product_name__contains = q, category=1)
            context = {'query':q, 'products':products}
        else:
            context = {}
        return render(request, "search1.html", context)

class search2(View):
    def get(self, request):
        q = request.GET.get('search')
        if q:
            products = Product.objects.filter(product_name__contains = q, category=2)
            context = {'query':q, 'products':products}
        else:
            context = {}
        return render(request, "search2.html", context)