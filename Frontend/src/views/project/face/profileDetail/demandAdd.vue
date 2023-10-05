<template>
  <div>
    <el-dialog title="Add Demand" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="Profile" :label-width="formLabelWidth">
          <el-select
            v-model="form.profile"
            filterable
            clearable
            placeholder="Please Choose a Person"
          >
            <el-option label="葛维冬" :value="1"></el-option>
            <el-option label="韩莉" :value="5"></el-option>
            <el-option label="葛丰炳" :value="33"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Title" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="Desc." :label-width="formLabelWidth">
          <el-input v-model="form.desc" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="onCancel">取 消</el-button>
        <el-button type="primary" @click="onConfirm">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import { addDemand } from '@/api/demand'
  export default {
    name: 'DemandAdd',
    components: {},
    props: {
      visible: {
        type: Boolean,
        default: false,
        required: true,
      },
    },
    data() {
      return {
        dialogFormVisible: false,
        form: {
          name: '',
          profile: '',
          desc: '',
        },
        formLabelWidth: '120px',
      }
    },
    computed: {},
    watch: {
      visible(newVal, oldVal) {
        console.log('demandAdd: watch visible', newVal)
        this.dialogFormVisible = newVal
      },
    },
    created() {
      console.log('demandAdd: component has been created --')
    },
    mounted() {
      console.log('demandAdd: component has been mounted --')
      this.dialogFormVisible = this.isVisible
    },
    activated() {
      console.log('demandAdd: component has been activated --')
    },
    deactivated() {
      console.log('demandAdd: component has been deactivated -- ')
    },
    methods: {
      //进入守卫：通过路由规则，进入该组件时被调用
      beforeRouteEnter(to, from, next) {
        console.log('demandAdd: component has been beforeRouteEnter -- ')
      },
      //离开守卫：通过路由规则，离开该组件时被调用
      beforeRouteLeave(to, from, next) {
        console.log('demandAdd: component has been beforeRouteLeave -- ')
      },

      onCancel() {
        console.log('demandAdd: onCancel')
        this.$emit('done', 'cancel')
      },
      onConfirm() {
        console.log('demandAdd: onConfirm', this.form)
        this.onAddDemand()
        this.$emit('done', 'confirm')
      },
      async onAddDemand() {
        // this.loading = true
        await addDemand(this.form).then((response) => {
          console.log('demandAdd: addDemand', response, response.id)
          // 后台更新返回后
          this.$message({
            message: `创建成功, name is ${response.name}, id is ${response.id}`,
            type: 'success',
          })
        })
      },
    },
  }
</script>

<style></style>
