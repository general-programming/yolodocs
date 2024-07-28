<template>
  <div id="subtitles">
    <li v-for="segment in parsedTranscript" @click="onClick(segment)" :class="segment.class">
      <span class="timestamp">[{{ segment.timestamp }}]</span> {{ segment.text }}
    </li>
  </div>
</template>

<script setup lang="ts">
import { ref, watchEffect } from 'vue'

import { parse } from '@plussub/srt-vtt-parser/dist'

const props = defineProps({
  media: { type: Object, required: true },
  currentTime: { type: Number, required: true }
})

const emit = defineEmits(['seek'])

const parsedTranscript = ref([])

watchEffect(() => {
  if (!props.media.transcript) return

  const newTranscript = []

  const parsed = parse(props.media.transcript)

  parsed.entries.forEach((segment) => {
    let classes = ''

    // handle 00:00
    if (segment.from == 0 && props.currentTime == 0) {
      classes = 'current'
    }

    if (segment.from <= props.currentTime && segment.to >= props.currentTime) {
      classes = 'current'
    }

    newTranscript.push({
      timestamp: new Date(segment.from).toISOString().substring(11, 22),
      start: segment.from,
      text: segment.text,
      class: classes
    })
  })

  parsedTranscript.value = newTranscript
})

function onClick(segment) {
  emit('seek', segment.start + 1)
}
</script>
