from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from bot_app.api_func import get_status
from bot_app.models import Products, Statuses, Payments
from django.db.models import Sum
from bot_app.dbworker import status_updater, payments_updater
from blockchain.wallet import Wallet
from blockchain.blockexplorer import get_address
from bot_app.config import wallet_id, wallet_pass, host, bitcoin_token

wallet = Wallet(wallet_id, wallet_pass, host)


class MainView(TemplateView):
    template_name = 'main.html'
    login_template = 'enter_form.html'

    def get(self, request):
        if request.user.is_authenticated:
            statuses_request = get_status(request.user)['package_list']
            for each in statuses_request:
                status_updater(request.user, each)
            payments_request = wallet.list_addresses()
            for each in payments_request:
                payments_updater(request.user, each)
            ctx = dict()
            if request.user == 'admin':
                ctx['balance'] = wallet.get_balance()
            else:
                ctx['balance'] = Payments.objects.filter(telegram_id=request.user).aggregate(Sum('amount'))['amount__sum']
            ctx['products'] = Products.objects.filter(telegram_id=request.user)
            ctx['statuses'] = Statuses.objects.filter(telegram_id=request.user)
            ctx['process'] = Statuses.objects.filter(telegram_id=request.user, status='Process').count()
            ctx['confirm'] = Statuses.objects.filter(telegram_id=request.user, status='Confirm').count()
            ctx['cancel'] = Statuses.objects.filter(telegram_id=request.user, status='Cancel').count()
            ctx['paid'] = Statuses.objects.filter(telegram_id=request.user, status='Paid').count()
            ctx['total'] = Statuses.objects.filter(telegram_id=request.user).count()
            ctx['sum'] = Products.objects.filter(telegram_id=request.user).aggregate(Sum('price'))['price__sum']
            ctx['payments'] = Payments.objects.filter(telegram_id=request.user)
            return render(request, self.template_name, ctx)
        else:
            return render(request, self.login_template, {})


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
