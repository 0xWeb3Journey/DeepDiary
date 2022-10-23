<template>
  <div class="gallery-container">
    <!-- <el-alert title="子组件消息提示的文案" type="info">
      <h4>this is img vue</h4>
      imgLoading: {{ imgLoading }}; route.query.id:{{ $route.query.id }}
    </el-alert> -->
    <div class="img_wrap">
      <el-image :src="img.src" lazy class="imgDetai"></el-image>

      <Tags :items="img.tags"></Tags>
    </div>

    <Album
      v-if="true"
      ref="album"
      title="人脸"
      type="img"
      :items="img.faces"
      :total="img.faces.length"
      @albumClick="onGetAlbumId"
    ></Album>

    <Mcs
      v-if="checkedIndex >= 0"
      :id="checkedId"
      :mcs="img.mcs"
      mcstype="face"
      :title="`Mcs Info-${checkedId}`"
    ></Mcs>
  </div>
</template>

<script>
  import $ from 'jquery'

  import {
    getGallery,
    getAlbum,
    getFaceAlbum,
    getFaceGallery,
    getImg,
    changeFaceName,
  } from '@/api/gallery'

  import Album from './album.vue'
  import Mcs from './mcs.vue'
  import Tags from './tags.vue'
  export default {
    name: 'Img',
    components: { Album, Mcs, Tags },
    //进入守卫：通过路由规则，进入该组件时被调用
    beforeRouteEnter(to, from, next) {
      console.log('beforeRouteEnter....')
      next()
    },
    //离开守卫：通过路由规则，离开该组件时被调用
    beforeRouteLeave(to, from, next) {
      console.log('beforeRouteLeave....')
      next()
    },
    props: {
      id: {
        type: Number,
        default: 113,
        required: false,
      },
      name: {
        type: String,
        default: '照片详情', // model field name
        required: false,
      },
    },
    data() {
      return {
        img: {
          src: '',
          faces: [], //faces info, include name and src
          tags: "'test1', 'test2'",
        },
        checkedIndex: 0,
        checkedId: 0,
        ImgQueryForm: {
          id: 0,
        },
        imgLoading: false,
        // srcList: this.items, //初始化直接用props中的值
      }
    },
    // computed: {
    //   img_id: function () {
    //     console.log('img_id have bee updated:', this.$route.query.id)
    //     return this.$route.query.id
    //   },
    // },
    watch: {
      'img.tags'(newVal, oldVal) {
        // console.log('img.tags have bee changed: %s --> %s', oldVal, newVal)
      },
      deep: true, //为true，表示深度监听，这时候就能监测到a值变化
    },
    created() {
      console.log('img vue created')
    },
    mounted() {
      console.log('img vue mounted')
    },
    activated() {
      console.log('the img component is activated')
      this.fetchImg()
    },
    deactivated() {
      console.log('the img component is deactivated')
    },
    methods: {
      onGetAlbumId(index, id) {
        console.log('recieved the child component value %d,%d', index, id)
        // 声明这个函数，便于子组件调用
        this.checkedIndex = index
        this.checkedId = id
      },

      async fetchImg() {
        console.log('start to get the img...')
        if (this.imgLoading) return //incase fetch more data during the fetching time

        this.imgLoading = true
        this.ImgQueryForm.id = this.$route.query.id
        const { data } = await getImg(this.ImgQueryForm)
        console.log(data)
        this.img = data

        setTimeout(() => {
          this.imgLoading = false
        }, 300)
      },
    },
  }
</script>

<style lang="css" scoped>
  .img_wrap {
    width: 100%;
    height: 400px;
    border: 1px dashed #ccc;
    display: table-cell;
    vertical-align: middle;
    text-align: center;
  }
</style>
