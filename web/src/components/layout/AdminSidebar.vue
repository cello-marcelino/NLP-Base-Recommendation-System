<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAdminAuthStore } from '../../stores/adminAuth'
import ServerStatusBadge from './ServerStatusBadge.vue'

const route = useRoute()
const router = useRouter()
const adminAuth = useAdminAuthStore()
const mobileOpen = ref(false)

const sections = [
  {
    label: 'Pengelolaan',
    items: [
      { name: 'Dashboard', path: '/admin/dashboard', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
      { name: 'Data Dosen & Riwayat', path: '/admin/dosen', icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z' },
    ]
  },
  {
    label: 'Engine & Tools',
    items: [
      { name: 'Konfigurasi Engine NLP', path: '/admin/config', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z' },
      { name: 'Batch Simulation', path: '/admin/batch', icon: 'M4 6h16M4 10h16M4 14h16M4 18h16', badge: 'Admin' },
    ]
  }
]

const handleLogout = () => {
  adminAuth.logout()
  router.push('/admin/login')
}
</script>

<template>
  <div v-if="mobileOpen" class="mobile-overlay" @click="mobileOpen = false" />

  <aside class="admin-sidebar" :class="{ 'mobile-open': mobileOpen }">
    <!-- Logo Header -->
    <div class="sidebar-logo">
      <router-link to="/admin/dashboard" class="logo-link" @click="mobileOpen = false">
        <div class="logo-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <div>
          <div class="logo-name">SiReDo Admin</div>
          <div class="logo-version">Data & Engine Management</div>
        </div>
      </router-link>
    </div>

    <!-- Admin User Badge -->
    <div class="admin-user-card" v-if="adminAuth.admin">
      <div class="user-avatar">{{ adminAuth.admin.name ? adminAuth.admin.name.charAt(0) : 'A' }}</div>
      <div class="user-info">
        <span class="user-name">{{ adminAuth.admin.name || adminAuth.admin.username }}</span>
        <span class="user-role">Administrator</span>
      </div>
    </div>

    <!-- Nav Sections -->
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
          <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
        </router-link>
      </div>

      <div class="nav-section">
        <div class="nav-section-label">Akses Portal</div>
        <router-link to="/" class="nav-item portal-link">
          <svg class="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
          <span>Ke Portal Publik</span>
        </router-link>
      </div>
    </nav>

    <!-- Footer Logout & Server Status -->
    <div class="sidebar-footer">
      <button type="button" @click="handleLogout" class="btn-logout">
        <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
        <span>Keluar (Logout)</span>
      </button>
      <ServerStatusBadge style="margin-top: 0.75rem;" />
    </div>
  </aside>

  <!-- Mobile Toggle -->
  <button class="mobile-toggle" @click="mobileOpen = !mobileOpen">
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path v-if="!mobileOpen" stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
      <path v-else stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
    </svg>
  </button>
</template>

<style scoped>
.admin-sidebar {
  position: fixed;
  left: 0; top: 0; bottom: 0;
  width: var(--sidebar-w, 260px);
  background: #064e3b; /* Deep Teal */
  color: #ecfdf5;
  border-right: 1px solid #047857;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  z-index: 100;
  transition: transform 0.25s ease;
}

.sidebar-logo {
  padding: 1.25rem 1rem 1rem;
  border-bottom: 1px solid #047857;
}
.logo-link {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  text-decoration: none;
}
.logo-icon {
  width: 36px; height: 36px;
  background: #0d9488; /* Teal 600 */
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  color: white;
}
.logo-icon svg { width: 20px; height: 20px; }
.logo-name {
  font-size: 0.98rem;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: -0.02em;
}
.logo-version {
  font-size: 0.68rem;
  color: #6ee7b7;
  font-family: var(--font-mono, monospace);
  margin-top: 1px;
}

.admin-user-card {
  margin: 0.85rem 0.85rem 0;
  padding: 0.6rem 0.75rem;
  background: #022c22;
  border: 1px solid #065f46;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.65rem;
}
.user-avatar {
  width: 30px; height: 30px;
  border-radius: 50%;
  background: #0d9488;
  color: white;
  font-weight: 700;
  font-size: 0.85rem;
  display: flex; align-items: center; justify-content: center;
}
.user-info { display: flex; flex-direction: column; }
.user-name { font-size: 0.8rem; font-weight: 600; color: #f0fdf4; }
.user-role { font-size: 0.65rem; color: #a7f3d0; font-family: var(--font-mono, monospace); }

.sidebar-nav {
  flex: 1;
  padding: 1rem 0.65rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}
.nav-section-label {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #6ee7b7;
  padding: 0 0.6rem;
  margin-bottom: 0.35rem;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.55rem 0.65rem;
  border-radius: 6px;
  font-size: 0.865rem;
  font-weight: 500;
  color: #d1fae5;
  text-decoration: none;
  transition: background 0.15s, color 0.15s;
}
.nav-item:hover {
  background: #047857;
  color: #ffffff;
}
.nav-item.active {
  background: #0d9488;
  color: #ffffff;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(0,0,0,0.15);
}
.nav-icon { width: 16px; height: 16px; flex-shrink: 0; opacity: 0.85; }
.nav-item.active .nav-icon { opacity: 1; }
.nav-badge {
  margin-left: auto;
  font-size: 0.6rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 99px;
  background: #ccfbf1; color: #0f766e;
}
.portal-link { color: #a7f3d0; border: 1px dashed #059669; margin-top: 0.2rem; }
.portal-link:hover { background: #059669; color: white; }

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid #047857;
}
.btn-logout {
  width: 100%;
  display: flex; align-items: center; justify-content: center; gap: 0.5rem;
  background: rgba(239, 68, 68, 0.15);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 6px;
  padding: 0.5rem;
  font-size: 0.8rem; font-weight: 600;
  cursor: pointer; transition: all 0.15s;
}
.btn-logout:hover {
  background: #dc2626; color: white; border-color: #dc2626;
}

.mobile-toggle {
  display: none;
  position: fixed; bottom: 1.25rem; right: 1.25rem; z-index: 200;
  width: 44px; height: 44px; background: #0d9488; color: white;
  border: none; border-radius: 50%; cursor: pointer;
  box-shadow: 0 4px 16px rgba(13, 148, 136, 0.4);
  align-items: center; justify-content: center;
}
.mobile-toggle svg { width: 20px; height: 20px; }
.mobile-overlay {
  display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 99;
}

@media (max-width: 900px) {
  .mobile-toggle { display: flex; }
  .mobile-overlay { display: block; }
  .admin-sidebar { transform: translateX(-100%); }
  .admin-sidebar.mobile-open { transform: translateX(0); }
}
</style>
