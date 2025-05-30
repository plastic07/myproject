
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('oauth2callback/', views.callback, name='oauth2callback'),
    path('orders/', views.create_order, name='create_order'),
    path('orders/get/', views.get_orders, name='get_orders'),
]

