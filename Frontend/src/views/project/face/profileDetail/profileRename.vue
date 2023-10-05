<template>
  <div class="reanme-container">
    <div class="edit-list" @click="onRenameReq">
      <span>人物命名</span>
      <span>{{ newName }}></span>
    </div>

    <el-dialog
      title="重命名"
      :visible.sync="dialogVisible"
      width="30%"
      :modal="false"
    >
      <el-form>
        <el-form-item label="姓名" label-width="120px">
          <el-input
            v-model="newName"
            autocomplete="off"
            placeholder="请输入新名字"
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="onConfirmRename">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  export default {
    name: 'Rename',
    components: {},
    props: {
      name: {
        type: String,
        default: '未命名', // model field name
        required: true,
      },
    },
    data() {
      return {
        dialogVisible: false,
        newName: '',
      }
    },
    watch: {
      name(newVal, oldVal) {
        console.log('Rename: watch name', newVal)
        this.newName = newVal
      },
    },
    mounted() {
      console.log('Rename: mounted', this.name)
      this.newName = this.name
    },

    methods: {
      onRenameReq() {
        this.dialogVisible = true
        console.log('Rename: onRenameReq')
        this.$emit('rename')
      },

      onConfirmRename(done) {
        console.log('Rename: handleConfirmName', this.newName)
        this.dialogVisible = false
        this.$emit('confirmRename', this.newName)
      },
    },
  }
</script>

<style>
  .edit-list {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    border-bottom: 1px solid #ebeef5;
    background-color: #f5f7fa;
  }
</style>
