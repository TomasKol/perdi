from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.db import IntegrityError
from .models import Entry, Language, Translation, Article, Topic
from .forms import AddLanguageForm, EditArticlesForm, EditTopicForm, EntryForm, TranslationForm
from .helpers import sanitize_string_input
from django.utils.translation import gettext_lazy as _

@login_required
def index(request):
  if request.user.profile.translate_by_home_lang:
    return get_translations(request)
  return get_entries(request)

@login_required
def get_entries(request):
  entries = Entry.objects.filter(
    user=request.user,
    language=request.user.profile.current_language,
  )
  context = {
    'entries': entries,
  }
  return render(request, 'entries/get_entries.html', context)

@login_required
def get_translations(request):
  translations = Translation.objects.filter(
    user=request.user,
    language=request.user.profile.current_language,
  )
  context = {
    'translations': translations,
  }
  return render(request, 'entries/get_translations.html', context)

@login_required
def my_languages(request):

  languages_query = Language.objects.filter(user=request.user)
  languages = []
  for language in languages_query:
    current_language = {
      'language': language,
      'entries': len(language.entries.all()),
      'translations': len(language.translations.all()),
      'topics': len(language.topics.all())
    }
    languages.append(current_language)

  context = {
    'languages': languages
  }

  return render(request, 'entries/languages.html', context)

@login_required
def add_language(request):

  duplicit = False
  abbreviation = ''

  if request.method == 'POST':
    form = AddLanguageForm(request.POST)

    if form.is_valid():

      abbreviation_caps = request.POST.get('abbreviation').upper()
  
      if Language.objects.filter(
        user=request.user, abbreviation=abbreviation_caps
      ):
        duplicit = True
        abbreviation = request.POST.get('abbreviation')

      else:

        # save the new language
        new_language = form.save(commit=False)
        new_language.user = request.user
        new_language.abbreviation = abbreviation_caps
        new_language.save()

        # process and save the articles, default zero article first
        Article.objects.create(user=request.user, language=new_language, name='')
        articles_set = sanitize_string_input(request.POST.get('articles'))
        for article in articles_set:
          Article.objects.create(user=request.user, language=new_language, name=article)

        # set this language as user's current_language
        request.user.profile.current_language = new_language
        request.user.profile.save()

        return edit_language(request, new_language.id)

  else:
    form = AddLanguageForm()

  context = {
    'form': form, 
    'duplicit': duplicit, 
    'abbreviation': abbreviation
  }
  return render(request, 'entries/add_language.html', context)

@login_required
def edit_language(request, lang_id):
  
  language = get_object_or_404(Language, pk=lang_id)
  duplicit = False
  abbreviation = ''

  if request.method == 'POST':
    form = AddLanguageForm(request.POST, instance=language)

    if form.is_valid():
      abbreviation_caps = request.POST.get('abbreviation').upper()

      if Language.objects.filter(
        user=request.user, 
        abbreviation=abbreviation_caps,
      ).exclude(pk=language.id):
        duplicit = True
        abbreviation = abbreviation_caps

      else:
        edited_language = form.save(commit=False)
        edited_language.abbreviation = abbreviation_caps
        edited_language.save()

        request.method = 'GET'
        return edit_language(request, lang_id)

    else:
      language = get_object_or_404(Language, pk=lang_id)

  else:
    form = AddLanguageForm(instance=language)

  context = {
    'language': language,
    'form': form,
    'duplicit': duplicit, 
    'abbreviation': abbreviation, # don't use language.abbreviation,
    'articles': language.articles.all()[1:], # to exclude the zero article
  }

  return render(request, 'entries/edit_language.html', context)

@login_required
def delete_language(request):
  language = get_object_or_404(
    Language,
    user=request.user,
    pk=request.POST.get('id')
  )

  if Language.objects.filter(user=request.user).exclude(pk=language.id).exists():
    if language == request.user.profile.current_language: 
      request.user.profile.current_language = Language.objects.filter(user=request.user).exclude(pk=language.id)[0]
  else:
    request.user.profile.current_language = None

  language.delete()
  request.user.profile.save()  

  return HttpResponse(status=204)

