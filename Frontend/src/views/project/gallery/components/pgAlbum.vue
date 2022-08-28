<template>
  <div>
    <!-- <el-alert title="消息提示的文案" type="info">
      <span v-for="album in albums" :key="album.id">{{ album.id }},</span>
    </el-alert>
    <el-button type="primary" @click="fetchAlbum()">get albums</el-button> -->
    <Album
      v-if="true"
      ref="album"
      title="相册"
      type="collection"
      route="Face_detail"
      :items="albums"
      @albumClick="onGetAlbumId"
    ></Album>
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
    name: 'PgAlbum',
    components: { Album },
    data: function () {
      return {
        checkedIndex: 0,
        checkedId: 0,
        albums: [],
        albumLoading: false,
        totalAlbumCnt: 0,
        queryForm: {
          page: 1,
          pageSize: 10,
          search: '',
        },
      }
    },
    created() {
      this.fetchAlbum()
    },
    mounted() {
      const $window = $(window)
      $window.fetchAlbum = this.fetchAlbum // 把这个函数赋值给window，便于全局调用
      // 未铺满整个页面加载
      $window.scroll(function () {
        if (
          $window.scrollTop() >=
          $(document).height() - $window.height() - 10
        ) {
          // console.log('infinite-scroll-gallery: start reload the data')
          $window.fetchAlbum()
        }
      })
    },
    methods: {
      onGetAlbumId(index, id) {
        console.log('recieved the child component value %d,%d', index, id)
        // 声明这个函数，便于子组件调用
        this.checkedIndex = index
        this.checkedId = id
      },
      async fetchAlbum() {
        console.log('start to get the album...')
        if (this.albumLoading) return //incase fetch more data during the fetching time

        this.albumLoading = true
        if (this.curAlbumCnt < this.totalAlbumCnt || this.totalAlbumCnt === 0) {
          const { data, totalCount } = await getAlbum(this.queryForm)
          if (totalCount === 0) return //could fetch any data
          this.queryForm.page += 1
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
        } else {
          this.msg = 'there is no more img any more'
        }
      },
    },
  }
</script>

<style></style>
