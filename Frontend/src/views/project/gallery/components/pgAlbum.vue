<template>
  <div>
    <!-- <el-alert title="消息提示的文案" type="info">
      <span v-for="album in albums" :key="album.id">{{ album.id }},</span>
    </el-alert>
    <el-button type="primary" @click="fetchAlbum()">get albums</el-button> -->
    <Album
      v-if="true"
      ref="album"
      title="Album"
      type="collection"
      route="Face_detail"
      :items="albums"
      :total="totalCount"
      @albumClick="onGetAlbumId"
    ></Album>
    <!-- <Tags v-if="checkedIndex >= 0" :items="albums[checkedIndex].tags"></Tags> -->
    <Tags v-if="checkedIndex >= 0" :items="img.tags"></Tags>
    <Color v-if="checkedIndex >= 0" :colors="img.colors"></Color>
    <Mcs
      v-if="checkedIndex >= 0"
      :mcs="img.mcs"
      mcstype="img"
      :title="`Mcs Info-${checkedId}`"
    ></Mcs>
  </div>
</template>

<script>
  import $ from 'jquery'
  import Album from './album.vue'
  import Mcs from './mcs.vue'

  import {
    getGallery,
    getAlbum,
    getFaceAlbum,
    getFaceGallery,
    getImg,
  } from '@/api/gallery'
  import Tags from './tags.vue'
  import Color from './color.vue'
  export default {
    name: 'PgAlbum',
    components: { Album, Mcs, Tags, Color },
    data: function () {
      return {
        checkedIndex: -1,
        checkedId: -1,
        albums: [],
        albumLoading: false,
        totalCount: 0,
        queryForm: {
          page: 1,
          search: '',
          id: '',
        },
        img: {
          id: 426,
          user: 'blue',
          tags: 'people,attractive,cover girl,sensual,adult,pretty,sexy,portrait,person,face,hair,lady,smasher,erotic',
          thumb:
            'http://localhost:8000/media/CACHE/images/blue/img/1970/01/01/e8e4be52ba59a1a124665c82bb3f5ae2/02ef4bc0bd7a2f7c593296a416974cfc.jpeg',
          img_url: 'http://localhost:8000/api/img/426/',
          mcs: {
            id: 426,
            file_upload_id: 478656,
            file_name: 'e8e4be52ba59a1a124665c82bb3f5ae2.jpeg',
            file_size: 259215,
            updated_at: '2022-09-11T06:26:51.749616+08:00',
            nft_url:
              'https://calibration-ipfs.filswan.com/ipfs/QmPJUCw8W8VRiVcJjVdnYcfrfo5SsjWSbU7FJnfFSSHSdt',
            pin_status: 'Pinned',
            payload_cid: 'QmPJUCw8W8VRiVcJjVdnYcfrfo5SsjWSbU7FJnfFSSHSdt',
            w_cid:
              '3dae0417-77b0-4a3b-9dee-84bff63628acQmPJUCw8W8VRiVcJjVdnYcfrfo5SsjWSbU7FJnfFSSHSdt',
            status: 'success',
            deal_success: true,
            is_minted: true,
            token_id: '106144',
            mint_address: '0x8B6Ad2eD1151ae4cA664D0d44CE4d42307c91708',
            nft_tx_hash:
              '0x8e6b8eb6d0f408c6adac1c0d6d6a9d0b870ed514b1f7b78e7c6877ebd6751ad1',
          },
          issue_url: 'http://localhost:8000/api/issue/426/',
          faces: [
            {
              id: 677,
              face_album: 53,
              name: 'unknown_CDfE6',
              src: 'http://localhost:8000/media/face/face_CDfE6.jpg',
            },
          ],
          names: ['unknown_CDfE6'],
          colors: {
            img: 426,
            background: [
              {
                id: 101,
                r: 242,
                g: 198,
                b: 156,
                closest_palette_color_html_code: '#fcd29e',
                closest_palette_color: 'fair beige',
                closest_palette_color_parent: 'skin',
                closest_palette_distance: 4.03573799133301,
                percent: 78.964111328125,
                html_code: '#f2c69c',
                color: 426,
              },
              {
                id: 102,
                r: 110,
                g: 73,
                b: 51,
                closest_palette_color_html_code: '#6e493a',
                closest_palette_color: 'cinnamon',
                closest_palette_color_parent: 'brown',
                closest_palette_distance: 3.06844806671143,
                percent: 20.9036521911621,
                html_code: '#6e4933',
                color: 426,
              },
            ],
            foreground: [
              {
                id: 103,
                r: 231,
                g: 169,
                b: 120,
                closest_palette_color_html_code: '#d4a27c',
                closest_palette_color: 'medium rose-beige',
                closest_palette_color_parent: 'skin',
                closest_palette_distance: 4.19777202606201,
                percent: 59.6222991943359,
                html_code: '#e7a978',
                color: 426,
              },
              {
                id: 104,
                r: 127,
                g: 80,
                b: 53,
                closest_palette_color_html_code: '#7a5747',
                closest_palette_color: 'almond',
                closest_palette_color_parent: 'light brown',
                closest_palette_distance: 5.13545513153076,
                percent: 40.1577339172363,
                html_code: '#7f5035',
                color: 426,
              },
            ],
            image: [
              {
                id: 105,
                r: 239,
                g: 181,
                b: 127,
                closest_palette_color_html_code: '#ecb694',
                closest_palette_color: 'fair rose-beige',
                closest_palette_color_parent: 'skin',
                closest_palette_distance: 5.52706098556519,
                percent: 35.521183013916,
                html_code: '#efb57f',
                color: 426,
              },
              {
                id: 106,
                r: 251,
                g: 232,
                b: 207,
                closest_palette_color_html_code: '#fce2c4',
                closest_palette_color: 'light rose-beige',
                closest_palette_color_parent: 'skin',
                closest_palette_distance: 2.80652976036072,
                percent: 23.5606784820557,
                html_code: '#fbe8cf',
                color: 426,
              },
              {
                id: 107,
                r: 192,
                g: 121,
                b: 77,
                closest_palette_color_html_code: '#ac7654',
                closest_palette_color: 'dark rose-beige',
                closest_palette_color_parent: 'skin',
                closest_palette_distance: 4.81060171127319,
                percent: 20.8791217803955,
                html_code: '#c0794d',
                color: 426,
              },
              {
                id: 108,
                r: 102,
                g: 68,
                b: 48,
                closest_palette_color_html_code: '#6e493a',
                closest_palette_color: 'cinnamon',
                closest_palette_color_parent: 'brown',
                closest_palette_distance: 3.43346619606018,
                percent: 19.7065620422363,
                html_code: '#664430',
                color: 426,
              },
            ],
            color_variance: 30,
            object_percentage: 36.7733726501465,
            color_percent_threshold: 1.75,
          },
          src: 'http://localhost:8000/media/blue/img/1970/01/01/e8e4be52ba59a1a124665c82bb3f5ae2.jpeg',
          year: 1970,
          month: 1,
          day: 1,
          filename: 'e8e4be52ba59a1a124665c82bb3f5ae2.jpeg',
          type: 'jpeg',
          wid: 2560,
          height: 1440,
          aspect_ratio: '0.56',
          is_exist: true,
          title: null,
          caption: null,
          label: null,
          is_located: false,
          longitude_ref: 'E',
          longitude: 0.0,
          latitude_ref: 'N',
          latitude: 0.0,
          altitude_ref: 0.0,
          altitude: 0.0,
          location: null,
          district: null,
          city: null,
          province: null,
          country: null,
          flag: 0,
          rating: 0,
          capture_date: '1970-01-01',
          capture_time: '00:00:00',
          earthly_branches: 4,
          is_weekend: false,
          holiday_type: 0,
          digitized_date: null,
          camera_brand: null,
          camera_model: null,
          total_views: 0,
          likes: 0,
          is_publish: false,
          state: 0,
          created_at: '2022-09-11T06:23:15.498255+08:00',
          updated_at: '2022-09-11T06:23:23.385116+08:00',
          category: null,
          size: '2560-1440',
        },
      }
    },
    created() {
      this.fetchAlbum()
    },
    mounted() {
      const $window = $(window)
      $window.fetchAlbum = this.fetchAlbum // 把这个函数赋值给window，便于全局调用
      // 未铺满整个页面加载
      $window.scroll(function () {
        if (
          $window.scrollTop() >=
          $(document).height() - $window.height() - 10
        ) {
          // console.log('infinite-scroll-gallery: start reload the data')
          $window.fetchAlbum()
        }
      })
    },
    methods: {
      onGetAlbumId(index, id) {
        console.log('recieved the child component value %d,%d', index, id)
        // 声明这个函数，便于子组件调用
        this.checkedIndex = index
        this.checkedId = id
        this.fetchImg()
      },
      async fetchAlbum() {
        console.log('start to get the album...')
        if (this.albumLoading) return //incase fetch more data during the fetching time

        this.albumLoading = true
        if (this.curAlbumCnt < this.totalCount || this.totalCount === 0) {
          const { data, totalCount } = await getAlbum(this.queryForm)
          if (totalCount === 0) return //could fetch any data
          this.queryForm.page += 1
          console.log(
            'get img api result, data is %o, total is %d',
            data,
            totalCount
          )
          this.albums = [...this.albums, ...data]
          this.curAlbumCnt = this.albums.length
          this.totalCount = totalCount
          setTimeout(() => {
            this.albumLoading = false
          }, 300)
        } else {
          this.msg = 'there is no more img any more'
        }
      },
      async fetchImg() {
        console.log('start to get the img ...')
        this.queryForm.id = this.checkedId
        const { data } = await getImg(this.queryForm)
        // if (data.mcs !== null) {

        //   this.mcs = data.mcs
        // }
        this.img = data
        console.log(this.img)
      },
    },
  }
</script>

<style></style>
