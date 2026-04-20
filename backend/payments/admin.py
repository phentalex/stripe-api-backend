from django.contrib import admin, messages

from payments.models import Discount, Item, Order, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'currency')
    search_fields = ('name', 'description')
    list_filter = ('price', 'currency')
    ordering = ('name',)
    readonly_fields = ('id',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'total_price', )
    search_fields = ('id',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'total_price')

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        order = form.instance
        currencies = order.items.values_list('currency', flat=True).distinct()
        if currencies.count() > 1:
            order.items.clear()
            self.message_user(
                request,
                'All items must be in the same currency. '
                'Order has been cleared.',
                level=messages.ERROR
            )


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'stripe_coupon_id')
    search_fields = ('name', 'stripe_coupon_id')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'stripe_tax_rate_id')
    search_fields = ('name', 'stripe_tax_rate_id')
