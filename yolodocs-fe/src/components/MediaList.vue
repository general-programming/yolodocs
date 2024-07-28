<template>
  <h1>Media Items (test ui)</h1>
  <h2>{{ totalMedia }} media items</h2>

  <table>
    <tbody>
      <tr>
        <th>Filename</th>
        <th>Length</th>
        <th>Size</th>
        <th>Created</th>
      </tr>
      <tr v-for="item in items">
        <td>
          <RouterLink :to="`/media/${item.filename}`">{{ item.filename }}</RouterLink>
        </td>
        <td>{{ item.media_length_ms / 1000 }}s</td>
        <td>{{ item.size }}</td>
        <td>{{ item.created }}</td>
      </tr>
    </tbody>
  </table>
  <PageControls
    :page="page"
    :total="totalPages"
    @next="updatePage(page + 1)"
    @prev="updatePage(page - 1)"
    @jump="updatePage($event)"
  />
</template>

<script setup lang="ts">
import MediaInfo from './MediaInfo.vue'
import PageControls from './PageControls.vue'
import { ref, watchEffect } from 'vue'

import { useRoute } from 'vue-router'

const items = ref([])
const totalMedia = ref(0)

const page = ref(1)
const totalPages = ref(0)

const updatePage = (newPage: number) => {
  // update location

  window.history.pushState({}, '', `?page=${newPage}`)

  page.value = newPage
}

const loadItems = () => {
  fetch(`/api/media/?page=${page.value}`, { method: 'GET' })
    .then((response) => response.json())
    .then((data) => {
      items.value = data.media
      totalMedia.value = data.total
      totalPages.value = data.pages
    })
}

// get current page from route params
const route = useRoute()
if (route.query.page) {
  updatePage(parseInt(route.query.page as string))
}

watchEffect(() => {
  loadItems()
})
</script>
