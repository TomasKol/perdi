# Perdi - Personal Dictionary

This is my cs50w final project - https://docs.cs50.net/web/2020/x/projects/final/final.html

Screencast: https://youtu.be/jF3HkdJwnwg

This django app is made for students of foreign languages, so they can keep their vocabularies in digital form and accessible online. A registered user can create whatever language(s) they want and then add new words - here named entries - one by one. Each entry can have multiple translations, one article and one topic associated with it. Entries and articles also can have custom commentaries/notes. The entries can be displayed in the 'dictionary section', queried by language, translation direction (foreign to home language or vice versa) and filtered by string input and topic. Of course, all content entered by the user can be subsequently edited or deleted.
The user can also choose in which language they want Perdi to display - English or Slovak, change their password or delete the account permanently.

The project is divided into two apps - accounts and entries.

Tech stack: python, django, javascript, jquery, html, bootstrap, sass. 

# Side note
In this repo there is sqlite database with a pre-created superuser for you to try (credentials: superuser/password1234), unlike the deployed version that uses Postgresql.

# Important
To run Perdi on your machine, you need to have GETTEXT installed on it.
https://stackoverflow.com/questions/27220052/django-i18n-make-sure-you-have-gnu-gettext-tools https://stackoverflow.com/questions/18985482/how-to-install-gnu-gettext-on-windows-7
