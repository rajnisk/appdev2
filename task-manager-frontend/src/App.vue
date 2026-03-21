<template>
  <div id="layout">
    <NavBar />
    <main class="main">
      <RouterView />
    </main>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
  components: { NavBar },
}
</script>

<style>
* {
  box-sizing: border-box;
}
body {
  margin: 0;
  font-family: system-ui, sans-serif;
  background: #f4f4f5;
}
.main {
  max-width: 640px;
  margin: 0 auto;
  padding: 1rem 1.25rem 2rem;
}
</style>
