<template>
  <div>
    <DetailHead
      :content="`人物详情 | ${profileDetail.data.name} | ${profileDetail.data.relation} | 共计${faces.totalCnt}张照片 `"
      @edit="onEdit"
      @remove="onRemove"
    ></DetailHead>
    <Carosel v-if="isShowCarosel" title="照片" :items="faces.data"></Carosel>
    <FaceListGallery
      v-if="isGetRoutePrarms"
      :id="profileDetail.query.id"
      :searchable="false"
      @faceData="onFaceData"
    ></FaceListGallery>

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
      console.log('profileDetail component have been created --')
    },
    mounted() {
      console.log('profileDetail component have been mounted --')
    },
    activated() {
      console.log('profileDetail component have been activated --')
      // change string format to int
      this.profileDetail.query.id = parseInt(this.$route.query.id)

      this.isGetRoutePrarms = true
    },
    deactivated() {
      this.faces.data = [] //退出之前清空缓存，防止下次进入的时候，先显示上次的数据，再显示新的数据
      console.log('profileDetail: the face component is deactivated')
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
        // console.log('ProfileDetail: onFaceData', data)
        this.faces = data
        this.isShowCarosel = true
      },
    },
  }
</script>

<style></style>
