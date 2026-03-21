<template>
  <div>
    <h1>Register</h1>
    <p v-if="error" class="err">{{ error }}</p>
    <form class="card" @submit.prevent="register">
      <label>
        Username
        <input v-model="form.username" type="text" required autocomplete="username" />
      </label>
      <label>
        Password
        <input v-model="form.password" type="password" required autocomplete="new-password" />
      </label>
      <label>
        Email (optional — for daily reminders)
        <input v-model="form.email" type="email" autocomplete="email" />
      </label>
      <button type="submit">Create account</button>
    </form>
    <p class="muted">
      Already have an account?
      <router-link to="/login">Login</router-link>
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
    async register() {
      this.error = ''
      try {
        const payload = {
          username: this.form.username,
          password: this.form.password,
          email: (this.form.email || '').trim() || undefined,
        }
        await axios.post(`${API}/register`, payload)
        this.form.password = ''
        this.$router.push('/login')
      } catch (e) {
        this.error = e.response?.data?.msg || 'Registration failed'
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
  background: #16a34a;
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
