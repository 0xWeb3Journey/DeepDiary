<template>
  <div class="amap-wrap">
    <el-amap
      ref="map"
      vid="amapContainer"
      :center="center"
      :zoom="zoom"
      view-mode="2D"
      class="amap-demo"
      @init="initMap"
      @click="clickMap"
      @complete="initMapComplete"
    >
      <!-- 浏览器定位 -->
      <el-amap-control-geolocation
        ref="location"
        :zoom-to-accuracy="true"
        :pan-to-location="true"
        :convert="true"
        position="LT"
        :offset="[5, 5]"
        extensions="all"
        @complete="getLocation"
      ></el-amap-control-geolocation>

      <!-- 点聚合 -->
      <el-amap-marker-cluster
        ref="cluster"
        :visible="visible"
        :points="points"
        @init="markerInit"
        @click="clickMarker"
      ></el-amap-marker-cluster>

      <!-- 搜索框 -->
      <el-amap-search-box
        ref="search"
        :visible="visible"
        @select="selectPoi"
        @choose="choosePoi"
      ></el-amap-search-box>

      <!-- 地图类型 -->
      <el-amap-control-map-type></el-amap-control-map-type>

      <!-- 操作工具条 -->
      <el-amap-control-tool-bar></el-amap-control-tool-bar>

      <!-- 比例尺 -->
      <el-amap-control-scale :visible="visible"></el-amap-control-scale>

      <!-- 覆盖物圆: 搜索结果 -->
      <!-- <el-amap-circle
        v-for="item in circles"
        :key="item.id"
        :center="item.center"
        :radius="item.radius"
        :fill-color="item.color"
        :stroke-color="item.color"
        :stroke-opacity="item.strokeOpacity"
        :stroke-weight="item.strokeWeight"
      ></el-amap-circle> -->

      <!-- 覆盖物圆: 搜索结果 -->
      <el-amap-circle-marker
        :center="poi.location"
        @click="
          (e) => {
            clickpoi(poi, e)
          }
        "
      ></el-amap-circle-marker>

      <!-- <el-amap-circle
        :center="[121.127403, 30.173497]"
        radius="100px"
      ></el-amap-circle> -->

      <!-- 覆盖物-停车场 -->
      <!-- <el-amap-marker
        v-for="(item, index) in parking"
        :key="item.id"
        :offset="item.offset"
        :content="item.content"
        :position="item.position"
        :vid="index"
      ></el-amap-marker> -->
      <!-- 覆盖物 -->
      <!-- <el-amap-marker
        v-for="(item, index) in parking"
        :key="index"
        :ext-data="item"
        :events="item.events"
        :offset="item.offsetText"
        :content="item.text"
        :position="item.position"
        :vid="index"
      ></el-amap-marker> -->
      <!--覆盖物 - 停车场 - 距离信息-->
      <!-- <el-amap-marker
        v-for="(item, index) in parkingInfo"
        :key="item.id"
        z-index="1000"
        :content="item.text"
        :offset="item.offset"
        :position="item.position"
        :vid="index"
      ></el-amap-marker> -->
    </el-amap>
  </div>
</template>

