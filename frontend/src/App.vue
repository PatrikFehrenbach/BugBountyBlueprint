<template>
  <div id="app">
    <nav class="bg-blue-500 p-4 flex items-center">
      <img src="@/assets/bug.png" alt="Logo" class="mr-4 h-12 w-12">
      <h1 class="text-white text-xl font-bold mr-4">Bug Bounty Blueprint</h1>
      <router-link to="/" class="nav-item">Markdown Editor</router-link>
      <router-link to="/templates" class="nav-item">Template Manager</router-link>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style scoped>
.nav-item {
  margin: 0 10px;
  padding: 10px 20px;
  text-decoration: none;
  color: white;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.router-link-active {
  font-weight: bold;
  border-bottom: 3px solid white;
}

h1 {
  margin: 0;
}

img {
  vertical-align: middle;  /* Aligns the image with the text vertically */
}
</style>

