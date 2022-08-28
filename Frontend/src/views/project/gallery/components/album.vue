<template>
  <div class="gallery-container">
    <!-- <el-alert title="子组件消息提示的文案" type="info">
      <br />
      albumInfo:
      <span v-for="album in items" :key="album.id">{{ album.id }},</span>
      <br />
      checkedIndex: {{ checkedIndex }};checkedId: {{ checkedId }}
    </el-alert> -->

    <vab-upload
      ref="vabUpload"
      url="/api/img/"
      name="src"
      :limit="50"
      :size="8"
    ></vab-upload>

    <!-- Album -->
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>{{ title }}</span>
        <span v-if="albumName">> {{ albumName }}</span>
        <el-page-header
          v-if="false"
          :content="title"
          @back="goBack"
        ></el-page-header>
        <el-button-group style="float: right">
          <el-button type="primary" icon="el-icon-plus"></el-button>
          <el-button type="primary" icon="el-icon-edit"></el-button>
          <el-button type="primary" icon="el-icon-map-location"></el-button>
          <el-button
            type="primary"
            icon="el-icon-user-solid"
            @click="onChangeDetailType('album')"
          ></el-button>

          <el-button
            type="primary"
            icon="el-icon-picture"
            @click="onChangeDetailType('face-img')"
          ></el-button>
          <el-button
            type="primary"
            icon="el-icon-upload"
            @click="handleShow({ key: 'value' })"
          ></el-button>
        </el-button-group>
      </div>

      <div id="album" ref="album">
        <div
          v-for="(album, index) in items"
          :key="album.id"
          class-name="album-item"
          @click="onAlbumChoose($event, index, album)"
          @dblclick="onDoubleClick($event, index, album)"
        >
          <img
            className="img-responsive"
            :class="checkedIndex === index ? 'img-checked' : 'img-unchecked'"
            :src="album.src"
            :alt="album.name"
            :title="album.name"
          />
          <!-- <div class="jg-caption">I'm only in the alt</div> -->
        </div>
      </div>
    </el-card>
    <!-- <el-drawer
      title="我是标题"
      :visible.sync="drawer"
      :direction="direction"
      :modal-append-to-body="true"
    >
      <span>我来啦!</span>
    </el-drawer> -->
  </div>
</template>

<script>
  import $ from 'jquery'

  import 'justifiedGallery/dist/js/jquery.justifiedGallery.min'
  import 'justifiedGallery/dist/css/justifiedGallery.css'

  import VabUpload from '@/components/VabUpload'

  export default {
    name: 'Album',
    components: { VabUpload },
    props: {
      items: {
        type: Array,
        default: () => [],
        required: true,
      },
      title: {
        type: String,
        default: '88888888888888', // model field name
        required: true,
      },
      type: {
        type: String,
        default: 'face', // could be face, personal, group, collection, address, obect
        required: false,
      },
      route: {
        type: String,
        default: 'Face_detail', // could be face, personal, group, collection, address, obect
        required: false,
      },
      limit: {
        type: Number,
        default: 50,
        required: false,
      },
      size: {
        type: Number,
        default: 8,
        required: false,
      },
    },
    data() {
      return {
        drawer: false,
        direction: 'rtl',
        plugin: null,
        elementLoadingText: '正在加载...',
        msg: '',
        queryForm: {
          page: 1,
          pageSize: 10,
          search: '',
        },
        // albums: [],
        albumLoading: false,
        totalAlbumCnt: 0,
        curAlbumCnt: 0,

        checkedIndex: '0',
        checkedId: '0',

        albumName: '', //相册下面的具体名字
      }
    },
    watch: {
      items(newVal, oldVal) {
        this.$nextTick(() => {
          console.log('onAlbumChoose have been changed', newVal)
          // window.album.refresh()
          $('#album').justifiedGallery()
          // $('#album').justifiedGallery('norewind')
        })
      },
    },
    created() {
      // this.fetchAlbum()
    },
    mounted() {
      this.justifyInit()
    },
    methods: {
      justifyInit: function () {
        // $('#album')
        $('[id=album]')
          .justifiedGallery({
            captions: true,
            lastRow: 'left',
            rowHeight: 150,
            margins: 5,
          })
          .on('jg.complete', function () {
            console.log('jg.complete event was trigged')
          })
      },

      onAlbumChoose($event, index, item) {
        console.log('单击事件')
        this.checkedIndex = index
        this.drawer = true

        if (this.type === 'face') {
          this.checkedId = item.face_album
          this.routeName = 'FaceGallery'
          this.albumName = item.name
        }
        if (this.type === 'personal') {
          this.checkedId = item.id
          this.routeName = 'FaceGallery'
          this.albumName = item.name
        }
        if (this.type === 'collection') {
          this.checkedId = item.id
          this.routeName = 'Img'
          // this.albumName = item.names.join(',')
          this.albumName = item.filename
        }
        console.log(this.checkedIndex, this.checkedId)
        // $('#album').justifiedGallery()
        this.$emit('albumClick', index, this.checkedId) //自定义事件  传递值“子向父组件传值”
      },

      //双击事件
      onDoubleClick(event, index, item) {
        console.log('双击事件')
        this.$router.push({
          name: this.routeName,
          query: {
            id: this.checkedId,
            title: item.name,
          },
        })
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
</style>