<script>
  // import { AMapManager, lazyAMapApiLoaderInstance } from 'vue-amap'
  import VueAMap from '@vuemap/vue-amap'
  import { lazyAMapApiLoaderInstance } from '@vuemap/vue-amap'
  import { SelfLocation } from './location'
  import { Walking } from './walking'
  import StyleCss from './style'
  import '@/plugins/aMap'
  // let amapManager = new AMapManager()

  import AMapLoader from '@amap/amap-jsapi-loader'

  export default {
    name: 'Map',
    props: {
      parking: {
        type: Array,
        default: () => [
          {
            id: 1,
            content: '',
            position: [],
            offset: [],
          },
        ],
      },
    },

    data() {
      const _this = this
      return {
        // map: null,

        // map attribute
        center: [116.127808, 30.173239],
        zoom: 12,
        self_lng: '',
        self_lat: '',

        circles: [],
        // 停车场位置
        parkingData: {},
        // 停车场信息
        parkingInfo: [],
        visible: true,
        points: [
          { lnglat: ['121.127808', '30.173239'] },
          { lnglat: ['121.227808', '30.973239'] },
          { lnglat: ['121.123808', '29.175539'] },
          { lnglat: ['121.427808', '30.473239'] },
          { lnglat: ['121.157808', '32.654322'] },
          { lnglat: ['121.876543', '30.673239'] },
          { lnglat: ['121.177808', '30.473239'] },
          { lnglat: ['122.727808', '30.373239'] },
          { lnglat: ['118.125808', '30.273239'] },
          { lnglat: ['123.345675', '31.987654'] },
          { lnglat: ['121.098753', '30.373239'] },
        ], // cluster marker points
        auto: null,
        placeSearch: null, // poi search instance
        searchPlaceInput: '',

        poi: {
          location: [116.127808, 30.173239],
          district: '',
          name: '',
          typecode: '',
        },
      }
    },
    watch: {},
    mounted() {
      // lazyAMapApiLoaderInstance.then(() => {
      //   // your code ...
      //   new AMap.Map('amapContainer', {
      //     center: new AMap.LngLat(121.127808, 30.173239),
      //     zoom: this.zoom,
      //   })
      // })
    },
    beforeDestroy() {
      console.log('beforeDestroy')
      // 销毁地图，并清空地图容器
      this.map.destroy()
    },
    methods: {
      // map functions
      clickMap(e) {
        // console.log('click map :', e)
        console.log('click map :', e.lnglat.lng, e.lnglat.lat)
        this.map.setCenter([e.lnglat.lng, e.lnglat.lat])

        this.poi.location = [e.lnglat.lng, e.lnglat.lat]
      },
      initMap(map) {
        console.log('init map: ', map)
        this.map = this.$refs.map.$$getInstance()
        // this.map.on('complete', this.initMapComplete)
      },
      initMapComplete() {
        // 地图图块加载完成后触发
        console.log('finish loading the map ')
        let geolocation = this.$refs.location.$$getInstance()
        geolocation.getCurrentPosition(this.onLocationComplete)
      },
      // location functions
      onLocationComplete(status, result) {
        console.log('onLocationComplete: ')
        if (status == 'complete') {
          this.onLocationSuccess(result)
        } else {
          this.onLocationError(result)
        }
      },
      onLocationSuccess(data) {
        var str = []
        str.push('定位结果：' + data.position)
        str.push('定位类别：' + data.location_type)
        if (data.accuracy) {
          str.push('精度：' + data.accuracy + ' 米')
        } //如为IP精确定位结果则没有精度信息
        str.push('是否经过偏移：' + (data.isConverted ? '是' : '否'))
        console.log(str)
      },
      onLocationError(result) {
        var str = []
        str.push(
          '失败原因排查信息' +
            data.message +
            '</br>浏览器返回信息：' +
            data.originMessage
        )
        console.log(str)
      },
      getLocation(e) {
        console.log('getLocation: ', e.position.lat, e.position.lng)
        this.lat = e.position.lat
        this.lng = e.position.lng
      },
      // marker fuctions
      markerInit(e) {
        console.log('marker init: ', e)
      },
      clickMarker(e) {
        alert('点击了标号')
        console.log('marker click: ', e)
        // this.map.setZoom(5)
      },
      // poi fuctions
      selectPoi(e) {
        console.log('selectPoi: ', e)
        if (this.placeSearch !== null) {
          this.placeSearch.clear()
        } //构造地点查询类

        this.zoom = 18
        this.center = [e.poi.location.lng, e.poi.location.lat]
        this.poi.location = [e.poi.location.lng, e.poi.location.lat]
        this.poi.district = e.poi.district
        this.poi.name = e.poi.name
        this.poi.typecode = e.poi.typecode

        // this.map.setZoom(5)
      },
      choosePoi(e) {
        console.log('choosePoi: ', e)
        if (this.placeSearch === null) {
          this.placeSearch = new AMap.PlaceSearch({
            map: this.map,
          }) //构造地点查询类
        }

        this.placeSearch.setCity(e.poi.adcode)
        this.placeSearch.search(e.poi.name) //关键字查询查询
        console.log('PoiList:', this.placeSearch.PoiList)
      },
      clickpoi(marker) {
        console.log('点击了标号,标号ID： %o', marker)
      },
    },
  }
</script>

<style lang="scss">
  .amap-wrap {
    // height: 100vh;
    height: 80vh;
  }
  .el-vue-search-box-container {
    position: absolute;
    left: 45px;
    top: 5px;
    z-index: 10;
    width: 300px;
    height: 30px;
    background: #fff;
    box-shadow: 0 2px 2px rgb(0 0 0 / 15%);
    border-radius: 2px 3px 3px 2px;
  }
</style>
