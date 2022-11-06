<template>
  <div>
    <h1>这里是合影页的vue。。。</h1>
  </div>
</template>

<script>
  import $ from 'jquery'

  import Gallery from './gallery.vue'
  import Img from './img.vue'

  import { getImg, getFaceAlbum, getFaceGallery } from '@/api/gallery'
  export default {
    name: 'PgFaceGroup',
    components: {},
    data: function () {
      return {
        bannerHeight: '',
        ImgQueryForm: {
          page: 1,
          pageSize: 10,
          search: '',
          faceAlumId: 1,
          faces__id__gte: 0,
        },
        gallerys: [],
        galleryLoading: false,
        totalGalleryCnt: 0,
        curGalleryCnt: 0,
        checkedGalleryIndex: -1,
        checkedGalleryId: -1,
      }
    },
    created() {
      this.fetchGallery()
    },
    mounted() {},
    methods: {
      async fetchGallery() {
        console.log('start to get the img...')
        console.log(this.galleryLoading)
        if (this.galleryLoading) return //incase fetch more data during the fetching time

        this.galleryLoading = true
        if (
          this.curGalleryCnt < this.totalGalleryCnt ||
          this.totalGalleryCnt === 0
        ) {
          const { data, totalCount } = await getImg(this.ImgQueryForm)
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
