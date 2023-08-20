<template>
  <div>
    <DetailHead
      content="人脸详情"
      @edit="onEdit"
      @remove="onRemove"
    ></DetailHead>
    <Carosel title="照片" :items="groups"></Carosel>
    <Gallery
      ref="face"
      :name="$route.query.title"
      :items="groups"
      :total="groups.length"
      disp-type="img"
    ></Gallery>
  </div>
</template>

<script>
  import Gallery from '@/components/Gallery'
  import Carosel from '@/components/Carosel'
  import { getGroupDetail } from '@/api/category'
  import DetailHead from './detailHead.vue'
  export default {
    name: 'GroupDetail',
    components: { Gallery, Carosel, DetailHead },

    data() {
      return {
        groups: [],
        totalCnt: 0,
        queryForm: {
          id: '',
        },
      }
    },
    computed: {},
    watch: {
      'queryForm.id'(newVal, oldVal) {
        console.log(
          'this.faceQueryForm.id have bee changed: %d --> %d',
          oldVal,
          newVal
        )
        this.groups = []
        this.fetchGroupDetail()
      },
    },
    created() {
      console.log('component have been created --')
    },
    mounted() {
      console.log('component have been mounted --')
      // this.fetchGroupDetail()
    },
    activated() {
      console.log('the face component is activated')
      this.queryForm.id = this.$route.query.id
    },
    deactivated() {
      console.log('the face component is deactivated')
    },
    methods: {
      async fetchGroupDetail() {
        console.log('start to get the fetchGroupDetail...')

        this.queryForm.id = this.$route.query.id
        // console.log('this.queryForm.id: ', this.queryForm.id)
        const { data } = await getGroupDetail(this.$route.query.id)
        console.log('fetchGroupDetail: ', data)
        this.groups = [...data.imgs]
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
        console.log('groupDetail: onEdit')
      },
      onRemove() {
        console.log('groupDetail: onRemove')
      },
    },
  }
</script>

<style></style>
