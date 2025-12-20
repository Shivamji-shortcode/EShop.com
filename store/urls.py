from django.contrib import admin
from django.urls import path
from .views.home import Index, store
from .views.signup import Signup
from .views.login import Login, logout
from .views.cart import Cart
from .views.checkout import CheckOut, create_order, verify_payment  # ✅ added here
from .views.orders import OrderView
from .views import profile
from .middlewares.auth import auth_middleware

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store, name='store'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('cart', auth_middleware(Cart.as_view()), name='cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('profile/', profile.profile_view, name='profile'),
    # path('index',)
    # ✅ Razorpay payment routes
    path('create-order', create_order, name='create_order'),
    path('verify-payment', verify_payment, name='verify_payment'),
]
        