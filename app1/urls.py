from django.contrib import admin
from django.urls import path, include
from app1 import views

#django admin header customization
admin.site.site_header = " login to Shopare"
admin.site.site_title = "Welcome to Shopare Dashboard"
admin.site.index_title = "Welcome Rudraksh Todwal"

urlpatterns = [

    path ("", views.index, name="home"),
    path ("about", views.about, name="about"),
    path ("contact", views.contact, name="contact"),
    path ("product", views.product, name="products"),

   
]
