<template>
  <div class="flex space-x-6 text-light-text dark:text-dark-text">
    <div class="p-2 text-2xl rounded-full bg-light-menu dark:bg-dark-menu h-min elem-shadow-sm">
      <Icon icon="ooui:logo-wikimedia" />
    </div>
    <div v-if="response && response.sources">
      <div v-for="s in response.sources" :key="s.id">
        <div v-if="s.score > 2" class="mb-2">
          <details
            class="pt-2 text-sm cursor-pointer text-light-distinct-text dark:text-dark-distinct-text"
          >
            <summary>
              {{ $t('source') }} ({{ s.score.toFixed(1) }}/5):
              <a class="link-text" :href="s.src">{{ s.src }}</a>
            </summary>
            <p class="pt-2 pl-4">{{ s.content }}</p>
          </details>
        </div>
      </div>
      <div v-if="response" class="text-lg">
        {{ response.answer }}
      </div>
    </div>
    <div v-else class="text-lg">
      {{ $t('no-response-message') }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue'
import type { ResponseObject } from '../../types/response-object.d.ts'

defineProps<{
  response?: ResponseObject
}>()
</script>
