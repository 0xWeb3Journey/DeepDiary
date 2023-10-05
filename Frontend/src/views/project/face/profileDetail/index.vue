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

    <el-collapse v-model="activeName" accordion>
      <!-- <el-collapse-item name="carousel">
        <template slot="title">跑马灯 Carousel</template>
      </el-collapse-item>
      <el-collapse-item title="人脸 Faces" name="faces"></el-collapse-item> -->
      <el-collapse-item name="resources">
        <template slot="title">三大资源 Resources</template>

        <ResourceDemand
          :items="profileDetail.data.resources"
          type="resource"
        ></ResourceDemand>
      </el-collapse-item>
      <el-collapse-item title="三大需求 Demands" name="demands">
        <ResourceDemand
          :items="profileDetail.data.demands"
          type="demand"
        ></ResourceDemand>
      </el-collapse-item>

      <el-collapse-item title="工作经历 Experiences" name="experience">
        <Experience :items="profileDetail.data.experiences"></Experience>
      </el-collapse-item>
    </el-collapse>

    <ProfileEdit
      :profile="profileDetail.data"
      :edit="isDoEdit"
      title="编辑人物信息"
      @close="onClose"
    ></ProfileEdit>
  </div>
</template>

<script>
  import Carosel from '@/components/Carosel'
  import { getProfileDetail } from '@/api/profile'
  import DetailHead from '../detailHead.vue'
  import ProfileEdit from './profileEdit.vue'
  import FaceListGallery from '../faceListGallery.vue'
  import ResourceDemand from './resourceDemand.vue'
  import Experience from './experience.vue'
  import Menu from '@/components/Menu'
  export default {
    name: 'ProfileDetail',
    components: {
      DetailHead,
      FaceListGallery,
      Carosel,
      ProfileEdit,
      ResourceDemand,
      Experience,
    },
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
        activeName: 'faces',
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
        this.faces.data = [] //获取新id数据之前清空缓存，防止下次进入的时候，先显示上次的数据，再显示新的数据
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
