<template>
  <div>
    <!-- <ProfileList></ProfileList> -->
    <GroupList></GroupList>
    <!-- <SelectAvatar
      :id="profiles.checkedId"
      :is-disp="isDisp"
      @handleClose="handleClose"
      @cancelForm="cancelForm"
    ></SelectAvatar>
    <el-collapse v-model="activeName" accordion>
      <el-collapse-item title="已命名 Named" name="1">
        <Album
          v-if="activeName == 1"
          ref="named"
          title="已命名"
          :items="$store.state.face.isGroupMode ? groups.data : profiles.data"
          :total="profiles.totalCnt"
          @albumClick="onGetAlbumId"
          @doubleClick="onRouteJump"
          @changeAvatar="onChangeAvatar"
        ></Album>
      </el-collapse-item>
      <el-collapse-item title="未命名 Unnamed" name="2">
        <div
          v-infinite-scroll="loadMore"
          infinite-scroll-disabled="busy"
          infinite-scroll-distance="50"
          infinite-scroll-immediate-check="true"
          class="content"
        >
          <Album
            v-if="activeName == 2"
            ref="unamed"
            title="未命名"
            :items="faces.data"
            :total="faces.totalCnt"
            @albumClick="onGetAlbumId"
            @doubleClick="onRouteJump"
            @changeName="onChangeFaceName"
            @load="onLoad"
          ></Album>
        </div>
        <div v-show="faces.busy" class="loading">{{ msg }}</div>
      </el-collapse-item>
    </el-collapse> -->
  </div>
</template>

