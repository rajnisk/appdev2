<template>
  <div>
    <h1>Login</h1>
    <p v-if="error" class="err">{{ error }}</p>
    <form class="card" @submit.prevent="login">
      <label>
        Username
        <input v-model="form.username" type="text" required autocomplete="username" />
      </label>
      <label>
        Password
        <input v-model="form.password" type="password" required autocomplete="current-password" />
      </label>
      <button type="submit">Login</button>
    </form>
    <p class="muted">
      No account?
      <router-link to="/register">Register</router-link>
    </p>
  </div>
</template>

<script>
import axios from 'axios'

const API = 'http://127.0.0.1:5000'

export default {
  data() {
    return {
      form: { username: '', password: '' },
      error: '',
    }
  },
  methods: {
    async login() {
      this.error = ''
      try {
        const res = await axios.post(`${API}/login`, this.form)
        localStorage.setItem('token', res.data.token)
        localStorage.setItem('username', res.data.username || this.form.username)
        localStorage.setItem('role', res.data.role || 'employee')
        window.dispatchEvent(new Event('auth-changed'))
        const redirect = this.$route.query.redirect || '/'
        this.$router.push(redirect)
      } catch (e) {
        this.error = e.response?.data?.msg || 'Login failed'
      }
    },
  },
}
</script>

<style scoped>
h1 {
  margin-top: 0;
}
.card {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 320px;
  padding: 1rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.08);
}
label {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.85rem;
}
input {
  padding: 0.45rem 0.5rem;
  border: 1px solid #d4d4d8;
  border-radius: 6px;
}
button[type='submit'] {
  margin-top: 0.25rem;
  padding: 0.5rem 0.75rem;
  border: none;
  border-radius: 6px;
  background: #2563eb;
  color: #fff;
  cursor: pointer;
}
.err {
  color: #b91c1c;
}
.muted {
  color: #71717a;
  font-size: 0.9rem;
}
</style>
