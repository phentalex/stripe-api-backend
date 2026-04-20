from unittest.mock import MagicMock

import pytest

from payments.models import Discount, Item, Order, Tax


@pytest.fixture
def item(db):
    return Item.objects.create(
        name='Test Item',
        description='Test description',
        price='100.00',
        currency='usd',
    )


@pytest.fixture
def order(db, item):
    order = Order.objects.create()
    order.items.add(item)
    return order


@pytest.fixture
def order_with_discount_and_tax(db, item):
    discount = Discount.objects.create(name='10%', stripe_coupon_id='SAVE10')
    tax = Tax.objects.create(name='VAT', stripe_tax_rate_id='txr_test')
    order = Order.objects.create(discount=discount, tax=tax)
    order.items.add(item)
    return order


@pytest.fixture
def mock_stripe_session():
    session = MagicMock()
    session.id = 'cs_test_session_id'
    return session