@login_required
def edit_articles(request, lang_id):

  articles = []
  language = get_object_or_404(Language, pk=lang_id, user=request.user)
  integrity_error = ''

  if request.method == 'GET':
    articles = language.articles.all().exclude(name='')
    ArticlesFormSet = modelformset_factory(Article, form=EditArticlesForm, extra=0)
    formset = ArticlesFormSet(queryset=articles)

  else:
    ArticlesFormSet = modelformset_factory(Article, form=EditArticlesForm, extra=0)
    formset = ArticlesFormSet(request.POST)

    if formset.is_valid():
      try:
        formset.save()
        request.method = 'GET' # before directing
        return edit_articles(request, lang_id)
      except IntegrityError:
        integrity_error = _('Each article must be unique. Please avoid duplicates.')
        # re-query the instances so the duplicate user input is replaced with the real value from the db
        articles = language.articles.all().exclude(name='')
        formset = ArticlesFormSet(queryset=articles)

    request.method = 'GET' # before directing to edit_language
    
  context = {
    'formset': formset,
    'articles_length': len(articles),
    'lang_id': lang_id,
    'lang_name': language.name,
    'integrity_error': integrity_error,
  }

  return render(request, 'entries/edit_articles.html', context)

@login_required
def add_articles(request, lang_id):
  assert request.method == 'POST'

  language = get_object_or_404(Language, pk=lang_id)
  articles_set = sanitize_string_input(request.POST.get('articles'))
  for article in articles_set:
    if not Article.objects.filter(
      user=request.user,
      language=language,
      name=article,
    ).exists() and len(article) <= 5:
      Article.objects.create(
        user=request.user,
        language=language,
        name=article,
      )

  request.method = 'GET'
  return edit_articles(request, lang_id)

@login_required
def delete_article(request):
  assert request.method == 'POST'

  article = get_object_or_404(
    Article,
    user=request.user,
    pk=request.POST.get('id'),
  )

  # entries using this article will be assigned with the zero article instead of setting Null value
  language = get_object_or_404(Language, pk=article.language.id)
  zero_article = Article.objects.filter(language=language).first()
  entries = Entry.objects.filter(user=request.user,article=article)
  for entry in entries:
    entry.article = zero_article
    entry.save()
  
  article.delete()

  return HttpResponse(status=204)

@login_required
def edit_topics(request, lang_id):

  topics = []
  language = get_object_or_404(Language, pk=lang_id)
  integrity_error = ''

  if request.method == 'GET':
    topics = Topic.objects.filter(user=request.user, language=language)
    TopicsFormSet = modelformset_factory(Topic, form=EditTopicForm, extra=0)
    formset = TopicsFormSet(queryset=topics)

  else:
    TopicsFormSet = modelformset_factory(Topic, form=EditTopicForm, extra=0)
    formset = TopicsFormSet(request.POST)

    if formset.is_valid():
      # formset.is_valid checks on the correct form inputs, then try checks the UniqueConstraint
      try:
        formset.save()
        request.method = 'GET' # before directing to edit_language
        return edit_topics(request, lang_id)
      except IntegrityError:
        integrity_error = _('Each topic must be unique. Please avoid duplicates.')
        # re-query the instances so the duplicate user input is replaced with the real value from the db
        topics = Topic.objects.filter(user=request.user, language=language)
        formset = TopicsFormSet(queryset=topics)

    request.method = 'GET' # before directing to edit_language
    
  context = {
    'formset': formset,
    'topics_length': len(topics),
    'lang_id': lang_id,
    'lang_name': language.name,
    'integrity_error': integrity_error,
  }

  return render(request, 'entries/edit_topics.html', context)

