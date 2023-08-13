<template>
  <div class="gallery-container">
    <!-- <el-alert title="子组件消息提示的文案" type="info">
      <br />
      <span>this is carosel vue</span>
    </el-alert> -->

    <el-carousel
      :interval="2000"
      indicator-position="none"
      arrow="always"
      height="300px"
      type="card"
      @change="carouselChange"
    >
      <el-carousel-item v-for="item in items" :key="item.id">
        <el-row :gutter="12">
          <el-col
            style="height: 400px; margin-bottom: 20px display: flex; align-items: center; justify-content: center"
          >
            <img
              ref="banner"
              :src="item.thumb"
              alt=""
              style="max-width: 100%; max-height: 100%; object-fit: contain"
            />
          </el-col>
        </el-row>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
  export default {
    name: 'Carosel',
    components: {},
    props: {
      items: {
        type: Array,
        default: () => [],
        required: true,
      },
      title: {
        type: String,
        default: 'deep-diary', // model field name
        required: false,
      },
    },
    data() {
      return {
        bannerHeight: '',
      }
    },
    watch: {
      items(newVal, oldVal) {
        console.log('Carosel: watch items changed', newVal)
      },
    },
    created() {
      // this.fetchAlbum()
    },
    mounted() {},
    methods: {
      carouselChange: function (key1, key2) {
        // const id = this.gallerys[key1].id
        // console.log(key1, key2)
      },
    },
  }
</script>

<style lang="css" scoped></style>
