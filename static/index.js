// global vars
const LANGUAGE = document.getElementsByTagName('html')[0].lang;
const TRANSLATIONS = {
  en: {
    sure_to_delete: 'Are you sure to delete the',
    rela_arts_tops_ents_trans : 'and all its related articles, topics, entries and translations',
    rela_trans: 'and all its related translations',
    undone: 'This cannot be undone.',
    article: 'article',
    topic: 'topic',
    language: 'language',
    entry: 'entry',
    translation: 'translation',
    no_article: '(no article)'
  },
  sk: {
    sure_to_delete: 'Určite chceš vymazať',
    rela_arts_tops_ents_trans : 'a všetky súvisiace členy, témy, slovíčka a preklady',
    rela_trans: 'a všetky súvisiace preklady',
    undone: 'Vymazanie sa nedá vrátiť späť.',
    article: 'člen',
    topic: 'tému', // akuzatív
    language: 'jazyk',
    entry: 'slovíčko',
    translation: 'preklad',
    no_article: '(bez člena)'
  }
}

// delete buttons
const deleteButtons = document.querySelectorAll('.delete');
for (let i = 0; i < deleteButtons.length; i++) {
  const btn = deleteButtons[i];
  btn.addEventListener('click', () => {

    let specificString = ''
    switch(btn.getAttribute('data-model')) {
      case 'language':
        specificString = TRANSLATIONS[LANGUAGE].rela_arts_tops_ents_trans;
        break;
      case 'entry':
        specificString = TRANSLATIONS[LANGUAGE].rela_trans;
        break;
    }

    if (!confirm(`${TRANSLATIONS[LANGUAGE].sure_to_delete} ${TRANSLATIONS[LANGUAGE][btn.getAttribute('data-model')]} "${btn.getAttribute('data-name')}" ${specificString}? ${TRANSLATIONS[LANGUAGE].undone}`)) {
      return;
    }

    const data = `id=${btn.getAttribute('data-id')}&${$('#get-token').serialize()}`

    $.ajax({
      url: btn.getAttribute('data-url'),
      method: 'POST',
      data: data,
      success: success
    });

    function success(response) {
      window.location.replace(btn.getAttribute('data-redirect'));
    }
  });
}

// search-string
const searchInput = document.querySelector('#search-string');
if (searchInput) {
  
  // pre-fill with the old search string
  searchInput.value = localStorage.getItem('search_input');
  
  // sanitize all data-name from diacritics for filtering purposes
  const containers = document.querySelectorAll('[data-name]');
  for (let i = 0; i < containers.length; i++) {
    containers[i].setAttribute('data-name', cleanString(containers[i].getAttribute('data-name')));
  }

  // perform the search filter in case of page load
    performQueryFilter();
  
  // listener
  searchInput.addEventListener('input', () => {
    localStorage.setItem('search_input', searchInput.value);
    performQueryFilter();
  });

}

// search-topic
const searchTopic = document.querySelector('#search-topic');
if (searchTopic) {
  
  // pre fill with the last searched for topic
  if (localStorage.getItem('search_topic') && document.querySelector(`.search-topic-option[value="${localStorage.getItem('search_topic')}"]`)) {
    document.querySelector(`.search-topic-option[value="${localStorage.getItem('search_topic')}"]`).selected = 'selected';
  }
  
  // listener
  searchTopic.addEventListener('change', () => {
    localStorage.setItem('search_topic', searchTopic.value);
    performQueryFilter();
  });
}

// filter the entries by search-string and search-topic
function performQueryFilter() {
  let string = '';
  if (localStorage.getItem('search_input')) {
    string = cleanString(localStorage.getItem('search_input'));
  }
  
  let topic = '';
  if (localStorage.getItem('search_topic')) {
    topic = cleanString(localStorage.getItem('search_topic'));
  }

  // filter the queryset
  if (!string && !topic) {
    $(`.entry-container`).show();
  }
  else if (string && !topic) {
    $(`.entry-container`).hide();
    $(`.entry-container[data-name^=${string}]`).show();
  }
  else if (!string && topic) {
    $(`.entry-container`).hide();
    $(`.entry-container[data-topic="${topic}"]`).show();
  }
  else {
    $(`.entry-container`).hide();
    $(`.entry-container[data-name^=${string}][data-topic="${topic}"]`).show();
  }

}

// placeholder for zero article in select tag (add_entry.html)
const articleSelectOption = document.querySelectorAll('.article-option');
if (articleSelectOption) {
  for (let i = 0; i < articleSelectOption.length; i++) {
    const opt = articleSelectOption[i];
    if (opt.innerHTML == '') {
      opt.innerHTML = TRANSLATIONS[LANGUAGE].no_article;
    }
  }
}

// toggle basic/detail div in dictionary part
const togglers = document.querySelectorAll('.toggler');
for (let i = 0; i < togglers.length; i++) {
  const tglr = togglers[i];
  tglr.addEventListener('click', () => {
    $(`.toggled.entry-basic[data-id!=${tglr.getAttribute('data-id')}]`).slideDown();
    $(`.toggled.entry-detail[data-id!=${tglr.getAttribute('data-id')}]`).slideUp();
    $(`.toggled[data-id=${tglr.getAttribute('data-id')}]`).slideToggle();
  });
}

function cleanString(string) {	
  return string
    .replace(/[AÀÁÂÃÄÅàáâãäå]/g,"a")
    .replace(/[Ææ]/g,"ae")
    .replace(/[B]/g,"b")
    .replace(/[CÇĆĈĊČçćĉċč]/g,"c")
    .replace(/[DÐĎðď]/g,"d")
    .replace(/[EÈÉÊËĚĒĖĘèéêëěēėę]/g,"e")
    .replace(/[F]/g,"f")
    .replace(/[GĜĞĠĢĝğġģ]/g,"g")
    .replace(/[HĤĦĥħ]/g,"h")
    .replace(/[IÌÍÎÏĨĪĬĮİìíîïĩīĭįi̇]/g,"i")
    .replace(/[JĴĵ]/g,"j")
    .replace(/[KĶķ]/g,"k")
    .replace(/[LĹĻĽĿŁĺļľŀł]/g,"l")
    .replace(/[M]/g,"m")
    .replace(/[NÑŇŃŅñňńņ]/g,"n")
    .replace(/[OÒÓÔÕÖŐØŌŎòóôõöőøōŏ]/g,"o")
    .replace(/[P]/g,"p")
    .replace(/[Q]/g,"q")
    .replace(/[RŔŖŘŕŗř]/g,"r")
    .replace(/[SŚŜŞŠśŝşš]/g,"s")
    .replace(/[TŢŤŦţťŧ]/g,"t")
    .replace(/[Œœ]/g,"oe")
    .replace(/[UÙÚÛÜŰŨŪŬŮŲùúûüűũūŭůų]/g,"u")
    .replace(/[V]/g,"v")
    .replace(/[WŴŵ]/g,"w")
    .replace(/[YÝŶŸýŷÿ]/g,"y")
    .replace(/[ZŹŻŽźżž]/g,"z")
}

// change display language by selecting an option (no submit button)
const langChanger = document.querySelector('#perdi-language-select');
if (langChanger) {
  langChanger.addEventListener('change', () => {
    $('#perdi-language-form').submit();
  });
}
