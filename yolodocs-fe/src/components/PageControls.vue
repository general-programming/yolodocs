<!-- Called with <PageControls :page="page" :total="totalMedia" @next="page++" @prev="page--" @jump="page = $event" /> -->
<script setup lang="ts">
defineProps({
  page: { type: Number, required: true },
  total: { type: Number, required: true }
})
</script>

<template>
  <div class="page-controls">
    <span>Page {{ page }} of {{ total }}</span>
    <button @click="$emit('jump', 1)" v-if="page > 1">First</button>
    <button v-if="page > 1" @click="$emit('prev')">Prev</button>
    <button v-if="page < total" @click="$emit('next')">Next</button>
    <button @click="$emit('jump', total)" v-if="page < total">Last</button>
  </div>
</template>
