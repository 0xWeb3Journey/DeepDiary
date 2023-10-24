<template>
  <div>
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
  </div>
</template>

<script>
  import AlbumContainer from '@/components/Album/content.vue'
  import store from '@/store'
  import axios from 'axios'
  import { baseURL } from '@/config'

  export default {
    name: 'RelationProfile',
    components: {},
    directives: {},
    props: {
      profiles: {
        type: Array,
        default: () => Array(40).fill({}), // Initialize with placeholder data,
        required: true,
      },
    },
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
      }
    },
    watch: {
      profiles(newVal, oldVal) {
        console.log(
          'Album.content: Album numbers have been changed',
          newVal.length,
          this.total,
          this.msg
        )
        this.genPersonList(newVal)
      },
    },
    created() {
      console.log('Relation: created')
    },
    mounted() {
      console.log('Relation: mounted', this.profiles)
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
        this.SelectedId = []
        this.relationForm = []
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
        // const recordsData = []
        for (let i = 0; i < this.SelectedId.length; i++) {
          const re_from = this.SelectedId[i]
          const re_to = userId
          const relation = this.relationValue
          this.relationForm.push({ re_from, re_to, relation })
        }
        // this.relationForm = JSON.stringify(recordsData)
        // this.relationForm = recordsData
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
            this.$message({
              message: 'Successed binding the relation!',
              type: 'success',
            })
            this.SelectedId = []
            this.relationForm = []
          })
          .catch((error) => {
            // 请求失败处理
            console.error('Error:', error)
            this.$message({
              message: error,
              type: 'error',
            })
            this.SelectedId = []
            this.relationForm = []
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
    },
  }
</script>

<style></style>
