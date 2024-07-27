<script setup lang="ts">
import { useRoute } from 'vue-router';
import { ref, onMounted, onBeforeUnmount } from 'vue';

import 'video.js/dist/video-js.css'
import 'videojs-wavesurfer/dist/css/videojs.wavesurfer.css'

import videojs from 'video.js'
import WaveSurfer from 'wavesurfer.js';
import 'videojs-wavesurfer/dist/videojs.wavesurfer.js';

import MediaInfo from '../components/MediaInfo.vue';
import MediaSubtitles from '../components/MediaSubtitles.vue';

const route = useRoute();
const mediaId = route.params.mediaId;

const mediaInfo = ref({});
const currentTime = ref(0);
let player = null;

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
        progressColor: 'green',
        cursorColor: 'green',
        hideScrollbar: true,
    }
}
};

function setupPlayer() {
    console.log("setting up player");
    if (!player) {
        player = videojs('#player', options, () => {});
    }

    player.src({src: `/api/media/${mediaId}/download`, type: 'audio/wav'});

    player.on('waveReady', event => {
        console.log('waveform is ready!');
        player.textTracks()[0].addEventListener('cuechange', event => {
            currentTime.value = player.currentTime() * 1000;
        });
    });

    player.on('playbackFinish', event => {
        console.log('playback finished.');
    });

    // error handling
    player.on('error', (element, error) => {
        console.warn(error);
    });
}

function seekPlayer(seconds) {
    console.log("seeking to ", seconds / 1000)
    player.currentTime(seconds / 1000);
}

onMounted(() => {
    fetch(`/api/media/${mediaId}`, { method: "GET" })
    .then((response) => response.json())
    .then((data) => {
        mediaInfo.value = data;
        setupPlayer();
    });
});

onBeforeUnmount(() => {
    if (player) player.dispose();
})
</script>

<template>
    <div class="flex-split">
        <section>
            <h1>{{ $route.params.mediaId }}</h1>
            <h2>{{ mediaInfo.created }}</h2>
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