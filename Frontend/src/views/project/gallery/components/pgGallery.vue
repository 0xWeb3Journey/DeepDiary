<template>
  <div>
    <!-- <h3>未完成mcs 存储的照片有：{{ totalgallerysWithoutMcsCnt }}</h3>
    <h3>{{ msg }}</h3>
    <h3>{{ gallerysWithoutMcs }}</h3>
    <h3 v-for="item in gallerysWithoutMcs" :key="item.id">{{ item.id }}</h3>
    <el-button
      type="primary"
      icon="el-icon-edit"
      @click="checkMcs(259)"
    ></el-button> -->
    <Gallery
      ref="gallery"
      name="相片"
      disp-type="thumb"
      storage-type="oss"
      :items="gallerys"
    ></Gallery>
  </div>
</template>

<script>
  import $ from 'jquery'

  import Gallery from './gallery.vue'
  import {
    getGallery,
    getAlbum,
    getFaceAlbum,
    getFaceGallery,
    checkImgMcs,
  } from '@/api/gallery'
  export default {
    name: 'PgGallery',
    components: { Gallery },
    data: function () {
      return {
        ImgQueryForm: {
          page: 1,
          pageSize: 10,
          search: '',
          faceAlumId: 1,
          id: '',
          // faces__id__gte: 0,
          mcs__file_upload_id: '',
        },
        gallerys: [],
        galleryLoading: false,
        totalGalleryCnt: 0,
        curGalleryCnt: 0,
        checkedGalleryIndex: -1,
        checkedGalleryId: -1,

        gallerysWithoutMcs: [],
        totalgallerysWithoutMcsCnt: 0,
        processedMcsCnt: 0,
        msg: '',
      }
    },
    created() {
      this.fetchGallery()
      this.fetchGalleryWithoutMcs()
    },
    mounted() {
      const $window = $(window)
      $window.fetchGallery = this.fetchGallery // 把这个函数赋值给window，便于全局调用
      // 未铺满整个页面加载
      $window.scroll(function () {
        // console.log(
        //   'scrollTop is %d,document height is %d,window height is %d',
        //   $window.scrollTop(),
        //   $(document).height(),
        //   $window.height()
        // )
        if (
          $window.scrollTop() >=
          $(document).height() - $window.height() - 10
        ) {
          // console.log('infinite-scroll-gallery: start reload the data')
          $window.fetchGallery()
        }
      })
    },
    methods: {
      async fetchGalleryWithoutMcs() {
        this.ImgQueryForm.mcs__file_upload_id = 0
        const { data, totalCount } = await getGallery(this.ImgQueryForm)
        if (totalCount === 0) return //could fetch any data
        console.log('start to get the img without mcs...')
        console.log('the img without mcs is %o', data)
        this.gallerysWithoutMcs = data
        this.totalgallerysWithoutMcsCnt = totalCount
      },
      async fetchGallery() {
        this.ImgQueryForm.mcs__file_upload_id = ''
        console.log('start to get the img...')
        console.log(this.galleryLoading)
        if (this.galleryLoading) return //incase fetch more data during the fetching time

        this.galleryLoading = true
        if (
          this.curGalleryCnt < this.totalGalleryCnt ||
          this.totalGalleryCnt === 0
        ) {
          const { data, totalCount } = await getGallery(this.ImgQueryForm)
          if (totalCount === 0) return //could fetch any data
          this.ImgQueryForm.page += 1
          console.log(
            'get img api result, data is %o, total is %d',
            data,
            totalCount
          )
          this.gallerys = [...this.gallerys, ...data]
          this.curGalleryCnt = this.gallerys.length
          this.totalGalleryCnt = totalCount
          setTimeout(() => {
            this.galleryLoading = false
          }, 300)
        }
      },
    },
  }
</script>

<style></style>
