<script setup lang="ts">
import { useRoute } from 'vue-router'
import { ref, onMounted, onBeforeUnmount, type Ref } from 'vue'

import 'video.js/dist/video-js.css'
import 'videojs-wavesurfer/dist/css/videojs.wavesurfer.css'

import videojs from 'video.js'
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import WaveSurfer from 'wavesurfer.js'
import 'videojs-wavesurfer/dist/videojs.wavesurfer.js'

import MediaSubtitles from '../components/MediaSubtitles.vue'

import { type MediaListResult } from '../types/mediatypes'
import type Player from 'video.js/dist/types/player'

const route = useRoute()
const mediaId = route.params.mediaId

const mediaInfo = ref<MediaListResult>({
  pages: 0,
  total: 0,
  items: []
})
const currentTime = ref(0)
let player: Player | undefined = undefined

// video player
const options = {
  controls: true,
  bigPlayButton: true,
  autoplay: false,
  fluid: true,
  loop: false,
  plugins: {
    // configure videojs-wavesurfer plugin
    wavesurfer: {
      backend: 'MediaElement',
      displayMilliseconds: true,
      debug: true,
      waveColor: '#1a1a1a',
      progressColor: 'white',
      cursorColor: 'white',
      hideScrollbar: true
    }
  }
}

function setupPlayer() {
  console.log('setting up player')
  if (!player) {
    player = videojs('#player', options, () => {})
  }

  player.src({ src: `/api/media/${mediaId}/download`, type: 'audio/wav' })

  player.on('waveReady', (event) => {
    console.log('waveform is ready!')
    player.textTracks()[0].addEventListener('cuechange', (event) => {
      currentTime.value = player.currentTime() * 1000
    })
  })

  player.on('playbackFinish', (event) => {
    console.log('playback finished.')
  })

  // error handling
  player.on('error', (element, error) => {
    console.warn(error)
  })
}

function seekPlayer(seconds: number) {
  console.log('seeking to ', seconds / 1000)
  if (player) player.currentTime(seconds / 1000)
}

onMounted(() => {
  fetch(`/api/media/${mediaId}`, { method: 'GET' })
    .then((response) => response.json())
    .then((data) => {
      mediaInfo.value = data
      setupPlayer()
    })
})

onBeforeUnmount(() => {
  if (player) player.dispose()
})
</script>

<template>
  <div class="flex-split">
    <section>
      <h1>{{ $route.params.mediaId }}</h1>
      <h2>{{ mediaInfo.created }}</h2>
      <h3><a :href="`/api/media/${mediaId}/download`">Download</a></h3>
      <audio id="player" class="video-js vjs-default-skin" :src="`/api/media/${mediaId}/download`">
        <track default kind="captions" :src="`/api/media/${mediaId}/transcript`" />
      </audio>
    </section>
    <section>
      <h1>Transcript</h1>
      <MediaSubtitles :media="mediaInfo" :currentTime="currentTime" @seek="seekPlayer" />
    </section>
  </div>
</template>
