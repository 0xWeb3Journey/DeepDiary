<template>
  <div class="search-container">
    <!-- one search -->
    <el-input
      v-model="faceQuery.search"
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
      <!-- confirmed filter -->
      <el-select
        v-model="faceQuery.confirmed"
        clearable
        filterable
        default-first-option
        placeholder="Is Confirmed?"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.confirmed"
          :key="item.name"
          :label="item.name"
          :value="item.value"
          :disabled="false"
        >
          <span style="float: left; color: #8492a6">{{ item.name }}</span>
          <!-- <span style="float: right; color: #8492a6; font-size: 13px">
            {{ item.value }}
          </span> -->
        </el-option>
      </el-select>
      <!-- relation filter -->
      <el-select
        v-model="faceQuery.relation"
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

      <!-- profile__name filter -->
      <el-select
        v-model="faceQuery.profile__name"
        clearable
        filterable
        default-first-option
        placeholder="Friend Name"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.profile__name"
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

      <!-- profill__isnull filter -->
      <el-select
        v-model="faceQuery.profile__isnull"
        clearable
        filterable
        default-first-option
        placeholder="Named Face or not"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.profile__isnull"
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

      <!-- det_score__gt filter -->
      <el-select
        v-model="faceQuery.det_score__gt"
        clearable
        filterable
        default-first-option
        placeholder="Det Score Bigger Then"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.det_score__gt"
          :key="item"
          :label="item"
          :value="item"
          :disabled="false"
        >
          <span style="float: left; color: #8492a6">{{ item }}</span>
          <span style="float: right; color: #8492a6; font-size: 13px">
            {{ item.value }}
          </span>
        </el-option>
      </el-select>

      <!-- det_score__lt filter -->
      <el-select
        v-model="faceQuery.det_score__lt"
        clearable
        filterable
        default-first-option
        placeholder="Det Score Smaller Then"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.det_score__lt"
          :key="item"
          :label="item"
          :value="item"
          :disabled="false"
        >
          <span style="float: left; color: #8492a6">{{ item }}</span>
          <span style="float: right; color: #8492a6; font-size: 13px">
            {{ item.value }}
          </span>
        </el-option>
      </el-select>

      <!-- face_score__gt filter -->
      <el-select
        v-model="faceQuery.face_score__gt"
        clearable
        filterable
        default-first-option
        placeholder="Face Score Bigger Then"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.face_score__gt"
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

      <!-- face_score__lt filter -->
      <el-select
        v-model="faceQuery.face_score__lt"
        clearable
        filterable
        default-first-option
        placeholder="Face Score Smaller Then"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.face_score__lt"
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

      <!-- gender filter -->
      <el-select
        v-model="faceQuery.gender"
        clearable
        filterable
        default-first-option
        placeholder="Gender"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.gender"
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

      <!-- pose_x__gt filter -->
      <el-select
        v-model="faceQuery.pose_x__gt"
        clearable
        filterable
        default-first-option
        placeholder="Look Up"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.pose_x__gt"
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

      <!-- pose_x__lt filter -->
      <el-select
        v-model="faceQuery.pose_x__lt"
        clearable
        filterable
        default-first-option
        placeholder="Look Down"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.pose_x__lt"
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

      <!-- pose_y__gt filter -->
      <el-select
        v-model="faceQuery.pose_y__gt"
        clearable
        filterable
        default-first-option
        placeholder="Look Right"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.pose_y__gt"
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

      <!-- pose_y__lt filter -->
      <el-select
        v-model="faceQuery.pose_y__lt"
        clearable
        filterable
        default-first-option
        placeholder="Look Left"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.pose_y__lt"
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

      <!-- pose_z__gt filter -->
      <el-select
        v-model="faceQuery.pose_z__gt"
        clearable
        filterable
        default-first-option
        placeholder="Rotate Right"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.pose_z__gt"
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

      <!-- pose_z__lt filter -->
      <el-select
        v-model="faceQuery.pose_z__lt"
        clearable
        filterable
        default-first-option
        placeholder="Rotate Left"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.pose_z__lt"
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

      <!-- wid__gt filter -->
      <el-select
        v-model="faceQuery.wid__gt"
        clearable
        filterable
        default-first-option
        placeholder="Width Bigger Then"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.wid__gt"
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

      <!-- wid__lt filter -->
      <el-select
        v-model="faceQuery.wid__lt"
        clearable
        filterable
        default-first-option
        placeholder="Width Smaller Then"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.wid__lt"
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

      <!-- state filter -->
      <el-select
        v-model="faceQuery.state"
        clearable
        filterable
        default-first-option
        placeholder="State"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.state"
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
  import { getFilterList } from '@/api/face'
  export default {
    name: 'FaceSearch',
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
        faceQuery: {
          page: 1,
          size: 25,
          search: '',
          confirmed: '1',
          profile__isnull: '',
          profile__name: '',
          profile: '',
          det_score__gt: '',
          det_score__lt: '',
          face_score__gt: '',
          face_score__lt: '',
          age__gt: '',
          age__lt: '',
          gender: '',
          pose_x__gt: '',
          pose_x__lt: '',
          pose_y__gt: '',
          pose_y__lt: '',
          pose_z__gt: '',
          pose_z__lt: '',
          wid__gt: '',
          wid__lt: '',
          state: '',
          relation: '',
        },
        checked_fcGroup: '',

        filterList: {
          profile__name: [
            {
              name: 'Avril',
              value: 17,
            },
            {
              name: 'allison',
              value: 7,
            },
          ],
          det_score__gt: [0.9, 0.8, 0.7, 0.6, 0.5],
        },

        list: [],
        loading: false,
        states: [],
        ratingColors: ['#99A9BF', '#F7BA2A', '#FF9900'],

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
      //       // this.categoryQuery.faces = this.faceQuery
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
        this.faceQuery.page = 1
        // 将faceQuery中的所有数组元素转换为字符串，转换好的结果实用新的局部变量来保存
        // 如果直接使用等号赋值，那就是引用，会改变原来的值
        let faceQueryStr = Object.assign({}, this.faceQuery)
        for (let key in this.faceQuery) {
          if (Array.isArray(this.faceQuery[key])) {
            // if (key === 'categories') {
            //   console.log('this.faceQuery[key]', this.faceQuery[key])
            //   faceQueryStr[key] = this.faceQuery[key]
            // } else {
            faceQueryStr[key] = this.faceQuery[key].toString()
            // }
          }
        }
        console.log('onCateSearch', this.faceQuery, faceQueryStr)
        this.$emit('handleFaceSearch', faceQueryStr) //自定义事件  传递值“子向父组件传值”
        this.fetchCategory(faceQueryStr) // 重新获取category列表
      },

      // 这里独立一个函数出来，因为group 和category都是对Categery表的查询，只是查询的字段不同
      onCateSearch(value) {
        //当搜索时，让其它下拉列表失效，不然会进行2次不同的搜索，返回值会重叠
        this.faceQuery.page = 1
        // 将faceQuery中的所有数组元素转换为字符串，转换好的结果实用新的局部变量来保存
        // 如果直接使用等号赋值，那就是引用，会改变原来的值
        let faceQueryStr = Object.assign({}, this.faceQuery)
        faceQueryStr.categories__name = value
        this.$emit('handlefaceSearch', faceQueryStr) //自定义事件  传递值“子向父组件传值”
        this.fetchCategory(faceQueryStr) // 重新获取category列表
      },

      async fetchCategory(faceQueryStr) {
        console.log('start to get the Category list...')
        const { data } = await getFilterList(faceQueryStr)
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
