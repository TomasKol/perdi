from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'accounts'

urlpatterns = [
    path('settings/', views.settings, name='settings'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('change_password/', views.change_password, name='change_password'),
    path('toggle_current_language/<slug:next_view>/', views.toggle_current_language, name='toggle_current_language'),
    path('toggle_translation_direction/', views.toggle_translation_direction, name='toggle_translation_direction'),
    path('set_current_language/<int:lang_id>', views.set_current_language, name='set_current_language'),
] 

urlpatterns += staticfiles_urlpatterns()