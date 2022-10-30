<template>
  <div>
    <!-- <h1>这里是地点页的vue。。。</h1> -->
    <!-- 地图 -->
    <Map ref="map" :parking="parking" @callbackComponent="callbackComponent" />
  </div>
</template>

<script>
  import Map from '../../amap/index.vue'
  export default {
    name: 'PgAddress',
    components: { Map },
    data() {
      return {
        parking: [
          {
            position: [121.127403, 30.173497],
            content: `"<img src="http://localhost:8000/media/CACHE/images/blue/img/2021/02/09/IMG_20210209_160111/833e2409837910a3f0c5892336f16d16.jpg" style="width: 80px; " />"`,
            offset: [-15, -35],
            offsetText: [35, -58],
            label: { content: '11', offset: [10, 10] },
            text: `<div style="width: 60px; font-size: 20px; color: #ff0000; text-align: center;line-height: 50px; height: 60px;">20</div>`,
          },
          {
            position: [121.129509, 30.193517],
            content: `"<img src="http://localhost:8000/media/CACHE/images/blue/img/2021/02/09/IMG_20210209_160111/833e2409837910a3f0c5892336f16d16.jpg" style="width: 80px; " />"`,
            offset: [-15, -35],
            offsetText: [35, -58],
            label: { content: '11', offset: [10, 10] },
            text: `<div style="width: 60px; font-size: 20px; color: #ff0000; text-align: center;line-height: 50px; height: 60px;">20</div>`,
          },
          {
            position: [121.133509, 30.193517],
            content: `"<img src="http://localhost:8000/media/CACHE/images/blue/img/2021/02/09/IMG_20210209_160111/833e2409837910a3f0c5892336f16d16.jpg" style="width: 80px; " />"`,
            offset: [-15, -35],
            offsetText: [35, -58],
            label: { content: '11', offset: [10, 10] },
            text: `<div style="width: 60px; font-size: 20px; color: #ff0000; text-align: center;line-height: 50px; height: 60px;">20</div>`,
          },
          {
            position: [121.126509, 30.193517],
            content: `"<img src="http://localhost:8000/media/CACHE/images/blue/img/2021/02/09/IMG_20210209_160111/833e2409837910a3f0c5892336f16d16.jpg" style="width: 80px; " />"`,
            offset: [-15, -35],
            offsetText: [35, -58],
            label: { content: '11', offset: [10, 10] },
            text: `<div style="width: 60px; font-size: 20px; color: #ff0000; text-align: center;line-height: 50px; height: 60px;">20</div>`,
          },
          {
            position: [121.131509, 30.203517],
            content: `"<img src="http://localhost:8000/media/CACHE/images/blue/img/2021/02/09/IMG_20210209_160111/833e2409837910a3f0c5892336f16d16.jpg" style="width: 80px; " />"`,
            offset: [-15, -35],
            offsetText: [35, -58],
            label: { content: '11', offset: [10, 10] },
            text: `<div style="width: 60px; font-size: 20px; color: #ff0000; text-align: center;line-height: 50px; height: 60px;">20</div>`,
          },
        ],
        // cars_active_data: JSON.parse(localStorage.getItem('cars_active')),
      }
    },
    computed: {
      show() {
        const rotuer = this.$route
        return rotuer.name === 'Index' ? false : true
      },
    },
    watch: {},
    beforeMount() {
      // !this.order_no && this.getCarsActivation()
    },
    methods: {
      callbackComponent(params) {
        params.function && this[params.function](params.data)
      },
      // 地图初始化完成回调
      loadMap() {
        this.getParking()
      },
      // 获取停车场数据
      getParking() {
        // Parking().then((response) => {
        //   const data = response.data.data
        //   data.forEach((item) => {
        //     item.position = item.lnglat.split(',')
        //     item.content = 'demo'
        //     item.offset = [-35, -60]
        //     item.offsetText = [-30, -55]
        //     item.label = { content: '11', offset: [10, 10] }
        //     item.text = `<div style="width: 60px; font-size: 20px; color: #fff; text-align: center;line-height: 50px; height: 60px;">${item.carsNumber}</div>`
        //     item.events = {
        //       click: (e) => {
        //         this.$store.commit('app/SET_CARS_LIST_REQUEST', true)
        //         this.walking(e) // 路线规划
        //         this.getCarsList(e) // 车辆列表
        //       },
        //     }
        //   })
        //   this.parking = data
        // })
      },
      // walking(e) {
      //   const data = e.target.getExtData()
      //   this.$refs.map.saveData({
      //     key: 'parkingData',
      //     value: data,
      //   })
      //   this.$refs.map.handlerWalking(data.lnglat.split(','))
      // },
      // getCarsList(e) {
      //   const data = e.target.getExtData()
      //   // 父组件调子组件的方法
      //   this.$refs.cars && this.$refs.cars.getCarsList(data.id)
      // },
      // /** 获取正在使用的车辆 */
      // /**
      //  * 简单的接口优化
      //  * 1、查找缓存里面的 order_no，
      //  * 2、没有情况就请求接口，
      //  * 3、如果有就不请求
      //  */
      // getCarsActivation() {
      //   GetCarsActivation().then((response) => {
      //     const data = response.data
      //     if (data) {
      //       this.cars_active_data = data
      //       localStorage.setItem('cars_active', JSON.stringify(data))
      //     }
      //   })
      // },
      // /** 取车 */
      // carsGet() {
      //   CarsGet({
      //     order_no: this.cars_active_data.order_no,
      //     cars_id: this.cars_active_data.cars_id,
      //   }).then((response) => {
      //     const data = response.data
      //     if (data && data.order_status) {
      //       this.$set(this.cars_active_data, 'order_status', data.order_status)
      //       localStorage.setItem(
      //         'cars_active',
      //         JSON.stringify(this.cars_active_data)
      //       )
      //     }
      //   })
      // },
      // /** 取车 */
      // carsReturn() {
      //   CarsReturn({
      //     order_no: this.cars_active_data.order_no,
      //     cars_id: this.cars_active_data.cars_id,
      //   }).then((response) => {
      //     this.$message({
      //       message: response.message,
      //       type: 'success',
      //     })
      //     this.cars_active_data = null
      //     localStorage.removeItem('cars_active')
      //   })
      // },
      // /** 取消 */
      // carsCancel() {
      //   CarsCancel({
      //     order_no: this.cars_active_data.order_no,
      //     cars_id: this.cars_active_data.cars_id,
      //   }).then((response) => {
      //     this.$message({
      //       message: response.message,
      //       type: 'success',
      //     })
      //     this.cars_active_data = null
      //     localStorage.removeItem('cars_active')
      //   })
      // },
    },
  }
</script>

<style></style>
