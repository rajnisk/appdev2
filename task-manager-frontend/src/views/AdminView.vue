<template>
  <div>
    <h1>Admin dashboard</h1>
    <p class="muted">Summary is cached for 60s — use “Clear cache” to force refresh.</p>

    <p v-if="error" class="err">{{ error }}</p>
    <p v-if="msg" class="ok">{{ msg }}</p>

    <p v-if="loading">Loading summary…</p>
    <div v-else-if="summary" class="card">
      <h2>Overview</h2>
      <ul class="stats">
        <li><strong>Total tasks</strong> {{ summary.total_tasks }}</li>
        <li><strong>Total users</strong> {{ summary.total_users }}</li>
        <li><strong>Employees</strong> {{ summary.employees }}</li>
        <li><strong>Admins</strong> {{ summary.admins }}</li>
      </ul>
      <h3>Tasks by status</h3>
      <ul>
        <li v-for="(n, s) in summary.tasks_by_status" :key="s">{{ s }}: {{ n }}</li>
      </ul>
    </div>

    <div class="actions">
      <button type="button" class="primary" :disabled="busy" @click="emailReport">
        Email me the report (CSV)
      </button>
      <button type="button" class="secondary" :disabled="busy" @click="clearCache">
        Clear server cache
      </button>
      <button type="button" class="ghost" :disabled="loading" @click="loadSummary">Refresh summary</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const API = 'http://127.0.0.1:5000'

export default {
  data() {
    return {
      summary: null,
      loading: false,
      busy: false,
      error: '',
      msg: '',
    }
  },
  mounted() {
    this.loadSummary()
  },
  methods: {
    authHeaders() {
      const token = localStorage.getItem('token')
      return token ? { Authorization: `Bearer ${token}` } : {}
    },
    async loadSummary() {
      this.loading = true
      this.error = ''
      this.msg = ''
      try {
        const res = await axios.get(`${API}/admin/summary`, { headers: this.authHeaders() })
        this.summary = res.data
      } catch (e) {
        this.error = e.response?.data?.msg || 'Could not load admin summary'
        this.summary = null
      } finally {
        this.loading = false
      }
    },
    async emailReport() {
      this.busy = true
      this.error = ''
      this.msg = ''
      try {
        const res = await axios.post(`${API}/admin/email-report`, {}, { headers: this.authHeaders() })
        this.msg = res.data.msg || 'Queued.'
      } catch (e) {
        this.error = e.response?.data?.msg || 'Could not queue report'
      } finally {
        this.busy = false
      }
    },
    async clearCache() {
      this.busy = true
      this.error = ''
      this.msg = ''
      try {
        const res = await axios.post(`${API}/admin/cache-clear`, {}, { headers: this.authHeaders() })
        this.msg = res.data.msg || 'Cache cleared.'
        await this.loadSummary()
      } catch (e) {
        this.error = e.response?.data?.msg || 'Could not clear cache'
      } finally {
        this.busy = false
      }
    },
  },
}
</script>

<style scoped>
h1 {
  margin-top: 0;
}
h2 {
  font-size: 1.1rem;
  margin: 0 0 0.5rem;
}
h3 {
  font-size: 0.95rem;
  margin: 1rem 0 0.35rem;
}
.card {
  background: #fff;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.08);
  margin-bottom: 1rem;
}
.stats {
  list-style: none;
  padding: 0;
  margin: 0;
}
.stats li {
  margin: 0.35rem 0;
}
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
button {
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font: inherit;
}
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.primary {
  background: #2563eb;
  color: #fff;
}
.secondary {
  background: #f59e0b;
  color: #1c1917;
}
.ghost {
  background: #e4e4e7;
  color: #18181b;
}
.err {
  color: #b91c1c;
}
.ok {
  color: #15803d;
}
.muted {
  color: #71717a;
  font-size: 0.9rem;
}
</style>
