from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UnicodeUsernameValidator, UserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail


class AuthorizedCustomers(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    telegram_id = models.IntegerField(null=False, verbose_name='Telegram ID')
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата авторизиции')

    class Meta:
        verbose_name_plural = 'Пользователи Бота'
        verbose_name = 'Пользователь'
        ordering = ['-created']


class Products(models.Model):
    api = models.CharField(max_length=150, verbose_name='API адрес добавления')
    telegram_id = models.CharField(max_length=50, verbose_name='Telegram ID')
    user_id = models.CharField(max_length=50, blank=True, verbose_name='User ID')
    task_id = models.CharField(max_length=50, blank=True, verbose_name='Номер заказа')
    zipcode = models.CharField(max_length=50, blank=True, verbose_name='Zipcode')
    store_name = models.CharField(max_length=50, blank=True, verbose_name='Название магазина')
    store_phone = models.CharField(max_length=50, null=True, verbose_name='Телефон магазина')
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
    api = models.CharField(max_length=150, verbose_name='API адрес добавления')
    task_id = models.CharField(max_length=50, blank=True, verbose_name='Номер заказа')
    status = models.CharField(max_length=50, blank=True, verbose_name='Статус')
    updated = models.DateTimeField(max_length=50, auto_now_add=True, db_index=True, verbose_name='Дата создания')

    class Meta:
        verbose_name_plural = 'Статусы'
        verbose_name = 'Статус'
        ordering = ['-api', '-task_id', '-status']


class Payments(models.Model):
    username = models.CharField(max_length=50, verbose_name='Username')
    address = models.CharField(max_length=50, blank=True, verbose_name='Address')
    amount = models.CharField(max_length=50, null=True, verbose_name='Amount')
    created = models.DateTimeField(max_length=50, auto_now_add=True, db_index=True, verbose_name='Дата создания')

    class Meta:
        verbose_name_plural = 'Платежи'
        verbose_name = 'Платеж'
        ordering = ['-username', '-address']


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    telegram = models.CharField(_('telegram'), max_length=30, blank=True)
    jabber = models.CharField(_('jabber'), max_length=30, blank=True)
    api_address = models.CharField(_('api address'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = False

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = self.username
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class ConnectedApi(models.Model):
    address = models.CharField(max_length=500, verbose_name='Адрес API')
    get_distance = models.CharField(max_length=500, verbose_name='Запрос get_distance')
    get_all = models.CharField(max_length=500, verbose_name='Запрос get_all')
    add_data = models.CharField(max_length=500, verbose_name='Запрос add_data')
    get_category = models.CharField(max_length=500, verbose_name='Запрос get_category')
    get_items = models.CharField(max_length=500, verbose_name='Запрос get_items')
    get_status = models.CharField(max_length=500, verbose_name='Запрос get_status')
    payment = models.CharField(max_length=500, verbose_name='Запрос payment')

    class Meta:
        verbose_name_plural = 'Адреса API'
        verbose_name = 'Адрес API'
        ordering = ['-address']


class Tickets(models.Model):
    username = models.CharField(max_length=50, verbose_name='Username')
    description = models.CharField(max_length=500, verbose_name='Description')
    answer = models.CharField(max_length=500, verbose_name='Answer', default='Fill')
    status = models.CharField(max_length=50, verbose_name='Status')
    created = models.DateTimeField(max_length=50, auto_now_add=True, db_index=True, verbose_name='Дата создания')

    class Meta:
        verbose_name_plural = 'Тикеты'
        verbose_name = 'Тикет'
        ordering = ['-username', '-status', '-created']
