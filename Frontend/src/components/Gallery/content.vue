<template>
  <div class="gallery-container">
    <!-- 照片墙展示 -->
    <div
      id="gallery_container"
      ref="gallery_container"
      v-infinite-scroll="load"
      infinite-scroll-disabled="busy"
      infinite-scroll-distance="50"
      infinite-scroll-immediate-check="true"
      :force-use-infinite-wrapper="true"
      class="gallery_container"
    >
      <div
        id="gallery"
        ref="gallery"
        v-infinite-scroll="load"
        class="infinite-list"
        style="overflow: auto"
      >
        <a
          v-for="item in items"
          :key="item.id"
          class="gallery infinite-list-item"
          className="gallery-item"
          :data-src="item.img"
          :data-sub-html="item.desc"
        >
          <img className="img-responsive" :src="item.thumb" />
        </a>
      </div>
      <div v-show="busy" class="loading">
        <h2>{{ msg }}</h2>
      </div>
    </div>
  </div>
</template>

<script>
  import $ from 'jquery'

  import lightGallery from 'lightgallery'
  // Plugins
  import lgThumbnail from 'lightgallery/plugins/thumbnail'
  import lgZoom from 'lightgallery/plugins/zoom'
  import lgAutoplay from 'lightgallery/plugins/autoplay'
  import lgRotate from 'lightgallery/plugins/rotate'
  import lgFullscreen from 'lightgallery/plugins/fullscreen'
  import lgMediumZoom from 'lightgallery/plugins/mediumZoom' //适用于博客照片放大

  import 'lightgallery/css/lightgallery-bundle.css' //CSS 打包引用

  import 'justifiedGallery/dist/js/jquery.justifiedGallery.min'
  import 'justifiedGallery/dist/css/justifiedGallery.css'

  import VabUpload from '@/components/VabUpload'

  export default {
    name: 'GalleryContainer',
    components: {},
    props: {
      items: {
        type: Array,
        default: () => Array(40).fill({}), // Initialize with placeholder data,
        required: true,
      },
      total: {
        type: Number,
        default: 50,
        required: true,
      },

      title: {
        type: String,
        default: 'Album', // model field name
        required: true,
      },
      busy: {
        type: Boolean,
        default: false, // model field name
        required: true,
      },
    },
    data() {
      return {
        msg: '正在加载...',
      }
    },
    computed: {},
    watch: {
      items(newVal, oldVal) {
        if (newVal.length === this.total) {
          this.msg = '已经加载完毕, 资源总数量为：' + this.total
        } else {
          this.msg = '正在加载... ' + newVal.length + '/' + this.total
        }
        this.$nextTick(() => {
          console.log('gallery have been changed')
          window.gallery.refresh()
          // $('#gallery').justifiedGallery('norewind')
          $('#gallery').justifiedGallery()
        })
      },
      busy(newVal, oldVal) {
        console.log('GalleryContainer: busy have been changed', newVal)
        if (newVal) {
          this.msg = '正在加载...'
        } else {
          this.msg = '已经加载完毕, 资源总数量为：' + this.total
        }
      },
    },
    created() {},
    mounted() {
      this.lgInit()
      this.justifyInit()
    },
    methods: {
      justifyInit: function () {
        $('#gallery')
          .justifiedGallery({
            captions: false,
            lastRow: 'left',
            rowHeight: 150,
            margins: 5,
          })
          .on('jg.complete', function () {
            console.log('jg.complete event was trigged')
          })
      },
      lgInit: function () {
        const lgGallery = document.getElementById('gallery')
        window.gallery = lightGallery(lgGallery, {
          // dynamic: true,
          addClass: 'gallery',
          autoplayFirstVideo: false,
          pager: false,
          galleryId: 'nature',
          plugins: [
            lgThumbnail,
            lgZoom,
            lgAutoplay,
            lgRotate,
            lgFullscreen,
            // lgMediumZoom,
          ],
          thumbnail: true,
          slideShowInterval: 2000,
          mobileSettings: {
            controls: false,
            showCloseIcon: false,
            download: false,
            rotate: false,
          },
        })
      },

      onChangeDsipType() {
        this.isDispFace = !this.isDispFace
        console.log('onChangeDsipType, current isDispFace: %s', this.isDispFace)
      },
      handleShow(data) {
        this.$refs['vabUpload'].handleShow(data)
      },
      load() {
        console.log('infinite loading... ', this.busy)
        // if (this.busy) return
        this.$emit('load') //自定义事件  传递值“子向父组件传值”load
      },
    },
  }
</script>

<style lang="css" scoped>
  .gallery_container {
    height: 500px; /* Set a fixed height to the container */
    overflow-y: auto;
  }
</style>
