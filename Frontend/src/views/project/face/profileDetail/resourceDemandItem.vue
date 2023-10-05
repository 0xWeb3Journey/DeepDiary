<template>
  <div>
    <el-card shadow="hover">
      <div slot="header" class="header">
        <span>{{ itemLocal.name }}</span>

        <Menu :menus="menus" class="menu-right" @command="handleCommand"></Menu>
      </div>
      <div class="text item">
        {{ itemLocal.desc }}
      </div>

      <el-carousel height="200px">
        <el-carousel-item v-for="img in itemLocal.images" :key="img.id">
          <el-image
            style="width: 100%"
            :src="img.thumb"
            fit="cover"
            :preview-src-list="srcList"
          ></el-image>
        </el-carousel-item>
      </el-carousel>
    </el-card>
  </div>
</template>

<script>
  import Menu from '@/components/Menu'
  export default {
    name: 'ResourceDemandItem',
    components: { Menu },
    props: {
      item: {
        type: Object,
        default: () => ({
          id: 1,
          name: '英语',
          desc: 'TEM8, 英语可以作为工作语言',
          images: [
            {
              id: 1,
              src: 'https://deep-diary.oss-accelerate.aliyuncs.com/media/user_info_img/%E5%9C%B0%E5%9B%BE%E6%98%BE%E7%A4%BA.png',
              thumb:
                'https://deep-diary.oss-accelerate.aliyuncs.com/media/CACHE/images/user_info_img/%E5%9C%B0%E5%9B%BE%E6%98%BE%E7%A4%BA/1ed8b21aca917ed0e325c8571f207821.jpg',
            },
            {
              id: 5,
              src: 'https://deep-diary.oss-accelerate.aliyuncs.com/media/user_info_img/deep-diary_cover.png',
              thumb:
                'https://deep-diary.oss-accelerate.aliyuncs.com/media/CACHE/images/user_info_img/deep-diary_cover/69e150672e13b78f12fc3edb4ed1c43c.jpg',
            },
          ],
        }),
        required: true,
      },
    },
    data() {
      return {
        itemLocal: this.item, // 用于存储 item 的本地副本
        srcList: [], // 用于存储所有图片的 src 的数组
        menus: [
          { icon: 'el-icon-circle-plus', text: 'Add' },
          { icon: 'el-icon-remove', text: 'Remove' },
          { icon: 'el-icon-edit', text: 'Edit' },
          {
            icon: 'el-icon-view',
            text: 'View',
          },
          {
            icon: 'el-icon-delete',
            text: 'Reset',
          },
          {
            icon: 'el-icon-upload',
            text: 'Upload',
          },
          {
            icon: 'el-icon-setting',
            text: 'Setting',
          },
        ],
      }
    },
    computed: {},

    watch: {
      item: {
        handler: function (newVal, oldVal) {
          console.log('ResourceDemandItem: item has been changed -- ')
          this.itemLocal = newVal
          console.log(this.itemLocal.images.length, '-------------------')
          // if this.srcList is empty, then set it to default value
          if (this.itemLocal.images.length === 0) {
            console.log('ResourceDemandItem: item.images is empty -- ')
            this.itemLocal.images = [
              {
                id: 1,
                src: 'https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png',
                thumb:
                  'https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png',
              },
            ]
            console.log(
              'ResourceDemandItem: this.itemLocal.images is -- ',
              this.itemLocal.images
            )
          }
          this.srcList = this.itemLocal.images.map((image) => image.src)
        },
        deep: true,
      },
    },
    created() {
      console.log('ResourceDemandItem: component has been created --')
    },
    mounted() {
      console.log('ResourceDemandItem: component has been mounted --')
      this.itemLocal = this.item
      // if this.srcList is empty, then set it to default value
      if (this.itemLocal.images.length === 0) {
        this.itemLocal.images = [
          {
            id: 1,
            src: 'https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png',
            thumb:
              'https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png',
          },
        ]
      }
      this.srcList = this.itemLocal.images.map((image) => image.src)
    },
    activated() {
      console.log('ResourceDemandItem: component has been activated --')
    },
    deactivated() {
      console.log('ResourceDemandItem: component has been deactivated -- ')
    },
    methods: {
      //进入守卫：通过路由规则，进入该组件时被调用
      beforeRouteEnter(to, from, next) {
        console.log(
          'ResourceDemandItem: component has been beforeRouteEnter -- '
        )
      },
      //离开守卫：通过路由规则，离开该组件时被调用
      beforeRouteLeave(to, from, next) {
        console.log(
          'ResourceDemandItem: component has been beforeRouteLeave -- '
        )
      },
      handleCommand(command) {
        this.$message('click on item ' + command)

        this.$emit('command', command) //自定义事件  传递值“子向父组件传值” command could be 'edit' or 'remove'
      },
    },
  }
</script>

<style>
  .text {
    font-size: 12px;
  }

  .header {
    display: flex;
    justify-content: space-between; /* 将内容向右对齐 */
  }
</style>
