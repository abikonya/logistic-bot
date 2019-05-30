from django.contrib import admin
from bot_app.models import AuthorizedCustomers, Products
# Register your models here.


class ACAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_id', 'created')
    search_fields = ('name', 'telegram_id')


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'task_id', 'zipcode', 'store_name', 'store_phone', 'order_number', 'pickup_person',
                    'pickup_location', 'more_info', 'product_category', 'product_item', 'price', 'created')
    search_fields = ('user_id', 'task_id', 'created')


admin.site.register(AuthorizedCustomers, ACAdmin)
admin.site.register(Products, ProductsAdmin)
