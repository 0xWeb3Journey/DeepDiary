<template>
  <div>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>{{ item.name }}</span>

        <el-dropdown
          style="float: right; padding: 3px 0"
          icon="el-icon-delete"
          @command="handleCommand"
        >
          <span class="el-dropdown-link">
            <i class="el-icon-menu el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="edit">
              <i class="el-icon-edit"></i>
              Edit
            </el-dropdown-item>
            <el-dropdown-item command="view">
              <i class="el-icon-view"></i>
              View
            </el-dropdown-item>
            <el-dropdown-item command="setting">
              <i class="el-icon-setting"></i>
              Setting
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
      <div class="text item">
        {{ item.desc }}
      </div>

      <!-- item.length > 0
                ? img.thumb
                : 'https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png' -->
      <el-carousel height="150px">
        <el-carousel-item v-for="img in item.images" :key="img.id">
          <el-image
            style="width: 400px; height: 248px"
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
  export default {
    name: 'ResourceDemandItem',
    components: {},
    props: {
      item: {
        type: Object,
        default: {
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
        },
        required: true,
      },
    },
    data() {
      return {
        srcList: [], // 用于存储所有图片的 src 的数组
      }
    },
    computed: {},
    watch: {
      item: {
        handler: function (val, oldVal) {
          console.log('ResourceDemandItem: item has been changed -- ')
          // if this.srcList is empty, then set it to default value
          if (this.item.images.length === 0) {
            console.log('ResourceDemandItem: item.images is empty -- ')
            this.item.images = [
              {
                id: 1,
                src: 'https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png',
                thumb:
                  'https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png',
              },
            ]
          }
          this.srcList = this.item.images.map((image) => image.src)
        },
        deep: true,
      },
    },
    created() {
      console.log('ResourceDemandItem: component has been created --')
    },
    mounted() {
      console.log('ResourceDemandItem: component has been mounted --')
      // 创建 srcList，收集所有图片的 src
      //   if this.srcList is empty, then set it to default value
      if (this.item.images.length === 0) {
        console.log('ResourceDemandItem: item.images is empty -- ')
        this.item.images = [
          {
            id: 1,
            src: 'https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png',
            thumb:
              'https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png',
          },
        ]
      }

      this.srcList = this.item.images.map((image) => image.src)
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

        this.$emit(command) //自定义事件  传递值“子向父组件传值” command could be 'edit' or 'remove'
      },
    },
  }
</script>

<style>
  .text {
    font-size: 14px;
  }

  .item {
    height: 50px;
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: '';
  }
  .clearfix:after {
    clear: both;
  }

  .box-card {
    width: 400px;
  }
</style>
