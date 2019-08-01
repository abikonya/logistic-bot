from django.db import models
from bot_app.models import User


class Statistic(models.Model):

    user = models.CharField(max_length=64, verbose_name='Имя пользователя')
    canceled = models.IntegerField(verbose_name='Отменено')
    process = models.IntegerField(verbose_name='В процессе')
    confirm = models.IntegerField(verbose_name='Принято')
    paid = models.IntegerField(verbose_name='Оплачено')
    total_orders = models.IntegerField(verbose_name='Заказов всего')
    sum = models.FloatField(null=True, default=0, verbose_name='Общая сумма')

    class Meta:
        verbose_name_plural = 'Статистика'
