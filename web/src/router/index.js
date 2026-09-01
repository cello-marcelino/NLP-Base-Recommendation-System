import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // --- Public Portal Routes ---
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
    path: '/preprocessing', 
    name: 'Preprocessing',
    component: () => import('../views/PreprocessingView.vue') 
  },
  { 
    path: '/docs', 
    name: 'Docs',
    component: () => import('../views/ApiDocsView.vue') 
  },
  {
    path: '/install',
    name: 'InstallSetup',
    component: () => import('../views/InstallSetupView.vue')
  },

  // --- SiReDo Admin Portal Routes ---
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/admin/AdminLoginView.vue'),
    meta: { layout: 'none' }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('../views/admin/AdminDashboardView.vue'),
    meta: { requiresAdmin: true, layout: 'admin' }
  },
  {
    path: '/admin/dosen',
    name: 'AdminDosen',
    component: () => import('../views/admin/AdminDosenView.vue'),
    meta: { requiresAdmin: true, layout: 'admin' }
  },
  {
    path: '/admin/batch',
    name: 'AdminBatch',
    component: () => import('../views/admin/AdminBatchView.vue'),
    meta: { requiresAdmin: true, layout: 'admin' }
  },
  {
    path: '/admin/config',
    name: 'AdminConfig',
    component: () => import('../views/admin/AdminConfigView.vue'),
    meta: { requiresAdmin: true, layout: 'admin' }
  },

  // Redirect legacy routes to admin equivalents or home
  { path: '/batch', redirect: '/admin/batch' },
  { path: '/dosen', redirect: '/admin/dosen' },
  { path: '/config', redirect: '/admin/config' },
  { path: '/admin', redirect: '/admin/dashboard' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('siredo_admin_token')
  if (to.meta.requiresAdmin && !token) {
    next('/admin/login')
  } else if (to.path === '/admin/login' && token) {
    next('/admin/dashboard')
  } else {
    next()
  }
})

export default router
