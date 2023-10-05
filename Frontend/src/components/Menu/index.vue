<template>
  <div class="menu-container">
    <el-dropdown @command="handleCommand">
      <span class="el-dropdown-link">
        <i class="el-icon-menu el-icon--right"></i>
      </span>
      <!-- 其中command 需要将item.text转换成小写即可 -->
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item
          v-for="item in menus"
          :key="item.text"
          :command="item.text.toLowerCase()"
        >
          <i :class="item.icon"></i>
          {{ item.text }}
        </el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>

<script>
  export default {
    name: 'Menu',
    components: {},
    props: {
      menus: {
        type: Array,
        default: () => [
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
        required: false,
      },
    },
    data() {
      return {}
    },
    watch: {},
    created() {},
    mounted() {},
    methods: {
      handleCommand(command) {
        this.$message('click on item ' + command)
        this.$emit('command', command) //自定义事件  传递值“子向父组件传值” command could be 'edit' or 'remove'
      },
    },
  }
</script>

<style lang="css" scoped></style>
