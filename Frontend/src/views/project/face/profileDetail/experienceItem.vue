<template>
  <div>
    <el-card shadow="hover">
      <div slot="header" class="clearfix">
        <span>{{ itemLocal.name }}</span>

        <Menu :menus="menus" @command="handleCommand"></Menu>
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
    name: 'ExperienceItem',
    components: { Menu },
    props: {
      item: {
        type: Object,
        default: () => ({
          id: 1,
          company: '宁波福尔达智能科技股份有限公司',
          company_PyInitial: 'nbfedznkjgfyxgs',
          images: [
            {
              id: 6,
              src: 'https://deep-diary.oss-accelerate.aliyuncs.com/media/user_info_img/avatar.jpg',
              thumb:
                'https://deep-diary.oss-accelerate.aliyuncs.com/media/CACHE/images/user_info_img/avatar/d5e22908141f1dca9b7144e4d08c25d8.jpg',
            },
            {
              id: 7,
              src: 'https://deep-diary.oss-accelerate.aliyuncs.com/media/user_info_img/IMG_20210909_194805.jpg',
              thumb:
                'https://deep-diary.oss-accelerate.aliyuncs.com/media/CACHE/images/user_info_img/IMG_20210909_194805/409854c23b91bb02ca91b98ff4114721.jpg',
            },
          ],
          position: '项目经理',
          start_date: '2021-10-08',
          end_date: '2023-09-27',
          name: 'SE336出风口',
          desc: '内叶片自动关风为导向传统出风口,出口安通林与HBPO终端客户为西班牙西亚特',
          duty: '1.全面主持项目日常管理工作，按照计划组织日常工作，同时进行全面管理及过程监督， \t\t保证进度，质量，控成本完成项目 \t2.参加设计评审会议，模具工装等评审会议，主持日常技术交流会议 \t3.基于公司经营项目制定的目标预算，利用产线合并，降低费用支出，严控预算使用风险 4.跟踪把控产品质量，外购标准件采购进度等，有效实施过程质量监控 5．根据进度节点制定上报计划及设置进度提醒机制，审核工、模、检等进度计划，对各个模块定期检查、分析进度完成情况',
          achievement:
            '1. 通过TR交流赢得客户认可，促进项目定点；2. 按时完成客户要求的节点并按时完成第一次产品交样',
        }),
        required: true,
      },
    },
    data() {
      return {
        itemLocal: this.item,
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
          console.log('ExperienceItem: item has been changed -- ')
          this.itemLocal = newVal
          if (this.itemLocal.images.length === 0) {
            console.log('ExperienceItem: item.images is empty -- ')
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
        deep: true,
      },
    },

    created() {
      console.log('ExperienceItem: component has been created --')
    },
    mounted() {
      console.log('ExperienceItem: component has been mounted --')
      // 创建 srcList，收集所有图片的 src
      //   if this.srcList is empty, then set it to default value
      console.log('ExperienceItem: item = ', this.item)
      // if (this.item.images.length === 0) {
      //   console.log('ExperienceItem: item.images is empty -- ')
      // this.item.images = [
      //   {
      //     id: 1,
      //     src: 'https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png',
      //     thumb:
      //       'https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png',
      //   },
      // ]
      // }

      // this.srcList = this.item.images.map((image) => image.src)
    },
    activated() {
      console.log('ExperienceItem: component has been activated --')
    },
    deactivated() {
      console.log('ExperienceItem: component has been deactivated -- ')
    },
    methods: {
      //进入守卫：通过路由规则，进入该组件时被调用
      beforeRouteEnter(to, from, next) {
        console.log('ExperienceItem: component has been beforeRouteEnter -- ')
      },
      //离开守卫：通过路由规则，离开该组件时被调用
      beforeRouteLeave(to, from, next) {
        console.log('ExperienceItem: component has been beforeRouteLeave -- ')
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
</style>
