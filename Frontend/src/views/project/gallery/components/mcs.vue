<template>
  <div class="mcs-container">
    <!-- <el-alert title="mcs组件消息提示的文案" type="info"></el-alert> -->

    <div id="mcs" ref="mcs">
      <el-descriptions
        class="margin-top"
        :title="title"
        extra="Extra"
        :column="3"
        size="small"
        border
      >
        <template slot="extra">
          <el-button type="primary" size="small">Sync</el-button>
        </template>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-user"></i>
            id
          </template>
          {{ mcs.id }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-mobile-phone"></i>
            file_upload_id
          </template>
          {{ mcs.file_upload_id }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-location-outline"></i>
            file_name
          </template>
          {{ mcs.file_name }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-tickets"></i>
            file_size
          </template>
          {{ mcs.file_size }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-office-building"></i>
            nft_url
          </template>
          <el-link type="primary" :href="mcs.nft_url">
            {{ mcs.nft_url }}
          </el-link>
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-office-building"></i>
            pin_status
          </template>
          {{ mcs.pin_status }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-office-building"></i>
            payload_cid
          </template>
          {{ mcs.payload_cid }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-office-building"></i>
            w_cid
          </template>
          {{ mcs.w_cid }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-office-building"></i>
            status
          </template>
          {{ mcs.status }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-office-building"></i>
            deal_success
          </template>
          {{ mcs.deal_success }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-office-building"></i>
            is_minted
          </template>
          {{ mcs.is_minted }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-office-building"></i>
            token_id
          </template>
          {{ mcs.token_id }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-office-building"></i>
            mint_address
          </template>
          {{ mcs.mint_address }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-office-building"></i>
            nft_tx_hash
          </template>
          {{ mcs.nft_tx_hash }}
        </el-descriptions-item>
      </el-descriptions>
    </div>
  </div>
</template>

<script>
  import $ from 'jquery'
  import {
    getGallery,
    getAlbum,
    getFaceAlbum,
    getFaceGallery,
    getMcs,
    getImg,
    getFace,
  } from '@/api/gallery'
  export default {
    name: 'Mcs',
    components: {},
    props: {
      mcstype: {
        type: String,
        default: 'img', // model field name
        required: false,
      },
      title: {
        type: String,
        default: '', // model field name
        required: false,
      },
      id: {
        type: Number,
        default: 269,
        required: true,
      },
    },
    data() {
      return {
        mcs: {
          id: -1,
          file_upload_id: 0,
          file_name: '',
          file_size: 0,
          // "updated_at": updated_at,
          nft_url: '',
          pin_status: 'Pinned',
          payload_cid: '',
          w_cid: '',
          status: '',
          deal_success: false,
          is_minted: false,
          token_id: 0,
          mint_address: '',
          nft_tx_hash: '',
        },
        mcsQueryForm: {
          id: 0,
        },
      }
    },
    computed: {},
    watch: {
      id(newVal, oldVal) {
        this.$nextTick(() => {
          console.log('gallery have been changed')
          if (this.mcstype === 'img') this.fetchImgMcs()
          if (this.mcstype === 'face') this.fetchFaceMcs()
        })
      },
    },
    created() {
      // this.fetchAlbum()
      // this.srcList = []
    },
    mounted() {},
    methods: {
      async fetchFaceMcs() {
        console.log('start to get the face mcs...')
        this.mcsQueryForm.id = this.id
        const { data } = await getFace(this.mcsQueryForm)
        if (data.mcs === null) {
          this.setMcsDefault()
        } else {
          // console.log(data)
          this.mcs = data.mcs
        }
      },
      async fetchImgMcs() {
        console.log('start to get the img mcs...')
        this.mcsQueryForm.id = this.id
        const { data } = await getImg(this.mcsQueryForm)
        if (data.mcs === null) {
          this.setMcsDefault()
        } else {
          // console.log(data)
          this.mcs = data.mcs
        }
      },
      setMcsDefault() {
        // console.log('null++++-----------')
        this.mcs.id = 0
        this.mcs.file_upload_id = 0
        this.mcs.file_name = ''
        this.mcs.file_size = 0
        // "updated_at": updated_at
        this.mcs.nft_url = ''
        this.mcs.pin_status = ''
        this.mcs.payload_cid = ''
        this.mcs.w_cid = ''
        this.mcs.status = ''
        this.mcs.deal_success = false
        this.mcs.is_minted = false
        this.mcs.token_id = 0
        this.mcs.mint_address = ''
        this.mcs.nft_tx_hash = ''
      },
    },
  }
</script>

<style lang="css" scoped></style>
