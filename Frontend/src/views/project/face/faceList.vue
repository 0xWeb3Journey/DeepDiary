<template>
  <div>
    <FaceSearch v-if="searchable" @handleFaceSearch="onFaceSearch"></FaceSearch>
    <AlbumContainer
      :items="faces.data"
      :total="faces.totalCnt"
      :title="faces.title"
      :busy="faces.loading"
      :finished="faces.finished"
      @albumClick="onClick"
      @load="onLoad"
      @changeName="onChangeName"
    />
  </div>
</template>

<script>
  import AlbumContainer from '@/components/Album/content.vue'
  import { getFace } from '@/api/face'
  import { changeFaceName } from '@/api/face'
  import FaceSearch from '@/components/Search/face'
  export default {
    name: 'FaceList',
    components: { AlbumContainer, FaceSearch },
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
        default: null, // model field name
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
            confirmed: '1',
            // profile__isnull: true,l
            // profile: 30,
            // det_score__gt: 0.8,
            // det_score__lt: 0.6,
            // face_score__gt: 0.8,
            // face_score__lt: 0.6,
            // age__gt: 35,
            // age__lt: 35,
            // gender: 0,
          },
        },
        patchParams: {
          id: 0,
          name: '',
          // relation: '',
        },
      }
    },
    watch: {
      // 'query.profile'(newVal, oldVal) {
      //   console.log('FaceList: watch: query.profile', newVal)
      //   this.faces.queryForm.profile = newVal
      //   this.faces.queryForm.page = 1
      //   this.faces.data = []
      //   this.fetchFace()
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
      console.log('FaceList: mounted')
      // this.faces.queryForm = this.query // 不使用父组件查询条件，使用本地查询条件
      // this.faces.queryForm.page = 1

      this.faces.queryForm.profile = this.id
      this.fetchFace()
    },
    methods: {
      onClick(index, item) {
        console.log('recieved the child component value %d,%o', index, item)
        // 声明这个函数，便于子组件调用
        this.faces.checkedIndex = index
        this.faces.checkedId = item.id || 0 // if return unexpected id, then set the id to default 1
        this.$emit('choosed', item)
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
          console.log('getFaceChangeAvatar', response)
          const { data, totalCnt, links } = response
          this.faces.data = [...this.faces.data, ...data]
          this.faces.curCnt = this.faces.data.length
          this.faces.totalCnt = totalCnt
          this.faces.links = links
          if (this.faces.links.next === null) {
            // no more data
            this.faces.finished = true
            console.log('FaceList: fetchFace: no more data------------')
          }
          this.$emit('faceData', this.faces.data)
        })
        setTimeout(() => {
          this.faces.loading = false
        }, 500)
      },

      onLoad() {
        console.log('FaceList: onLoad:loading:', this.faces.loading)
        if (this.faces.loading === true) return
        // deal with some logic that data is not enough
        if (this.faces.finished) {
          console.log(
            'FaceList: onLoad: faces.links.next is null, finished:',
            this.faces.finished
          )
          setTimeout(() => {
            this.faces.loading = false
          }, 3000)
          return
        }
        this.faces.queryForm.page++
        this.fetchFace()
      },
      onChangeName(value, album) {
        console.log('FaceList: onChangeName', value, album)
        this.patchParams.id = album.id
        this.patchParams.name = value
        this.onProcessEdit()
      },

      async onProcessEdit() {
        console.log(
          'faceList: onProcessEdit',
          `新名称：${this.patchParams.name}`
        )

        // this.loading = true
        await changeFaceName(this.patchParams).then((response) => {
          console.log('faceList: changeFaceName', response)
          // 后台更新返回后
          // this.loading = false
          this.patchParams.name = '' // 修改成功后，新名称重新置为空
          this.$message({
            message: `修改成功`,
            type: 'success',
          })
        })
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