<script>
  import ProfileList from './profileList.vue'
  import GroupList from './groupList.vue'
  import Album from '@/components/Album'
  import SelectAvatar from '@/components/SelectAvatar'
  import Profile from './profile.vue'
  import infiniteScroll from 'vue-infinite-scroll'
  import { getProfile, getGroup } from '@/api/gallery'
  import { getFace, changeFaceName } from '@/api/face'
  export default {
    name: 'Face',
    components: { GroupList },
    // components: { ProfileList, GroupList, Album, SelectAvatar },
    directives: { infiniteScroll },
    data: function () {
      return {
        activeName: '1',
        profiles: {
          busy: false,
          loading: false,
          checkedId: -1,
          checkedIndex: -1,
          totalCnt: 0,
          curCnt: 0,
          data: [],
          profileQueryForm: {
            page: 1,
            size: 30,
            search: '',
            // faceAlumId: 1,
            faces__id__gte: 0,
          },
        },
        groups: {
          busy: false,
          loading: false,
          checkedId: -1,
          checkedIndex: -1,
          totalCnt: 0,
          curCnt: 0,
          data: [],
          groupQueryForm: {
            page: 1,
            size: 20,
            name: 'group',
          },
        },
        faces: {
          busy: false,
          loading: false,
          checkedId: -1,
          checkedIndex: -1,
          totalCnt: 0,
          curCnt: 0,
          data: [],
          faceQueryForm: {
            page: 1,
            size: 25,
            profile__isnull: true,
            // profile: 30,
            det_score__gt: 0.8,
            // det_score__lt: 0.6,
            // face_score__gt: 0.8,
            // face_score__lt: 0.6,
            // age__gt: 35,
            // age__lt: 35,
            // gender: 0,
          },
          changeNameForm: {
            id: 0,
            name: '',
          },
        },
        // albumLoading: false,
        // faceLoading: false,
        // totalCnt: 0,
        // curAlbumCnt: 0,
        // checkedIndex: -1,
        // checkedId: -1,
        // checkedProfile: 0,
        msg: 'Loading.....',
        isDisp: false, // used to open the drawer
      }
    },
    watch: {
      '$store.state.face.isGroupMode'(newVal, oldVal) {
        console.log('$store.state.face.isGroupMode', newVal)
      },
    },
    created() {},
    mounted() {
      console.log(
        'this.$store.state.face.isGroupMode: ',
        this.$store.state.face.isGroupMode
      )
      this.fetchProfile()
      this.fetchGroup()
      this.fetchFace()
    },
    methods: {
      loadMore: function () {
        console.log('infinite loading... ', this.faces.busy)
        this.faces.busy = true
        setTimeout(() => {
          console.log('timing is out... ')
          // // 当前页数如果小于总页数，则继续请求数据，如果大于总页数，则滚动加载停止
          // if (this.currentCnt < this.totalCnt || this.totalCnt === 0) {
          //   //  这里是列表请求数据的接口,在这个接口中更新总页数
          //   this.msg = 'Loading.....'
          this.fetchFace()
          // } else {
          //   this.msg = 'there is no more img any more'
          // }
          this.faces.busy = false
        }, 1000)
      },
      onGetAlbumId(index, item) {
        console.log('recieved the child component value %d,%o', index, item)
        console.log(
          'this.persons[index].profile',
          this.profiles.data[index].profile
        )
        // 声明这个函数，便于子组件调用
        this.profiles.checkedIndex = index
        this.profiles.checkedId = item.id || 0 // if return unexpected id, then set the id to default 1
        // if (this.profiles.data[index] !== null)
        //   this.profiles.data[index].checkedProfile = this.profiles.data[index].profile
        // else {
        //   this.profiles.checkedProfile = 0
        // }
      },
      onRouteJump(index, item) {
        console.log('album double click event item is  %d,%o', index, item)
        this.$router.push({
          // name: 'GroupDetail',
          name: this.$store.state.face.isGroupMode
            ? 'GroupDetail'
            : 'ProfileDetail',
          query: {
            id: item.id,
            title: item.name,
          },
        })
      },

      async fetchProfile() {
        if (this.profiles.loading) return //incase fetch more data during the fetching time

        this.profiles.loading = true
        if (
          this.profiles.curAlbumCnt < this.profiles.totalCnt ||
          this.profiles.totalCnt === 0
        ) {
          console.log('start to get the album...')
          const { data, totalCnt } = await getProfile(
            this.profiles.profileQueryForm
          )
          if (totalCnt === 0) return //could fetch any data
          // this.profileQueryForm.page += 1
          console.log(
            'get fetchProfile result, data is %o, total is %d',
            data,
            totalCnt,
            this.$store.state.face.isGroupMode
          )
          this.profiles.data = [...this.profiles.data, ...data]
          this.profiles.curAlbumCnt = this.profiles.data.length
          this.profiles.totalCnt = totalCnt
          setTimeout(() => {
            this.profiles.albumLoading = false
          }, 300)
        }
      },
      async fetchGroup() {
        const { data, totalCnt } = await getGroup(this.groups.groupQueryForm)

        this.groups.data = data[0]['children']
        this.groups.curAlbumCnt = this.groups.data.length
        this.groups.totalCnt = totalCnt
        console.log(
          'get fetchGroup result, data is %o, total is %d',
          this.groups.groups,
          this.groups.totalCnt,
          this.$store.state.face.isGroupMode
        )
      },

      async fetchFace() {
        if (this.faces.loading) return //incase fetch more data during the fetching time

        this.faces.loading = true
        console.log(
          'start to judge the loading situation...',
          this.faces.curCnt,
          this.faces.totalCnt
        )
        if (
          this.faces.curCnt < this.faces.totalCnt ||
          this.faces.totalCnt === 0
        ) {
          console.log('start to get the album...')
          this.msg = 'Loading.....'
          const { data, totalCnt } = await getFace(this.faces.faceQueryForm)
          if (totalCnt === 0) return //could fetch any data
          this.faces.faceQueryForm.page += 1
          console.log(
            'get fetchface result, data is %o, total is %d',
            data,
            totalCnt
          )
          this.faces.data = [...this.faces.data, ...data]
          this.faces.curCnt = this.faces.data.length
          this.faces.totalCnt = totalCnt
          setTimeout(() => {
            this.faces.loading = false
          }, 500)
        } else {
          this.msg = 'there is no more img any more'
        }
      },

      // async changeFaceAlbumName(value, album) {
      //   console.log(value, this.albumName)
      //   // this.items[index].name = value
      //   if (value !== this.albumName) {
      //     this.postData.id = album.id //人脸相册id
      //     this.postData.name = value

      //     const { data, msg } = await changeFaceAlbumName(this.postData)
      //     console.log(data, msg)
      //     this.$message({
      //       message: `Success changed ${this.albumName} to ${value}`,
      //       type: 'success',
      //     })

      //     this.albumName = value
      //   }
      // },

      async onChangeFaceName(name, item) {
        console.log('onChangeFaceName', name, item)
        // this.items[index].name = value
        if (name !== null) {
          this.faces.changeNameForm.id = item.id
          this.faces.changeNameForm.name = name

          const { data, msg } = await changeFaceName(this.faces.changeNameForm)
          console.log(data, msg)
          this.$message({
            message: `Success changed ${name}`,
            type: 'success',
          })

          // this.albumName = value
        }
      },
      onLoad() {
        console.log('onLoad')
      },

      onChangeAvatar(id) {
        console.log('Face-->index: onChangeAvatar', this.profiles.checkedId, id)
        this.isDisp = true
      },
      handleClose(val) {
        console.log('Face-->index: handleClose', val)
        this.isDisp = false
      },
      cancelForm(val) {
        console.log('Face-->index: cancelForm', val)
        this.isDisp = val
      },
    },
  }
</script>

<style></style>
