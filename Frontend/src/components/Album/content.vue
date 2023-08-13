<template>
  <div class="album_container">
    <div
      id="album_container"
      ref="album_container"
      v-infinite-scroll="load"
      infinite-scroll-disabled="busy"
      infinite-scroll-distance="400"
      infinite-scroll-immediate-check="true"
      :force-use-infinite-wrapper="true"
      class="content"
    >
      <div
        v-for="(item, index) in items"
        :key="item.id"
        @click="onClick($event, index, item)"
        @dblclick="onDoubleClick($event, index, item)"
      >
        <img
          className="img-responsive"
          :class="checkedIndex === index ? 'img-checked' : 'img-unchecked'"
          :src="item.thumb"
          :alt="item.name"
        />

        <div class="jg-caption">
          <el-badge :value="item.value" :max="99" class="item" type="primary">
            <el-input
              v-model="item.name"
              size="small"
              placeholder="Change the Name"
              style="float: left; font-size: 8px"
              class="item-name"
              @blur="changeName(item.name, item)"
              @keyup.enter.native="enterBlur($event)"
            ></el-input>
          </el-badge>
        </div>
      </div>
      <div v-show="busy" class="loading">
        <h2>{{ msg }}</h2>
      </div>
    </div>
  </div>
</template>

<script>
  import $ from 'jquery'

  import 'justifiedGallery/dist/js/jquery.justifiedGallery.min'
  import 'justifiedGallery/dist/css/justifiedGallery.css'
  import infiniteScroll from 'vue-infinite-scroll'

  export default {
    name: 'AlbumContainer',
    directives: { infiniteScroll },
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

        checkedIndex: -1, //if set this default value to 0, then the album will auto checked once enter this page
        checkedId: 0,
      }
    },
    watch: {
      items(newVal, oldVal) {
        if (newVal.length === this.total) {
          this.msg = '已经加载完毕, 资源总数量为：' + this.total
        } else {
          this.msg = '正在加载... ' + newVal.length + '/' + this.total
        }
        console.log(
          'Album.content: Album numbers have been changed',
          newVal.length,
          this.total,
          this.msg
        )
        this.$nextTick(() => {
          // window.album.refresh()
          $('#album_container').justifiedGallery()
          // $('#album').justifiedGallery('norewind')
        })
      },
    },
    created() {
      console.log('Album.content: Album component created')
    },
    mounted() {
      this.justifyInit()
    },
    methods: {
      justifyInit: function () {
        // $('#album')
        $('[id=album_container]')
          .justifiedGallery({
            captions: true,
            lastRow: 'left',
            rowHeight: 150,
            margins: 5,
          })
          .on('jg.complete', function () {
            console.log('Album.content: jg.complete event was trigged')
          })
      },

      onClick($event, index, item) {
        console.log('Album.content: onClick: ', item)

        this.checkedIndex = index

        if (index < 0) return //reture directly if there is no item in items
        if (item === null) return //reture directly if there is no item in items
        this.checkedId = item.id
        this.$emit('albumClick', index, item) //自定义事件  传递值“子向父组件传值”
      },

      //双击事件
      onDoubleClick(event, index, item) {
        console.log('Album.content: onDoubleClick')
        this.$emit('doubleClick', index, item) //自定义事件  传递值“子向父组件传值”
      },

      changeName(value, album) {
        console.log('Album.content: changeName')
        this.$emit('changeName', value, album) //自定义事件  传递值“子向父组件传值”
      },

      //回车失去焦点
      enterBlur(event) {
        console.log('Album.content: enterBlur')
        event.target.blur()
      },

      load() {
        console.log('infinite loading... ', this.busy)
        if (this.busy) return
        this.$emit('load') //自定义事件  传递值“子向父组件传值”load
      },
    },
  }
</script>

<style lang="css" scoped>
  .img-checked {
    border-radius: 60px;
    border-style: solid;
    border-width: 3px;
    border-color: #1515f1c3;
    box-shadow: -20px -20px 20px rgba(34, 34, 183, 0.5);

    /* opacity: 0.1; */
  }
  .img-unchecked {
    opacity: 0.5;
  }
  /* .box-card {
    height: 500x;
    border: 1px solid rgb(8, 23, 231);
  } */
  .item {
    margin-top: 1px;
    margin-right: 15px;
  }
  /* .infinite-list {
    height: 550px;
    width: 100%;
    margin: 0 auto;
    overflow: auto;
  } */
  .album_container {
    height: 500px; /* Set a fixed height to the container */
    overflow-y: auto;
  }
</style>
