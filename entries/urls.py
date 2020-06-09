from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'entries'

urlpatterns = [
    path('', views.index, name='index'),
    path('my_languages/', views.my_languages, name='my_languages'),
    path('add_language/', views.add_language, name='add_language'),
    path('edit_language/<int:lang_id>/', views.edit_language, name='edit_language'),
    path('delete_language/', views.delete_language, name='delete_language'),
    path('edit_articles/<int:lang_id>/', views.edit_articles, name='edit_articles'), # if you change edit_articles here, make the change also in the delete_article view
    path('add_articles/<int:lang_id>/', views.add_articles, name='add_articles'),
    path('delete_article/', views.delete_article, name='delete_article'),
    path('edit_topics/<int:lang_id>/', views.edit_topics, name='edit_topics'), 
    path('add_topics/<int:lang_id>/', views.add_topics, name='add_topics'),
    path('delete_topic/', views.delete_topic, name='delete_topic'),
    path('add_entry/', views.add_entry, name='add_entry'),
    path('edit_entry/<int:entry_id>', views.edit_entry, name='edit_entry'),
    path('delete_entry/', views.delete_entry, name='delete_entry'),
    path('edit_translations/<int:entry_id>', views.edit_translations, name='edit_translations'),
    path('delete_translation/', views.delete_translation, name='delete_translation'),
    path('add_translation/<int:entry_id>', views.add_translation, name='add_translation'),
    
]

urlpatterns += staticfiles_urlpatterns()