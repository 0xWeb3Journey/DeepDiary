<template>
  <div>
    <FaceSearch v-if="searchable" @handleFaceSearch="onFaceSearch"></FaceSearch>
    <GalleryContainer
      :items="faces.data"
      :total="faces.totalCnt"
      :title="faces.title"
      :busy="faces.loading"
      :finished="faces.finished"
      @load="onLoad"
    />
    <!-- <Gallery
      ref="gallery"
      name="相片"
      disp-type="thumb"
      storage-type="oss"
      :items="faces.data"
      :total="faces.totalCnt"
    ></Gallery> -->
  </div>
</template>

<script>
  import GalleryContainer from '@/components/Gallery/content.vue'
  import Gallery from '@/components/Gallery'
  import { getFace } from '@/api/face'
  import FaceSearch from '@/components/Search/face'
  export default {
    name: 'FaceListGallery',
    components: { GalleryContainer, FaceSearch },
    directives: {},
    props: {
      query: {
        type: Object,
        default: null, // model field name
        required: false,
      },
      searchable: {
        type: Boolean,
        default: true, // model field name
        required: false,
      },
      id: {
        type: Number,
        default: null, // 如果默认设置为0，会导致id=0的情况下，后端无响应，应为不存在id=0对应的profile
        required: false,
      },
    },
    data: function () {
      return {
        faces: {
          title: 'Face List',
          loading: false,
          finished: false,
          checkedId: -1,
          checkedIndex: -1,
          totalCnt: 0,
          links: null,
          curCnt: 0,
          data: [],
          queryForm: {
            page: 1,
            size: 25,
            // profile__isnull: true,
            profile: '',
            // det_score__gt: 0.6,
            // det_score__lt: 0.6,
            // face_score__gt: 0.8,
            // face_score__lt: 0.6,
            // age__gt: 35,
            // age__lt: 35,
            // gender: 0,
          },
        },
      }
    },
    watch: {
      // query: {
      //   handler(newVal, oldVal) {
      //     console.log('FaceList: query', newVal)
      //     this.faces.queryForm = newVal
      //     this.faces.data = []
      //     console.log('FaceList: query', this.faces.data)
      //     // this.fetchFace()
      //   },
      //   deep: true,
      // },

      // 'query.profile'(newVal, oldVal) {
      id(newVal, oldVal) {
        console.log('FaceListGallery: watch: query.profile', newVal)
        this.faces.queryForm.profile = newVal
        this.faces.queryForm.page = 1
        this.faces.data = []
        this.fetchFace()
      },
    },
    created() {},
    mounted() {
      console.log('FaceListGallery: mounted', this.faces.queryForm)
      // this.faces.queryForm = this.query // 不使用父组件查询条件，使用本地查询条件
      // this.faces.queryForm.page = 1

      this.faces.queryForm.profile = this.id
      console.log('FaceListGallery: mounted', this.faces.queryForm)
      this.fetchFace()
    },
    methods: {
      onRouteJump(index, item) {
        console.log('recieved the child component value %d,%o', index, item)
        // 声明这个函数，便于子组件调用
        this.faces.checkedIndex = index
        this.faces.checkedId = item.id || 0 // if return unexpected id, then set the id to default 1
        // this.$router.push({
        //   // name: 'GroupDetail',
        //   name: 'profileDetail',
        //   query: {
        //     id: item.id,
        //     title: item.name,
        //   },
        // })
      },

      async fetchFace() {
        this.faces.loading = true
        this.faces.finished = false
        await getFace(this.faces.queryForm).then((response) => {
          console.log('FaceListGallery: getFace', response)
          const { data, totalCnt, links } = response
          this.faces.data = [...this.faces.data, ...data]
          this.faces.curCnt = this.faces.data.length
          this.faces.totalCnt = totalCnt
          this.faces.links = links
          if (this.faces.links.next === null) {
            this.faces.finished = true
            console.log(
              'FaceListGallery: fetchFace: no more data-----------------'
            )
          }
          console.log('FaceListGallery: emit faceData')
          this.$emit('faceData', this.faces.data)
        })

        setTimeout(() => {
          this.faces.loading = false
        }, 300)
      },

      onLoad() {
        console.log(
          'FaceListGallery: onLoad',
          this.faces.loading,
          this.faces.finished
        )
        if (this.faces.loading) return
        // deal with some logic that data is not enough
        if (this.faces.finished) {
          // no more data
          setTimeout(() => {
            this.faces.loading = false
          }, 3000)
          return
        }
        this.faces.queryForm.page++
        this.fetchFace()
      },
      onFaceSearch(queryForm) {
        console.log('recieve the queryForm info from the search component')
        console.log(queryForm)
        this.faces.queryForm = queryForm
        this.faces.totalCnt = 0
        this.faces.data = []
        this.fetchFace()
        // this.loadMore()
      },
    },
  }
</script>

<style></style>
