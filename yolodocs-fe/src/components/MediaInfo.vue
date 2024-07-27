<template>
    <ul>
        <li>{{ media.created }}</li>
        <li>{{ media.size }} bytes</li>
        <li>{{ media.media_length }} seconds</li>
    </ul>
</template>

<script setup lang="ts">
defineProps({
    media: { type: Object, required: true }
})
</script>