from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, PasswordForm
from .models import Profile
from entries.models import Language
from entries.views import index as entries_index, add_entry as entries_add_entry
from django.utils.translation import gettext_lazy as _


@login_required
def settings(request):
  return render (request, 'accounts/settings.html')

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      Profile.objects.create(user=user)
      login(request, user)
      return redirect('entries:my_languages')
  else:
    form = RegistrationForm()
  context = {'form': form}
  return render(request, 'accounts/register.html', context)

def login_view(request):
  if request.method == 'POST':
    form = LoginForm(data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)

      if 'next' in request.POST:
        return redirect(request.POST.get('next'))
      if not request.user.profile.current_language:
        # user with no languages cannot be redirected to the dictionary section
        return redirect('entries:my_languages')
      return redirect('entries:index')
  else:
    form = LoginForm()
  context = {'form': form}
  return render(request, 'accounts/login.html', context)

@login_required
def logout_view(request):
  logout(request)
  return redirect('accounts:login')

@login_required
def change_password(request):
  if request.method == 'POST':
    form = PasswordForm(request.user, request.POST)
    if form.is_valid():
      user = form.save()
      update_session_auth_hash(request, user)
      return render(request, 'accounts/change_password.html', {'message': _('Your password has been changed.')})
  else:
    form = PasswordForm(request.user)
  context = {'form': form}
  return render(request, 'accounts/change_password.html', context)

@login_required
def delete_user(request):
  # custom_error and form_valid are a hack to make sure that only the current user 
  # can be deleted (no cross-account deletion) while there is no way of hinting that 
  # you guessed the credentials of some other user

  custom_error = False
  if request.method == 'GET':
    form = LoginForm()
  else:
    form = LoginForm(data=request.POST)
    form_valid = form.is_valid()
    if request.user.username != request.POST.get('username'):
      form_valid = False
      custom_error = True
    if form_valid:
      user = form.get_user()
      user.delete()
      request.user = None
      request.method = 'GET'
      return login_view(request)

  return render(request, 'accounts/delete_user.html', {'form': form, 'custom_error': custom_error})

@login_required
def toggle_current_language(request, next_view):

  if Language.objects.filter(user=request.user).exists():

    languages = []
    for language in Language.objects.filter(user=request.user).order_by('id'):
      languages.append(language)
    curr_lang = request.user.profile.current_language
    curr_index = languages.index(curr_lang)

    curr_index += 1
    if curr_index == len(languages):
      curr_index = 0

    request.user.profile.current_language = languages[curr_index]
    request.user.profile.save()  

  if next_view == 'entries':
    return entries_index(request)
  if next_view == 'add_entry':
    return entries_add_entry(request)
  return HttpResponse(status=204)
    
@login_required
def set_current_language(request, lang_id):
  if Language.objects.filter(pk=lang_id, user=request.user).exists:
    for language in Language.objects.filter(user=request.user):
      if language.id == lang_id:
        request.user.profile.current_language = language
        request.user.profile.save()  
        return entries_add_entry(request)
  return HttpResponse('wrong language')

@login_required
def toggle_translation_direction(request):
  request.user.profile.translate_by_home_lang = not request.user.profile.translate_by_home_lang
  request.user.profile.save()
  return redirect(entries_index)