@login_required
def add_topics(request, lang_id):
  assert request.method == 'POST'

  language = get_object_or_404(Language, pk=lang_id)
  topics_set = sanitize_string_input(request.POST.get('topics'))
  for topic in topics_set:
    Topic.objects.create(
      user=request.user,
      language=language,
      name=topic,
    )

  request.method = 'GET'
  return edit_topics(request, lang_id)

@login_required
def delete_topic(request):
  assert request.method == 'POST'

  topic = get_object_or_404(
    Topic,
    user=request.user,
    pk=request.POST.get('id'),
  )
  topic.delete()

  return HttpResponse(status=204)

@login_required
def edit_entry(request, entry_id):
  entry = get_object_or_404(Entry, pk=entry_id, user=request.user)
  translations = []
  entry_integrity_error = ''
  
  if request.method == 'POST':
    # edit the entry itself
    try:
      entry_form = EntryForm(request.POST, instance=entry)
      if entry_form.is_valid():
        edited_entry = entry_form.save(commit=False)
        edited_entry.article = get_object_or_404(Article, pk=request.POST.get('article'), user=request.user)
        if request.POST.get('topic'):
          edited_entry.topic = get_object_or_404(Topic, pk=request.POST.get('topic'), user=request.user)
        else:
          edited_entry.topic = None
        edited_entry.save()

    except IntegrityError:
      entry_integrity_error = _("Such entry already exists.")
      entry = get_object_or_404(Entry, pk=entry_id, user=request.user) # refresh the instance to its actual state
      entry_form = EntryForm(instance=entry)

    # create the translations form for rendering
    translations = entry.translations.all()
    TranslationsFormSet = modelformset_factory(Translation, form=TranslationForm, extra=0)
    translations_formset = TranslationsFormSet(queryset=translations)
    translation_form = TranslationForm() # create it here, but evaluation is in its own view function

  else:
    entry_form = EntryForm(instance=entry)

    translations = entry.translations.all()
    TranslationsFormSet = modelformset_factory(Translation, form=TranslationForm, extra=0)
    translations_formset = TranslationsFormSet(queryset=translations)
    translation_form = TranslationForm() # create it here, but evaluation is in its own view function

  articles = entry.language.articles.all() # not [1:], include the zero article
  topics = entry.language.topics.all()

  context = {
    'entry': entry,
    'entry_form': entry_form, 
    'translations_formset': translations_formset,
    'translations_bool': bool(entry.translations.all()),
    'translation_form': translation_form,
    'articles': articles,
    'topics': topics,
    'entry_integrity_error': entry_integrity_error,
  }
  
  return render(request, 'entries/edit_entry.html', context)

@login_required
def add_entry(request):
  language = request.user.profile.current_language
  integrity_error_entry = ''
  integrity_error_message = ''

  if request.method == 'POST':
    entry_form = EntryForm(request.POST)
    translation_form = TranslationForm(request.POST)

    if entry_form.is_valid() and translation_form.is_valid():
      try:

        # add Entry instance
        new_entry = entry_form.save(commit=False)
        new_entry.user = request.user
        new_entry.language = request.user.profile.current_language

        if request.POST.get('article'):
          if language.articles.filter(pk=request.POST.get('article')):
            new_entry.article = get_object_or_404(language.articles, pk=request.POST.get('article'))
        else: 
          return HttpResponse(status=204) # anti cheat

        if request.POST.get('topic'):
          if language.topics.filter(pk=request.POST.get('topic')):
            new_entry.topic = get_object_or_404(language.topics, pk=request.POST.get('topic'))
        
        new_entry.save()
        
        # add translation instance
        new_translation = translation_form.save(commit=False)
        new_translation.language = request.user.profile.current_language
        new_translation.entry = new_entry
        new_translation.user = request.user
        new_translation.save()

        request.method = 'GET'
        if request.POST.get('go-to-edit'):
          return edit_translations(request, new_entry.id)
        return add_entry(request)

      except IntegrityError:
        integrity_error_entry = f"{new_entry.article.name} {new_entry.name}"
        integrity_error_message = _('already is in your dictionary.') 

  else:
    integrity_error_entry = ''
    integrity_error_message = ''
    entry_form = EntryForm()
    translation_form = TranslationForm()

  articles = language.articles.all() # not [1:], include the zero article
  topics = language.topics.all()

  context = {
    'entry_form': entry_form, 
    'translation_form': translation_form,
    'articles': articles,
    'topics': topics,
    'integrity_error_entry': integrity_error_entry,
    'integrity_error_message': integrity_error_message, 
  }

  return render(request, 'entries/add_entry.html', context)

