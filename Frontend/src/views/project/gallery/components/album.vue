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
        <span>{{ title }}({{ checkedIndex + 1 }} / {{ total }})</span>
        <span v-if="albumName">> {{ albumName }} ({{ albumCnt }})</span>
        <el-page-header
          v-if="false"
          :content="title"
          @back="goBack"
        ></el-page-header>
        <el-button-group style="float: right">
          <el-button type="primary" icon="el-icon-plus"></el-button>
          <el-button type="primary" icon="el-icon-edit"></el-button>
          <el-button
            type="primary"
            icon="el-icon-map-location"
            @click="clear"
          ></el-button>
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
          />
          <!-- :title="album.name" -->
          <div class="jg-caption">
            <el-row>
              <el-col :span="20">
                <el-input
                  v-model="album.name"
                  placeholder="Change the Name"
                  style="float: left; font-size: 8px"
                  @blur="changeName(album.name, album)"
                  @keyup.enter.native="enterBlur($event)"
                ></el-input>
              </el-col>
              <el-col :span="4">
                <label
                  for="name"
                  style="float: right; display: inline-block; font-size: 15px"
                >
                  {{ album.item_cnt }}
                </label>
              </el-col>
            </el-row>
          </div>
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

  import {
    getGallery,
    getAlbum,
    getFaceAlbum,
    changeFaceAlbumName,
    changeFaceName,
    clear_face_album,
  } from '@/api/gallery'

  export default {
    name: 'Album',
    components: { VabUpload },
    props: {
      items: {
        type: Array,
        default: () => [],
        required: true,
      },
      total: {
        type: Number,
        default: 50,
        required: true,
      },

      title: {
        type: String,
        default: '88888888888888', // model field name
        required: true,
      },
      type: {
        type: String,
        default: 'img', // could be face, personal, group, collection, address, obect
        required: false,
      },
      route: {
        type: String,
        default: 'Face_detail', // could be face, personal, group, collection, address, obect
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
        postData: {
          id: 0,
          name: '',
        },
        // albums: [],
        albumLoading: false,
        totalAlbumCnt: 0,
        curAlbumCnt: 0,

        checkedIndex: -1, //if set this default value to 0, then the album will auto checked once enter this page
        checkedId: 0,
        checkedName: '',
        jumpId: 0,

        albumName: '', //相册下面的具体名字
        albumCnt: 1, //某个相册下面的具体数量
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
        console.log('单击事件', this.type, this.total)
        this.checkedIndex = index
        this.drawer = true
        let jumpId

        if (this.type === 'img') {
          this.jumpId = item.face_album //choose the face album
          this.checkedId = item.id // choose the face img
          this.routeName = 'FaceGallery'
          this.albumName = item.name
          // this.albumCnt = item.item_cnt
        }
        if (this.type === 'personal') {
          this.jumpId = item.id
          this.checkedId = item.profile
          this.routeName = 'FaceGallery'
          this.albumName = item.name
          this.albumCnt = item.item_cnt
        }
        if (this.type === 'collection') {
          this.jumpId = item.id
          this.checkedId = item.id
          this.routeName = 'Img'
          // this.albumName = item.names.join(',')
          this.albumName = item.filename
          // this.albumCnt = item.item_cnt
        }
        console.log(this.type, this.checkedIndex, this.checkedId)
        // $('#album').justifiedGallery()
        this.$emit('albumClick', index, this.checkedId) //自定义事件  传递值“子向父组件传值”
      },

      async changeFaceAlbumName(value, album) {
        console.log(value, this.albumName)
        // this.items[index].name = value
        if (value !== this.albumName) {
          this.postData.id = album.id //人脸相册id
          this.postData.name = value
          // this.$message({
          //   message: `Success changed ${this.albumName} to ${value}`,
          //   type: 'success',
          // })

          const { data, msg } = await changeFaceAlbumName(this.postData)
          console.log(data, msg)
          this.$message({
            message: `Success changed ${this.albumName} to ${value}`,
            type: 'success',
          })

          this.albumName = value
        }
      },

      async changeFaceName(value, album) {
        console.log(value, this.albumName)
        // this.items[index].name = value
        if (value !== this.albumName) {
          this.postData.id = this.checkedId
          this.postData.name = value
          // this.$message({
          //   message: `Success changed ${this.albumName} to ${value}`,
          //   type: 'success',
          // })
          const { data, msg } = await changeFaceName(this.postData)
          console.log(data, msg)
          this.$message({
            message: `Success changed ${this.albumName} to ${value}`,
            type: 'success',
          })

          this.albumName = value
        }
      },

      changeName(value, album) {
        if (this.type === 'personal') {
          this.changeFaceAlbumName(value, album)
        }
        if (this.type === 'img') {
          this.changeFaceName(value, album)
        }
      },

      //回车失去焦点
      enterBlur(event) {
        event.target.blur()
      },

      async clear() {
        const { data, msg } = await clear_face_album(this.postData)
        console.log(msg)
        this.$message({
          message: msg,
          type: 'success',
        })
      },
      //upload the img
      handleShow(data) {
        this.$refs['vabUpload'].handleShow(data)
      },

      //双击事件
      onDoubleClick(event, index, item) {
        console.log('双击事件')
        this.$router.push({
          name: this.routeName,
          query: {
            id: this.jumpId,
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
  /* .box-card {
    height: 500x;
    border: 1px solid rgb(8, 23, 231);
  } */
</style>
