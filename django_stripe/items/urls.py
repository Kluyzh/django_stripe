from django.urls import path

from .views import (create_checkout_session, create_order_checkout_session,
                    item_detail, order_detail)

urlpatterns = [
    path('items/<int:id>/', item_detail, name='item_detail'),
    path('buy/<int:id>/', create_checkout_session,
         name='create_checkout_session'),
    path('order/<int:id>/', order_detail, name='order_detail'),
    path('buy_order/<int:id>/', create_order_checkout_session,
         name='create_order_checkout_session'),
]
