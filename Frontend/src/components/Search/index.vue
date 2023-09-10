<template>
  <div class="search-container">
    <!-- one search -->
    <el-input
      v-model="imgQuery.search"
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
      <el-button
        slot="append"
        icon="el-icon-delete"
        @click="reset_search"
      ></el-button>
    </el-input>

    <!-- advance search -->
    <div v-if="advanced" class="advancedSearch">
      <!-- Category filter -->

      <el-cascader
        v-model="imgQuery.categories"
        :options="filterList.categories"
        :props="{
          expandTrigger: 'hover',
          multiple: false,
          checkStrictly: true,
        }"
        :show-all-levels="false"
        collapse-tags
        clearable
        filterable
        @change="onSearch"
      >
        <template slot-scope="{ data }">
          <span>{{ data.label }}</span>
          <!-- <span v-if="!node.isLeaf">({{ data.count }})</span> -->
          <span>({{ data.count }})</span>
        </template>
      </el-cascader>

      <el-select
        v-model="imgQuery.fc_nums"
        clearable
        filterable
        default-first-option
        placeholder="People Numbers"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.fc_nums"
          :key="item.value"
          :label="item.value"
          :value="item.value"
          :disabled="false"
        ></el-option>
      </el-select>

      <!-- face group filter -->
      <el-select
        v-model="checked_fcGroup"
        clearable
        filterable
        default-first-option
        placeholder="Group Name"
        :loading="loading"
        @change="onCateSearch"
      >
        <el-option
          v-for="item in filterList.group"
          :key="item.name"
          :label="item.name"
          :value="item.name"
          :disabled="false"
        >
          <span style="float: left; color: #8492a6">{{ item.name }}</span>
          <span style="float: right; color: #8492a6; font-size: 13px">
            {{ item.img_nums }}
          </span>
        </el-option>
      </el-select>
      <!-- face name filter -->
      <el-select
        v-model="imgQuery.fc_name"
        multiple
        clearable
        filterable
        default-first-option
        placeholder="Friend Name"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.fc_name"
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
      <!-- Tags filter -->
      <el-select
        v-model="imgQuery.tags"
        multiple
        clearable
        filterable
        placeholder="Tags"
        default-first-option
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.tags"
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

      <!-- address filter -->
      <el-select
        v-model="imgQuery.address__city"
        clearable
        filterable
        default-first-option
        placeholder="City"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.city"
          :key="item.name"
          :label="item.name"
          :value="item.name"
          :disabled="false"
        >
          <span style="float: left; color: #8492a6">{{ item.name }}</span>
          <span style="float: right; color: #8492a6; font-size: 13px">
            {{ item.img_nums }}
          </span>
        </el-option>
      </el-select>

      <!-- category filter -->
      <el-select
        v-model="imgQuery.categories__name"
        clearable
        filterable
        default-first-option
        placeholder="Auto Category"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.scene"
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

      <!-- Layout filter -->
      <el-select
        v-model="imgQuery.layout"
        clearable
        filterable
        default-first-option
        placeholder="Layout"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.layout"
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

      <!-- image color filter -->
      <el-select
        v-model="imgQuery.c_img"
        multiple
        clearable
        filterable
        default-first-option
        placeholder="Image Colors"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.c_img"
          :key="item.name"
          :label="item.name"
          :value="item.name"
          :disabled="false"
          :style="`background-color: ${item.color}`"
        >
          <span style="float: left; color: #ffffff">{{ item.name }}</span>
          <span style="float: right; color: #ffffff; font-size: 13px">
            {{ item.value }}
          </span>
        </el-option>
      </el-select>

      <!-- rating -->
      <el-select
        v-model="imgQuery.evaluates__rating"
        clearable
        filterable
        default-first-option
        placeholder="Rating"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in [1, 2, 3, 4, 5]"
          :key="item"
          :label="item"
          :value="item"
          :disabled="false"
        >
          <el-rate
            :value="item"
            disabled
            show-score
            text-color="#ff9900"
            :colors="ratingColors"
          ></el-rate>
        </el-option>
      </el-select>

      <!-- ordering -->
      <el-select
        v-model="imgQuery.ordering"
        clearable
        filterable
        default-first-option
        placeholder="Ording"
        :loading="loading"
        @change="onSearch"
      >
        <el-option
          v-for="item in filterList.ordering"
          :key="item"
          :label="item"
          :value="item"
          :disabled="false"
        ></el-option>
      </el-select>
      <!-- date -->
      <el-row :gutter="10">
        <el-col :xs="24" :sm="12">
          <!-- date filter -->
          <!-- <div class="block">
          <span class="demonstration">Date Range</span> -->
          <el-date-picker
            v-model="imgQuery.dates__capture_date__range"
            type="daterange"
            unlink-panels
            range-separator="To"
            start-placeholder="Start Date"
            end-placeholder="End Date"
            :picker-options="pickerOptions"
            value-format="yyyy-MM-dd"
            @change="onSearch"
          ></el-date-picker>
          <!-- </div> -->
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
  import { getFilterList } from '@/api/img'
  export default {
    name: 'ImgSearch',
    components: {},
    props: {
      // imgs: {
      //   type: String,
      //   default: '', // model field name
      //   required: false,
      // },
      filteredList: {
        type: Object,
        default: function () {
          return {
            img_color: ['skin', 'black', 'grey', 'blue', 'light grey'],
            fore_color: ['light brown', 'beige', 'light blue'],
            back_color: ['black', 'blue', 'light grey'],
          }
        },
        required: false,
      },
    },
    data() {
      return {
        // categoryQuery: {
        //   page: 1,
        //   size: 20,
        //   name: '',
        //   type: '',
        //   value: '',
        //   // imgs: '',
        //   c_img: '',
        //   c_fore: '',
        //   c_back: '',
        // },
        imgQuery: {
          page: 1,
          size: 20,
          search: '',
          id: '',
          fc_nums: '',
          fc_name: [],
          c_img: [],
          c_fore: '',
          c_back: '',
          address__city: '',
          dates__capture_date__range: [],
          categories: '',
          categories__name: '',
          tags: [],
          layout: '',
          evaluates__rating: '',
          search: '',
          ordering: '',
        },
        checked_fcGroup: '',
        options: [
          {
            value: 'date',
            label: 'date',
            count: 55,
            children: [
              {
                value: '2023',
                label: '2023',
                count: 31,
                children: [
                  {
                    value: '2023-01',
                    label: '2023-01',
                    count: 1,
                    children: [
                      {
                        value: '2023-01-22',
                        label: '2023-01-22',
                        count: 1,
                        children: [],
                      },
                    ],
                  },
                  {
                    value: '2023-03',
                    label: '2023-03',
                    count: 1,
                    children: [
                      {
                        value: '2023-03-27',
                        label: '2023-03-27',
                        count: 1,
                        children: [],
                      },
                      {
                        value: '2023-03-07',
                        label: '2023-03-07',
                        count: 0,
                        children: [],
                      },
                    ],
                  },
                  {
                    value: '2023-04',
                    label: '2023-04',
                    count: 2,
                    children: [
                      {
                        value: '2023-04-10',
                        label: '2023-04-10',
                        count: 1,
                        children: [],
                      },
                      {
                        value: '2023-04-17',
                        label: '2023-04-17',
                        count: 1,
                        children: [],
                      },
                    ],
                  },
                  {
                    value: '2023-08',
                    label: '2023-08',
                    count: 27,
                    children: [
                      {
                        value: '2023-08-05',
                        label: '2023-08-05',
                        count: 27,
                        children: [],
                      },
                    ],
                  },
                ],
              },
              {
                value: '1970',
                label: '1970',
                count: 3,
                children: [
                  {
                    value: '1970-01',
                    label: '1970-01',
                    count: 3,
                    children: [
                      {
                        value: '1970-01-01',
                        label: '1970-01-01',
                        count: 3,
                        children: [],
                      },
                    ],
                  },
                ],
              },
              {
                value: '2021',
                label: '2021',
                count: 21,
                children: [
                  {
                    value: '2021-10',
                    label: '2021-10',
                    count: 6,
                    children: [
                      {
                        value: '2021-10-11',
                        label: '2021-10-11',
                        count: 1,
                        children: [],
                      },
                      {
                        value: '2021-10-10',
                        label: '2021-10-10',
                        count: 1,
                        children: [],
                      },
                      {
                        value: '2021-10-04',
                        label: '2021-10-04',
                        count: 1,
                        children: [],
                      },
                      {
                        value: '2021-10-03',
                        label: '2021-10-03',
                        count: 2,
                        children: [],
                      },
                      {
                        value: '2021-10-15',
                        label: '2021-10-15',
                        count: 1,
                        children: [],
                      },
                    ],
                  },
                  {
                    value: '2021-09',
                    label: '2021-09',
                    count: 7,
                    children: [
                      {
                        value: '2021-09-23',
                        label: '2021-09-23',
                        count: 1,
                        children: [],
                      },
                      {
                        value: '2021-09-19',
                        label: '2021-09-19',
                        count: 2,
                        children: [],
                      },
                      {
                        value: '2021-09-21',
                        label: '2021-09-21',
                        count: 2,
                        children: [],
                      },
                      {
                        value: '2021-09-06',
                        label: '2021-09-06',
                        count: 1,
                        children: [],
                      },
                      {
                        value: '2021-09-09',
                        label: '2021-09-09',
                        count: 1,
                        children: [],
                      },
                    ],
                  },
                  {
                    value: '2021-08',
                    label: '2021-08',
                    count: 5,
                    children: [
                      {
                        value: '2021-08-27',
                        label: '2021-08-27',
                        count: 1,
                        children: [],
                      },
                      {
                        value: '2021-08-22',
                        label: '2021-08-22',
                        count: 3,
                        children: [],
                      },
                      {
                        value: '2021-08-18',
                        label: '2021-08-18',
                        count: 1,
                        children: [],
                      },
                    ],
                  },
                  {
                    value: '2021-07',
                    label: '2021-07',
                    count: 3,
                    children: [
                      {
                        value: '2021-07-04',
                        label: '2021-07-04',
                        count: 1,
                        children: [],
                      },
                      {
                        value: '2021-07-31',
                        label: '2021-07-31',
                        count: 2,
                        children: [],
                      },
                    ],
                  },
                ],
              },
            ],
          },
          {
            value: 'location',
            label: 'location',
            count: 55,
            children: [
              {
                value: '中国',
                label: '中国',
                count: 50,
                children: [
                  {
                    value: '浙江省',
                    label: '浙江省',
                    count: 50,
                    children: [
                      {
                        value: '台州市',
                        label: '台州市',
                        count: 3,
                        children: [
                          {
                            value: '临海市',
                            label: '临海市',
                            count: 3,
                          },
                        ],
                      },
                      {
                        value: '宁波市',
                        label: '宁波市',
                        count: 47,
                        children: [
                          {
                            value: '慈溪市',
                            label: '慈溪市',
                            count: 46,
                          },
                          {
                            value: '余姚市',
                            label: '余姚市',
                            count: 1,
                          },
                        ],
                      },
                    ],
                  },
                ],
              },
              {
                value: 'No GPS',
                label: 'No GPS',
                count: 5,
              },
            ],
          },
          {
            value: 'img_color',
            label: 'img_color',
            count: 55,
            children: [
              {
                value: 'brown',
                label: 'brown',
                count: 20,
                children: [],
              },
              {
                value: 'grey',
                label: 'grey',
                count: 26,
                children: [],
              },
              {
                value: 'skin',
                label: 'skin',
                count: 9,
                children: [],
              },
              {
                value: 'blue',
                label: 'blue',
                count: 11,
                children: [],
              },
              {
                value: 'light grey',
                label: 'light grey',
                count: 44,
                children: [],
              },
              {
                value: 'light brown',
                label: 'light brown',
                count: 19,
                children: [],
              },
              {
                value: 'maroon',
                label: 'maroon',
                count: 4,
                children: [],
              },
              {
                value: 'beige',
                label: 'beige',
                count: 0,
                children: [],
              },
              {
                value: 'light blue',
                label: 'light blue',
                count: 7,
                children: [],
              },
              {
                value: 'teal',
                label: 'teal',
                count: 1,
                children: [],
              },
              {
                value: 'black',
                label: 'black',
                count: 22,
                children: [],
              },
              {
                value: 'olive green',
                label: 'olive green',
                count: 29,
                children: [],
              },
              {
                value: 'red',
                label: 'red',
                count: 10,
                children: [],
              },
              {
                value: 'yellow',
                label: 'yellow',
                count: 2,
                children: [],
              },
              {
                value: 'light green',
                label: 'light green',
                count: 4,
                children: [],
              },
              {
                value: 'lavender',
                label: 'lavender',
                count: 4,
                children: [],
              },
              {
                value: 'green',
                label: 'green',
                count: 1,
                children: [],
              },
              {
                value: 'white',
                label: 'white',
                count: 2,
                children: [],
              },
              {
                value: 'violet',
                label: 'violet',
                count: 1,
                children: [],
              },
              {
                value: 'purple',
                label: 'purple',
                count: 2,
                children: [],
              },
              {
                value: 'hot pink',
                label: 'hot pink',
                count: 3,
                children: [],
              },
              {
                value: 'navy blue',
                label: 'navy blue',
                count: 1,
                children: [],
              },
            ],
          },
          {
            value: 'scene',
            label: 'scene',
            count: 28,
            children: [
              {
                value: 'people portraits',
                label: 'people portraits',
                count: 25,
                children: [],
              },
              {
                value: 'pets animals',
                label: 'pets animals',
                count: 4,
                children: [],
              },
              {
                value: 'food drinks',
                label: 'food drinks',
                count: 10,
                children: [],
              },
              {
                value: 'events parties',
                label: 'events parties',
                count: 6,
                children: [],
              },
              {
                value: 'interior objects',
                label: 'interior objects',
                count: 4,
                children: [],
              },
              {
                value: 'nature landscape',
                label: 'nature landscape',
                count: 1,
                children: [],
              },
              {
                value: 'sunrises sunsets',
                label: 'sunrises sunsets',
                count: 1,
                children: [],
              },
              {
                value: 'cars vehicles',
                label: 'cars vehicles',
                count: 2,
                children: [],
              },
              {
                value: 'beaches seaside',
                label: 'beaches seaside',
                count: 4,
                children: [],
              },
              {
                value: 'paintings art',
                label: 'paintings art',
                count: 2,
                children: [],
              },
            ],
          },
          {
            value: 'size',
            label: 'size',
            count: 28,
            children: [
              {
                value: 'Extra large',
                label: 'Extra large',
                count: 25,
                children: [],
              },
              {
                value: 'Small',
                label: 'Small',
                count: 3,
                children: [],
              },
            ],
          },
          {
            value: 'layout',
            label: 'layout',
            count: 28,
            children: [
              {
                value: 'Wide',
                label: 'Wide',
                count: 21,
                children: [],
              },
              {
                value: 'Tall',
                label: 'Tall',
                count: 7,
                children: [],
              },
            ],
          },
          {
            value: 'group',
            label: 'group',
            count: 22,
            children: [
              {
                value: '葛昱琛 葛维冬',
                label: '葛昱琛 葛维冬',
                count: 10,
                children: [],
              },
              {
                value: '葛昱琛 葛昱琛 葛维冬 葛维冬',
                label: '葛昱琛 葛昱琛 葛维冬 葛维冬',
                count: 1,
                children: [],
              },
              {
                value: '葛丰炳 葛昱琛 葛菊英',
                label: '葛丰炳 葛昱琛 葛菊英',
                count: 1,
                children: [],
              },
              {
                value: '葛维冬 葛菊英',
                label: '葛维冬 葛菊英',
                count: 1,
                children: [],
              },
              {
                value: '葛昱琛 葛维冬 葛菊英',
                label: '葛昱琛 葛维冬 葛菊英',
                count: 1,
                children: [],
              },
              {
                value: '张立华 韩莉',
                label: '张立华 韩莉',
                count: 1,
                children: [],
              },
              {
                value: '葛昱琛 葛菊英',
                label: '葛昱琛 葛菊英',
                count: 1,
                children: [],
              },
              {
                value: '葛维冬 韩莉',
                label: '葛维冬 韩莉',
                count: 1,
                children: [],
              },
              {
                value: '叶四妹 葛顺法',
                label: '叶四妹 葛顺法',
                count: 1,
                children: [],
              },
              {
                value: '葛丰炳 葛昱琛',
                label: '葛丰炳 葛昱琛',
                count: 2,
                children: [],
              },
              {
                value: '葛昱琛 葛维冬 韩莉',
                label: '葛昱琛 葛维冬 韩莉',
                count: 1,
                children: [],
              },
              {
                value: '张立华 葛昱琛 葛菊英 韩莉',
                label: '张立华 葛昱琛 葛菊英 韩莉',
                count: 1,
                children: [],
              },
            ],
          },
        ],

        filterList: {
          categories: [],
          fc_nums: [0, 1, 2, 3, 4, 6, 10],
          fc_name: [
            {
              name: 'Avril',
              value: 17,
            },
            {
              name: 'allison',
              value: 7,
            },
          ],
          tags: ['abbess', 'adorable', 'adult'],
          c_img: [
            {
              name: 'beige',
              value: '#e0c4b2',
            },
            {
              name: 'black',
              value: '#39373b',
            },
          ],
          c_back: [
            {
              name: 'white',
              value: '#f4f5f0',
            },
            {
              name: 'yellow',
              value: '#ebd07f',
            },
          ],
          c_fore: [
            {
              name: 'skin',
              value: '#bd9769',
            },
            {
              name: 'white',
              value: '#f4f5f0',
            },
          ],
          category: [
            {
              name: 'streetview architecture',
              value: null,
            },
            {
              name: 'text visuals',
              value: null,
            },
          ],
          group: [
            {
              name: 'single face',
              value: null,
            },
            {
              name: '奶奶,爷爷',
              value: null,
            },
          ],
          city: [
            {
              name: 'No GPS',
              value: null,
            },
            {
              name: '台州市',
              value: null,
            },
            {
              name: '宁波市',
              value: null,
            },
          ],
          layout: ['Square', 'Wide', 'Tall'],
          size: ['Small', 'Medium', 'Large', 'Extra large', 'At least'],
          license: [
            'Public domain',
            'Free to share and use',
            'Free to share and use commercially',
          ],
        },

        list: [],
        loading: false,
        states: [],
        ratingColors: ['#99A9BF', '#F7BA2A', '#FF9900'],

        pickerOptions: {
          shortcuts: [
            {
              text: '最近一周',
              onClick(picker) {
                const end = new Date()
                const start = new Date()
                start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
                picker.$emit('pick', [start, end])
              },
            },
            {
              text: '最近一个月',
              onClick(picker) {
                const end = new Date()
                const start = new Date()
                start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
                picker.$emit('pick', [start, end])
              },
            },
            {
              text: '最近三个月',
              onClick(picker) {
                const end = new Date()
                const start = new Date()
                start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
                picker.$emit('pick', [start, end])
              },
            },
          ],
        },
        advanced: false,
      }
    },
    watch: {
      // filteredList(newVal, oldVal) {
      //   deep: true,
      //     this.$nextTick(() => {
      //       console.log('filtered category have been changed', newVal)
      //       this.opt_cImg = newVal.img_color
      //       this.opt_cFore = newVal.fore_color
      //       this.opt_cBack = newVal.back_color
      //       // this.categoryQuery.imgs = newVal
      //       // this.categoryQuery.imgs = this.imgQuery
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
        this.imgQuery.page = 1
        // 将imgQuery中的所有数组元素转换为字符串，转换好的结果实用新的局部变量来保存
        // 如果直接使用等号赋值，那就是引用，会改变原来的值
        let imgQueryStr = Object.assign({}, this.imgQuery)
        for (let key in this.imgQuery) {
          if (Array.isArray(this.imgQuery[key])) {
            // if (key === 'categories') {
            //   console.log('this.imgQuery[key]', this.imgQuery[key])
            //   imgQueryStr[key] = this.imgQuery[key]
            // } else {
            imgQueryStr[key] = this.imgQuery[key].toString()
            // }
          }
        }
        console.log('onCateSearch', this.imgQuery, imgQueryStr)
        this.$emit('handleImgSearch', imgQueryStr) //自定义事件  传递值“子向父组件传值”
        this.fetchCategory(imgQueryStr) // 重新获取category列表
      },

      // 这里独立一个函数出来，因为group 和category都是对Categery表的查询，只是查询的字段不同
      onCateSearch(value) {
        //当搜索时，让其它下拉列表失效，不然会进行2次不同的搜索，返回值会重叠
        this.imgQuery.page = 1
        // 将imgQuery中的所有数组元素转换为字符串，转换好的结果实用新的局部变量来保存
        // 如果直接使用等号赋值，那就是引用，会改变原来的值
        let imgQueryStr = Object.assign({}, this.imgQuery)
        imgQueryStr.categories__name = value
        this.$emit('handleImgSearch', imgQueryStr) //自定义事件  传递值“子向父组件传值”
        this.fetchCategory(imgQueryStr) // 重新获取category列表
      },

      async fetchCategory(imgQueryStr) {
        console.log('start to get the Category list...')
        const { data } = await getFilterList(imgQueryStr)
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
    },
  }
</script>

<style lang="css" scoped></style>
