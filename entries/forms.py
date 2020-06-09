from django import forms
from .models import Language, Article, Entry, Topic, Translation
from django.utils.translation import gettext_lazy as _

class AddLanguageForm(forms.ModelForm):
  name = forms.CharField(widget=forms.TextInput(
    attrs={'placeholder': _('language'), 'title': _('name of the language'), 'autocomplete': 'off', 'autofocus': 'on'}))
  abbreviation = forms.CharField(widget=forms.TextInput(
    attrs={'placeholder': _('abbreviation (max 4 chars)'), 'title': _('abbreviation')}))

  class Meta:
    model = Language
    fields = ['name', 'abbreviation',]

class EditArticlesForm(forms.ModelForm):
  name = forms.CharField(widget=forms.TextInput(
    attrs={'placeholder': _('article'), 'required': 'true', 'maxlength': '5'}
  ))

  class Meta:
    model = Article
    fields = ['name']

class EditTopicForm(forms.ModelForm):

  name = forms.CharField(widget=forms.TextInput(
    attrs={'required': 'true', 'placeholder': _('topic name')}
  ))

  class Meta:
    model = Article
    fields = ['name']

class EntryForm(forms.ModelForm):

  name = forms.CharField(widget=forms.TextInput(
    attrs={'required': 'true', 'placeholder': _('new word'), 'autofocus': 'on'}
  ))

  commentary = forms.CharField(
    required=False,
    widget=forms.Textarea(
      attrs={'placeholder': _('commentary'), 'cols': '17', 'rows': '1'}
    )
  )

  class Meta:
    model = Entry
    fields = ['name', 'commentary']

class TranslationForm(forms.ModelForm):

  content = forms.CharField(
    required=True,
    widget=forms.TextInput(
      attrs={'placeholder': _('translation*'), 'required': 'true'}
    )
  )

  note = forms.CharField(
    required=False,
    widget=forms.Textarea(
      attrs={'placeholder': _('translation note'), 'cols': '17', 'rows': '1'}
    )
  )

  class Meta:
    model = Translation
    fields = ['content', 'note']


