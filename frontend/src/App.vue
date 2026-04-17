<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
@import "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap";

@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: #FFFFFF;
  color: #1D1D1F;
  -webkit-font-smoothing: antialiased;
}

#app {
  min-height: 100vh;
}
</style>