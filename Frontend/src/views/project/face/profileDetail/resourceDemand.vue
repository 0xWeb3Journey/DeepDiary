<template>
  <div>
    <el-row :gutter="12" type="flex" class="row-bg" justify="space-around">
      <el-col
        v-for="item in items"
        :key="item.id"
        :xs="24"
        :sm="12"
        :md="12"
        :lg="8"
        :xl="6"
      >
        <resourceDemandItem :item="item"></resourceDemandItem>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import resourceDemandItem from './resourceDemandItem.vue'
  export default {
    name: 'ResourceDemand',
    components: { resourceDemandItem },
    props: {
      items: {
        type: Array,
        default: () => [
          {
            id: 1,
            name: '英语',
            desc: 'TEM8, 英语可以作为工作语言',
            images: [
              {
                id: 1,
                src: 'https://deep-diary.oss-accelerate.aliyuncs.com/media/user_info_img/%E5%9C%B0%E5%9B%BE%E6%98%BE%E7%A4%BA.png',
                thumb:
                  'https://deep-diary.oss-accelerate.aliyuncs.com/media/CACHE/images/user_info_img/%E5%9C%B0%E5%9B%BE%E6%98%BE%E7%A4%BA/1ed8b21aca917ed0e325c8571f207821.jpg',
              },
              {
                id: 5,
                src: 'https://deep-diary.oss-accelerate.aliyuncs.com/media/user_info_img/deep-diary_cover.png',
                thumb:
                  'https://deep-diary.oss-accelerate.aliyuncs.com/media/CACHE/images/user_info_img/deep-diary_cover/69e150672e13b78f12fc3edb4ed1c43c.jpg',
              },
            ],
          },
          {
            id: 2,
            name: '项目管理',
            desc: '汽车行业项目管理多年，具有PMP证书',
            images: [
              {
                id: 2,
                src: 'https://deep-diary.oss-accelerate.aliyuncs.com/media/user_info_img/graph.png',
                thumb:
                  'https://deep-diary.oss-accelerate.aliyuncs.com/media/CACHE/images/user_info_img/graph/95d18d95174b3b62eff00d33573b8058.jpg',
              },
            ],
          },
          {
            id: 3,
            name: '英语教培',
            desc: '曾在上海精锐担任过培训讲师，带过超千名学生',
            images: [
              {
                id: 3,
                src: 'https://deep-diary.oss-accelerate.aliyuncs.com/media/user_info_img/gallery.png',
                thumb:
                  'https://deep-diary.oss-accelerate.aliyuncs.com/media/CACHE/images/user_info_img/gallery/049f4164c4e2e5252543419c2f4f584f.jpg',
              },
            ],
          },
        ],
        required: false,
      },
    },
    data() {
      return {}
    },
    computed: {},
    watch: {
      items(newVal, oldVal) {
        console.log('ResourceDemand: items have bee changed: ', newVal)
      },
    },
    created() {
      console.log('ResourceDemand: component has been created --')
    },
    mounted() {
      console.log('ResourceDemand: component has been mounted --')
    },
    activated() {
      console.log('ResourceDemand: component has been activated --')
    },
    deactivated() {
      console.log('ResourceDemand: component has been deactivated -- ')
    },
    methods: {
      //进入守卫：通过路由规则，进入该组件时被调用
      beforeRouteEnter(to, from, next) {
        console.log('ResourceDemand: component has been beforeRouteEnter -- ')
      },
      //离开守卫：通过路由规则，离开该组件时被调用
      beforeRouteLeave(to, from, next) {
        console.log('ResourceDemand: component has been beforeRouteLeave -- ')
      },
    },
  }
</script>

<style></style>
