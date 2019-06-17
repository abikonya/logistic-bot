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
    user_id = models.CharField(max_length=50, blank=True, verbose_name='User ID')
    task_id = models.CharField(max_length=50, blank=True, verbose_name='Номер заказа')
    zipcode = models.CharField(max_length=50, blank=True, verbose_name='Zipcode')
    store_name = models.CharField(max_length=50, blank=True, verbose_name='Название магазина')
    store_phone = models.CharField(max_length=50, blank=True, verbose_name='Телефон магазина')
    order_number = models.CharField(max_length=50, blank=True, verbose_name='Номер заказа')
    pickup_person = models.CharField(max_length=50, blank=True, verbose_name='Получатель')
    pickup_location = models.CharField(max_length=50, blank=True, verbose_name='Точка погрузки')
    more_info = models.TextField(blank=True, verbose_name='Дополнительное инфо')
    product_category = models.CharField(max_length=50, blank=True, verbose_name='Категория товара')
    product_item = models.CharField(max_length=50, blank=True, verbose_name='Товар')
    price = models.FloatField(max_length=50, blank=True, verbose_name='Цена')
    created = models.DateTimeField(max_length=50, auto_now_add=True, db_index=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'
        ordering = ['-created']


class Statuses(models.Model):
    user_id = models.CharField(max_length=50, blank=True, verbose_name='User ID')
    task_id = models.CharField(max_length=50, blank=True, verbose_name='Номер заказа')
    status = models.CharField(max_length=50, blank=True, verbose_name='Статус')
    updated = models.DateTimeField(max_length=50, auto_now_add=True, db_index=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name_plural = 'Статусы'
        verbose_name = 'Статус'
        ordering = ['-user_id', '-task_id', '-status']


class Wallets(models.Model):
    user_id = models.CharField(max_length=50, blank=True, verbose_name='User ID')
    address = models.CharField(max_length=50, blank=True, verbose_name='Address')
    created = models.DateTimeField(max_length=50, auto_now_add=True, db_index=True, verbose_name='Дата создания')

    class Meta:
        verbose_name_plural = 'Кошельки'
        verbose_name = 'Кошелек'
        ordering = ['-user_id']


class Payments(models.Model):
    user_id = models.CharField(max_length=50, blank=True, verbose_name='User ID')
    address = models.CharField(max_length=50, blank=True, verbose_name='Address')
    amount = models.CharField(max_length=50, blank=True, verbose_name='Amount')
    created = models.DateTimeField(max_length=50, auto_now_add=True, db_index=True, verbose_name='Дата создания')

    class Meta:
        verbose_name_plural = 'Платежи'
        verbose_name = 'Платеж'
        ordering = ['-user_id', '-address']
