from django.urls import path, include
from . import views
from .views import Shiv, Indianbakery, cart, checkout, register, login, search1, search2
from accounts.middleware.auth import auth_middleware

urlpatterns = [

    path ("register", register.as_view(), name="register"),
    path ("login", login.as_view(), name="login"),
    path ("logout", views.logout, name="logout"),
    path ("", views.home, name="home"),
    path ("grocery", views.grocery, name="Groceries"),
    path ("bakery", views.bakery, name="Bakery"),
    path ("medical", views.medical, name="Medical"),
    path ("electronic", views.electronic, name="Electronics"),
    path ("hospital", views.hospital, name="Hospital"),
    path ("clothing", views.clothing, name="Clothing"),
    path ("shiv", Shiv.as_view(), name="shiv"),
    path ("indianbakery", Indianbakery.as_view(), name="indianbakery"),
    path ("comingsoon", views.comingsoon, name="commingsoon"),
    path ("cart", cart.as_view(), name="cart"),
    path ("checkout",auth_middleware(checkout.as_view()), name="checkout"),
    path ("confirmation", auth_middleware(views.confirmation), name="confirmation"),
    path ("search1", search1.as_view(), name="search1"),
    path ("search2", search2.as_view(), name="search2"),
]