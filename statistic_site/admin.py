from django.contrib import admin
from bot_app.models import User, Statuses, Products, Payments
from statistic_site.models import Statistic
from django.conf.urls import url
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.db.models import Sum


class StatisticAdmin(admin.ModelAdmin):
    list_display = ['user', 'process', 'confirm', 'canceled', 'paid', 'total_orders', 'sum']
    search_fields = ['user', 'process', 'confirm', 'canceled', 'paid', 'sum']

    def get_urls(self):
        urls = super().get_urls()

        new_urls = [
            url(r'^update_info/$', self.admin_site.admin_view(self.update_info),
                name='Обновить данные')
        ]
        return new_urls + urls

    def change_list(self, request):
        context = (self.admin_site.each_context(request))
        return TemplateResponse(request, 'admin/statistic_site/change_list.html', context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['balance'] = Payments.objects.all().aggregate(Sum('amount'))['amount__sum']
        return super(StatisticAdmin, self).changelist_view(request, extra_context=extra_context)

    def update_info(self, request):
        for each in User.objects.all():
            obj, created = Statistic.objects.update_or_create(
                user=each.username,
                canceled=Statuses.objects.filter(api=each.api_address, status='Cancel').count(),
                process=Statuses.objects.filter(api=each.api_address, status='Process').count(),
                confirm=Statuses.objects.filter(api=each.api_address, status='Confirm').count(),
                paid=Statuses.objects.filter(api=each.api_address, status='Paid').count(),
                total_orders=Statuses.objects.filter(api=each.api_address).count(),
                sum=Products.objects.filter(api=each.api_address).aggregate(Sum('price'))['price__sum']
            )
        return HttpResponseRedirect('/admin/statistic_site/statistic/')


admin.site.register(Statistic, StatisticAdmin)
