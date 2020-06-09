from django.contrib import admin
from .models import Language, Article, Entry, Topic, Translation

admin.site.register(Language)
admin.site.register(Article)
admin.site.register(Entry)
admin.site.register(Topic)
admin.site.register(Translation)