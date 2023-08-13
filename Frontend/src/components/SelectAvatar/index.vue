<template>
  <div class="select-avatar-container">
    <AlbumContainer
      :items="profile.data"
      :total="profile.totalCnt"
      :title="profile.title"
      :busy="busy"
      @albumClick="onGetAlbumId"
      @load="onLoad"
    />
  </div>
</template>

<script>
  import AlbumContainer from '@/components/Album/content.vue'
  import { getProfileChangeAvatar } from '@/api/profile'
  import { getFace } from '@/api/face'

  export default {
    name: 'SelectAvatar',
    components: { AlbumContainer }, //album container
    props: {},
    data() {
      return {
        profile: {
          name: '',
          title: 'select avatar',
          totalCnt: 100,
          links: null,
          queryForm: {
            id: 30,
          },
          data: [],
        },
        // used in changeAvatar API
        changeAvatarParams: {
          face_id: 0,
        },
        getAvatarsParams: {
          profile: 30,
          page: 1,
          size: 20,
        },
      }
    },
    watch: {},
    mounted() {},
    methods: {
      handleClose(done) {
        console.log('SelectAvatar: handleClose', this.id, this.avatar_id, done) //this.id is the profile id
        if (this.loading === false) {
          this.dialog = false
          this.profile.data = []
          this.timer = setTimeout(() => {
            done()
            this.$emit('handleClose', this.avatar_id) //自定义事件  传递值“子向父组件传值”
          }, 400)
          return
        }
        this.onChangeAvatar()
        this.timer = setTimeout(() => {
          done()
          // 动画关闭需要一定的时间
          setTimeout(() => {
            this.loading = false
            this.$emit('handleClose', this.avatar_id) //自定义事件  传递值“子向父组件传值”
          }, 400)
        }, 2000)
      },
      cancelForm() {
        this.loading = false
        this.dialog = false
        clearTimeout(this.timer)
        this.$emit('cancelForm', this.dialog) //自定义事件  传递值“子向父组件传值”
      },

      submitForm() {
        this.loading = true
        this.$refs.drawer.closeDrawer()
      },

      onGetAlbumId(index, item) {
        console.log('SelectAvatar: onGetAlbumId', index, item)
        this.changeAvatarParams.face_id = item.id
      },
      onLoad() {
        console.log('SelectAvatar: onLoad')
        this.busy = true
        // deal with some logic that data is not enough
        if (this.links.next == null) {
          // no more data
          setTimeout(() => {
            this.busy = false
          }, 3000)
          return
        }
        this.getAvatarsParams.page++
        this.onGetAvatars()
      },
      // change the avatar
      async onGetAvatars() {
        console.log('onChangeAvatar: onChangeAvatar')
        this.busy = true
        await getFace(this.getAvatarsParams).then((response) => {
          console.log('getProfileChangeAvatar', response)
          const { data, totalCnt, links } = response
          this.profile.data = [...this.profile.data, ...data]
          this.profile.totalCnt = totalCnt
          this.links = links
          this.busy = false
        })
      },
      // change the avatar
      async onChangeAvatar() {
        console.log('onChangeAvatar: onChangeAvatar')
        await getProfileChangeAvatar(this.changeAvatarParams, this.id).then(
          (response) => {
            console.log('getProfileChangeAvatar', response)
            this.$message({
              message: '修改成功',
              type: 'success',
            })
          }
        )
      },
    },
  }
</script>
