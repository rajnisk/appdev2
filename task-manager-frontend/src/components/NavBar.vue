<template>
  <nav class="nav">
    <router-link class="brand" to="/">Task Manager</router-link>
    <span class="spacer" />
    <template v-if="isLoggedIn">
      <router-link v-if="isAdmin" to="/admin">Admin</router-link>
      <span class="hi">Hi, {{ username }}</span>
      <button type="button" class="linkish" @click="logout">Logout</button>
    </template>
    <template v-else>
      <router-link to="/login">Login</router-link>
      <router-link to="/register">Register</router-link>
    </template>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      token: localStorage.getItem('token'),
      username: localStorage.getItem('username') || '',
    }
  },
  computed: {
    isLoggedIn() {
      return !!this.token
    },
  },
  mounted() {
    window.addEventListener('auth-changed', this.syncAuth)
  },
  beforeUnmount() {
    window.removeEventListener('auth-changed', this.syncAuth)
  },
  methods: {
    syncAuth() {
      this.token = localStorage.getItem('token')
      this.username = localStorage.getItem('username') || ''
      this.role = localStorage.getItem('role') || ''
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('role')
      this.syncAuth()
      this.$router.push('/login')
    },
  },
}
</script>

<style scoped>
.nav {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 1.25rem;
  background: #18181b;
  color: #fafafa;
}
.nav a {
  color: #a5d8ff;
  text-decoration: none;
}
.nav a.router-link-active {
  text-decoration: underline;
}
.brand {
  font-weight: 700;
}
.spacer {
  flex: 1;
}
.hi {
  opacity: 0.9;
  font-size: 0.9rem;
}
.linkish {
  background: transparent;
  border: none;
  color: #fda4af;
  cursor: pointer;
  font: inherit;
  text-decoration: underline;
}
</style>
