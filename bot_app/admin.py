from django.contrib import admin
from bot_app.models import AuthorizedCustomers, Products, Statuses, Payments, ConnectedApi
from bot_app.models import (User as MyUser)
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from django.db import models
from django.conf import settings


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'telegram', 'jabber', 'api_address')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'telegram', 'jabber', 'api_address',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('telegram', 'jabber', 'email', 'api_address')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'telegram', 'jabber', 'api_address', 'is_staff')
    search_fields = ('username', 'telegram', 'jabber', 'email')


class ACAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_id', 'created')
    search_fields = ('name', 'telegram_id')


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('api', 'telegram_id', 'user_id', 'task_id', 'zipcode', 'store_name', 'store_phone', 'order_number', 'pickup_person',
                    'pickup_location', 'more_info', 'product_category', 'product_item', 'price', 'created')
    search_fields = ('api', 'task_id', 'created')


class StatusesAdmin(admin.ModelAdmin):
    list_display = ('api', 'task_id', 'status', 'updated')
    search_fields = ('api', 'task_id', 'status', 'updated')


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('username', 'address', 'amount', 'created')
    search_fields = ('username', 'address', 'amount', 'created')


class ConnectedApiAdmin(admin.ModelAdmin):
    list_display = ('address', 'get_distance', 'get_all', 'add_data', 'get_category', 'get_items', 'get_status', 'payment')
    search_fields = ('address',)


admin.site.register(AuthorizedCustomers, ACAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Statuses, StatusesAdmin)
admin.site.register(Payments, PaymentsAdmin)
admin.site.register(MyUser, UserAdmin)
admin.site.register(ConnectedApi, ConnectedApiAdmin)
admin.site.unregister(Group)
