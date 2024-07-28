import { createRouter, createWebHistory } from 'vue-router'
import MediaListView from '../views/MediaListView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MediaListView
    },
    {
      path: '/medialist/:mediaListId',
      name: 'medialist_page',
      component: () => import('../views/MediaListView.vue')
    },
    {
      path: '/media/:mediaId',
      name: 'media',
      component: () => import('../views/MediaView.vue')
    }
  ]
})

export default router
