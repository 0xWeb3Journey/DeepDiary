<template>
  <div>
    <el-row :gutter="12" type="flex" class="row-bg" justify="space-around">
      <el-col
        v-for="item in items"
        :key="item.id"
        :xs="24"
        :sm="12"
        :md="12"
        :lg="8"
        :xl="6"
      >
        <experienceItem :item="item"></experienceItem>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import ExperienceItem from './experienceItem.vue'
  export default {
    name: 'Experience',
    components: { ExperienceItem },
    props: {
      items: {
        type: Array,
        default: () => [
          {
            id: 1,
            company: '宁波福尔达智能科技股份有限公司',
            company_PyInitial: 'nbfedznkjgfyxgs',
            position: '项目经理',
            start_date: '2021-10-08',
            end_date: '2023-09-27',
            name: 'SE336出风口',
            desc: '内叶片自动关风为导向传统出风口,出口安通林与HBPO终端客户为西班牙西亚特',
            duty: '1.全面主持项目日常管理工作，按照计划组织日常工作，同时进行全面管理及过程监督， \t\t保证进度，质量，控成本完成项目 \t2.参加设计评审会议，模具工装等评审会议，主持日常技术交流会议 \t3.基于公司经营项目制定的目标预算，利用产线合并，降低费用支出，严控预算使用风险 4.跟踪把控产品质量，外购标准件采购进度等，有效实施过程质量监控 5．根据进度节点制定上报计划及设置进度提醒机制，审核工、模、检等进度计划，对各个模块定期检查、分析进度完成情况',
            achievement:
              '1. 通过TR交流赢得客户认可，促进项目定点；2. 按时完成客户要求的节点并按时完成第一次产品交样',
            profile: 5,
          },
          {
            id: 2,
            company: '宁波一彬电子科技股份有限公司',
            company_PyInitial: 'nbybdzkjgfyxgs',
            position: '项目经理',
            start_date: '2018-03-03',
            end_date: '2021-10-03',
            name: 'P519机舱件',
            desc: '沃尔沃SPA2平台上开发的新能源车型，用机舱内的塑料件',
            duty: '1. 跟踪项目进度，主动设置进度提醒事项，提前掌握、沟通项目进度要求，保证项目进 \t\t度提醒及时准确 2. 根据公司目标，市场情况及资源情况，制定项目计划，统筹项目预算成本，人员，时间以及风险要素，按照计划推进项目执行 3. 对项目过程中问题风险分析，沟通项目内外人员商定解决对策并落地执行，及时发现问题避免损失 4.负责与客户需求对接及后续变更跟进，从提出、分析、实施三个方面闭环跟踪',
            achievement: '项目顺利量产',
            profile: 5,
          },
          {
            id: 3,
            company: '宁波一彬电子科技股份有限公司',
            company_PyInitial: 'nbybdzkjgfyxgs',
            position: '项目经理',
            start_date: '2018-03-03',
            end_date: '2021-10-03',
            name: 'P519机舱件',
            desc: '沃尔沃SPA2平台上开发的新能源车型，用机舱内的塑料件',
            duty: '1. 跟踪项目进度，主动设置进度提醒事项，提前掌握、沟通项目进度要求，保证项目进 \t\t度提醒及时准确 2. 根据公司目标，市场情况及资源情况，制定项目计划，统筹项目预算成本，人员，时间以及风险要素，按照计划推进项目执行 3. 对项目过程中问题风险分析，沟通项目内外人员商定解决对策并落地执行，及时发现问题避免损失 4.负责与客户需求对接及后续变更跟进，从提出、分析、实施三个方面闭环跟踪',
            achievement: '项目顺利量产',
            profile: 5,
          },
        ],
        required: false,
      },
    },
    data() {
      return {}
    },
    computed: {},
    watch: {
      items(newVal, oldVal) {
        console.log('Experience: items have bee changed: ', newVal)
      },
    },
    created() {
      console.log('Experience: component has been created --')
    },
    mounted() {
      console.log('Experience: component has been mounted --')
    },
    activated() {
      console.log('Experience: component has been activated --')
    },
    deactivated() {
      console.log('Experience: component has been deactivated -- ')
    },
    methods: {
      //进入守卫：通过路由规则，进入该组件时被调用
      beforeRouteEnter(to, from, next) {
        console.log('Experience: component has been beforeRouteEnter -- ')
      },
      //离开守卫：通过路由规则，离开该组件时被调用
      beforeRouteLeave(to, from, next) {
        console.log('Experience: component has been beforeRouteLeave -- ')
      },
    },
  }
</script>

<style></style>
