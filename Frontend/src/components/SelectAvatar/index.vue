<template>
  <div class="select-avatar-container">
    <el-drawer
      ref="drawer"
      title="请选择相册封面"
      :before-close="handleClose"
      :visible.sync="dialog"
      direction="rtl"
      custom-class="demo-drawer"
    >
      <div class="demo-drawer__content">
        <AlbumContainer
          :items="profile.data"
          :total="profile.totalCnt"
          :title="profile.title"
          :busy="busy"
          @albumClick="onGetAlbumId"
          @load="onLoad"
        />

        <div class="demo-drawer__footer">
          <el-button @click="cancelForm">取 消</el-button>
          <el-button type="primary" :loading="loading" @click="submitForm">
            {{ loading ? '提交中 ...' : '确 定' }}
          </el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
  import AlbumContainer from '@/components/Album/content.vue'
  import { getProfileChangeAvatar } from '@/api/profile'
  import { getFace } from '@/api/face'

  export default {
    name: 'SelectAvatar',
    components: { AlbumContainer }, //album container
    props: {
      isDisp: {
        type: Boolean,
        default: false, // model field name
        required: true,
      },
      id: {
        type: Number,
        default: 30,
        required: true,
      },
    },
    data() {
      return {
        dialog: false,
        loading: false, //used for the stat of changing the name
        busy: true, //used for the stat of loading more faces
        timer: null,

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
    watch: {
      isDisp(newVal, oldVal) {
        this.dialog = newVal
        if (newVal) {
          this.getAvatarsParams.page = 1
          this.onGetAvatars()
        }
      },
      id(newVal, oldVal) {
        console.log('SelectAvatar: watch id changed', newVal)
        this.getAvatarsParams.profile = newVal
      },
    },
    mounted() {
      // mounted first, then the id will be clicked, so those code is not working
      //   console.log('SelectAvatar: mounted', this.id)
      //   this.getAvatarsParams.profile = this.id
    },
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
      // get the avatars
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
