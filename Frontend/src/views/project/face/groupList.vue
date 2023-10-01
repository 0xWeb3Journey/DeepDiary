<template>
  <div>
    <AlbumContainer
      :items="groups.data"
      :total="groups.totalCnt"
      :title="groups.title"
      :busy="groups.loading"
      :finished="groups.finished"
      @albumClick="onRouteJump"
      @load="onLoad"
    />
  </div>
</template>

<script>
  import AlbumContainer from '@/components/Album/content.vue'
  import { getGroup } from '@/api/category'
  export default {
    name: 'GroupList',
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
        groups: {
          title: 'Profile List',
          loading: false,
          finished: false,
          checkedId: -1,
          checkedIndex: -1,
          totalCnt: 0,
          links: null,
          curCnt: 0,
          data: [],
          groupQueryForm: {
            page: 1,
            size: 30,
            name: 'group',
          },
        },
      }
    },
    watch: {
      // query: {
      //   handler(newVal, oldVal) {
      //     console.log('GroupList: query', newVal)
      //     this.groups.groupQueryForm = newVal
      //     this.groups.data = []
      //     this.fetchGroup()
      //   },
      //   deep: true,
      // },
    },
    created() {},
    mounted() {
      this.groups.groupQueryForm.page = 1
      this.fetchGroup()
    },
    methods: {
      onRouteJump(index, item) {
        console.log('recieved the child component value %d,%o', index, item)
        // 声明这个函数，便于子组件调用
        this.groups.checkedIndex = index
        this.groups.checkedId = item.id || 0 // if return unexpected id, then set the id to default 1
        this.$router.push({
          // name: 'GroupDetail',
          name: 'GroupDetail',
          query: {
            id: item.id,
            title: item.name,
          },
        })
      },

      async fetchGroup() {
        console.log('GroupList: fetchGroup')
        this.groups.loading = true
        this.groups.finished = false
        await getGroup(this.groups.groupQueryForm).then((response) => {
          console.log('GroupList: ', response)
          const { data, totalCnt, links } = response
          this.groups.data = [...this.groups.data, ...data[0]['children']]
          this.groups.curCnt = this.groups.data.length
          // this.groups.totalCnt = totalCnt
          this.groups.totalCnt = this.groups.data.length
          this.groups.links = links
          if (this.groups.links.next === null) {
            // no more data
            this.groups.finished = true
          }
          this.$emit('groupData', this.groups.data)
          setTimeout(() => {
            this.groups.loading = false
          }, 300)
        })
      },

      onLoad() {
        console.log('GroupList: onLoad')
        this.groups.loading = true
        // deal with some logic that data is not enough
        if (this.groups.finished) {
          // no more data
          setTimeout(() => {
            this.groups.loading = false
          }, 3000)
          return
        }
        this.groups.groupQueryForm.page++
        this.fetchGroup()
      },
    },
  }
</script>

<style></style>
