<template>
    <h1>Media Items (test ui)</h1>
    <h2>{{ items.length }} media items</h2>

    <table>
        <tbody>
            <tr>
                <th>Filename</th>
                <th>Length</th>
                <th>Size</th>
                <th>Created</th>
            </tr>
            <tr v-for="item in items">
                <td><RouterLink :to="`/media/${item.filename}`">{{ item.filename }}</RouterLink></td>
                <td>{{ item.media_length_ms / 1000 }}s</td>
                <td>{{ item.size }}</td>
                <td>{{ item.created }}</td>
            </tr>
        </tbody>
    </table>
</template>

<script setup lang="ts">
import MediaInfo from './MediaInfo.vue';
import { ref } from 'vue';

const items = ref([]);

fetch("/api/media/", { method: "GET" })
    .then((response) => response.json())
    .then((data) => {
        items.value = data;
    })
</script>
