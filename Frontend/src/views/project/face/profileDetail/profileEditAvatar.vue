<template>
  <div class="reanme-container">
    <div class="edit-list" @click="onChangeAvatarReq">
      <img class="user-avatar" :src="avatar" alt="" />
      <!-- <el-avatar :size="60" :src="newAvatar" fit="fill"></el-avatar> -->
      <span>选择封面></span>
    </div>

    <el-dialog
      title="选择封面"
      :visible.sync="dialogVisible"
      width="30%"
      :modal="false"
    >
      <FaceList
        v-if="isMounted"
        :id="FaceQueryForm.profile"
        @choosed="onChoosed"
      ></FaceList>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="onConfirmAvatar">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  import FaceList from '../faceList.vue'
  export default {
    name: 'EditAvatar',
    components: { FaceList },
    props: {
      avatar: {
        type: String,
        default: '未命名', // model field name
        required: true,
      },
      id: {
        type: Number,
        default: 0,
        required: true,
      },
    },
    data() {
      return {
        dialogVisible: false,
        isMounted: false,
        choosedFace: null,
        newAvatar: '',
        FaceQueryForm: {
          page: 1,
          size: 20,
          // profile__isnull: true,
          profile: 1,
          det_score__gt: 0.7,
          // det_score__lt: 0.6,
          // face_score__gt: 0.8,
          // face_score__lt: 0.6,
          // age__gt: 35,
          // age__lt: 35,
          // gender: 0,
        },
      }
    },
    watch: {},
    mounted() {
      console.log('EditAvatar: mounted', this.avatar)
      this.newAvatar = this.avatar
    },

    methods: {
      onChangeAvatarReq() {
        this.dialogVisible = true
        this.FaceQueryForm.profile = this.id
        this.isMounted = true
        console.log(
          'EditAvatar: onChangeAvatarReq, this.FaceQueryForm.id',
          this.FaceQueryForm.profile
        )
      },

      onChoosed(face) {
        this.choosedFace = face
        console.log('EditAvatar: onChoosed', this.newAvatar)
      },

      onConfirmAvatar(done) {
        console.log('EditAvatar: onConfirmAvatar', this.newAvatar)
        this.dialogVisible = false
        this.newAvatar = this.choosedFace.thumb
        this.$emit('confirmAvatar', this.choosedFace)
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
  .user-avatar {
    width: 60px;
    height: 60px;
    cursor: pointer;
    border-radius: 50%;
  }
</style>
