<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppSidebar from './components/layout/AppSidebar.vue'
import AdminSidebar from './components/layout/AdminSidebar.vue'

const route = useRoute()

const isNoneLayout = computed(() => {
  return route.path === '/' || route.path === '/admin/login' || route.meta.layout === 'none'
})

const isAdminLayout = computed(() => {
  return route.path.startsWith('/admin') && route.path !== '/admin/login'
})
</script>

<template>
  <div class="app-shell" :class="{ 'has-sidebar': !isNoneLayout }">
    <!-- Admin Sidebar for Admin Portal -->
    <AdminSidebar v-if="isAdminLayout" />
    <!-- Public Sidebar for Public Portal -->
    <AppSidebar v-else-if="!isNoneLayout" />

    <div class="app-content" :class="{ 'full-width': isNoneLayout }">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<style>
.app-shell {
  display: flex;
  min-height: 100svh;
  background: var(--bg);
}
.app-shell.has-sidebar {
  padding-left: var(--sidebar-w);
}
.app-content {
  flex: 1;
  min-width: 0;
  width: 100%;
  background: var(--bg);
  box-sizing: border-box;
}
.app-content.full-width {
  width: 100%;
}
@media (max-width: 900px) {
  .app-shell.has-sidebar {
    padding-left: 0;
  }
}
</style>
