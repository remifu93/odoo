from django.contrib import admin
from .models import Customer, OrderProduct, OrderLine, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('companyName', 'city', 'country')
    search_fields = ('companyName', 'city')


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'type')
    search_fields = ('name', 'sku')


@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('order', 'orderProduct', 'quantity', 'unitPrice')
    list_filter = ('orderProduct',)
    search_fields = ('orderProduct__name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'fiscal_position', 'status')
    list_filter = ('status',)
    search_fields = ('customer__companyName', 'fiscal_position')
