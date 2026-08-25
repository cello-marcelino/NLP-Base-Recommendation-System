<script setup>
import AppSidebar from './components/layout/AppSidebar.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const noSidebar = ['/']
</script>

<template>
  <div class="app-shell" :class="{ 'has-sidebar': !noSidebar.includes(route.path) }">
    <AppSidebar v-if="!noSidebar.includes(route.path)" />
    <div class="app-content" :class="{ 'full-width': noSidebar.includes(route.path) }">
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
  background: var(--bg);
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
