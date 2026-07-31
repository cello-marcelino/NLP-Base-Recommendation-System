<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import ServerStatusBadge from './ServerStatusBadge.vue'

const route = useRoute()
const mobileOpen = ref(false)

const sections = [
  {
    label: 'Mulai',
    items: [
      { name: 'Beranda', path: '/', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
      { name: 'Pipeline NLP', path: '/preprocessing', icon: 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z' },
    ]
  },
  {
    label: 'API Reference',
    items: [
      { name: 'Dokumentasi API', path: '/docs', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z', badge: 'REST' },
    ]
  },
  {
    label: 'Data Master',
    items: [
      { name: 'Data Dosen', path: '/dosen', icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z' },
    ]
  },
  {
    label: 'Tools',
    items: [
      { name: 'Single Recommendation', path: '/single', icon: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z', badge: 'Live' },
      { name: 'Batch Recommendation', path: '/batch', icon: 'M4 6h16M4 10h16M4 14h16M4 18h16', badge: 'Live' },
    ]
  },
  {
    label: 'Sistem',
    items: [
      { name: 'Konfigurasi', path: '/config', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z' },
      { name: 'Instalasi & Setup', path: '/install', icon: 'M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' }
    ]
  },
]
</script>

<template>
  <!-- Mobile overlay -->
  <div v-if="mobileOpen" class="mobile-overlay" @click="mobileOpen = false" />

  <!-- Sidebar -->
  <aside class="sidebar" :class="{ 'mobile-open': mobileOpen }">
    <!-- Logo -->
    <div class="sidebar-logo">
      <router-link to="/" class="logo-link" @click="mobileOpen = false">
        <div class="logo-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <div>
          <div class="logo-name">SiReDo</div>
          <div class="logo-version">v3 · Docs</div>
        </div>
      </router-link>
    </div>

    <!-- Nav sections -->
    <nav class="sidebar-nav">
      <div v-for="section in sections" :key="section.label" class="nav-section">
        <div class="nav-section-label">{{ section.label }}</div>
        <router-link
          v-for="item in section.items"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: route.path === item.path }"
          @click="mobileOpen = false"
        >
          <svg class="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" :d="item.icon" />
          </svg>
          <span>{{ item.name }}</span>
          <span v-if="item.badge" class="nav-badge" :class="item.badge === 'Live' ? 'badge-live' : 'badge-rest'">{{ item.badge }}</span>
        </router-link>
      </div>
    </nav>

    <!-- Footer -->
    <div class="sidebar-footer">
      <ServerStatusBadge />
    </div>
  </aside>

  <!-- Mobile toggle button -->
  <button class="mobile-toggle" @click="mobileOpen = !mobileOpen">
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path v-if="!mobileOpen" stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
      <path v-else stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
    </svg>
  </button>
</template>

<style scoped>
.sidebar {
  position: fixed;
  left: 0; top: 0; bottom: 0;
  width: var(--sidebar-w);
  background: var(--bg-subtle);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  z-index: 100;
  transition: transform 0.25s ease;
}

/* Logo */
.sidebar-logo {
  padding: 1.25rem 1rem 1rem;
  border-bottom: 1px solid var(--border);
}
.logo-link {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  text-decoration: none;
}
.logo-icon {
  width: 34px; height: 34px;
  background: var(--brand);
  border-radius: var(--radius);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  color: white;
}
.logo-icon svg { width: 18px; height: 18px; }
.logo-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}
.logo-version {
  font-size: 0.68rem;
  color: var(--text-muted);
  font-family: var(--font-mono);
  margin-top: 1px;
}

/* Nav */
.sidebar-nav {
  flex: 1;
  padding: 1rem 0.65rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.nav-section-label {
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
  padding: 0 0.6rem;
  margin-bottom: 0.35rem;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.5rem 0.65rem;
  border-radius: var(--radius);
  font-size: 0.865rem;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  transition: background 0.15s, color 0.15s;
}
.nav-item:hover {
  background: var(--bg-muted);
  color: var(--text-primary);
}
.nav-item.active {
  background: var(--brand-light);
  color: var(--brand);
  font-weight: 600;
}
.nav-icon {
  width: 16px; height: 16px;
  flex-shrink: 0;
  opacity: 0.7;
}
.nav-item.active .nav-icon { opacity: 1; }
.nav-badge {
  margin-left: auto;
  font-size: 0.6rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 99px;
  font-family: var(--font-mono);
  letter-spacing: 0.04em;
}
.badge-live { background: #dcfce7; color: #16a34a; }
.badge-rest { background: var(--blue-bg); color: var(--blue); }

/* Footer */
.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid var(--border);
}

/* Mobile */
.mobile-toggle {
  display: none;
  position: fixed;
  bottom: 1.25rem; right: 1.25rem;
  z-index: 200;
  width: 44px; height: 44px;
  background: var(--brand);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(91,75,219,0.35);
  align-items: center; justify-content: center;
}
.mobile-toggle svg { width: 20px; height: 20px; }

.mobile-overlay {
  display: none;
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.35);
  z-index: 99;
}

@media (max-width: 900px) {
  .mobile-toggle { display: flex; }
  .mobile-overlay { display: block; }
  .sidebar {
    transform: translateX(-100%);
  }
  .sidebar.mobile-open {
    transform: translateX(0);
  }
}
</style>
