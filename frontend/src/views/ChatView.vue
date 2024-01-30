<template>
  <main class="h-screen bg-light-content dark:bg-dark-content">
    <div class="p-6 space-y-5">
      <h1 class="flex space-x-3 text-3xl text-light-text dark:text-dark-text font-display">
        <Icon icon="ooui:logo-wikimedia" />
        <p class="-mt-[0.1em]">ChatGSWiki</p>
      </h1>
      <div>
        <div
          class="relative flex w-2/3 text-xl rounded-md bg-light-menu dark:bg-dark-menu elem-shadow-sm"
        >
          <input
            v-model="inputText"
            type="text"
            class="w-full pl-3 bg-transparent rounded-md h-9 placeholder:text-light-distinct-text dark:placeholder:text-dark-distinct-text text-light-text dark:text-dark-text"
            placeholder="Message ChatGSWiki..."
            autocomplete="off"
            @keyup.enter="inputText.length > 0 ? search() : {}"
            @focus="inputFocused = true"
            @blur="inputFocused = false"
          />
          <Icon
            class="absolute -translate-y-1/2 right-2 top-1/2"
            :class="{
              'text-light-text dark:text-dark-text ': inputFocused && inputText.length === 0,
              'text-light-text dark:text-dark-text hover:text-light-distinct-text dark:hover:text-dark-distinct-text hover:cursor-pointer':
                inputFocused && inputText.length > 0,
              'text-light-distinct-text dark:text-dark-distinct-text': !inputFocused
            }"
            icon="fluent:send-24-filled"
            size="2em"
            @click="inputText.length > 0 ? search() : {}"
          />
        </div>
        <p class="pt-2 pl-3 text-sm text-light-distinct-text dark:text-dark-distinct-text">
          Please check the linked wiki page to make sure that the information provided is correct.
        </p>
      </div>
      <div v-if="response" class="w-2/3 pl-3 results text-light-text dark:text-dark-text">
        {{ response.answer }}
      </div>

      <div v-if="response && response.sources && response.sources.length > 0">
        <h2 class="text-xl font-bold mt-2">Sources</h2>
        <div
          v-if="response"
          v-for="src in response.sources"
          class="w-2/3 pl-3 results text-light-text dark:text-dark-text"
        >
          <div class="mb-8">
            {{ src.content }}
            <div class="text-xs text-right">
              Score {{ src.score.toFixed(1) }} |
              <a class="text-blue-800 underline" :href="src.src">{{ src.src }}</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { ref } from 'vue'

type Source = {
  src: string
  content: string
  score: number
}

interface AnswerObject {
  answer: string
  sources?: Source[]
}

const inputText = ref('')
const response = ref<AnswerObject | null>(null)
const inputFocused = ref(false)

// response.value = {
//   answer:
//     'Question: What should happen with confidential information?\nAnswer: Confidential information should not be used or disclosed except as necessary for performance under the agreement. (Document 1)\n\nExplanation: The answer provided in Document 1 directly addresses the question about using and disclosing confidential information. It states that any waiver of compliance with this provision must be in writing, and this Agreement shall be governed by and construed in accordance with the laws of the State of New York. These details do not answer the original question but provide additional context related to confidentiality.',
//   sources: [
//     {
//       src: 'https://example.com/document1',
//       content:
//         'Parties agree that Confidential Information shall not be used or disclosed except as necessary for performance hereunder.',
//       score: 4.975016137070867
//     },
//     {
//       src: 'https://example.com/document12',
//       content: 'Any waiver of compliance with any provision of this Agreement must be in writing.',
//       score: 2.1152231308302407
//     },
//     {
//       src: 'https://example.com/document19',
//       content:
//         'This Agreement shall be governed by and construed in accordance with the laws of the State of New York.',
//       score: 1.8400423245643809
//     }
//   ]
// }

function search() {
  fetch(`/api?q=${inputText.value}`)
    .then((response) => response.json())
    .then((data) => {
      response.value = data
    })
}
</script>
