from django.db import models


class CurrencyChoices(models.TextChoices):
    USD = 'usd', 'USD'
    EUR = 'eur', 'EUR'


class Item(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=1000,
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2,
    )
    currency = models.CharField(
        verbose_name='Валюта',
        max_length=3,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.USD,
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.name} ({self.price} {self.currency.upper()})'


class Discount(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    stripe_coupon_id = models.CharField(
        verbose_name='ID купона в Stripe',
        max_length=255,
    )

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    stripe_tax_rate_id = models.CharField(
        verbose_name='ID налоговой ставки в Stripe',
        max_length=255,
    )

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(
        Item,
        verbose_name='Товары',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    discount = models.ForeignKey(
        Discount,
        verbose_name='Скидка',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    tax = models.ForeignKey(
        Tax,
        verbose_name='Налог',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order #{self.id}'

    def total_price(self):
        return sum(item.price for item in self.items.all())
