from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from bot_app.models import AuthorizedCustomers


class MainView(TemplateView):
    template_name = 'main.html'
    login_template = 'enter_form.html'

    def get(self, request):
        if request.user.is_authenticated:
            customers = AuthorizedCustomers.objects.all()
            ctx = dict()
            ctx['customers'] = customers
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
