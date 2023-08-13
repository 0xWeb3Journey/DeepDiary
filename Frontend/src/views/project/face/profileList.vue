<template>
  <div>
    <AlbumContainer
      :items="profiles.data"
      :total="profiles.totalCnt"
      :title="profiles.title"
      :busy="profiles.loading"
      @albumClick="onRouteJump"
      @load="onLoad"
    />
  </div>
</template>

<script>
  import AlbumContainer from '@/components/Album/content.vue'
  import { getProfile } from '@/api/profile'
  export default {
    name: 'ProfileList',
    components: { AlbumContainer },
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
        profiles: {
          title: 'Profile List',
          loading: false,
          checkedId: -1,
          checkedIndex: -1,
          totalCnt: 0,
          links: null,
          curCnt: 0,
          data: [],
          profileQueryForm: {
            page: 1,
            size: 30,
          },
        },
      }
    },
    watch: {
      // query: {
      //   handler(newVal, oldVal) {
      //     console.log('ProfileList: query', newVal)
      //     this.profiles.profileQueryForm = newVal
      //     this.profiles.data = []
      //     this.fetchProfile()
      //   },
      //   deep: true,
      // },
    },
    created() {},
    mounted() {
      this.profiles.profileQueryForm.page = 1
      this.fetchProfile()
    },
    methods: {
      onRouteJump(index, item) {
        console.log('recieved the child component value %d,%o', index, item)
        // 声明这个函数，便于子组件调用
        this.profiles.checkedIndex = index
        this.profiles.checkedId = item.id || 0 // if return unexpected id, then set the id to default 1
        this.$router.push({
          // name: 'GroupDetail',
          name: 'ProfileDetail',
          query: {
            id: item.id,
            title: item.name,
          },
        })
      },

      async fetchProfile() {
        console.log('ProfileList: fetchProfile')
        this.profiles.loading = true
        await getProfile(this.profiles.profileQueryForm).then((response) => {
          console.log('getProfileChangeAvatar', response)
          const { data, totalCnt, links } = response
          this.profiles.data = [...this.profiles.data, ...data]
          this.profiles.curCnt = this.profiles.data.length
          this.profiles.totalCnt = totalCnt
          this.profiles.links = links
          this.$emit('profileData', this.profiles.data)
          setTimeout(() => {
            this.profiles.loading = false
          }, 300)
        })
      },

      onLoad() {
        console.log('ProfileList: onLoad')
        this.profiles.loading = true
        // deal with some logic that data is not enough
        if (this.profiles.links.next == null) {
          // no more data
          setTimeout(() => {
            this.profiles.loading = false
          }, 3000)
          return
        }
        this.profiles.profileQueryForm.page++
        this.fetchProfile()
      },
    },
  }
</script>

<style></style>
