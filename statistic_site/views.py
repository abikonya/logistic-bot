from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from bot_app.api_func import get_status
from bot_app.models import Products, Statuses, Payments, Tickets
from django.db.models import Sum
from bot_app.dbworker import status_updater, payments_updater
from blockchain.wallet import Wallet
from bot_app.config import wallet_id, wallet_pass, host
from bot_app.models import User
from django.utils import timezone

wallet = Wallet(wallet_id, wallet_pass, host)


class MainView(TemplateView):
    template_name = 'main.html'
    login_template = 'enter_form.html'

    def get(self, request):
        if request.user.is_authenticated:
            statuses_request = get_status()
            # for each in statuses_request:
            #     status_updater(each)
            # payments_request = wallet.list_addresses()
            # for each in payments_request:
            #     payments_updater(each)
            ctx = dict()
            api = User.objects.get(username=request.user).api_address
            total_sum = Payments.objects.filter(username=request.user).aggregate(Sum('amount'))['amount__sum']
            if total_sum is not None:
                ctx['balance'] = total_sum
            else:
                ctx['balance'] = 0
            ctx['products'] = Products.objects.filter(api=api).order_by('-created')
            ctx['statuses'] = Statuses.objects.filter(api=api)
            ctx['process'] = Statuses.objects.filter(api=api, status='Process').count()
            ctx['confirm'] = Statuses.objects.filter(api=api, status='Confirm').count()
            ctx['cancel'] = Statuses.objects.filter(api=api, status='Cancel').count()
            ctx['paid'] = Statuses.objects.filter(api=api, status='Paid').count()
            ctx['total'] = Statuses.objects.filter(api=api).count()
            ctx['sum'] = Products.objects.filter(api=api).aggregate(Sum('price'))['price__sum']
            ctx['payments'] = Payments.objects.filter(username=request.user).order_by('-created')
            ctx['tickets'] = Tickets.objects.filter(username=request.user).order_by('-created')
            return render(request, self.template_name, ctx)
        else:
            return render(request, self.login_template, {})

    def post(self, request):
        new_ticket = Tickets(username=request.POST.get('username'),
                             description=request.POST.get('description'),
                             status='new')
        new_ticket.save()
        return HttpResponseRedirect('/lgstc/statistic/')


class LoginFormView(FormView):
    form_class = AuthenticationForm

    template_name = 'enter_form.html'

    success_url = '/statistic/'

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/statistic/login')


def getwallet(request, id):
    new_address = wallet.new_address(label=id)
    return HttpResponse(new_address.address)
