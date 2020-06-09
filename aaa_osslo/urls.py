from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from entries import views as views_entries
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('', include('django.conf.urls.i18n')),
    path('', views_entries.index, name='index'),
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls"), name='accounts'),
    path("entries/", include("entries.urls"), name='entries'),
]

urlpatterns += staticfiles_urlpatterns()