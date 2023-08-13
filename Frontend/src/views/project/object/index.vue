<template>
  <div>
    <h2>this is object model</h2>
    <AlbumContainer :items="items" :total="total" :title="title" />
  </div>
</template>

<script>
  import AlbumContainer from '@/components/Album/content.vue'
  export default {
    name: 'Object',
    components: { AlbumContainer }, //ImgSearch
    data: function () {
      return {}
    },
    created() {},
    mounted() {},
    methods: {},
  }
</script>

<style></style>
