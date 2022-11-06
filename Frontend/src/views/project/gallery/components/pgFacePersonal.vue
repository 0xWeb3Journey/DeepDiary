<template>
  <div>
    <!-- <el-alert title="父组件消息提示的文案" type="info">
      <span>curAlbumCnt: {{ curAlbumCnt }}, totalCnt: {{ totalCnt }}</span>
    </el-alert>
    <el-button type="primary" @click="fetchFaceAlbum()">get persons</el-button>
     -->
    <Album
      v-if="true"
      ref="album"
      title="人脸相册"
      type="personal"
      :items="persons"
      :total="totalCnt"
      @albumClick="onGetAlbumId"
      @doubleClick="onRouteJump"
    ></Album>

    <Profile v-if="checkedProfile" :id="checkedProfile" mcstype="img"></Profile>
    <!-- :title="`Profile Info-${checkedId}`" -->
    <br />
    <!-- <span>下面是通过路由加载的内容</span>
    <router-view /> -->
  </div>
</template>

<script>
  import $ from 'jquery'
  import Album from './album.vue'
  import Profile from './profile.vue'
  import {
    getGallery,
    getAlbum,
    getFaceAlbum,
    getFaceGallery,
  } from '@/api/gallery'
  export default {
    name: 'PgFacePersonal',
    components: { Album, Profile },
    data: function () {
      return {
        faceAlbumQueryForm: {
          page: 1,
          pageSize: 10,
          search: '',
          faceAlumId: 1,
          faces__id__gte: 0,
        },

        persons: [],
        groups: [],
        albumLoading: false,
        totalCnt: 0,
        curAlbumCnt: 0,
        checkedIndex: -1,
        checkedId: -1,
        checkedProfile: 0,
      }
    },
    created() {
      this.fetchFaceAlbum()
    },
    mounted() {},
    methods: {
      onGetAlbumId(index, id) {
        console.log('recieved the child component value %d,%d', index, id)
        // 声明这个函数，便于子组件调用
        this.checkedIndex = index
        this.checkedId = id || 0 // if return unexpected id, then set the id to default 1
        if (this.persons[index].profile !== null)
          this.checkedProfile = this.persons[index].profile
        else this.checkedProfile = 0
      },
      onRouteJump(index, item) {
        console.log('album double click event item is  %d,%o', index, item)
        this.$router.push({
          name: 'FaceGallery',
          query: {
            id: item.id,
            title: item.name,
          },
        })
      },

      async fetchFaceAlbum() {
        if (this.albumLoading) return //incase fetch more data during the fetching time

        this.albumLoading = true
        if (this.curAlbumCnt < this.totalCnt || this.totalCnt === 0) {
          console.log('start to get the album...')
          const { data, totalCnt } = await getFaceAlbum(this.faceAlbumQueryForm)
          if (totalCnt === 0) return //could fetch any data
          // this.faceAlbumQueryForm.page += 1
          console.log(
            'get img api result, data is %o, total is %d',
            data,
            totalCnt
          )
          this.persons = [...this.persons, ...data]
          this.curAlbumCnt = this.persons.length
          this.totalCnt = totalCnt
          setTimeout(() => {
            this.albumLoading = false
          }, 300)
        }
      },
    },
  }
</script>

<style></style>
