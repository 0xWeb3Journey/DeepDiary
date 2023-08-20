<template>
  <div>
    <DetailHead
      content="人脸详情"
      @edit="onEdit"
      @remove="onRemove"
    ></DetailHead>
    <Carosel v-if="isShowCarosel" title="照片" :items="faces.data"></Carosel>
    <FaceListGallery
      v-if="isGetRoutePrarms"
      :query="faces.query"
      @faceData="onFaceData"
    ></FaceListGallery>
    <!-- <Gallery
      ref="face"
      :name="$route.query.title"
      :items="faces"
      :total="faces.length"
      disp-type="face"
    ></Gallery> -->

    <ProfileEdit
      :profile="profileDetail.data"
      :edit="isDoEdit"
      title="编辑人物信息"
      @close="onClose"
    ></ProfileEdit>
  </div>
</template>

<script>
  import Gallery from '@/components/Gallery'
  import Carosel from '@/components/Carosel'
  import { getGallery, getAlbum, getFaceGallery } from '@/api/gallery'
  import { getProfile, getProfileDetail } from '@/api/profile'
  import DetailHead from './detailHead.vue'
  import ProfileEdit from './profileEdit.vue'
  import FaceListGallery from './faceListGallery.vue'
  export default {
    name: 'ProfileDetail',
    components: { DetailHead, FaceListGallery, Carosel, ProfileEdit },
    data() {
      return {
        isGetRoutePrarms: false,
        isShowCarosel: false,
        isDoEdit: false,
        faces: {
          query: {
            page: 1,
            size: 20,
            // profile__isnull: true,
            profile: 30,
            det_score__gt: 0.7,
            // det_score__lt: 0.6,
            // face_score__gt: 0.8,
            // face_score__lt: 0.6,
            // age__gt: 35,
            // age__lt: 35,
            // gender: 0,
          },
          data: [],
        },
        profileDetail: {
          data: {},
          query: {
            id: -1,
          },
        },
      }
    },
    computed: {
      // album_id: function () {
      //   console.log('album_id have bee updated:')
      //   return this.$route.query.id
      // },
    },
    watch: {
      'profileDetail.query.id'(newVal, oldVal) {
        console.log(
          'this.profileDetail.query.id have bee changed: %d --> %d',
          oldVal,
          newVal
        )
        this.fetchProfileDetail()
      },
    },
    created() {
      console.log('component have been created --')
    },
    mounted() {
      console.log('component have been mounted --')
      // this.fetchProfileDetail()
    },
    activated() {
      // change string format to int
      this.profileDetail.query.id = parseInt(this.$route.query.id)
      this.faces.query.profile = this.profileDetail.query.id
      this.faces.query.page = 1
      this.isGetRoutePrarms = true
      console.log(
        'ProfileDetail: the face component is activated',
        this.faces.query.profile
      )
    },
    deactivated() {
      console.log('the face component is deactivated')
    },
    methods: {
      async fetchProfileDetail() {
        console.log(
          'start to get the fetchProfileDetail...',
          this.profileDetail.query.id
        )

        const { data } = await getProfileDetail(this.profileDetail.query)
        console.log('getProfileDetail: ', data)
        this.profileDetail.data = data
      },
      //进入守卫：通过路由规则，进入该组件时被调用
      beforeRouteEnter(to, from, next) {
        console.log('beforeRouteEnter....')
      },
      //离开守卫：通过路由规则，离开该组件时被调用
      beforeRouteLeave(to, from, next) {
        console.log('beforeRouteLeave....')
      },
      onEdit() {
        console.log('ProfileDetail: onEdit')
        this.isDoEdit = true
      },
      onRemove() {
        console.log('ProfileDetail: onRemove')
      },
      onClose() {
        console.log('ProfileDetail: onClose')
        this.isDoEdit = false
      },
      onFaceData(data) {
        console.log('ProfileDetail: onFaceData', data)
        this.faces.data = data
        this.isShowCarosel = true
      },
    },
  }
</script>

<style></style>
