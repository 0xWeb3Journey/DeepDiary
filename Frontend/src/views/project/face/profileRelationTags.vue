<template>
  <div>
    <div class="edit-list">
      <span>与我的关系</span>
      <el-tag
        v-if="isHaveTag"
        closable
        :disable-transitions="false"
        @close="onTagDelete(selectedTag)"
      >
        {{ selectedTag }}
      </el-tag>
    </div>
    <el-radio-group v-model="selectedTag" @input="onRelationChoosed">
      <el-radio-button v-for="tag in dynamicTags" :key="tag" :label="tag">
        {{ tag }}
      </el-radio-button>
    </el-radio-group>

    <el-input
      v-if="inputVisible"
      ref="saveTagInput"
      v-model="inputValue"
      class="input-new-tag"
      size="small"
      @keyup.enter.native="handleInputConfirm"
      @blur="handleInputConfirm"
    ></el-input>
    <el-button v-else class="button-new-tag" size="small" @click="showInput">
      + New Tag
    </el-button>
  </div>
</template>

<script>
  export default {
    name: 'ProfileRelationTags',
    props: {
      relation: {
        type: String,
        default: '',
        required: false,
      },
    },
    data() {
      return {
        dynamicTags: [
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
          '其他',
        ],
        inputVisible: false,
        inputValue: '',
        selectedTag: '', // Added for single selection
        isHaveTag: false,
      }
    },
    watch: {
      relation(newVal, oldVal) {
        console.log('ProfileRelationTags: relation', newVal, oldVal)
        this.selectedTag = newVal
      },
    },
    mounted() {
      // 如果没有tag， 则不显示
      if (this.relation === '') {
        this.isHaveTag = false
      } else {
        this.isHaveTag = true
        this.selectedTag = this.relation
      }

      console.log('ProfileRelationTags: mounted', this.selectedTag)
    },
    methods: {
      handleClose(tag) {
        this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1)
      },

      showInput() {
        this.inputVisible = true
        this.$nextTick((_) => {
          this.$refs.saveTagInput.$refs.input.focus()
        })
      },

      handleInputConfirm() {
        let inputValue = this.inputValue
        if (inputValue) {
          this.dynamicTags.push(inputValue)
        }
        this.inputVisible = false
        this.inputValue = ''
      },
      onTagDelete(tag) {
        console.log('ProfileRelationTags: onTagDelete', tag)
        this.isHaveTag = false
      },
      onRelationChoosed(value) {
        console.log(
          'ProfileRelationTags: onRelationChoosed',
          this.selectedTag,
          value
        )
        this.isHaveTag = true
        this.$emit('relationChoosed', this.selectedTag) // value and this.selectedTag are the same
      },
    },
  }
</script>

<style>
  .el-tag + .el-tag {
    margin-left: 10px;
  }
  .button-new-tag {
    margin-left: 10px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
  }
  .input-new-tag {
    width: 90px;
    margin-left: 10px;
    vertical-align: bottom;
  }
  .edit-list {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    border-bottom: 1px solid #ebeef5;
    background-color: #f5f7fa;
  }
</style>
