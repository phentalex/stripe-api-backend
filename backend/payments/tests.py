from http import HTTPStatus
from unittest.mock import patch

from django.urls import reverse


class TestPageViews:
    def test_index_returns_200(self, client, db):
        response = client.get(reverse('index'))
        assert response.status_code == HTTPStatus.OK

    def test_item_page_returns_200(self, client, item):
        response = client.get(reverse('get_item', args=(item.pk,)))
        assert response.status_code == HTTPStatus.OK

    def test_item_page_404(self, client, db):
        response = client.get(reverse('get_item', args=(999,)))
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_order_page_returns_200(self, client, order):
        response = client.get(reverse('get_order', args=(order.pk,)))
        assert response.status_code == HTTPStatus.OK

    def test_order_page_404(self, client, db):
        response = client.get(reverse('get_order', args=(999,)))
        assert response.status_code == HTTPStatus.NOT_FOUND


class TestBuyItem:
    def test_buy_item_returns_session_id(
        self,
        client,
        item,
        mock_stripe_session
    ):
        with patch(
            'stripe.checkout.Session.create',
            return_value=mock_stripe_session
        ):
            response = client.get(reverse('buy_item', args=(item.pk,)))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'id': 'cs_test_session_id'}

    def test_buy_item_404(self, client, db):
        response = client.get(reverse('buy_item', args=(999,)))
        assert response.status_code == HTTPStatus.NOT_FOUND


class TestBuyOrder:
    def test_buy_order_returns_session_id(
        self,
        client,
        order,
        mock_stripe_session
    ):
        with patch(
            'stripe.checkout.Session.create',
            return_value=mock_stripe_session
        ):
            response = client.get(reverse('buy_order', args=(order.pk,)))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'id': 'cs_test_session_id'}

    def test_buy_order_with_discount_and_tax(
        self, client, order_with_discount_and_tax, mock_stripe_session
    ):
        with patch(
            'stripe.checkout.Session.create', return_value=mock_stripe_session
        ) as mock_create:
            response = client.get(
                reverse('buy_order', args=(order_with_discount_and_tax.pk,))
            )
        assert response.status_code == HTTPStatus.OK
        assert mock_create.call_args.kwargs['discounts'] == [
            {'coupon': 'SAVE10'}
        ]

    def test_buy_order_404(self, client, db):
        response = client.get(reverse('buy_order', args=(999,)))
        assert response.status_code == HTTPStatus.NOT_FOUND
