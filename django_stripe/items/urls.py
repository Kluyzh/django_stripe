from django.urls import path

from .views import create_checkout_session, item_detail

urlpatterns = [
    path('items/<int:id>/', item_detail, name='item_detail'),
    path('buy/<int:id>/', create_checkout_session,
         name='create_checkout_session'),
]
