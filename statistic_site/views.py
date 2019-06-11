from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from bot_app.api_func import get_status
from bot_app.models import Products, Statuses
from bot_app.dbworker import status_updater
from blockchain.wallet import Wallet


wallet = Wallet('fde7f71c-3c5b-45ad-bf60-8736d92e3ae6', 'lkebalsdu771WJndssR0!nccvLhG', 'http://localhost:3000/')


class MainView(TemplateView):
    template_name = 'main.html'
    login_template = 'enter_form.html'

    def get(self, request):
        if request.user.is_authenticated:
            print(request.user)
            statuses_request = get_status(request.user)['package_list']
            for each in statuses_request:
                if Statuses.objects.get(task_id=each['pack_id']):
                    status_updater('D87hd487ft4', each)
            ctx = dict()
            if request.user == 'admin':
                ctx['balance'] = wallet.get_balance()
            else:
                ctx['balance'] = '$BALANCE$'
            ctx['products'] = Products.objects.filter(user_id=request.user)
            ctx['statuses'] = Statuses.objects.filter(user_id=request.user)
            ctx['process'] = Statuses.objects.filter(user_id=request.user, status='Process').count()
            ctx['confirm'] = Statuses.objects.filter(user_id=request.user, status='Confirm').count()
            ctx['cancel'] = Statuses.objects.filter(user_id=request.user, status='Cancel').count()
            ctx['paid'] = Statuses.objects.filter(user_id=request.user, status='Paid').count()
            ctx['total'] = Statuses.objects.filter(user_id=request.user).count()

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
