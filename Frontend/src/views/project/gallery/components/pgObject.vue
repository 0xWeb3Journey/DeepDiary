<template>
  <div>
    <h1>这里是事物页的vue。。。</h1>
    <Mapview></Mapview>
  </div>
</template>

<script>
  import Mapview from '../../amap/MapContainer.vue'
  export default {
    name: 'PgObject',
    components: { Mapview },
  }
</script>

<style></style>
