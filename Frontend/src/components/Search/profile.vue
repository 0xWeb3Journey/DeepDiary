<template>
  <div class="search-container">
    <!-- one search -->
    <el-input
      v-model="profileQuery.search"
      clearable
      placeholder="Please input what you want"
      @change="onSearch"
    >
      <!-- <el-button slot="append" icon="el-icon-search"></el-button> -->
      <i
        slot="prefix"
        class="el-input__icon el-icon-search"
        @click="advancedSearch"
      ></i>

      <el-dropdown slot="append" icon="el-icon-delete" @command="handleCommand">
        <span class="el-dropdown-link">
          <i class="el-icon-menu el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="edit">
            <i class="el-icon-edit"></i>
            Edit
          </el-dropdown-item>
          <el-dropdown-item command="view">
            <i class="el-icon-view"></i>
            View
          </el-dropdown-item>
          <el-dropdown-item command="delete">
            <i class="el-icon-delete"></i>
            Reset
          </el-dropdown-item>
          <el-dropdown-item command="setting">
            <i class="el-icon-setting"></i>
            Setting
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </el-input>

    <!-- advance search -->
    <div v-if="advanced" class="advancedSearch">
      <!-- relation filter -->
      <el-select
        v-model="profileQuery.relation"
        clearable
        filterable
        default-first-option
        placeholder="Relation to Me"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.relation"
          :key="item"
          :label="item"
          :value="item"
          :disabled="false"
        >
          <span style="float: left; color: #8492a6">{{ item }}</span>
          <!-- <span style="float: right; color: #8492a6; font-size: 13px">
            {{ item.value }}
          </span> -->
        </el-option>
      </el-select>

      <!-- name filter -->
      <el-select
        v-model="profileQuery.name"
        clearable
        filterable
        default-first-option
        placeholder="Friend Name"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.name"
          :key="item.name"
          :label="item.name"
          :value="item.name"
          :disabled="false"
        >
          <span style="float: left; color: #8492a6">{{ item.name }}</span>
          <span style="float: right; color: #8492a6; font-size: 13px">
            {{ item.value }}
          </span>
        </el-option>
      </el-select>

      <!-- relation__isnull filter -->
      <el-select
        v-model="profileQuery.re_from_relations__isnull"
        clearable
        filterable
        default-first-option
        placeholder="Is Defined a Relation?"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.re_from_relations__isnull"
          :key="item.name"
          :label="item.name"
          :value="item.value"
          :disabled="false"
        >
          <span style="float: left; color: #8492a6">{{ item.name }}</span>
          <!-- <span style="float: right; color: #8492a6; font-size: 13px">
            {{ item.value }} -->
          <!-- </span> -->
        </el-option>
      </el-select>
    </div>
  </div>
</template>

<script>
  import { getFilterList } from '@/api/profile'
  export default {
    name: 'ProfileSearch',
    components: {},
    props: {
      // faces: {
      //   type: String,
      //   default: '', // model field name
      //   required: false,
      // },
      filteredList: {
        type: Object,
        default: function () {
          return {
            face_color: ['skin', 'black', 'grey', 'blue', 'light grey'],
            fore_color: ['light brown', 'beige', 'light blue'],
            back_color: ['black', 'blue', 'light grey'],
          }
        },
        required: false,
      },
    },
    data() {
      return {
        profileQuery: {
          page: 1,
          size: 25,
          search: '',
          re_from_relations__isnull: '',
          re_to_relations__isnull: '',
          // re_from_relations__re_to: 1,
          profile: '',
          relation: '',
        },

        filterList: {},

        loading: false,

        advanced: false,
      }
    },
    watch: {
      // filteredList(newVal, oldVal) {
      //   deep: true,
      //     this.$nextTick(() => {
      //       console.log('filtered category have been changed', newVal)
      //       this.opt_cface = newVal.face_color
      //       this.opt_cFore = newVal.fore_color
      //       this.opt_cBack = newVal.back_color
      //       // this.categoryQuery.faces = newVal
      //       // this.categoryQuery.faces = this.profileQuery
      //       // this.fetchCategory()
      //       // this.fetchProfile()
      //     })
      // },
    },
    created() {},
    mounted() {
      // this.list = this.states.map((item) => {
      //   return { value: `value:${item}`, label: `label:${item}` }
      // })
      this.fetchCategory()
    },
    methods: {
      onSearch() {
        //当搜索时，让其它下拉列表失效，不然会进行2次不同的搜索，返回值会重叠
        this.profileQuery.page = 1
        // 将profileQuery中的所有数组元素转换为字符串，转换好的结果实用新的局部变量来保存
        // 如果直接使用等号赋值，那就是引用，会改变原来的值
        let profileQueryStr = Object.assign({}, this.profileQuery)
        for (let key in this.profileQuery) {
          if (Array.isArray(this.profileQuery[key])) {
            // if (key === 'categories') {
            //   console.log('this.profileQuery[key]', this.profileQuery[key])
            //   profileQueryStr[key] = this.profileQuery[key]
            // } else {
            profileQueryStr[key] = this.profileQuery[key].toString()
            // }
          }
        }
        console.log('onCateSearch', this.profileQuery, profileQueryStr)
        this.$emit('handleProfileSearch', profileQueryStr) //自定义事件  传递值“子向父组件传值”
        this.fetchCategory(profileQueryStr) // 重新获取category列表
      },

      // 这里独立一个函数出来，因为group 和category都是对Categery表的查询，只是查询的字段不同
      onCateSearch(value) {
        //当搜索时，让其它下拉列表失效，不然会进行2次不同的搜索，返回值会重叠
        this.profileQuery.page = 1
        // 将profileQuery中的所有数组元素转换为字符串，转换好的结果实用新的局部变量来保存
        // 如果直接使用等号赋值，那就是引用，会改变原来的值
        let profileQueryStr = Object.assign({}, this.profileQuery)
        profileQueryStr.categories__name = value
        this.$emit('handleProfileSearch', profileQueryStr) //自定义事件  传递值“子向父组件传值”
        this.fetchCategory(profileQueryStr) // 重新获取category列表
      },

      async fetchCategory(profileQueryStr) {
        console.log('start to get the Category list...')
        const { data } = await getFilterList(profileQueryStr)
        this.filterList = data
        console.log('this.filterList', this.filterList, data)
      },

      reset_search() {
        console.log(this.$data)
        console.log(this.$options.data())
        Object.assign(this.$data, this.$options.data())
        this.fetchCategory()
        this.onSearch()
      },
      advancedSearch() {
        console.log('advancedSearch')
        this.advanced = !this.advanced
      },
      handleCommand(command) {
        this.$message('click on item ' + command)
        if (command === 'reset') {
          this.reset_search()
        } else {
          this.$emit(command) //自定义事件  传递值“子向父组件传值” command could be 'edit' or 'remove'
        }
      },
    },
  }
</script>

<style lang="css" scoped></style>
