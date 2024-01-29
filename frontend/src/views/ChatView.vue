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
      <div v-if="responseText" class="w-2/3 pl-3 results text-light-text dark:text-dark-text">
        {{ responseText }}
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { ref } from 'vue'

const inputText = ref('')
const responseText = ref('')
const inputFocused = ref(false)

function search() {
  fetch(`/api?q=${inputText.value}`)
    .then((response) => response.json())
    .then((data) => {
      responseText.value = data
    })
}
</script>
