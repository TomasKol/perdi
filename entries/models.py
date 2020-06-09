from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Lower


class Language(models.Model):
  name = models.CharField(max_length=50)
  abbreviation = models.CharField(max_length=4)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='languages')

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['abbreviation', 'user'], name='constraint - unique language')
    ]

  def __str__(self):
    return f"{self.abbreviation} {self.name}"


class Article(models.Model):
  # every new language will come automatically with a zero article to be matched with entries without an article
  # this is so the unique constraint of Entry model could work for such words (no article broke the assertion)
  name = models.CharField(max_length=5)
  language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='articles')
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['name', 'language', 'user'], name='constraint - unique article')
    ]

  def __str__(self):
    name = self.name or '--'
    return f"{name} / {self.language.abbreviation} / {self.user} "


class Topic(models.Model):
  name = models.CharField(max_length=50)
  language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='topics')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  def __str__(self):
    return f"{self.name} / {self.language.abbreviation} / {self.user} "

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['name', 'language', 'user'], name='constraint - unique topic')
    ]
    ordering = [Lower('name')]


class Entry(models.Model):
  name = models.CharField(max_length=200)
  language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='entries')
  commentary = models.CharField(max_length=500, blank=True, null=True)
  article = models.ForeignKey(Article, on_delete=models.SET_NULL, related_name='entries', blank=True, null=True)
  topic = models.ForeignKey(Topic, related_name='entries', blank=True, null=True, on_delete=models.SET_NULL)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['name', 'language', 'user', 'article'], name='constraint - unique entry')
    ]
    ordering = [Lower('name')]

  def full_name(self):
    if self.article:
      return f"{self.article.name} {self.name}"
    return f"{self.name}"

  def __str__(self):
    article = f"{self.article.name}" if self.article else '--'
    topic = f"({self.topic.name})" if self.topic else ''
    return f"{article} {self.name} {topic} / {self.language.abbreviation}, {self.user}"


class Translation(models.Model):
  entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='translations')
  content = models.CharField(max_length=200)
  note = models.CharField(max_length=500, blank=True, null=True)
  language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='translations')
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='translations')
  def __str__(self):
    return f"{self.content} => {self.entry.name} / {self.language.abbreviation} / {self.entry.user} "
    
  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['entry', 'content'], name='constraint - unique translation')
    ]

    ordering = [Lower('content')]

