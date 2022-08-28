<template>
  <div>
    <!-- <el-alert title="父组件消息提示的文案" type="info">
      <span>
        curAlbumCnt: {{ curAlbumCnt }}, totalAlbumCnt: {{ totalAlbumCnt }}
      </span>
      <br />
      title
      <span v-for="album in albums" :key="album.id">{{ album.id }},</span>
    </el-alert>
    <el-button type="primary" @click="fetchFaceAlbum()">get albums</el-button> -->
    <Album
      v-if="true"
      ref="album"
      title="人脸相册"
      type="personal"
      :items="albums"
      @albumClick="onGetAlbumId"
    ></Album>
    <br />
    <!-- <span>下面是通过路由加载的内容</span>
    <router-view /> -->
  </div>
</template>

<script>
  import $ from 'jquery'
  import Album from './album.vue'
  import {
    getGallery,
    getAlbum,
    getFaceAlbum,
    getFaceGallery,
  } from '@/api/gallery'
  export default {
    name: 'PgFacePersonal',
    components: { Album },
    data: function () {
      return {
        faceAlbumQueryForm: {
          page: 1,
          pageSize: 10,
          search: '',
          faceAlumId: 1,
          faces__id__gte: 0,
        },

        albums: [],
        albumLoading: false,
        totalAlbumCnt: 0,
        curAlbumCnt: 0,
        checkedIndex: -1,
        checkedId: -1,
      }
    },
    created() {
      this.fetchFaceAlbum()
    },
    mounted() {
      // const $window = $(window)
      // $window.fetchFaceAlbum = this.fetchFaceAlbum // 把这个函数赋值给window，便于全局调用
      // // 未铺满整个页面加载
      // $window.scroll(function () {
      //   // console.log(
      //   //   'scrollTop is %d,document height is %d,window height is %d',
      //   //   $window.scrollTop(),
      //   //   $(document).height(),
      //   //   $window.height()
      //   // )
      //   if (
      //     $window.scrollTop() >=
      //     $(document).height() - $window.height() - 10
      //   ) {
      //     // console.log('infinite-scroll-gallery: start reload the data')
      //     $window.fetchFaceAlbum()
      //   }
      // })
    },
    methods: {
      onGetAlbumId(index, id) {
        console.log('recieved the child component value %d,%d', index, id)
        // 声明这个函数，便于子组件调用
        this.checkedIndex = index
        this.checkedId = id
      },
      async fetchFaceAlbum() {
        if (this.albumLoading) return //incase fetch more data during the fetching time

        this.albumLoading = true
        if (this.curAlbumCnt < this.totalAlbumCnt || this.totalAlbumCnt === 0) {
          console.log('start to get the album...')
          const { data, totalCount } = await getFaceAlbum(
            this.faceAlbumQueryForm
          )
          if (totalCount === 0) return //could fetch any data
          // this.faceAlbumQueryForm.page += 1
          console.log(
            'get img api result, data is %o, total is %d',
            data,
            totalCount
          )
          this.albums = [...this.albums, ...data]
          this.curAlbumCnt = this.albums.length
          this.totalAlbumCnt = totalCount
          setTimeout(() => {
            this.albumLoading = false
          }, 300)
        }
      },
    },
  }
</script>

<style></style>
