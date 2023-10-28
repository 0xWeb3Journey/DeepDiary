<template>
  <div>
    <ImgSearch @handleImgSearch="onImgSearch" @command="onCommand"></ImgSearch>
    <!-- <div v-show="imgs.loading" class="loading">
      <h2>Loading...</h2>
    </div> -->
    <GalleryContainer
      :items="imgs.data"
      :total="imgs.totalCnt"
      :title="imgs.title"
      :busy="imgs.loading"
      :finished="imgs.finished"
      @load="onLoad"
    />

    <vab-upload
      ref="vabUpload"
      url="/api/img/"
      name="src"
      :limit="500"
      :size="8"
    ></vab-upload>
  </div>
</template>

<script>
  import GalleryContainer from '@/components/Gallery/content.vue'
  import ImgSearch from '@/components/Search'
  import store from '@/store'
  import { getImg } from '@/api/img'
  import VabUpload from '@/components/VabUpload'
  export default {
    name: 'Gallery',
    components: { GalleryContainer, ImgSearch, VabUpload },
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
        imgs: {
          title: 'Img List',
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
            search: '',
            id: '',
            fc_nums: -1, //-1 ,means all, 6 means the fc_nums > 6
            fc_name: '',
            c_img: '',
            c_fore: '',
            c_back: '',
            address__is_located: '',
            address__city: '',
            address__longitude__range: '',
            address__latitude__range: '',
            user__username: store.getters['user/username'],
          },
        },
      }
    },
    watch: {
      // 'query.profile'(newVal, oldVal) {
      //   console.log('Gallery Index: watch: query.profile', newVal)
      //   this.imgs.queryForm.profile = newVal
      //   this.imgs.queryForm.page = 1
      //   this.imgs.data = []
      //   this.fetchImg()
      // },
    },
    created() {},
    mounted() {
      console.log('Gallery Index: mounted', this.imgs.queryForm)
      // this.imgs.queryForm = store.getters['img/queryForm']
      this.fetchImg()
    },
    methods: {
      onRouteJump(index, item) {
        console.log('recieved the child component value %d,%o', index, item)
        // 声明这个函数，便于子组件调用
        this.imgs.checkedIndex = index
        this.imgs.checkedId = item.id || 0 // if return unexpected id, then set the id to default 1
        // this.$router.push({
        //   // name: 'GroupDetail',
        //   name: 'profileDetail',
        //   query: {
        //     id: item.id,
        //     title: item.name,
        //   },
        // })
      },

      async fetchImg() {
        console.log('Gallery Index: fetchImg')
        this.imgs.loading = true
        this.imgs.finished = false
        await getImg(this.imgs.queryForm).then((response) => {
          console.log('Gallery Index: getImg', response)
          const { data, totalCnt, links } = response
          this.imgs.data = [...this.imgs.data, ...data]
          this.imgs.curCnt = this.imgs.data.length
          this.imgs.totalCnt = totalCnt
          this.imgs.links = links
          if (this.imgs.links.next === null) this.imgs.finished = true

          console.log('Gallery Index: emit imgData')
          this.$emit('imgData', this.imgs.data)
          setTimeout(() => {
            this.imgs.loading = false
          }, 2000)
        })
      },

      onLoad() {
        console.log(
          'Gallery Index: onLoad, this.imgs.loading',
          this.imgs.loading
        )
        // if (this.imgs.loading) return  //子组件已经做了处理
        // deal with some logic that data is not enough
        if (this.imgs.finished) {
          // no more data
          setTimeout(() => {
            this.imgs.loading = false
          }, 10000)
          return
        }
        console.log(
          'Gallery Index imgs.queryForm.page: ',
          this.imgs.queryForm.page
        )
        this.imgs.queryForm.page++
        this.fetchImg()
      },
      onImgSearch(queryForm) {
        console.log('recieve the queryForm info from the search component')
        console.log(queryForm)
        this.imgs.queryForm = queryForm
        this.imgs.totalCnt = 0
        this.imgs.data = []
        this.fetchImg()
        // this.loadMore()
      },

      onCommand(Command) {
        console.log('Gallery Index: onCommand', Command)
        if (Command === 'upload') {
          console.log('Gallery Index: onCommand: uploading the image....')
          this.handleShow({ key: 'value' })
        }
      },
      handleShow(data) {
        this.$refs['vabUpload'].handleShow(data)
      },
    },
  }
</script>

<style></style>
