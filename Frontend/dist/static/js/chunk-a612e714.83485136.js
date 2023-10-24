/*!
 *  build: vue-admin-better 
 *  vue-admin-beautiful.com 
 *  https://gitee.com/chu1204505056/vue-admin-better 
 *  time: 2023-10-24 19:41:02
 */
(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-a612e714"],{"1c46":function(e,t,l){"use strict";l("ea93")},"1d44":function(e,t,l){"use strict";l.r(t);var i=function(){var e=this,t=e.$createElement,l=e._self._c||t;return l("div",{staticClass:"img-container"},[l("DetailHead",{attrs:{content:"图片详情"}}),l("div",{staticClass:"img_wrap"},[l("el-image",{staticClass:"imgDetail",attrs:{src:e.img.src,lazy:""}})],1),l("Tags",{attrs:{items:e.img.tags}}),l("Album",{ref:"album",attrs:{title:"Person",type:"person",items:e.img.profiles,total:e.totalPerson},on:{albumClick:e.onGetAlbumId,doubleClick:e.onRouteJump}}),l("div",{staticClass:"amap-wrap"},[l("el-amap",{ref:"map",staticClass:"amap-demo",attrs:{vid:"amapContainer",center:e.img.lnglat,zoom:18,"view-mode":"2D"}},[l("el-amap-marker",{attrs:{position:e.img.lnglat}})],1)],1),l("h3",[e._v(e._s(e.img.address.location))]),e.img.colors?l("Color",{attrs:{colors:e.img.colors}}):e._e()],1)},a=[],o=l("970f"),s=l("9b5c"),c=(l("41cf"),l("937c"),l("abc8")),n=l("d7fb"),r=l("705f"),d=(l("203a"),{name:"Img",components:{Album:s["default"],Tags:c["default"],Color:n["default"],DetailHead:r["default"]},beforeRouteEnter(e,t,l){console.log("beforeRouteEnter...."),l()},beforeRouteLeave(e,t,l){console.log("beforeRouteLeave...."),l()},props:{id:{type:Number,default:113,required:!1},name:{type:String,default:"照片详情",required:!1}},data(){return{img:{id:434,user:"blue",tags:"people,family,爷爷,奶奶",thumb:"http://localhost:8000/media/CACHE/images/blue/img/2021/09/19/IMG_20210919_110530_lAcSgku/161945f6ee4f8c09e9c27f350ce65132.jpg",img_url:"http://localhost:8000/api/img/434/",issue_url:"http://localhost:8000/api/issue/434/",faces:[{id:687,face_album:48,name:"奶奶",src:"http://localhost:8000/media/face/face_28Ee5.jpg"},{id:686,face_album:50,name:"爷爷",src:"http://localhost:8000/media/face/face_67OCn.jpg"}],names:["奶奶","爷爷"],mcs:null,colors:{img:434,background:[{id:144,r:170,g:166,b:161,closest_palette_color_html_code:"#9f9c99",closest_palette_color:"cathedral",closest_palette_color_parent:"grey",closest_palette_distance:3.22788548469543,percent:64.1514358520508,html_code:"#aaa6a1",color:434},{id:145,r:110,g:99,b:87,closest_palette_color_html_code:"#7a5747",closest_palette_color:"almond",closest_palette_color_parent:"light brown",closest_palette_distance:10.5113162994385,percent:30.0297298431396,html_code:"#6e6357",color:434},{id:146,r:39,g:36,b:38,closest_palette_color_html_code:"#3a3536",closest_palette_color:"graphite",closest_palette_color_parent:"black",closest_palette_distance:5.65835523605347,percent:5.81883382797241,html_code:"#272426",color:434}],foreground:[{id:147,r:37,g:36,b:45,closest_palette_color_html_code:"#2b2e43",closest_palette_color:"navy blue",closest_palette_color_parent:"navy blue",closest_palette_distance:6.52309560775757,percent:55.4630889892578,html_code:"#25242d",color:434},{id:148,r:152,g:117,b:99,closest_palette_color_html_code:"#ac7654",closest_palette_color:"dark rose-beige",closest_palette_color_parent:"skin",closest_palette_distance:6.76996755599976,percent:23.6442947387695,html_code:"#987563",color:434},{id:149,r:133,g:145,b:195,closest_palette_color_html_code:"#81a0d4",closest_palette_color:"periwinkle",closest_palette_color_parent:"light blue",closest_palette_distance:6.60187721252441,percent:20.8926162719727,html_code:"#8591c3",color:434}],image:[{id:150,r:172,g:169,b:165,closest_palette_color_html_code:"#9f9c99",closest_palette_color:"cathedral",closest_palette_color_parent:"grey",closest_palette_distance:3.92975735664368,percent:44.0937881469727,html_code:"#aca9a5",color:434},{id:151,r:111,g:99,b:88,closest_palette_color_html_code:"#7a5747",closest_palette_color:"almond",closest_palette_color_parent:"light brown",closest_palette_distance:9.85335826873779,percent:26.4559421539307,html_code:"#6f6358",color:434},{id:152,r:36,g:35,b:42,closest_palette_color_html_code:"#39373b",closest_palette_color:"black",closest_palette_color_parent:"black",closest_palette_distance:6.68468189239502,percent:17.472957611084,html_code:"#24232a",color:434},{id:153,r:172,g:138,b:110,closest_palette_color_html_code:"#ac8a64",closest_palette_color:"light brown",closest_palette_color_parent:"skin",closest_palette_distance:3.47950530052185,percent:6.38603115081787,html_code:"#ac8a6e",color:434},{id:154,r:129,g:141,b:192,closest_palette_color_html_code:"#81a0d4",closest_palette_color:"periwinkle",closest_palette_color_parent:"light blue",closest_palette_distance:7.39144563674927,percent:5.59128093719482,html_code:"#818dc0",color:434}],color_variance:27,object_percentage:24.5679988861084,color_percent_threshold:1.75},dates:{img:434,year:2021,month:9,day:19,capture_date:"2021-09-19",capture_time:"11:05:30",earthly_branches:2,is_weekend:!0,holiday_type:0,digitized_date:null},evaluates:{img:434,flag:0,rating:3,total_views:0,likes:0},address:{img:434,is_located:!0,country:"中国",province:"浙江省",city:"台州市",district:"临海市",location:"浙江省台州市临海市杜桥镇石道地",lnglat:[121.518013,28.72691]},src:"",name:"",type:"jpg",wid:1904,height:4096,aspect_ratio:"2.15",is_exist:!0,title:null,caption:null,label:null,camera_brand:"HUAWEI",camera_model:"NOH-AN00",is_publish:!1,state:0,created_at:"2022-09-23T21:46:01.951693+08:00",updated_at:"2022-09-23T22:42:37.217883+08:00",size:"1904-4096",lnglat:[121.518013,28.72691]},checkedIndex:0,checkedId:0,totalPerson:0,ImgQueryForm:{id:0}}},watch:{"img.tags"(e,t){},deep:!0},created(){console.log("img vue created")},mounted(){console.log("img vue mounted")},activated(){console.log("the img component is activated"),this.fetchImgDetail()},deactivated(){console.log("the img component is deactivated")},methods:{onGetAlbumId(e,t){console.log("recieved the child component value %d,%o",e,t),this.checkedIndex=e,this.checkedId=t.face_album,this.checkedId=t.id},onRouteJump(e,t){console.log("album double click event item is  %d,%o, start join to FaceGallery",e,t),this.$router.push({name:"ProfileDetail",query:{id:t.id,title:t.name}})},async fetchImgDetail(){console.log("start to get the img, id is : ",this.$route.query.id),this.ImgQueryForm.id=this.$route.query.id;const{data:e}=await Object(o["getImgDetail"])(this.ImgQueryForm.id);console.log(e),this.img=e,this.totalPerson=this.img.profiles.length}}}),u=d,m=(l("9936"),l("2877")),p=Object(m["a"])(u,i,a,!1,null,"a8885b0c",null);t["default"]=p.exports},"203a":function(e,t,l){"use strict";l.r(t);var i=l("a026"),a=l("544d"),o=l.n(a);l("9466");i["default"].use(o.a),o.a.initAMapApiLoader({key:"966044df467348180e9bc1276a7f7d2f",version:"2.0",plugins:["AMap.Geolocation","AMap.Walking","AMap.MapType","AMap.MarkerCluster","AMap.AutoComplete","AMap.PlaceSearch","AMap.Scale","AMap.OverView","AMap.ToolBar","AMap.PolyEditor","AMap.CircleEditor","AMap.Weather"]}),window._AMapSecurityConfig={securityJsCode:"aa6935254da67f77412663214c4bff37"}},"41cf":function(e,t,l){"use strict";l.r(t);var i=function(){var e=this,t=e.$createElement,l=e._self._c||t;return l("div",{staticClass:"album_container"},[l("div",{directives:[{name:"infinite-scroll",rawName:"v-infinite-scroll",value:e.load,expression:"load"}],ref:"album_container",staticClass:"content",attrs:{id:"album_container","infinite-scroll-disabled":"busy","infinite-scroll-distance":"400","infinite-scroll-immediate-check":"true","force-use-infinite-wrapper":!0}},[e._l(e.items,(function(t,i){return l("div",{key:t.id,on:{click:function(l){return e.onClick(l,i,t)},dblclick:function(l){return e.onDoubleClick(l,i,t)}}},[l("el-tooltip",{attrs:{content:t.caption?t.caption:"No Caption",placement:"top"}},[l("img",{class:e.checkedIndex===i?"img-checked":"img-unchecked",attrs:{className:"img-responsive",src:t.thumb,alt:t.name}})]),l("div",{staticClass:"jg-caption"},[l("el-badge",{staticClass:"item",attrs:{value:t.value,max:99,type:"primary"}},[l("el-input",{staticClass:"item-name",staticStyle:{float:"left","font-size":"8px"},attrs:{size:"small",placeholder:"Change the Name"},on:{blur:function(l){return e.changeName(t.name,t)}},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.enterBlur(t)}},model:{value:t.name,callback:function(l){e.$set(t,"name",l)},expression:"item.name"}})],1)],1)],1)})),l("div",{directives:[{name:"show",rawName:"v-show",value:e.busy,expression:"busy"}],staticClass:"loading"},[l("h3",[e._v(e._s(e.msg))])])],2),l("el-divider",{directives:[{name:"show",rawName:"v-show",value:e.finished,expression:"finished"}]},[l("i",{staticClass:"el-icon-finished"})])],1)},a=[],o=l("1157"),s=l.n(o),c=(l("cfd5"),l("a809"),l("487a")),n=l.n(c),r={name:"AlbumContainer",directives:{infiniteScroll:n.a},props:{items:{type:Array,default:()=>Array(40).fill({}),required:!0},total:{type:Number,default:50,required:!0},title:{type:String,default:"Album",required:!0},busy:{type:Boolean,default:!1,required:!0},finished:{type:Boolean,default:!1,required:!1}},data(){return{msg:"正在加载...",intervalId:null,checkedIndex:-1,checkedId:0}},watch:{items(e,t){console.log("Album.content: Album numbers have been changed",e.length,this.total,this.msg),this.$nextTick(()=>{s()("#album_container").justifiedGallery()}),this.checkDivHeight()}},created(){console.log("Album.content: Album component created")},mounted(){this.justifyInit()},activated(){console.log("Album contetn: activated"),this.checkDivHeight()},deactivated(){console.log("Album contetn: deactivated"),clearInterval(this.intervalId),this.intervalId=null},methods:{justifyInit:function(){s()("[id=album_container]").justifiedGallery({captions:!0,lastRow:"left",rowHeight:150,margins:5}).on("jg.complete",(function(){console.log("Album.content: jg.complete event was trigged")}))},onClick(e,t,l){console.log("Album.content: onClick: ",l),this.checkedIndex=t,t<0||null!==l&&(this.checkedId=l.id,this.$emit("albumClick",t,l))},onDoubleClick(e,t,l){console.log("Album.content: onDoubleClick"),this.$emit("doubleClick",t,l)},changeName(e,t){console.log("Album.content: changeName"),this.$emit("changeName",e,t)},enterBlur(e){console.log("Album.content: enterBlur"),e.target.blur()},load(){console.log("infinite loading... ",this.busy),this.busy||this.$emit("load")},checkDivHeight(){if(null===this.intervalId){var e=this.$refs.album_container;e&&(this.intervalId=setInterval(()=>{if(!1===this.busy){var t=e.scrollHeight,l=e.scrollTop,i=1e3;console.log("Gallery Contetn: checkDivHeight:divElement: The div is not filled.",l,t,i,this.finished),t>i||this.finished?(clearInterval(this.intervalId),this.intervalId=null,console.log("timer has been closed")):this.$emit("load")}},1e3))}else console.log("Gallery content: checkDivHeight: intervalId is not null")}}},d=r,u=(l("689c"),l("2877")),m=Object(u["a"])(d,i,a,!1,null,"9f13ec50",null);t["default"]=m.exports},"498e":function(e,t,l){},"51ad":function(e,t,l){"use strict";l("6e35")},"5d1d":function(e,t,l){e.exports={"menu-color":"rgba(255,255,255,.95)","menu-color-active":"rgba(255,255,255,.95)","menu-background":"#21252b"}},"635a":function(e,t,l){"use strict";l.r(t);var i=function(){var e=this,t=e.$createElement,l=e._self._c||t;return l("el-dialog",{attrs:{"before-close":e.handleClose,"close-on-click-modal":!1,title:e.title,visible:e.dialogFormVisible,width:"909px"},on:{"update:visible":function(t){e.dialogFormVisible=t}}},[l("div",{staticClass:"upload"},[l("el-alert",{attrs:{closable:!1,title:"支持jpg、jpeg、png格式，单次可最多选择"+e.limit+"张图片，每张不可大于"+e.size+"M，如果大于"+e.size+"M会自动为您过滤",type:"info"}}),l("br"),l("el-upload",{ref:"upload",staticClass:"upload-content",attrs:{action:e.action,"auto-upload":!1,"close-on-click-modal":!1,data:e.data,"file-list":e.fileList,headers:e.headers,limit:e.limit,multiple:!0,name:e.name,"on-change":e.handleChange,"on-error":e.handleError,"on-exceed":e.handleExceed,"on-preview":e.handlePreview,"on-progress":e.handleProgress,"on-remove":e.handleRemove,"on-success":e.handleSuccess,accept:"image/png, image/jpeg","list-type":"picture-card"}},[l("i",{staticClass:"el-icon-plus",attrs:{slot:"trigger"},slot:"trigger"}),l("el-dialog",{attrs:{visible:e.dialogVisible,"append-to-body":"",title:"查看大图"},on:{"update:visible":function(t){e.dialogVisible=t}}},[l("div",[l("img",{attrs:{src:e.dialogImageUrl,alt:"",width:"100%"}})])])],1)],1),l("div",{staticClass:"dialog-footer",staticStyle:{position:"relative","padding-right":"15px","text-align":"right"},attrs:{slot:"footer"},slot:"footer"},[e.show?l("div",{staticStyle:{position:"absolute",top:"10px",left:"15px",color:"#999"}},[e._v(" 正在上传中... 当前上传成功数:"+e._s(e.imgSuccessNum)+"张 当前上传失败数:"+e._s(e.imgErrorNum)+"张 ")]):e._e(),l("el-button",{attrs:{type:"primary"},on:{click:e.handleClose}},[e._v("关闭")]),l("el-button",{staticStyle:{"margin-left":"10px"},attrs:{loading:e.loading,size:"small",type:"success"},on:{click:e.submitUpload}},[e._v(" 开始上传 ")])],1)])},a=[],o=l("f121"),s=l("4360"),c=l("970f"),n={name:"Upload",props:{url:{type:String,default:"api/img/",required:!0},name:{type:String,default:"src",required:!0},limit:{type:Number,default:500,required:!0},size:{type:Number,default:8,required:!0}},data(){return{show:!1,loading:!1,dialogVisible:!1,dialogImageUrl:"",action:o["baseURL"]+this.url,headers:{Authorization:"Bearer "+s["default"].getters["user/accessToken"]},fileList:[],picture:"picture",imgNum:0,imgSuccessNum:0,imgErrorNum:0,typeList:null,title:"上传",dialogFormVisible:!1,data:{}}},computed:{percentage(){return 0==this.allImgNum?0:100*this.$baseLodash.round(this.imgNum/this.allImgNum,2)}},methods:{submitUpload(){this.api=`${window.location.protocol}//${window.location.host}`,this.action=this.api+this.url,console.log("this.action:",this.action,"production",o["baseURL"]),this.$refs.upload.submit()},handleProgress(e,t,l){this.loading=!0,this.show=!0},handleChange(e,t){e.size>1048576*this.size?(t.map((l,i)=>{l===e&&t.splice(i,1)}),this.fileList=t):this.allImgNum=t.length},handleSuccess(e,t,l){this.imgNum=this.imgNum+1,this.imgSuccessNum=this.imgSuccessNum+1,l.length===this.imgNum&&setTimeout(()=>{this.$baseMessage(`上传完成! 共上传${l.length}张图片`,"success")},1e3),setTimeout(()=>{this.loading=!1,this.show=!1},1e3)},handleError(e,t,l){this.imgNum=this.imgNum+1,this.imgErrorNum=this.imgErrorNum+1,this.$baseMessage(`文件[${t.raw.name}]上传失败,文件大小为${this.$baseLodash.round(t.raw.size/1024,0)}KB`,"error"),setTimeout(()=>{this.loading=!1,this.show=!1},1e3)},handleRemove(e,t){this.imgNum=this.imgNum-1,this.allNum=this.allNum-1},handlePreview(e){this.dialogImageUrl=e.url,this.dialogVisible=!0},handleExceed(e,t){this.$baseMessage(`当前限制选择 ${this.limit} 个文件，本次选择了\n           ${e.length}\n           个文件`,"error")},handleShow(e){this.title="上传",this.data=e,this.dialogFormVisible=!0},handleClose(){this.fileList=[],this.picture="picture",this.allImgNum=0,this.imgNum=0,this.imgSuccessNum=0,this.imgErrorNum=0,this.uploadFinished(),this.dialogFormVisible=!1},async uploadFinished(){console.log("handleClose");const{msg:e}=await Object(c["getUploadState"])("");this.$message({message:e,type:"success"})}}},r=n,d=(l("73d2"),l("2877")),u=Object(d["a"])(r,i,a,!1,null,"2c7c9ebb",null);t["default"]=u.exports},"689c":function(e,t,l){"use strict";l("d0ee")},"6e35":function(e,t,l){},"705f":function(e,t,l){"use strict";l.r(t);var i=function(){var e=this,t=e.$createElement,l=e._self._c||t;return l("div",{staticClass:"header-container"},[l("el-page-header",{attrs:{content:e.content},on:{back:e.goBack}})],1)},a=[],o={name:"DetailHead",components:{},props:{content:{type:String,default:"人脸详情",required:!0}},methods:{goBack(){console.log("go back"),this.$router.go(-1)},handleCommand(e){this.$message("click on item "+e),this.$emit(e)}}},s=o,c=(l("1c46"),l("2877")),n=Object(c["a"])(s,i,a,!1,null,null,null);t["default"]=n.exports},"73d2":function(e,t,l){"use strict";l("db9f")},"937c":function(e,t,l){"use strict";l.r(t);var i=function(){var e=this,t=e.$createElement,l=e._self._c||t;return l("div",{staticClass:"mcs-container"},[l("div",{ref:"mcs",attrs:{id:"mcs"}},[null!==e.mcs?l("el-descriptions",{staticClass:"margin-top",attrs:{title:e.title,extra:"Extra",column:3,size:"small",border:""}},[l("template",{slot:"extra"},[l("el-button",{attrs:{type:"primary",size:"small"}},[e._v("Sync")])],1),l("el-descriptions-item",[l("template",{slot:"label"},[l("i",{staticClass:"el-icon-user"}),e._v(" id ")]),e._v(" "+e._s(e.mcs.id)+" ")],2),l("el-descriptions-item",[l("template",{slot:"label"},[l("i",{staticClass:"el-icon-mobile-phone"}),e._v(" file_upload_id ")]),e._v(" "+e._s(e.mcs.file_upload_id)+" ")],2),l("el-descriptions-item",[l("template",{slot:"label"},[l("i",{staticClass:"el-icon-location-outline"}),e._v(" file_name ")]),e._v(" "+e._s(e.mcs.file_name)+" ")],2),l("el-descriptions-item",[l("template",{slot:"label"},[l("i",{staticClass:"el-icon-tickets"}),e._v(" file_size ")]),e._v(" "+e._s(e.mcs.file_size)+" ")],2),l("el-descriptions-item",[l("template",{slot:"label"},[l("i",{staticClass:"el-icon-office-building"}),e._v(" nft_url ")]),l("el-link",{attrs:{type:"primary",href:e.mcs.nft_url,target:"_blank"}},[e._v(" "+e._s(e.mcs.nft_url)+" ")])],2),l("el-descriptions-item",[l("template",{slot:"label"},[l("i",{staticClass:"el-icon-office-building"}),e._v(" pin_status ")]),e._v(" "+e._s(e.mcs.pin_status)+" ")],2),l("el-descriptions-item",[l("template",{slot:"label"},[l("i",{staticClass:"el-icon-office-building"}),e._v(" payload_cid ")]),e._v(" "+e._s(e.mcs.payload_cid)+" ")],2),l("el-descriptions-item",[l("template",{slot:"label"},[l("i",{staticClass:"el-icon-office-building"}),e._v(" w_cid ")]),e._v(" "+e._s(e.mcs.w_cid)+" ")],2),l("el-descriptions-item",[l("template",{slot:"label"},[l("i",{staticClass:"el-icon-office-building"}),e._v(" status ")]),e._v(" "+e._s(e.mcs.status)+" ")],2),l("el-descriptions-item",[l("template",{slot:"label"},[l("i",{staticClass:"el-icon-office-building"}),e._v(" deal_success ")]),e._v(" "+e._s(e.mcs.deal_success)+" ")],2),l("el-descriptions-item",[l("template",{slot:"label"},[l("i",{staticClass:"el-icon-office-building"}),e._v(" is_minted ")]),e._v(" "+e._s(e.mcs.is_minted)+" ")],2),l("el-descriptions-item",[l("template",{slot:"label"},[l("i",{staticClass:"el-icon-office-building"}),e._v(" token_id ")]),e._v(" "+e._s(e.mcs.token_id)+" ")],2),l("el-descriptions-item",[l("template",{slot:"label"},[l("i",{staticClass:"el-icon-office-building"}),e._v(" mint_address ")]),e._v(" "+e._s(e.mcs.mint_address)+" ")],2),l("el-descriptions-item",[l("template",{slot:"label"},[l("i",{staticClass:"el-icon-office-building"}),e._v(" nft_tx_hash ")]),e._v(" "+e._s(e.mcs.nft_tx_hash)+" ")],2)],2):l("el-alert",{attrs:{title:" this image haven't been synchronized to mcs yet",type:"warning"}})],1)])},a=[],o=(l("1157"),l("970f"),{name:"Mcs",components:{},props:{mcs:{type:Object,default:function(){return{id:426,file_upload_id:478656,file_name:"e8e4be52ba59a1a124665c82bb3f5ae2.jpeg",file_size:259215,updated_at:"2022-09-11T06:26:51.749616+08:00",nft_url:"https://calibration-ipfs.filswan.com/ipfs/QmPJUCw8W8VRiVcJjVdnYcfrfo5SsjWSbU7FJnfFSSHSdt",pin_status:"Pinned",payload_cid:"QmPJUCw8W8VRiVcJjVdnYcfrfo5SsjWSbU7FJnfFSSHSdt",w_cid:"3dae0417-77b0-4a3b-9dee-84bff63628acQmPJUCw8W8VRiVcJjVdnYcfrfo5SsjWSbU7FJnfFSSHSdt",status:"success",deal_success:!0,is_minted:!0,token_id:"106144",mint_address:"0x8B6Ad2eD1151ae4cA664D0d44CE4d42307c91708",nft_tx_hash:"0x8e6b8eb6d0f408c6adac1c0d6d6a9d0b870ed514b1f7b78e7c6877ebd6751ad1"}}},mcstype:{type:String,default:"img",required:!1},title:{type:String,default:"",required:!1}},data(){return{}},computed:{},watch:{},created(){},mounted(){},methods:{}}),s=o,c=l("2877"),n=Object(c["a"])(s,i,a,!1,null,"a221ed0a",null);t["default"]=n.exports},"970f":function(e,t,l){"use strict";l.r(t),l.d(t,"getImg",(function(){return a})),l.d(t,"getImgDetail",(function(){return o})),l.d(t,"getMcs",(function(){return s})),l.d(t,"getTags",(function(){return c})),l.d(t,"getUploadState",(function(){return n})),l.d(t,"getProfile",(function(){return r})),l.d(t,"getProfileDetail",(function(){return d})),l.d(t,"changeFaceAlbumName",(function(){return u})),l.d(t,"clear_face_album",(function(){return m})),l.d(t,"getFace",(function(){return p})),l.d(t,"changeFaceName",(function(){return _})),l.d(t,"getFaceGallery",(function(){return h})),l.d(t,"doEdit",(function(){return g})),l.d(t,"doDelete",(function(){return f})),l.d(t,"upload",(function(){return b})),l.d(t,"getFilterList",(function(){return v})),l.d(t,"getAddress",(function(){return y}));var i=l("b775");function a(e){return Object(i["default"])({url:"/api/img/",method:"get",params:e})}function o(e){return Object(i["default"])({url:"/api/img/"+e+"/",method:"get"})}function s(e){return Object(i["default"])({url:"/api/mcs/"+e.id+"/",method:"get"})}function c(e){return Object(i["default"])({url:"/api/img/"+e.id+" / set_tags/",method:"get"})}function n(e){return Object(i["default"])({url:"/api/img/upload_finished/",method:"get"})}function r(e){return Object(i["default"])({url:"/api/profile/",method:"get",params:e})}function d(e){return Object(i["default"])({url:"/api/profile/"+e.id+"/",method:"get",params:e})}function u(e){return Object(i["default"])({url:"/api/profile/"+e.id+"/",method:"put",data:e})}function m(e){return Object(i["default"])({url:"/api/profile/clear_face_album/",method:"get"})}function p(e){return Object(i["default"])({url:"/api/face/"+e.id+"/",method:"get"})}function _(e){return Object(i["default"])({url:"/api/face/"+e.id+"/",method:"put",data:e})}function h(e){return console.log(e),Object(i["default"])({url:"/api/face/",method:"get",params:e})}function g(e){return Object(i["default"])({url:"/gallery/doEdit",method:"post",data:e})}function f(e){return Object(i["default"])({url:"/gallery/doDelete",method:"post",data:e})}function b(e){return Object(i["default"])({url:"/api/img/",method:"post",data:e})}function v(e){return console.log(e),Object(i["default"])({url:"/api/category/get_filter_list/",method:"get",params:e})}function y(e){return console.log(e),Object(i["default"])({url:"/api/address/",method:"get",params:e})}},9936:function(e,t,l){"use strict";l("498e")},"9b5c":function(e,t,l){"use strict";l.r(t);var i=function(){var e=this,t=e.$createElement,l=e._self._c||t;return l("div",{staticClass:"gallery-container"},[l("vab-upload",{ref:"vabUpload",attrs:{url:"/api/img/",name:"src",limit:50,size:8}}),l("el-card",{staticClass:"box-card"},[l("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[l("span",[e._v(e._s(e.title)+"("+e._s(e.checkedIndex+1)+" / "+e._s(e.total)+")")]),e.albumName?l("span",[e._v("> "+e._s(e.albumName)+" ("+e._s(e.albumCnt)+")")]):e._e(),e._e(),l("el-button-group",{staticStyle:{float:"right"}},[l("el-button",{attrs:{type:"primary",icon:"el-icon-picture-outline"},on:{click:e.changeAvatar}}),l("el-button",{attrs:{type:"primary",icon:"el-icon-user-solid"},on:{click:e.changeFaceMode}}),l("el-button",{attrs:{type:"primary",icon:"el-icon-remove"},on:{click:function(t){return e.onAlbumChoose(t,-1,null)}}}),l("el-button",{attrs:{type:"primary",icon:"el-icon-upload"},on:{click:function(t){return e.handleShow({key:"value"})}}})],1)],1),l("div",{directives:[{name:"infinite-scroll",rawName:"v-infinite-scroll",value:e.load,expression:"load"}],ref:"album",staticClass:"infinite-list",staticStyle:{overflow:"auto"},attrs:{id:"album","infinite-scroll-distance":"50"}},e._l(e.items,(function(t,i){return l("div",{key:t.id,staticClass:"infinite-list-item",attrs:{"class-name":"album-item"},on:{click:function(l){return e.onAlbumChoose(l,i,t)},dblclick:function(l){return e.onDoubleClick(l,i,t)}}},[l("img",{class:e.checkedIndex===i?"img-checked":"img-unchecked",attrs:{className:"img-responsive",src:t.thumb,alt:t.name}}),l("div",{staticClass:"jg-caption"},[l("el-badge",{staticClass:"item",attrs:{value:t.value,max:99,type:"primary"}},[l("el-input",{staticClass:"album-name",staticStyle:{float:"left","font-size":"8px"},attrs:{size:"small",placeholder:"Change the Name"},on:{blur:function(l){return e.changeName(t.name,t)}},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.enterBlur(t)}},model:{value:t.name,callback:function(l){e.$set(t,"name",l)},expression:"album.name"}})],1)],1)])})),0)])],1)},a=[],o=l("1157"),s=l.n(o),c=(l("cfd5"),l("a809"),l("635a")),n=(l("970f"),{name:"Album",components:{VabUpload:c["default"]},props:{items:{type:Array,default:()=>[],required:!0},total:{type:Number,default:50,required:!0},title:{type:String,default:"Album",required:!0},type:{type:String,default:"img",required:!1},route:{type:String,default:"Face_detail",required:!1}},data(){return{drawer:!1,direction:"rtl",plugin:null,elementLoadingText:"正在加载...",msg:"",postData:{id:0,name:""},albumLoading:!1,totalAlbumCnt:0,curAlbumCnt:0,checkedIndex:-1,checkedId:0,checkedName:"",albumName:"",albumCnt:1}},watch:{items(e,t){this.$nextTick(()=>{console.log("Album numbers have been changed",e.length),s()("#album").justifiedGallery()})}},created(){console.log("Album component created")},mounted(){this.justifyInit()},methods:{justifyInit:function(){s()("[id=album]").justifiedGallery({captions:!0,lastRow:"left",rowHeight:150,margins:5}).on("jg.complete",(function(){console.log("jg.complete event was trigged")}))},onAlbumChoose(e,t,l){console.log("单击事件: ",l),this.checkedIndex=t,t<0||null!==l&&(this.checkedId=l.id,this.$emit("albumClick",t,l))},onDoubleClick(e,t,l){console.log("双击事件"),this.$emit("doubleClick",t,l)},changeName(e,t){this.$emit("changeName",e,t)},changeAvatar(){this.$emit("changeAvatar",this.checkedId)},changeFaceMode(){this.$store.state.face.isGroupMode=!this.$store.state.face.isGroupMode,this.checkedIndex=-1,console.log("this.$store.state.face.isGroupMode",this.$store.state.face.isGroupMode)},enterBlur(e){e.target.blur()},handleShow(e){this.$refs["vabUpload"].handleShow(e)},load(){this.$emit("load")}}}),r=n,d=(l("bf43"),l("2877")),u=Object(d["a"])(r,i,a,!1,null,"454d323d",null);t["default"]=u.exports},a4d0:function(e,t,l){},abc8:function(e,t,l){"use strict";l.r(t);var i=function(){var e=this,t=e.$createElement,l=e._self._c||t;return l("div",{staticClass:"tag-container"},[e._l(e.dynamicTags,(function(t){return l("el-tag",{key:t,attrs:{closable:"","disable-transitions":!1,size:"mini"},on:{close:function(l){return e.handleClose(t)}}},[e._v(" "+e._s(t)+" ")])})),e.inputVisible?l("el-input",{ref:"saveTagInput",staticClass:"input-new-tag",attrs:{size:"mini"},on:{blur:e.handleInputConfirm},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleInputConfirm.apply(null,arguments)}},model:{value:e.inputValue,callback:function(t){e.inputValue=t},expression:"inputValue"}}):l("el-button",{staticClass:"button-new-tag",attrs:{size:"mini"},on:{click:e.showInput}},[e._v(" + ")])],2)},a=[],o={name:"Tags",props:{items:{type:String,default:()=>"",required:!1}},data(){return{dynamicTags:[],inputVisible:!1,inputValue:""}},watch:{items(e,t){this.dynamicTags=e?e.split(","):[]}},mounted(){this.items?this.dynamicTags=this.items.split(","):this.dynamicTags=[]},methods:{handleClose(e){this.dynamicTags.splice(this.dynamicTags.indexOf(e),1),console.log("INFO: one of the tag was deleteded")},showInput(){this.inputVisible=!0,this.$nextTick(e=>{this.$refs.saveTagInput.$refs.input.focus()})},handleInputConfirm(){let e=this.inputValue;e&&this.dynamicTags.push(e),this.inputVisible=!1,this.inputValue="",console.log("INFO: addtional tag is confirmed")}}},s=o,c=(l("51ad"),l("2877")),n=Object(c["a"])(s,i,a,!1,null,"06fe6d79",null);t["default"]=n.exports},bf43:function(e,t,l){"use strict";l("a4d0")},d0ee:function(e,t,l){},d7fb:function(e,t,l){"use strict";l.r(t);var i=function(){var e=this,t=e.$createElement,l=e._self._c||t;return l("div",{staticClass:"color-container"},[l("h4",[e._v("background-color")]),null!==e.colors?l("el-button-group",e._l(e.colors.background,(function(e){return l("el-button",{key:e.id,staticClass:"background-color",style:"background-color: "+e.html_code+";width:"+5*e.percent+"px"})})),1):e._e(),l("h4",[e._v("foreground-color")]),null!==e.colors?l("el-button-group",e._l(e.colors.foreground,(function(e){return l("el-button",{key:e.id,staticClass:"foreground-color",style:"background-color: "+e.html_code+";width:"+5*e.percent+"px"})})),1):e._e(),l("h4",[e._v("image-color")]),null!==e.colors?l("el-button-group",e._l(e.colors.image,(function(e){return l("el-button",{key:e.id,staticClass:"image-color",style:"background-color: "+e.html_code+";width:"+5*e.percent+"px"})})),1):e._e()],1)},a=[],o={name:"Color",components:{},props:{colors:{type:Object,default:function(){return{img:426,background:[{id:101,r:242,g:198,b:156,closest_palette_color_html_code:"#fcd29e",closest_palette_color:"fair beige",closest_palette_color_parent:"skin",closest_palette_distance:4.03573799133301,percent:78.964111328125,html_code:"#f2c69c",color:426},{id:102,r:110,g:73,b:51,closest_palette_color_html_code:"#6e493a",closest_palette_color:"cinnamon",closest_palette_color_parent:"brown",closest_palette_distance:3.06844806671143,percent:20.9036521911621,html_code:"#6e4933",color:426}],foreground:[{id:103,r:231,g:169,b:120,closest_palette_color_html_code:"#d4a27c",closest_palette_color:"medium rose-beige",closest_palette_color_parent:"skin",closest_palette_distance:4.19777202606201,percent:59.6222991943359,html_code:"#e7a978",color:426},{id:104,r:127,g:80,b:53,closest_palette_color_html_code:"#7a5747",closest_palette_color:"almond",closest_palette_color_parent:"light brown",closest_palette_distance:5.13545513153076,percent:40.1577339172363,html_code:"#7f5035",color:426}],image:[{id:105,r:239,g:181,b:127,closest_palette_color_html_code:"#ecb694",closest_palette_color:"fair rose-beige",closest_palette_color_parent:"skin",closest_palette_distance:5.52706098556519,percent:35.521183013916,html_code:"#efb57f",color:426},{id:106,r:251,g:232,b:207,closest_palette_color_html_code:"#fce2c4",closest_palette_color:"light rose-beige",closest_palette_color_parent:"skin",closest_palette_distance:2.80652976036072,percent:23.5606784820557,html_code:"#fbe8cf",color:426},{id:107,r:192,g:121,b:77,closest_palette_color_html_code:"#ac7654",closest_palette_color:"dark rose-beige",closest_palette_color_parent:"skin",closest_palette_distance:4.81060171127319,percent:20.8791217803955,html_code:"#c0794d",color:426},{id:108,r:102,g:68,b:48,closest_palette_color_html_code:"#6e493a",closest_palette_color:"cinnamon",closest_palette_color_parent:"brown",closest_palette_distance:3.43346619606018,percent:19.7065620422363,html_code:"#664430",color:426}],color_variance:30,object_percentage:36.7733726501465,color_percent_threshold:1.75}}},mcstype:{type:String,default:"img",required:!1},title:{type:String,default:"",required:!1},id:{type:Number,default:269,required:!1}},data(){return{}},computed:{setColor(){return console.log("setting the color now"),{"background-color":this.colors.background[1].closest_palette_color_html_code}}},watch:{id(e,t){this.$nextTick(()=>{console.log("id have been changed")})}},created(){},mounted(){},methods:{}},s=o,c=(l("e4e6"),l("2877")),n=Object(c["a"])(s,i,a,!1,null,null,null);t["default"]=n.exports},db9f:function(e,t,l){},e4e6:function(e,t,l){"use strict";l("5d1d")},ea93:function(e,t,l){}}]);