<template>
  <div>
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="Profiles" name="profiles">
        <ProfileList v-if="activeName === 'profiles'"></ProfileList>
      </el-tab-pane>
      <el-tab-pane label="Groups" name="groups">
        <GroupList v-if="activeName === 'groups'"></GroupList>
      </el-tab-pane>
      <el-tab-pane label="Faces" name="faces">
        <FaceList
          v-if="activeName === 'faces'"
          :query="FaceQueryForm"
        ></FaceList>
      </el-tab-pane>
      <el-tab-pane label="FacesGallery" name="faces-gallery">
        <FaceListGallery
          v-if="activeName === 'faces-gallery'"
          :query="FaceQueryForm"
        ></FaceListGallery>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
  import ProfileList from './profileList.vue'
  import GroupList from './groupList.vue'
  import FaceList from './faceList.vue'
  import FaceListGallery from './faceListGallery.vue'

  export default {
    name: 'Face',
    components: { ProfileList, GroupList, FaceList, FaceListGallery },

    directives: {},
    data: function () {
      return {
        activeName: 'profiles',
        FaceQueryForm: {
          page: 1,
          size: 20,
          // profile__isnull: true,
          // profile: 30,
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
    created() {},
    mounted() {},
    methods: {
      handleClick(tab, event) {
        console.log(tab, event)
      },
    },
  }
</script>

<style></style>
