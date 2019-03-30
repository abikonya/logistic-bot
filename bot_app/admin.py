from django.contrib import admin
from bot_app.models import AuthorizedCustomers
# Register your models here.


class ACAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_id', 'created')
    search_fields = ('name', 'telegram_id')


admin.site.register(AuthorizedCustomers, ACAdmin)
