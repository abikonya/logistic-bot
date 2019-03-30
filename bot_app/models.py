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