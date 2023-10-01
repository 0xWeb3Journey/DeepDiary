<template>
  <div>
    <ProfileSearch
      v-if="searchable"
      @handleProfileSearch="onProfileSearch"
    ></ProfileSearch>
    <Transfer :profiles="profiles.data"></Transfer>

    <AlbumContainer
      :items="profiles.data"
      :total="profiles.totalCnt"
      :title="profiles.title"
      :busy="profiles.loading"
      :finished="profiles.finished"
      @albumClick="onRouteJump"
      @load="onLoad"
    />
  </div>
</template>

<script>
  import AlbumContainer from '@/components/Album/content.vue'
  import { getProfile } from '@/api/profile'
  import ProfileSearch from '@/components/Search/profile'
  import Transfer from './transfer.vue'
  export default {
    name: 'Relation',
    components: { AlbumContainer, ProfileSearch, Transfer },
    directives: {},
    props: {},
    data() {
      return {
        profiles: {
          title: 'Profile List',
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
            size: 30,
          },
        },
        searchable: true,
      }
    },
    watch: {},
    created() {
      console.log('Relation: created')
    },
    mounted() {
      console.log('Relation: mounted')
      this.profiles.queryForm.page = 1
      this.fetchProfile()
    },
    activated() {
      console.log('Relation: activated')
    },
    deactivated() {
      console.log('Relation: deactivated')
    },
    methods: {
      async fetchProfile() {
        console.log('ProfileList: fetchProfile')
        this.profiles.loading = true
        this.profiles.finished = false
        await getProfile(this.profiles.queryForm).then((response) => {
          console.log('getProfileChangeAvatar', response)
          const { data, totalCnt, links } = response
          this.profiles.data = [...this.profiles.data, ...data]
          this.profiles.curCnt = this.profiles.data.length
          this.profiles.totalCnt = totalCnt
          this.profiles.links = links
          if (this.profiles.links.next === null) {
            // no more data
            this.profiles.finished = true
          }
          this.$emit('profileData', this.profiles.data)
        })
        // move to the outside, incase of no response
        setTimeout(() => {
          this.profiles.loading = false
        }, 300)
      },
      onRouteJump(index, item) {
        console.log('recieved the child component value %d,%o', index, item)
      },

      onLoad() {
        console.log('ProfileList: onLoad')
        this.profiles.loading = true
        // deal with some logic that data is not enough
        if (this.profiles.finished) {
          // no more data
          setTimeout(() => {
            this.profiles.loading = false
          }, 3000)
          return
        }
        this.profiles.queryForm.page++
        this.fetchProfile()
      },

      onProfileSearch(queryForm) {
        console.log('recieve the queryForm info from the search component')
        console.log(queryForm)
        this.profiles.queryForm = queryForm
        this.profiles.totalCnt = 0
        this.profiles.data = []
        this.fetchProfile()
        // this.loadMore()
      },
    },
  }
</script>

<style></style>
