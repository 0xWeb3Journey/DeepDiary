<template>
  <div>
    <GalleryContainer
      :items="faces.data"
      :total="faces.totalCnt"
      :title="faces.title"
      :busy="faces.loading"
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
  export default {
    name: 'FaceListGallery',
    components: { GalleryContainer },
    directives: {},
    props: {
      query: {
        type: Object,
        default: null, // model field name
        required: false,
      },
    },
    data: function () {
      return {
        faces: {
          title: 'Face List',
          loading: false,
          checkedId: -1,
          checkedIndex: -1,
          totalCnt: 0,
          links: null,
          curCnt: 0,
          data: [],
          FaceQueryForm: {
            page: 1,
            size: 25,
            // profile__isnull: true,
            profile: 30,
            det_score__gt: 0.8,
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
      //     this.faces.FaceQueryForm = newVal
      //     this.faces.data = []
      //     console.log('FaceList: query', this.faces.data)
      //     // this.fetchFace()
      //   },
      //   deep: true,
      // },
      'query.profile'(newVal, oldVal) {
        console.log('FaceList: watch: query.profile', newVal)
        this.faces.FaceQueryForm.profile = newVal
        this.faces.FaceQueryForm.page = 1
        this.faces.data = []
        this.fetchFace()
      },
    },
    created() {},
    mounted() {
      console.log('FaceList: mounted', this.faces.FaceQueryForm)
      this.faces.FaceQueryForm = this.query
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
        console.log('FaceList: fetchFace')
        this.faces.loading = true
        await getFace(this.faces.FaceQueryForm).then((response) => {
          console.log('getFaceChangeAvatar', response)
          const { data, totalCnt, links } = response
          this.faces.data = [...this.faces.data, ...data]
          this.faces.curCnt = this.faces.data.length
          this.faces.totalCnt = totalCnt
          this.faces.links = links
          console.log('FaceList: emit faceData')
          this.$emit('faceData', this.faces.data)
          setTimeout(() => {
            this.faces.loading = false
          }, 300)
        })
      },

      onLoad() {
        console.log('FaceList: onLoad')
        if (this.faces.loading) return
        // deal with some logic that data is not enough
        if (this.faces.links.next == null) {
          // no more data
          setTimeout(() => {
            this.faces.loading = false
          }, 3000)
          return
        }
        this.faces.FaceQueryForm.page++
        this.fetchFace()
      },
    },
  }
</script>

<style></style>
