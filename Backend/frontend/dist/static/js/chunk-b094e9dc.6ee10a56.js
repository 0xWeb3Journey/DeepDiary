/*!
 *  build: vue-admin-better 
 *  vue-admin-beautiful.com 
 *  https://gitee.com/chu1204505056/vue-admin-better 
 *  time: 2022-8-30 07:03:59
 */
(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-b094e9dc"],{"0bd5":function(t,e,i){"use strict";i("fd23")},"633d":function(t,e,i){"use strict";i.r(e);var l=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"gallery-container"},[i("vab-upload",{ref:"vabUpload",attrs:{url:"/api/img/",name:"src",limit:50,size:8}}),i("el-card",{staticClass:"box-card"},[i("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[i("span",[t._v(t._s(t.name))]),i("el-button-group",{staticStyle:{float:"right"}},[i("el-button",{attrs:{type:"primary",icon:"el-icon-plus"}}),i("el-button",{attrs:{type:"primary",icon:"el-icon-edit"}}),i("el-button",{attrs:{type:"primary",icon:"el-icon-map-location"}}),i("el-button",{attrs:{type:"primary",icon:"el-icon-user-solid"},on:{click:function(e){return t.onChangeDispType("face")}}}),i("el-button",{attrs:{type:"primary",icon:"el-icon-picture"},on:{click:function(e){return t.onChangeDispType("thumb")}}}),i("el-button",{attrs:{type:"primary",icon:"el-icon-upload"},on:{click:function(e){return t.handleShow({key:"value"})}}}),i("el-button",{attrs:{type:"primary",icon:"el-icon-plus"}})],1)],1),i("div",{directives:[{name:"infinite-scroll",rawName:"v-infinite-scroll",value:t.load,expression:"load"}],ref:"gallery",staticClass:"infinite-list",staticStyle:{overflow:"auto"},attrs:{id:"gallery"}},t._l(t.items,(function(e){return i("a",{key:e.id,staticClass:"gallery infinite-list-item",attrs:{className:"gallery-item","data-src":"oss"===t.storageType?e.src:e.mcs.nft_url,"data-sub-html":e.desc}},[i("img",{attrs:{className:"img-responsive",src:"face"===t.dispType?e.thumb_face:e.thumb}})])})),0)])],1)},a=[],s=i("1157"),r=i.n(s),o=i("2690"),n=i("c3c6"),c=i("c79a"),u=i("4dcd"),d=i("c1da"),m=i("5c2b"),g=(i("5abb"),i("5d6f"),i("cfd5"),i("a809"),i("970f"),i("635a"));i("6719");var h={name:"Gallery",components:{VabUpload:g["default"]},props:{items:{type:Array,default:()=>[],required:!0},name:{type:String,default:"88888888888888",required:!0},dispType:{type:String,default:"face",required:!0},storageType:{type:String,default:"oss",required:!0},limit:{type:Number,default:50,required:!1},size:{type:Number,default:8,required:!1}},data(){return{}},computed:{},watch:{items(t,e){this.$nextTick(()=>{console.log("gallery have been changed"),window.gallery.refresh(),r()("#gallery").justifiedGallery("norewind")})}},created(){},mounted(){this.lgInit(),this.justifyInit()},methods:{justifyInit:function(){r()("#gallery").justifiedGallery({captions:!1,lastRow:"left",rowHeight:150,margins:5}).on("jg.complete",(function(){console.log("jg.complete event was trigged")}))},lgInit:function(){const t=document.getElementById("gallery");window.gallery=Object(o["a"])(t,{addClass:"gallery",autoplayFirstVideo:!1,pager:!1,galleryId:"nature",plugins:[n["a"],c["a"],u["a"],d["a"],m["a"]],thumbnail:!0,slideShowInterval:2e3,mobileSettings:{controls:!1,showCloseIcon:!1,download:!1,rotate:!1}})},onChangeDispType(t){},handleShow(t){this.$refs["vabUpload"].handleShow(t)},load(){console.log("loading...")}}},p=h,f=i("2877"),y=Object(f["a"])(p,l,a,!1,null,"70a57ded",null);e["default"]=y.exports},"635a":function(t,e,i){"use strict";i.r(e);var l=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("el-dialog",{attrs:{"before-close":t.handleClose,"close-on-click-modal":!1,title:t.title,visible:t.dialogFormVisible,width:"909px"},on:{"update:visible":function(e){t.dialogFormVisible=e}}},[i("div",{staticClass:"upload"},[i("el-alert",{attrs:{closable:!1,title:"支持jpg、jpeg、png格式，单次可最多选择"+t.limit+"张图片，每张不可大于"+t.size+"M，如果大于"+t.size+"M会自动为您过滤",type:"info"}}),i("br"),i("el-upload",{ref:"upload",staticClass:"upload-content",attrs:{action:t.action,"auto-upload":!1,"close-on-click-modal":!1,data:t.data,"file-list":t.fileList,headers:t.headers,limit:t.limit,multiple:!0,name:t.name,"on-change":t.handleChange,"on-error":t.handleError,"on-exceed":t.handleExceed,"on-preview":t.handlePreview,"on-progress":t.handleProgress,"on-remove":t.handleRemove,"on-success":t.handleSuccess,accept:"image/png, image/jpeg","list-type":"picture-card"}},[i("i",{staticClass:"el-icon-plus",attrs:{slot:"trigger"},slot:"trigger"}),i("el-dialog",{attrs:{visible:t.dialogVisible,"append-to-body":"",title:"查看大图"},on:{"update:visible":function(e){t.dialogVisible=e}}},[i("div",[i("img",{attrs:{src:t.dialogImageUrl,alt:"",width:"100%"}})])])],1)],1),i("div",{staticClass:"dialog-footer",staticStyle:{position:"relative","padding-right":"15px","text-align":"right"},attrs:{slot:"footer"},slot:"footer"},[t.show?i("div",{staticStyle:{position:"absolute",top:"10px",left:"15px",color:"#999"}},[t._v(" 正在上传中... 当前上传成功数:"+t._s(t.imgSuccessNum)+"张 当前上传失败数:"+t._s(t.imgErrorNum)+"张 ")]):t._e(),i("el-button",{attrs:{type:"primary"},on:{click:t.handleClose}},[t._v("关闭")]),i("el-button",{staticStyle:{"margin-left":"10px"},attrs:{loading:t.loading,size:"small",type:"success"},on:{click:t.submitUpload}},[t._v(" 开始上传 ")])],1)])},a=[],s=(i("f121"),i("4360")),r={name:"Upload",props:{url:{type:String,default:"api/img/",required:!0},name:{type:String,default:"src",required:!0},limit:{type:Number,default:50,required:!0},size:{type:Number,default:8,required:!0}},data(){return{show:!1,loading:!1,dialogVisible:!1,dialogImageUrl:"",action:"http://localhost:8000/api/img/",headers:{Authorization:"Bearer "+s["default"].getters["user/accessToken"]},fileList:[],picture:"picture",imgNum:0,imgSuccessNum:0,imgErrorNum:0,typeList:null,title:"上传",dialogFormVisible:!1,data:{}}},computed:{percentage(){return 0==this.allImgNum?0:100*this.$baseLodash.round(this.imgNum/this.allImgNum,2)}},methods:{submitUpload(){this.$refs.upload.submit()},handleProgress(t,e,i){this.loading=!0,this.show=!0},handleChange(t,e){t.size>1048576*this.size?(e.map((i,l)=>{i===t&&e.splice(l,1)}),this.fileList=e):this.allImgNum=e.length},handleSuccess(t,e,i){this.imgNum=this.imgNum+1,this.imgSuccessNum=this.imgSuccessNum+1,i.length===this.imgNum&&setTimeout(()=>{this.$baseMessage(`上传完成! 共上传${i.length}张图片`,"success")},1e3),setTimeout(()=>{this.loading=!1,this.show=!1},1e3)},handleError(t,e,i){this.imgNum=this.imgNum+1,this.imgErrorNum=this.imgErrorNum+1,this.$baseMessage(`文件[${e.raw.name}]上传失败,文件大小为${this.$baseLodash.round(e.raw.size/1024,0)}KB`,"error"),setTimeout(()=>{this.loading=!1,this.show=!1},1e3)},handleRemove(t,e){this.imgNum=this.imgNum-1,this.allNum=this.allNum-1},handlePreview(t){this.dialogImageUrl=t.url,this.dialogVisible=!0},handleExceed(t,e){this.$baseMessage(`当前限制选择 ${this.limit} 个文件，本次选择了\n           ${t.length}\n           个文件`,"error")},handleShow(t){this.title="上传",this.data=t,this.dialogFormVisible=!0},handleClose(){this.fileList=[],this.picture="picture",this.allImgNum=0,this.imgNum=0,this.imgSuccessNum=0,this.imgErrorNum=0,this.dialogFormVisible=!1}}},o=r,n=(i("0bd5"),i("2877")),c=Object(n["a"])(o,l,a,!1,null,"a9a08f94",null);e["default"]=c.exports},"970f":function(t,e,i){"use strict";i.r(e),i.d(e,"getAlbum",(function(){return a})),i.d(e,"getGallery",(function(){return s})),i.d(e,"getImg",(function(){return r})),i.d(e,"checkImgMcs",(function(){return o})),i.d(e,"getFaceAlbum",(function(){return n})),i.d(e,"getFaceAlbumDetail",(function(){return c})),i.d(e,"getFaceGallery",(function(){return u})),i.d(e,"doEdit",(function(){return d})),i.d(e,"doDelete",(function(){return m})),i.d(e,"upload",(function(){return g}));var l=i("b775");function a(t){return Object(l["default"])({url:"/api/img/",method:"get",params:t})}function s(t){return Object(l["default"])({url:"/api/img/",method:"get",params:t})}function r(t){return Object(l["default"])({url:"/api/img/"+t.id+"/",method:"get"})}function o(t){return Object(l["default"])({url:"/api/img/"+t.id+"/check_mcs/",method:"get"})}function n(t){return Object(l["default"])({url:"/api/faces/",method:"get",params:t})}function c(t){return Object(l["default"])({url:"/api/faces/"+t.id+"/",method:"get",params:t})}function u(t){return console.log(t),Object(l["default"])({url:"/api/face/",method:"get",params:t})}function d(t){return Object(l["default"])({url:"/gallery/doEdit",method:"post",data:t})}function m(t){return Object(l["default"])({url:"/gallery/doDelete",method:"post",data:t})}function g(t){return Object(l["default"])({url:"/api/img/",method:"post",data:t})}},"9ac4":function(t,e,i){"use strict";i.r(e);var l=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",[i("Gallery",{ref:"gallery",attrs:{name:"相片","disp-type":"thumb","storage-type":"mcs",items:t.gallerys}})],1)},a=[],s=i("1157"),r=i.n(s),o=i("633d"),n=i("970f"),c={name:"PgGallery",components:{Gallery:o["default"]},data:function(){return{ImgQueryForm:{page:1,pageSize:10,search:"",faceAlumId:1,id:"",mcs__file_upload_id:""},gallerys:[],galleryLoading:!1,totalGalleryCnt:0,curGalleryCnt:0,checkedGalleryIndex:-1,checkedGalleryId:-1,gallerysWithoutMcs:[],totalgallerysWithoutMcsCnt:0,processedMcsCnt:0,msg:""}},created(){this.fetchGallery(),this.fetchGalleryWithoutMcs()},mounted(){const t=r()(window);t.fetchGallery=this.fetchGallery,t.scroll((function(){t.scrollTop()>=r()(document).height()-t.height()-10&&t.fetchGallery()}))},methods:{async checkMcs(t){this.ImgQueryForm.id=t;const{data:e}=await Object(n["checkImgMcs"])(this.ImgQueryForm);this.msg=e,console.log(e)},async fetchGalleryWithoutMcs(){this.ImgQueryForm.mcs__file_upload_id=0;const{data:t,totalCount:e}=await Object(n["getGallery"])(this.ImgQueryForm);0!==e&&(console.log("start to get the img without mcs..."),console.log("the img without mcs is %o",t),this.gallerysWithoutMcs=t,this.totalgallerysWithoutMcsCnt=e)},async fetchGallery(){if(this.ImgQueryForm.mcs__file_upload_id="",console.log("start to get the img..."),console.log(this.galleryLoading),!this.galleryLoading&&(this.galleryLoading=!0,this.curGalleryCnt<this.totalGalleryCnt||0===this.totalGalleryCnt)){const{data:t,totalCount:e}=await Object(n["getGallery"])(this.ImgQueryForm);if(0===e)return;this.ImgQueryForm.page+=1,console.log("get img api result, data is %o, total is %d",t,e),this.gallerys=[...this.gallerys,...t],this.curGalleryCnt=this.gallerys.length,this.totalGalleryCnt=e,setTimeout(()=>{this.galleryLoading=!1},300)}}}},u=c,d=i("2877"),m=Object(d["a"])(u,l,a,!1,null,null,null);e["default"]=m.exports},fd23:function(t,e,i){}}]);