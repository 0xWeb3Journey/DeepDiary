<template>
  <div>
    <ProfileSearch
      v-if="searchable"
      @handleProfileSearch="onProfileSearch"
    ></ProfileSearch>
    <el-transfer
      v-model="SelectedId"
      filterable
      :titles="['Persons', relationName]"
      :data="profileList"
    >
      <el-select
        slot="left-footer"
        v-model="relationValue"
        filterable
        clearable
        placeholder="请选择"
        @change="onChange"
      >
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        ></el-option>
      </el-select>

      <el-button
        slot="right-footer"
        type="primary"
        size="small"
        class="transfer-footer"
        icon="el-icon-finished"
        @click="addRelation"
      >
        Submit
      </el-button>
      <el-button
        slot="right-footer"
        type="primary"
        size="small"
        class="transfer-footer"
        icon="el-icon-delete"
        @click="delRelation"
      >
        Delete
      </el-button>
    </el-transfer>
    <AlbumContainer
      :items="profiles.data"
      :total="profiles.totalCnt"
      :title="profiles.title"
      :busy="profiles.loading"
      :finished="profiles.finished"
      @albumClick="onRouteJump"
      @load="onLoad"
    />
  </div>
</template>

<script>
  import AlbumContainer from '@/components/Album/content.vue'
  import { getProfile } from '@/api/profile'
  import { apiAddRelation } from '@/api/recontact'
  import store from '@/store'
  import axios from 'axios'
  import { baseURL } from '@/config'
  import ProfileSearch from '@/components/Search/profile'
  export default {
    name: 'Relation',
    components: { AlbumContainer, ProfileSearch },
    directives: {},
    props: {},
    data() {
      const relation_strings = [
        '我',
        '妻子',
        '丈夫',
        '儿子',
        '女儿',
        '爸爸',
        '妈妈',
        '爷爷',
        '奶奶',
        '外公',
        '外婆',
        '家人',
        '哥哥',
        '姐姐',
        '弟弟',
        '妹妹',
        '亲戚',
        '男朋友',
        '女朋友',
        '同事',
        '朋友',
        '同学',
        '闺蜜',
        '客户',
        '供应商',
        '合作伙伴',
        '其他',
      ]

      const processedOptions = relation_strings.map((label, index) => ({
        value: index,
        label: label,
      }))

      return {
        SelectedId: [],
        relationValue: '',
        relationName: '',
        relationForm: [],
        options: processedOptions,
        profileList: [],
        profiles: {
          title: 'Profile List',
          loading: false,
          finished: false,
          checkedId: -1,
          checkedIndex: -1,
          totalCnt: 0,
          links: null,
          curCnt: 0,
          data: [],
          queryForm: {
            page: 1,
            size: 30,
          },
        },
        searchable: true,
      }
    },
    watch: {},
    created() {
      console.log('Relation: created')
    },
    mounted() {
      console.log('Relation: mounted')
      this.profiles.queryForm.page = 1
      this.fetchProfile()
    },
    activated() {
      console.log('Relation: activated')
    },
    deactivated() {
      console.log('Relation: deactivated')
    },
    methods: {
      onChange(value) {
        console.log('Relation: onChange', value)
        this.relationName = this.options.find(
          (option) => option.value === value
        ).label
        console.log('Relation: onChange', this.relationName)
      },
      onRouteJump(index, item) {
        console.log('recieved the child component value %d,%o', index, item)
      },

      async fetchProfile() {
        console.log('ProfileList: fetchProfile')
        this.profiles.loading = true
        this.profiles.finished = false
        await getProfile(this.profiles.queryForm).then((response) => {
          console.log('getProfileChangeAvatar', response)
          const { data, totalCnt, links } = response
          this.profiles.data = [...this.profiles.data, ...data]
          this.profiles.curCnt = this.profiles.data.length
          this.profiles.totalCnt = totalCnt
          this.profiles.links = links
          if (this.profiles.links.next === null) {
            // no more data
            this.profiles.finished = true
          }
          // get the profileList
          this.genPersonList(this.profiles.data)
          this.$emit('profileData', this.profiles.data)
        })
        // move to the outside, incase of no response
        setTimeout(() => {
          this.profiles.loading = false
        }, 300)
      },

      onLoad() {
        console.log('ProfileList: onLoad')
        this.profiles.loading = true
        // deal with some logic that data is not enough
        if (this.profiles.finished) {
          // no more data
          setTimeout(() => {
            this.profiles.loading = false
          }, 3000)
          return
        }
        this.profiles.queryForm.page++
        this.fetchProfile()
      },
      genPersonList(data) {
        this.profileList = []
        for (let i = 0; i < data.length; i++) {
          this.profileList.push({
            key: data[i].id,
            label: data[i].name,
          })
        }
      },
      creatFormData() {
        //if this.relationValue is null
        if (this.relationValue === '') {
          this.$message({
            message: '请选择关系',
            type: 'warning',
          })
          return
        }
        //get the user id from the store
        const userId = store.getters['user/id']
        console.log(
          'Relation: onSubmit->SelectedId and userId are: ',
          this.SelectedId,
          userId
        )
        console.log('Relation: onSubmit', this.relationValue, this.relationName)
        // 收集所有记录的数据
        const recordsData = []
        for (let i = 0; i < this.SelectedId.length; i++) {
          const re_from = this.SelectedId[i]
          const re_to = userId
          const relation = this.relationValue
          recordsData.push({ re_from, re_to, relation })
        }
        // this.relationForm = JSON.stringify(recordsData)
        this.relationForm = recordsData
      },

      async addRelation() {
        console.log('Relation: addRelation', this.relationForm)
        this.creatFormData()

        // 使用框架 发送 POST 请求， 暂时不支持列表格式
        // await apiAddRelation(this.relationForm).then((response) => {
        //   console.log('Relation: addRelation: response', response)
        //   // const { data, totalCnt, links } = response
        // })

        // axios 发送 POST 请求
        await axios
          .post(`${baseURL}/api/recontact/`, this.relationForm, {
            headers: {
              'Content-Type': 'application/json', // 设置请求头
            },
          })
          .then((response) => {
            // 请求成功处理
            console.log('Response:', response.data)
          })
          .catch((error) => {
            // 请求失败处理
            console.error('Error:', error)
          })
      },
      async delRelation() {
        console.log('Relation: addRelation', this.relationForm)
        this.creatFormData()
        // 使用框架 发送 POST 请求， 暂时不支持列表格式
        // await apiAddRelation(this.relationForm).then((response) => {
        //   console.log('Relation: addRelation: response', response)
        //   // const { data, totalCnt, links } = response
        // })

        // axios 发送 POST 请求
        await axios
          .delete(`${baseURL}/api/recontact/`, this.relationForm, {
            headers: {
              'Content-Type': 'application/json', // 设置请求头
            },
          })
          .then((response) => {
            // 请求成功处理
            console.log('Response:', response.data)
          })
          .catch((error) => {
            // 请求失败处理
            console.error('Error:', error)
          })
      },
      onProfileSearch(queryForm) {
        console.log('recieve the queryForm info from the search component')
        console.log(queryForm)
        this.profiles.queryForm = queryForm
        this.profiles.totalCnt = 0
        this.profiles.data = []
        this.fetchProfile()
        // this.loadMore()
      },
    },
  }
</script>

<style></style>
