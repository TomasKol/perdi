from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _

class RegistrationForm(UserCreationForm):
  username = forms.CharField(widget=forms.TextInput(
    attrs={'placeholder': _('username'), 'title': _('username'), 'autocomplete': 'off'}))
  password1 = forms.CharField(widget=forms.PasswordInput(
    attrs={'placeholder': _('password'), 'title': _('password')}))
  password2 = forms.CharField(widget=forms.PasswordInput(
    attrs={'placeholder': _('confirm password'), 'title': _('confirm password')}))

  class Meta:
    model = User
    fields = ['username', 'password1', 'password2',]

class LoginForm(AuthenticationForm):
  username = forms.CharField(widget=forms.TextInput(
    attrs={'placeholder': _('username'), 'title': _('username'), 'autocomplete': 'off'}))
  password = forms.CharField(widget=forms.PasswordInput(
    attrs={'placeholder': _('password'), 'title': _('password')}))

  class Meta:
    model = User
    fields = ['username', 'password']

class PasswordForm(PasswordChangeForm):
  old_password = forms.CharField(widget=forms.PasswordInput(
    attrs={'placeholder': _('old password'), 'title': _('old password'), 'autocomplete': 'off'}))
  new_password1 = forms.CharField(widget=forms.PasswordInput(
    attrs={'placeholder': _('new password'), 'title': _('new password')}))
  new_password2 = forms.CharField(widget=forms.PasswordInput(
    attrs={'placeholder': _('confirm new password'), 'title': _('confirm new password')}))

  class Meta:
    model = User
    fields = ['old_password', 'new_password1', 'new_password2',]
