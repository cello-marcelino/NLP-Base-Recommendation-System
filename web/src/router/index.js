import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { 
    path: '/', 
    name: 'Home',
    component: () => import('../views/HomeView.vue') 
  },
  { 
    path: '/single', 
    name: 'Single',
    component: () => import('../views/SingleRecommendationView.vue') 
  },
  { 
    path: '/batch', 
    name: 'Batch',
    component: () => import('../views/BatchRecommendationView.vue') 
  },
  { 
    path: '/docs', 
    name: 'Docs',
    component: () => import('../views/ApiDocsView.vue') 
  },
  { 
    path: '/config', 
    name: 'Config',
    component: () => import('../views/ConfigurationView.vue') 
  },
  { 
    path: '/preprocessing', 
    name: 'Preprocessing',
    component: () => import('../views/PreprocessingView.vue') 
  },
  {
    path: '/dosen',
    name: 'DosenData',
    component: () => import('../views/DosenDataView.vue')
  },
  {
    path: '/install',
    name: 'InstallSetup',
    component: () => import('../views/InstallSetupView.vue')
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
