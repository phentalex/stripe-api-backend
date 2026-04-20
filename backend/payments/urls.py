from django.urls import path

from payments.views import (BuyItemView, BuyOrderView, CancelView,
                            GetItemView, GetOrderView, IndexView,
                            SuccessView)


urlpatterns = [
    path('buy/order/<int:pk>/', BuyOrderView.as_view(), name='buy_order'),
    path('buy/<int:pk>/', BuyItemView.as_view(), name='buy_item'),
    path('item/<int:pk>/', GetItemView.as_view(), name='get_item'),
    path('order/<int:pk>/', GetOrderView.as_view(), name='get_order'),
    path('success/', SuccessView.as_view(), name='payment_success'),
    path('cancel/', CancelView.as_view(), name='payment_cancel'),
    path('', IndexView.as_view(), name='index'),
]
