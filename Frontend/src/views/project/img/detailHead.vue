<template>
  <div class="header-container">
    <!-- el-page-header 需要居左，el-dropdown需要居右 -->
    <el-page-header :content="content" @back="goBack"></el-page-header>
    <!-- <el-dropdown @command="handleCommand">
      <span class="el-dropdown-link">
        菜单
        <i class="el-icon-arrow-down el-icon--right"></i>
      </span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item command="edit">人物信息编辑</el-dropdown-item>
        <el-dropdown-item command="remove">移除该人物</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown> -->
  </div>
</template>

<script>
  export default {
    name: 'DetailHead',
    components: {},
    props: {
      content: {
        type: String,
        default: '人脸详情', // model field name
        required: true,
      },
    },
    methods: {
      goBack() {
        console.log('go back')
        this.$router.go(-1)
      },
      handleCommand(command) {
        this.$message('click on item ' + command)
        this.$emit(command) //自定义事件  传递值“子向父组件传值” command could be 'edit' or 'remove'
      },
    },
  }
</script>

<style>
  .el-dropdown-link {
    cursor: pointer;
    color: #409eff;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
  .header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    border-bottom: 1px solid #ebeef5;
    background-color: #f5f7fa;
  }

  .el-page-header {
    margin: 0; /* Override default margin */
  }

  .el-dropdown {
    margin: 0; /* Override default margin */
  }

  .el-page-header {
    /* font-size: 40px; */
    line-height: 20px;
    /* color: rgb(132, 21, 235); */
  }
  .el-page-header__content {
    font-size: 14px; /* 设置合适的字体大小 */
    line-height: 20px;
    /* color: white; */
  }
</style>
