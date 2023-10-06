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
          <el-tooltip
            :content="item.caption ? item.caption : 'No Caption'"
            placement="top"
          >
            <img className="img-responsive" :src="item.thumb" />
          </el-tooltip>
        </a>
      </div>

      <div v-show="busy" class="loading">
        <h3>{{ msg }}</h3>
      </div>
    </div>
    <el-divider v-show="finished"><i class="el-icon-finished"></i></el-divider>
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
      finished: {
        type: Boolean,
        default: false, // model field name
        required: false,
      },
    },
    data() {
      return {
        msg: 'Loading...',
        intervalId: null, // Variable to hold the interval ID
      }
    },
    computed: {},
    watch: {
      items(newVal, oldVal) {
        // if (newVal.length === this.total) {
        //   this.msg = '已经加载完毕, 资源总数量为：' + this.total
        // } else {
        //   this.msg = '正在加载... ' + newVal.length + '/' + this.total
        // }
        // if (newVal.length === 0) {
        //   this.msg = '没有找到任何资源'
        // }
        this.checkDivHeight() // 内容更新后，需要检查下div的高度
        this.$nextTick(() => {
          console.log('gallery have been changed')
          window.gallery.refresh()
          // $('#gallery').justifiedGallery('norewind')
          $('#gallery').justifiedGallery()
        })
      },
    },
    created() {},
    mounted() {
      this.lgInit()
      this.justifyInit()
      // this.checkDivHeight()
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
        if (this.busy) return
        this.$emit('load') //自定义事件  传递值“子向父组件传值”load
      },

      checkDivHeight() {
        // if this.intervalId is null, then return
        if (this.intervalId !== null) {
          console.log('Gallery content: checkDivHeight: intervalId is not null')
          return
        }
        // Get a reference to the div element
        var divElement = this.$refs.gallery_container
        // Check if the div element exists
        if (divElement) {
          // Create an interval to check the div's height every 1 second
          this.intervalId = setInterval(() => {
            //init the height
            this.$refs.gallery_container.style.height = 600 + 'px'
            // Check if the component is busy
            if (this.busy === false) {
              // Get the current scroll height of the div
              var scrollHeight = divElement.scrollHeight

              // Get the current scrollTop of the div
              var scrollTop = divElement.scrollTop

              // Get the client height of the div
              // var divHeight = divElement.clientHeight
              var divHeight = 1000

              // check if all the data has been loaded

              if (scrollHeight > divHeight) {
                // The div is filled, so clear the interval
                clearInterval(this.intervalId)
                this.intervalId = null // Reset the interval ID
                console.log('timer has been closed', scrollHeight, divHeight)
              } else {
                if (this.finished) {
                  clearInterval(this.intervalId)
                  this.intervalId = null // Reset the interval ID
                  // set the gallery_container div to scrollHeight

                  const contentHeight = this.$refs.gallery.scrollHeight

                  // const scrollHeight = content.scrollHeight
                  this.$refs.gallery_container.style.height =
                    contentHeight + 'px'

                  console.log(
                    'Set the divHeight to match content height:',
                    this.$refs.gallery_container.style.height
                  )
                } else {
                  // The div is not filled, continue monitoring

                  this.$emit('load') //自定义事件  传递值“子向父组件传值”load  //content.vue:204  Uncaught TypeError: this.$emit is not a function
                }
              }

              // // Check if the div's height is greater than or equal to the screen height
              // if (scrollHeight > divHeight || this.finished) {
              //   // The div is filled, so clear the interval
              //   clearInterval(this.intervalId)
              //   this.intervalId = null // Reset the interval ID
              //   console.log('timer has been closed')
              // } else {
              //   // The div is not filled, continue monitoring

              //   this.$emit('load') //自定义事件  传递值“子向父组件传值”load  //content.vue:204  Uncaught TypeError: this.$emit is not a function
              // }
            }
          }, 1000) // Check every 1 second
        }
      },
    },
  }
</script>

<style lang="css" scoped>
  .gallery_container {
    height: 800px;
    overflow-y: auto;
  }
</style>
