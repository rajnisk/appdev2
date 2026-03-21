<template>
  <div>
    <h1>My tasks</h1>
    <p v-if="error" class="err">{{ error }}</p>

    <form class="card add" @submit.prevent="addTask">
      <h2>New task</h2>
      <label>
        Title
        <input v-model="newTask.title" type="text" required placeholder="What to do?" />
      </label>
      <label>
        Description
        <input v-model="newTask.description" type="text" placeholder="Optional" />
      </label>
      <label>
        Priority
        <select v-model="newTask.priority">
          <option>Low</option>
          <option>Medium</option>
          <option>High</option>
        </select>
      </label>
      <button type="submit">Add</button>
    </form>

    <p v-if="loading">Loading…</p>
    <p v-else-if="!tasks.length" class="muted">No tasks yet. Add one above.</p>

    <ul v-else class="list">
      <li v-for="t in tasks" :key="t.id" class="card task">
        <div class="row">
          <strong>{{ t.title }}</strong>
          <button type="button" class="danger" @click="remove(t.id)">Delete</button>
        </div>
        <p v-if="t.description" class="desc">{{ t.description }}</p>
        <div class="row meta">
          <label>
            Status
            <select v-model="t.status" @change="saveTask(t)">
              <option>Pending</option>
              <option>In Progress</option>
              <option>Completed</option>
            </select>
          </label>
          <label>
            Priority
            <select v-model="t.priority" @change="saveTask(t)">
              <option>Low</option>
              <option>Medium</option>
              <option>High</option>
            </select>
          </label>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

const API = 'http://127.0.0.1:5000'

export default {
  data() {
    return {
      tasks: [],
      loading: false,
      error: '',
      newTask: {
        title: '',
        description: '',
        priority: 'Medium',
      },
    }
  },
  mounted() {
    this.loadTasks()
  },
  methods: {
    authHeaders() {
      const token = localStorage.getItem('token')
      return token ? { Authorization: `Bearer ${token}` } : {}
    },
    async loadTasks() {
      this.loading = true
      this.error = ''
      try {
        const res = await axios.get(`${API}/tasks`, { headers: this.authHeaders() })
        this.tasks = res.data
      } catch (e) {
        this.error = e.response?.data?.msg || 'Could not load tasks'
      } finally {
        this.loading = false
      }
    },
    async addTask() {
      this.error = ''
      try {
        await axios.post(`${API}/tasks`, this.newTask, { headers: this.authHeaders() })
        this.newTask = { title: '', description: '', priority: 'Medium' }
        await this.loadTasks()
      } catch (e) {
        this.error = e.response?.data?.msg || 'Could not add task'
      }
    },
    async saveTask(t) {
      this.error = ''
      try {
        await axios.put(
          `${API}/tasks/${t.id}`,
          {
            title: t.title,
            description: t.description,
            status: t.status,
            priority: t.priority,
          },
          { headers: this.authHeaders() }
        )
      } catch (e) {
        this.error = e.response?.data?.msg || 'Could not update task'
        await this.loadTasks()
      }
    },
    async remove(id) {
      if (!confirm('Delete this task?')) return
      this.error = ''
      try {
        await axios.delete(`${API}/tasks/${id}`, { headers: this.authHeaders() })
        await this.loadTasks()
      } catch (e) {
        this.error = e.response?.data?.msg || 'Could not delete'
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
  margin: 0 0 0.5rem;
  font-size: 1rem;
}
.card {
  background: #fff;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.08);
}
.add {
  margin-bottom: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
label {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.8rem;
}
input,
select {
  padding: 0.4rem 0.5rem;
  border: 1px solid #d4d4d8;
  border-radius: 6px;
}
button[type='submit'] {
  align-self: flex-start;
  padding: 0.45rem 0.85rem;
  border: none;
  border-radius: 6px;
  background: #2563eb;
  color: #fff;
  cursor: pointer;
}
.list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.task .row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}
.meta {
  margin-top: 0.5rem;
  flex-wrap: wrap;
}
.meta label {
  flex: 1;
  min-width: 140px;
}
.desc {
  margin: 0.35rem 0 0;
  color: #52525b;
  font-size: 0.9rem;
}
.danger {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
  border-radius: 6px;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  font-size: 0.8rem;
}
.err {
  color: #b91c1c;
}
.muted {
  color: #71717a;
}
</style>
