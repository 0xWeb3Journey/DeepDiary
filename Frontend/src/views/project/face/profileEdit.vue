<template>
  <div class="edit-container">
    <h1>here is the ProfileEdit</h1>
    <el-drawer
      :title="title"
      :visible.sync="drawer"
      :with-header="true"
      :before-close="handleClose"
    >
      <!-- <el-col>
        <div class="edit-list" @click="onChooseAvatar">
          <el-avatar :size="50" :src="profileNew.avatar"></el-avatar>
          <span>选择封面></span>
        </div>
      </el-col> -->

      <EditAvatar
        :id="profileNew.id"
        :avatar="profileNew.avatar"
        @confirmAvatar="onConfirmAvatar"
      ></EditAvatar>
      <Rename :name="profileNew.name" @confirmRename="onConfirmRename"></Rename>

      <ProfileRelationTags
        :relation="profileNew.relation"
        @relationChoosed="onRelationChoosed"
      ></ProfileRelationTags>
      <div>
        <el-button
          class="dialog-footer"
          type="primary"
          :loading="loading"
          @click="onProcessEdit"
        >
          {{ loading ? '提交中 ...' : '确 定' }}
        </el-button>
      </div>
    </el-drawer>
  </div>
</template>

<script>
  import ProfileRelationTags from './profileRelationTags.vue'
  import Rename from './rename.vue'
  import EditAvatar from './editAvatar.vue'
  import { patchProfile } from '@/api/profile'
  export default {
    name: 'ProfileEdit',
    components: { ProfileRelationTags, Rename, EditAvatar },
    props: {
      title: {
        type: String,
        default: '人脸详情', // model field name
        required: true,
      },

      edit: {
        type: Boolean,
        default: false, // model field name
        required: true,
      },
      profile: {
        type: Object,
        default: null,
        required: true,
      },
    },
    data() {
      return {
        drawer: false,
        loading: false, //used for the stat of changing the name
        dialogVisible: false,
        isHaveTag: true,
        newRelation: '',
        profileNew: {
          avatar:
            'https://cube.elemecdn.com/6/7b/03f0a0a0b0e2f6b5b6b5e2f0a0e0b0a0.jpeg',
          name: 'DeepDiary',
          relation: '',
        },
        fetchParams: {
          id: 0,
          name: '',
          // relation: '',
        },
      }
    },
    watch: {
      edit(newVal, oldVal) {
        this.drawer = newVal
        if (newVal) {
          console.log('ProfileEdit: watch edit changed', newVal)
        }
      },
      profile(newVal, oldVal) {
        this.profileNew = newVal

        console.log('ProfileEdit: watch profile changed', newVal)
      },
    },
    mounted() {
      this.profileNew = this.profile
      console.log('ProfileEdit: mounted', this.profile, this.profileNew)
    },

    methods: {
      onCancel() {
        console.log('ProfileEdit: onCancel')
        this.$emit('cancel')
      },
      onConfirm() {
        console.log('ProfileEdit: onConfirm')
        this.$emit('confirm')
      },
      handleClose(done) {
        console.log('ProfileEdit: handleClose')
        done()
        this.$emit('close')
      },
      onChooseAvatar() {
        console.log('ProfileEdit: onChooseAvatar')
        this.$emit('chooseAvatar')
      },

      onConfirmAvatar(faceItem) {
        console.log('ProfileEdit: onConfirmAvatar', faceItem)
        this.profileNew.avatar = faceItem.thumb
        this.fetchParams.id = faceItem.id
      },

      onConfirmRename(newName) {
        console.log(
          `ProfileEdit: handleConfirmName, new name: ${newName}, old name: ${this.profile.name}`
        )
        // this.profileNew.name = newName
        this.fetchParams.name = newName
      },
      onRelationChoosed(tag) {
        this.newRelation = tag
        this.isHaveTag = true
        console.log(
          'ProfileEdit: onRelationChoosed, newRelation ',
          this.newRelation
        )
        // this.fetchParams.relation = this.newRelation
      },
      async onProcessEdit() {
        console.log(
          'ProfileEdit: onProcessEdit',
          `新名称：${this.fetchParams.name}, 老名称为:${this.profile.name}`
        )
        // 如果fetchParams.mame==='', 则直接返回
        // 如果名字未做更改，也直接返回
        // if (
        //   this.fetchParams.name === '' ||
        //   this.fetchParams.name === this.profile.name
        // ) {
        //   this.$message({
        //     message: `名称未做更改, 新名称：${this.fetchParams.name}, 老名称为:${this.profile.name}`,
        //     type: 'warning',
        //   })
        //   return
        // }
        this.loading = true
        await patchProfile(this.fetchParams, this.profile.id).then(
          (response) => {
            console.log('ProfileEdit: patchProfile', response)
            // 后台更新返回后
            this.loading = false
            this.fetchParams.name = '' // 修改成功后，新名称重新置为空
            this.$emit('close')
            this.$message({
              message: `修改成功，修改后的名称是：${response.data.name}`,
              type: 'success',
            })
          }
        )
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
