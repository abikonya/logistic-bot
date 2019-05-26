from django.db import models

# Create your models here.


class AuthorizedCustomers(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    telegram_id = models.IntegerField(null=False, verbose_name='Telegram ID')
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата авторизиции')

    class Meta:
        verbose_name_plural = 'Клиенты'
        verbose_name = 'Клиент'
        ordering = ['-created']


class Products(models.Model):
    user_id = models.CharField(max_length=50, null=False, verbose_name='User ID')
    zipcode = models.CharField(max_length=50, null=False, verbose_name='Zipcode')
    store_name = models.CharField(max_length=50, null=True, verbose_name='Название магазина')
    store_phone = models.CharField(max_length=50, null=True, verbose_name='Телефон магазина')
    order_number = models.CharField(max_length=50, null=False, verbose_name='Номер заказа')
    pickup_person = models.CharField(max_length=50, null=False, verbose_name='Получатель')
    pickup_location = models.CharField(max_length=50, null=False, verbose_name='Точка погрузки')
    more_info = models.TextField(null=True, verbose_name='Дополнительное инфо')
    product_category = models.CharField(max_length=50, null=False, verbose_name='Категория товара')
    product_item = models.CharField(max_length=50, null=False, verbose_name='Товар')
    price = models.CharField(max_length=50, null=False, verbose_name='Цена')
    created = models.DateTimeField(max_length=50, auto_now_add=True, db_index=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'
        ordering = ['-created']