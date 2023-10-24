<template>
  <div>
    <el-transfer
      v-model="SelectedId"
      filterable
      :titles="['Persons', relationName]"
      :data="profileList"
      @change="onTransferChange"
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
          v-for="item in companyList"
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
  import { getCompany } from '@/api/company'

  export default {
    name: 'RelationCompany',
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
      // const relation_strings = [
      //   '我',
      //   '妻子',
      //   '丈夫',
      //   '儿子',
      //   '女儿',
      //   '爸爸',
      //   '妈妈',
      //   '爷爷',
      //   '奶奶',
      //   '外公',
      //   '外婆',
      //   '家人',
      //   '哥哥',
      //   '姐姐',
      //   '弟弟',
      //   '妹妹',
      //   '亲戚',
      //   '男朋友',
      //   '女朋友',
      //   '同事',
      //   '朋友',
      //   '同学',
      //   '闺蜜',
      //   '客户',
      //   '供应商',
      //   '合作伙伴',
      //   '其他',
      // ]

      // const processedOptions = this.companyList.map((label, index) => ({
      //   value: index,
      //   label: label,
      // }))

      return {
        SelectedId: [],
        relationValue: '',
        relationName: '',
        relationForm: [],

        profileList: [],
        companyList: [],
        // recordsData: [], // 收集所有记录的数据
        Companies: {
          title: 'Company List',
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
      this.fetchCompany()
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
        this.relationName = this.companyList.find(
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
      genCompanyList(data) {
        this.companyList = []
        for (let i = 0; i < data.length; i++) {
          this.companyList.push({
            key: data[i].id,
            label: data[i].name,
            value: data[i].id,
          })
        }
        console.log('Relation: genCompanyList', this.companyList)
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
          const profile = this.SelectedId[i]
          const company = this.relationValue
          const name = 'worked in'
          this.relationForm.push({ profile, company, name })
        }
        // this.relationForm = JSON.stringify(this.recordsData)
        // this.relationForm = this.recordsData
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
          .post(`${baseURL}/api/experience/`, this.relationForm, {
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
      async fetchCompany() {
        console.log('CompanyList: fetchCompany')
        this.Companies.loading = true
        this.Companies.finished = false
        await getCompany(this.Companies.queryForm).then((response) => {
          console.log('getCompaniesChangeAvatar', response)
          const { data, totalCnt, links } = response
          this.Companies.data = [...this.Companies.data, ...data]
          this.Companies.curCnt = this.Companies.data.length
          this.Companies.totalCnt = totalCnt
          this.Companies.links = links
          this.genCompanyList(this.Companies.data)
          if (this.Companies.links.next === null) {
            // no more data
            this.Companies.finished = true
          }
          this.$emit('companyData', this.Companies.data)
        })
        // move to the outside, incase of no response
        setTimeout(() => {
          this.Companies.loading = false
        }, 300)
      },
      onTransferChange() {
        console.log('transfer on change', this.SelectedId)
      },
    },
  }
</script>

<style></style>
