from django.contrib import admin
from app1.models import Contact
from app1.models import Product
from app1.models import Category
from app1.models import Order
from app1.models import Customer


class AdminProduct(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'category']


admin.site.register(Contact)
admin.site.register(Product, AdminProduct)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Customer)



