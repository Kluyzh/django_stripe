import os

import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Item, Order

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    context = {
        'item': item,
        'STRIPE_PUBLISHABLE_KEY': os.getenv('STRIPE_PUBLISHABLE_KEY')
    }
    return render(request, 'items/item_detail.html', context)


def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    context = {
        'order': order,
        'STRIPE_PUBLISHABLE_KEY': os.getenv('STRIPE_PUBLISHABLE_KEY')
    }
    return render(request, 'items/order_detail.html', context)


def create_checkout_session(request, id):
    item = get_object_or_404(Item, id=id)
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount': item.get_price_in_cents(),
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri('/') + '?success=true',
            cancel_url=request.build_absolute_uri('/') + '?canceled=true',
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def create_order_checkout_session(request, id):
    order = get_object_or_404(Order, id=id)
    try:
        line_items = []
        for order_item in order.orderitem_set.all():
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': order_item.item.name,
                        'description': order_item.item.description,
                    },
                    'unit_amount': order_item.item.get_price_in_cents(),
                },
                'quantity': order_item.count,
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/') + '?success=true',
            cancel_url=request.build_absolute_uri('/') + '?canceled=true',
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
