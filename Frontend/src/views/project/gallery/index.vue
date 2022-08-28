<template>
  <div class="gallery-container">
    <el-tabs type="border-card">
      <el-tab-pane label="照片"><PgGallery></PgGallery></el-tab-pane>
      <el-tab-pane label="相册"><PgAlbum></PgAlbum></el-tab-pane>
      <el-tab-pane label="人像"><PgFace></PgFace></el-tab-pane>
      <el-tab-pane label="地点"><PgAddress></PgAddress></el-tab-pane>
      <el-tab-pane label="事物"><PgObject></PgObject></el-tab-pane>
    </el-tabs>

    <vab-upload
      ref="vabUpload"
      url="/api/img/"
      name="src"
      :limit="50"
      :size="8"
    ></vab-upload>
  </div>
</template>

<script>
  import 'lightgallery/css/lightgallery-bundle.css' //CSS 打包引用

  import 'justifiedGallery/dist/js/jquery.justifiedGallery.min'
  import 'justifiedGallery/dist/css/justifiedGallery.css'

  import VabUpload from '@/components/VabUpload'
  import { clearScreenDown } from 'readline'
  import Album from './components/album.vue'
  import PgGallery from './components/pgGallery.vue'
  import PgFace from './components/pgFace.vue'
  import PgAlbum from './components/pgAlbum.vue'
  import PgAddress from './components/pgAddress.vue'
  import PgObject from './components/pgObject.vue'

  export default {
    name: 'Gallery',
    components: { VabUpload, PgGallery, PgFace, PgAlbum, PgAddress, PgObject },
    // data() {
    //   return {
    //     plugin: null,
    //     dispType: 'face', //could be face, thumb, map
    //     detailType: 'album', //could be album, face-img, etc.
    //     disp: true,

    //     elementLoadingText: '正在加载...',
    //     ImgQueryForm: {
    //       page: 1,
    //       pageSize: 10,
    //       search: '',
    //       faceAlumId: 1,
    //       faces__id__gte: 0,
    //     },
    //     gallerys: [],
    //     galleryLoading: false,
    //     totalGalleryCnt: 0,
    //     curGalleryCnt: 0,
    //     checkedGalleryIndex: -1,
    //     checkedGalleryId: -1,

    //     albums: [],
    //     albumLoading: false,
    //     totalAlbumCnt: 0,
    //     curAlbumCnt: 0,
    //     checkedIndex: -1,
    //     checkedId: -1,

    //     faces: [],
    //     faceLoading: false,
    //     totalFaceCnt: 0,
    //     curFaceCnt: 0,
    //     faceQueryForm: {
    //       page: 1,
    //       pageSize: 10,
    //       search: '',
    //       face_album__id: '',
    //       img__id: '',
    //     },
    //   }
    // },
    // computed: {
    //   faceName: function () {
    //     console.log(
    //       'compute the face name: the faces length is %d, checkedIndex is %d, %o',
    //       this.albums.length,
    //       this.checkedIndex,
    //       this.albums[this.checkedIndex]
    //     )
    //     // 获取选中的人脸
    //     if (this.albums[this.checkedIndex]) {
    //       return this.albums[this.checkedIndex].name
    //     } else return 'pls click a person to show ...'
    //   },
    // },
    // watch: {
    //   dispType(newVal, oldVal) {
    //     this.fetchFaceGallery()
    //   },
    //   checkedIndex(newVal, oldVal) {
    //     // this.faces = []
    //     this.fetchFaceGallery()
    //     // console.log(this.checkedIndex)
    //     // console.log(this.faces)
    //     // console.log(this.faces[this.checkedIndex])
    //   },

    //   checkedGalleryIndex(newVal, oldVal) {
    //     // this.faces = []
    //     this.fetchFaceGallery()
    //     // console.log(this.checkedIndex)
    //     // console.log(this.faces)
    //     // console.log(this.faces[this.checkedIndex])
    //   },

    //   // faces(newVal, oldVal) {
    //   //   this.$nextTick(() => {
    //   //     console.log('faces have been changed')
    //   //     window.face.refresh()
    //   //     $('#face').justifiedGallery()
    //   //   })
    //   // },
    //   albums(newVal, oldVal) {
    //     this.$nextTick(() => {
    //       console.log('albumChoose have been changed')
    //       // window.album.refresh()
    //       $('#album').justifiedGallery('norewind')
    //     })
    //   },
    //   gallerys(newVal, oldVal) {
    //     this.$nextTick(() => {
    //       console.log('gallerys have been changed')
    //       // window.gallery.refresh()
    //       $('#gallery').justifiedGallery('norewind')
    //     })
    //   },
    // },
    // created() {
    //   // this.fetchGallery()
    //   // this.fetchFaceGallery()
    //   // this.fetchFaceAlbum()
    // },
    // mounted() {
    //   // this.lgInit()
    //   // this.justifyInit()
    //   // const $window = $(window)
    //   // $window.fetchGallery = this.fetchGallery // 把这个函数赋值给window，便于全局调用
    //   // $window.fetchFaceAlbum = this.fetchFaceAlbum // 把这个函数赋值给window，便于全局调用
    //   // // 未铺满整个页面加载
    //   // $window.scroll(function () {
    //   //   // console.log(
    //   //   //   'scrollTop is %d,document height is %d,window height is %d',
    //   //   //   $window.scrollTop(),
    //   //   //   $(document).height(),
    //   //   //   $window.height()
    //   //   // )
    //   //   if (
    //   //     $window.scrollTop() >=
    //   //     $(document).height() - $window.height() - 10
    //   //   ) {
    //   //     // console.log('infinite-scroll-gallery: start reload the data')
    //   //     $window.fetchGallery()
    //   //   }
    //   // })
    // },
    // methods: {
    //   queryData() {
    //     this.ImgQueryForm.page = 1
    //     this.fetchGallery()
    //   },
    //   async fetchGallery() {
    //     console.log('start to get the img...')
    //     console.log(this.galleryLoading)
    //     if (this.galleryLoading) return //incase fetch more data during the fetching time

    //     this.galleryLoading = true
    //     if (
    //       this.curGalleryCnt < this.totalGalleryCnt ||
    //       this.totalGalleryCnt === 0
    //     ) {
    //       const { data, totalCount } = await getGallery(this.ImgQueryForm)
    //       if (totalCount === 0) return //could fetch any data
    //       this.ImgQueryForm.page += 1
    //       console.log(
    //         'get img api result, data is %o, total is %d',
    //         data,
    //         totalCount
    //       )
    //       this.gallerys = [...this.gallerys, ...data]
    //       this.albums = [...this.albums, ...data]
    //       this.curGalleryCnt = this.gallerys.length
    //       this.totalGalleryCnt = totalCount
    //       setTimeout(() => {
    //         this.galleryLoading = false
    //       }, 300)
    //     }
    //   },
    //   async fetchFaceGallery() {
    //     console.log('start to get the fetchFaceGallery...')
    //     // if (this.faceLoading) return //incase fetch more data during the fetching time
    //     // this.faceLoading = true
    //     // await getFaceGallery(this.faceQueryForm, 1)
    //     // if (this.curFaceCnt < this.totalFaceCnt || this.totalFaceCnt === 0) {

    //     // if (this.checkedIndex < 0) {
    //     //   return
    //     // }

    //     const { data } = await getFaceGallery(
    //       this.faceQueryForm
    //       // this.checkedId
    //     )
    //     // if (totalCount === 0) return //could fetch any data
    //     // // this.ImgQueryForm.page += 1
    //     // console.log(
    //     //   'get img api result, data is %o, total is %d',
    //     //   data,
    //     //   totalCount
    //     // )
    //     this.faces = [...data]
    //     console.log(this.faces)
    //     this.curFaceCnt = this.faces.length
    //     // this.totalFaceCnt = totalCount
    //     setTimeout(() => {
    //       this.albumLoading = false
    //     }, 300)
    //     // }
    //   },
    //   async fetchFaceAlbum() {
    //     console.log('start to get the album...')
    //     if (this.albumLoading) return //incase fetch more data during the fetching time

    //     this.albumLoading = true
    //     if (this.curAlbumCnt < this.totalAlbumCnt || this.totalAlbumCnt === 0) {
    //       const { data, totalCount } = await getFaceAlbum(this.ImgQueryForm)
    //       if (totalCount === 0) return //could fetch any data
    //       // this.ImgQueryForm.page += 1
    //       console.log(
    //         'get img api result, data is %o, total is %d',
    //         data,
    //         totalCount
    //       )
    //       this.albums = [...this.albums, ...data]
    //       this.curAlbumCnt = this.albums.length
    //       this.totalAlbumCnt = totalCount
    //       setTimeout(() => {
    //         this.albumLoading = false
    //       }, 300)
    //     }
    //   },
    //   updateSlides: function () {
    //     this.gallerys = [
    //       ...this.gallerys,
    //       {
    //         id: '4',
    //         size: '1400-933',
    //         src: 'https://images.unsplash.com/photo-1609902726285-00668009f004?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1400&q=80',
    //         thumb:
    //           'https://images.unsplash.com/photo-1609902726285-00668009f004?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=240&q=80',
    //         subHtml: `<div class="lightGallery-captions">
    //               <h4>Photo by <a href="https://unsplash.com/@bruno_adam">Bruno Adam</a></h4>
    //               <p>Published on January 6, 2021</p>
    //           </div>`,
    //       },
    //     ]
    //   },
    //   lgInit: function () {
    //     const lgFace = document.getElementById('face')
    //     const lgGallery = document.getElementById('gallery')
    //     window.face = lightGallery(lgFace, {
    //       addClass: 'gallery',
    //       autoplayFirstVideo: false,
    //       pager: false,
    //       galleryId: 'nature',
    //       plugins: [
    //         lgThumbnail,
    //         lgZoom,
    //         lgAutoplay,
    //         lgRotate,
    //         lgFullscreen,
    //         // lgMediumZoom,
    //       ],
    //       thumbnail: true,
    //       slideShowInterval: 2000,
    //       mobileSettings: {
    //         controls: false,
    //         showCloseIcon: false,
    //         download: false,
    //         rotate: false,
    //       },
    //     })
    //     // window.gallery = lightGallery(lgGallery, {
    //     //   addClass: 'gallery',
    //     //   autoplayFirstVideo: false,
    //     //   pager: false,
    //     //   galleryId: 'nature',
    //     //   plugins: [
    //     //     lgThumbnail,
    //     //     lgZoom,
    //     //     lgAutoplay,
    //     //     lgRotate,
    //     //     lgFullscreen,
    //     //     // lgMediumZoom,
    //     //   ],
    //     //   thumbnail: true,
    //     //   slideShowInterval: 2000,
    //     //   mobileSettings: {
    //     //     controls: false,
    //     //     showCloseIcon: false,
    //     //     download: false,
    //     //     rotate: false,
    //     //   },
    //     // })
    //   },
    //   justifyInit: function () {
    //     $('#gallery,#album,#face')
    //       .justifiedGallery({
    //         captions: true,
    //         randomize: false,
    //         lastRow: 'left',
    //         rowHeight: 120,
    //         margins: 5,
    //       })
    //       .on('jg.complete', function () {
    //         console.log('jg.complete event was trigged')
    //       })
    //   },
    //   handleShow(data) {
    //     this.$refs['vabUpload'].handleShow(data)
    //   },

    //   //单击事件，进入选中模式
    //   albumChoose(album, index, id) {
    //     console.log(album, index, id)
    //     // console.log(this.$refs.radiobox_img[index].checked)
    //     this.checkedIndex = index
    //     this.checkedId = id
    //     this.faceQueryForm.face_album__id = id
    //     this.faceQueryForm.img__id = ''
    //   },

    //   //单击事件，进入选中模式
    //   galleryChoose(gallery, index, id) {
    //     console.log(gallery, index, id)
    //     // // console.log(this.$refs.radiobox_img[index].checked)
    //     this.checkedGalleryIndex = index
    //     this.checkedGalleryId = id
    //     this.faceQueryForm.face_album__id = ''
    //     this.faceQueryForm.img__id = id
    //   },
    //   //双击事件，右抽屉弹出，进入编辑模式
    //   onEdit(index) {
    //     console.log('双击事件')
    //   },

    //   onChangeDispType(type) {
    //     this.dispType = type
    //     this.faces = []
    //   },
    //   onChangeDetailType(type) {
    //     this.detailType = type
    //     this.albums = []
    //     this.fetchGallery()
    //   },
    // },
  }
</script>

<style lang="css" scoped>
  .img-checked {
    border-radius: 60px;
    border-style: solid;
    border-width: 3px;
    border-color: #1515f1c3;
    box-shadow: -20px -20px 20px rgba(34, 34, 183, 0.5);

    opacity: 0.1;
  }
  .img-unchecked {
    opacity: 0.5;
  }
</style>
