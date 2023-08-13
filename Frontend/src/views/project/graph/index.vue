<template>
  <div class="interactiveGraph-container">
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="GraphNavigator" name="navigator">
        <!-- 使用v-if会报错，只有第一个组件正常显示，后面的组件都无法正常显示 -->
        <GraphNavigator v-if="activeName === 'navigator'"></GraphNavigator>
      </el-tab-pane>
      <el-tab-pane label="GraphExplorer" name="explorer">
        <GraphExplorer v-if="activeName === 'explorer'"></GraphExplorer>
      </el-tab-pane>
      <el-tab-pane label="RelFinder" name="finder">
        <RelFinder v-if="activeName === 'finder'"></RelFinder>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
  import GraphNavigator from './navigator.vue'
  import GraphExplorer from './explorer.vue'
  import RelFinder from './finder.vue'
  export default {
    name: 'Graph',
    components: { GraphNavigator, GraphExplorer, RelFinder },
    props: {},
    data() {
      return {
        activeName: 'navigator',
      }
    },
    computed: {},
    watch: {},
    created() {},
    mounted() {},

    methods: {
      handleClick(tab, event) {
        console.log(tab, event)
      },
    },
  }
</script>

<style lang="css" scoped></style>
