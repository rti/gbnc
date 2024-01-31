import './assets/tailwind.css'

import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import router from './router'

const i18n = createI18n({
  locale: window.navigator.language,
  fallbackLocale: 'de',
  messages: {
    en: {
      'chat-prompt': 'Message ChatGSWiki...',
      'check-linked-wiki-pages-notice':
        'Please check the linked source to make sure that the information provided is correct.',
      'no-response-message':
        'Sorry, but no valid response was returned for your question. Please try rephrasing it.',
      source: 'Source'
    },
    de: {
      'chat-prompt': 'Schreib ChatGSWiki...',
      'check-linked-wiki-pages-notice':
        'Bitte überprüfen Sie die verlinkten Quellen, um sicherzustellen, dass die bereitgestellten Informationen korrekt sind.',
      'no-response-message':
        'Leider wurde auf Ihre Frage keine gültige Antwort zurückgegeben. Bitte versuchen Sie es umzuformulieren.',
      source: 'Quelle'
    }
  }
})

const app = createApp(App)

app.use(i18n)
app.use(router)

app.mount('#app')
