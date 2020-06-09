from django.db import models
from django.contrib.auth.models import User
from entries.models import Language

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  current_language = models.ForeignKey(Language, null=True, blank=True, on_delete=models.SET_NULL)
  translate_by_home_lang = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.user.username}/{self.current_language}"