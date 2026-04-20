import os

import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView

from payments.models import Item, Order


STRIPE_KEYS = {
    'usd': os.getenv('STRIPE_SECRET_KEY_USD'),
    'eur': os.getenv('STRIPE_SECRET_KEY_EUR'),
}


class BuyItemView(View):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        session = stripe.checkout.Session.create(
            api_key=STRIPE_KEYS[item.currency],
            payment_method_types=('card',),
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,

                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return JsonResponse({'id': session.id})


class GetItemView(View):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        return render(request, 'payments/item.html', {
            'item': item,
            'stripe_public_key': os.getenv('STRIPE_PUBLIC_KEY'),
        })


class SuccessView(TemplateView):
    template_name = 'payments/success.html'


class CancelView(TemplateView):
    template_name = 'payments/cancel.html'


class IndexView(View):
    def get(self, request):
        items = Item.objects.all()
        return render(request, 'payments/index.html', {'items': items})


class BuyOrderView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        line_items = [{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
            'tax_rates': [order.tax.stripe_tax_rate_id] if order.tax else [],
        } for item in order.items.all()]
        session = stripe.checkout.Session.create(
            api_key=STRIPE_KEYS[order.items.first().currency],
            payment_method_types=('card',),
            line_items=line_items,
            mode='payment',
            discounts=[{
                'coupon': order.discount.stripe_coupon_id,
            }] if order.discount else [],
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return JsonResponse({'id': session.id})


class GetOrderView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        return render(request, 'payments/order.html', {
            'order': order,
            'stripe_public_key': os.getenv('STRIPE_PUBLIC_KEY'),
            'currency': order.items.first().currency.upper()
            if order.items.exists() else '',
        })
