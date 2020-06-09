import re

def sanitize_string_input(string_input):
  articles_list = string_input.strip(',').strip().split(',')
  articles_clean = []
  for article in articles_list:
    cleaned = re.sub(r'[.,:;<>{}()"$@&#*\[\]%§?!]', '', article)
    if cleaned.strip():     
      articles_clean.append(cleaned.strip())
  return set(articles_clean)