@login_required
def delete_entry(request):
  assert request.method == 'POST'
  entry = get_object_or_404(Entry, user=request.user, pk=request.POST.get('id'))
  entry.delete()
  return HttpResponse(status=204)

@login_required
def edit_translations(request, entry_id):
  translations = []
  entry = get_object_or_404(Entry, pk=entry_id, user=request.user)
  translation_edit_integrity_error = ''
  
  if request.method == 'GET':
    translations = entry.translations.all()
    TranslationsFormSet = modelformset_factory(Translation, form=TranslationForm, extra=0)
    formset = TranslationsFormSet(queryset=translations)

  else:
    try:
      TranslationsFormSet = modelformset_factory(Translation, form=TranslationForm, extra=0)
      formset = TranslationsFormSet(request.POST)

      if formset.is_valid():
        formset.save()
        request.method = 'GET'
        return edit_translations(request, entry_id)

    except IntegrityError:
      translation_edit_integrity_error = _('Each translation must be unique. Please avoid duplicates.')
      translations = entry.translations.all()
      formset = TranslationsFormSet(queryset=translations)
      request.method = 'GET'

  context = {
    'entry': get_object_or_404(Entry, pk=entry_id, user=request.user),
    'entry_form': EntryForm(instance=entry),
    'articles': entry.language.articles.all(), # not [:1]
    'topics': entry.language.topics.all(),
    'translations_formset': formset,
    'translations_bool': bool(entry.translations.all()),
    'translation_form': TranslationForm(),
    'translation_edit_integrity_error': translation_edit_integrity_error,
  }

  return render(request, 'entries/edit_entry.html', context)

@login_required
def delete_translation(request):
  assert request.method == 'POST'
  translation = get_object_or_404(Translation, user=request.user, pk=request.POST.get('id'))
  translation.delete()
  return HttpResponse(status=204)

@login_required
def add_translation(request, entry_id):
  assert request.method == 'POST'
    
  entry = get_object_or_404(Entry, pk=entry_id, user=request.user)
  translation_integrity_error = ''
  form = TranslationForm(request.POST)
  try:
    if form.is_valid():
      new_translation = form.save(commit=False)
      new_translation.entry = entry
      new_translation.language = entry.language
      new_translation.user = request.user
      new_translation.save()
      request.method = 'GET'
      return edit_entry(request, entry_id)
      
  except IntegrityError:
    translation_integrity_error = _('This entry already has the same translation.')
    request.method = 'GET'

  translations = entry.translations.all()
  TranslationsFormSet = modelformset_factory(Translation, form=TranslationForm, extra=0)
  formset = TranslationsFormSet(queryset=translations)
  
  context = {
    'entry': get_object_or_404(Entry, pk=entry_id, user=request.user),
    'entry_form': EntryForm(instance=entry),
    'articles': entry.language.articles.all(), # not [:1]
    'topics': entry.language.topics.all(),
    'translations_formset': formset,
    'translations_bool': bool(entry.translations.all()),
    'translation_form': form,
    'translation_integrity_error': translation_integrity_error,
  }

  return render(request, 'entries/edit_entry.html', context)



