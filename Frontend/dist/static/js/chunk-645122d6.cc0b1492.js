/*!
 *  build: vue-admin-better 
 *  vue-admin-beautiful.com 
 *  https://gitee.com/chu1204505056/vue-admin-better 
 *  time: 2023-10-6 09:04:45
 */
(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-645122d6"],{1372:function(e,t,i){},"635a":function(e,t,i){"use strict";i.r(t);var a=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("el-dialog",{attrs:{"before-close":e.handleClose,"close-on-click-modal":!1,title:e.title,visible:e.dialogFormVisible,width:"909px"},on:{"update:visible":function(t){e.dialogFormVisible=t}}},[i("div",{staticClass:"upload"},[i("el-alert",{attrs:{closable:!1,title:"支持jpg、jpeg、png格式，单次可最多选择"+e.limit+"张图片，每张不可大于"+e.size+"M，如果大于"+e.size+"M会自动为您过滤",type:"info"}}),i("br"),i("el-upload",{ref:"upload",staticClass:"upload-content",attrs:{action:e.action,"auto-upload":!1,"close-on-click-modal":!1,data:e.data,"file-list":e.fileList,headers:e.headers,limit:e.limit,multiple:!0,name:e.name,"on-change":e.handleChange,"on-error":e.handleError,"on-exceed":e.handleExceed,"on-preview":e.handlePreview,"on-progress":e.handleProgress,"on-remove":e.handleRemove,"on-success":e.handleSuccess,accept:"image/png, image/jpeg","list-type":"picture-card"}},[i("i",{staticClass:"el-icon-plus",attrs:{slot:"trigger"},slot:"trigger"}),i("el-dialog",{attrs:{visible:e.dialogVisible,"append-to-body":"",title:"查看大图"},on:{"update:visible":function(t){e.dialogVisible=t}}},[i("div",[i("img",{attrs:{src:e.dialogImageUrl,alt:"",width:"100%"}})])])],1)],1),i("div",{staticClass:"dialog-footer",staticStyle:{position:"relative","padding-right":"15px","text-align":"right"},attrs:{slot:"footer"},slot:"footer"},[e.show?i("div",{staticStyle:{position:"absolute",top:"10px",left:"15px",color:"#999"}},[e._v(" 正在上传中... 当前上传成功数:"+e._s(e.imgSuccessNum)+"张 当前上传失败数:"+e._s(e.imgErrorNum)+"张 ")]):e._e(),i("el-button",{attrs:{type:"primary"},on:{click:e.handleClose}},[e._v("关闭")]),i("el-button",{staticStyle:{"margin-left":"10px"},attrs:{loading:e.loading,size:"small",type:"success"},on:{click:e.submitUpload}},[e._v(" 开始上传 ")])],1)])},s=[],l=i("f121"),n=i("4360"),o=i("970f"),r={name:"Upload",props:{url:{type:String,default:"api/img/",required:!0},name:{type:String,default:"src",required:!0},limit:{type:Number,default:50,required:!0},size:{type:Number,default:8,required:!0}},data(){return{show:!1,loading:!1,dialogVisible:!1,dialogImageUrl:"",action:l["baseURL"]+this.url,headers:{Authorization:"Bearer "+n["default"].getters["user/accessToken"]},fileList:[],picture:"picture",imgNum:0,imgSuccessNum:0,imgErrorNum:0,typeList:null,title:"上传",dialogFormVisible:!1,data:{}}},computed:{percentage(){return 0==this.allImgNum?0:100*this.$baseLodash.round(this.imgNum/this.allImgNum,2)}},methods:{submitUpload(){this.api=`${window.location.protocol}//${window.location.host}`,this.action=this.api+this.url,console.log("this.action:",this.action,"production",l["baseURL"]),this.$refs.upload.submit()},handleProgress(e,t,i){this.loading=!0,this.show=!0},handleChange(e,t){e.size>1048576*this.size?(t.map((i,a)=>{i===e&&t.splice(a,1)}),this.fileList=t):this.allImgNum=t.length},handleSuccess(e,t,i){this.imgNum=this.imgNum+1,this.imgSuccessNum=this.imgSuccessNum+1,i.length===this.imgNum&&setTimeout(()=>{this.$baseMessage(`上传完成! 共上传${i.length}张图片`,"success")},1e3),setTimeout(()=>{this.loading=!1,this.show=!1},1e3)},handleError(e,t,i){this.imgNum=this.imgNum+1,this.imgErrorNum=this.imgErrorNum+1,this.$baseMessage(`文件[${t.raw.name}]上传失败,文件大小为${this.$baseLodash.round(t.raw.size/1024,0)}KB`,"error"),setTimeout(()=>{this.loading=!1,this.show=!1},1e3)},handleRemove(e,t){this.imgNum=this.imgNum-1,this.allNum=this.allNum-1},handlePreview(e){this.dialogImageUrl=e.url,this.dialogVisible=!0},handleExceed(e,t){this.$baseMessage(`当前限制选择 ${this.limit} 个文件，本次选择了\n           ${e.length}\n           个文件`,"error")},handleShow(e){this.title="上传",this.data=e,this.dialogFormVisible=!0},handleClose(){this.fileList=[],this.picture="picture",this.allImgNum=0,this.imgNum=0,this.imgSuccessNum=0,this.imgErrorNum=0,this.uploadFinished(),this.dialogFormVisible=!1},async uploadFinished(){console.log("handleClose");const{msg:e}=await Object(o["getUploadState"])("");this.$message({message:e,type:"success"})}}},d=r,c=(i("6839"),i("2877")),u=Object(c["a"])(d,a,s,!1,null,"073731fa",null);t["default"]=u.exports},6839:function(e,t,i){"use strict";i("a43e")},"75b3":function(e,t,i){"use strict";i.r(t);var a=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{staticClass:"gallery-container"},[i("div",{directives:[{name:"infinite-scroll",rawName:"v-infinite-scroll",value:e.load,expression:"load"}],ref:"gallery_container",staticClass:"gallery_container",attrs:{id:"gallery_container","infinite-scroll-disabled":"busy","infinite-scroll-distance":"50","infinite-scroll-immediate-check":"true","force-use-infinite-wrapper":!0}},[i("div",{ref:"gallery",staticClass:"infinite-list",staticStyle:{overflow:"auto"},attrs:{id:"gallery"}},e._l(e.items,(function(e){return i("a",{key:e.id,staticClass:"gallery infinite-list-item",attrs:{className:"gallery-item","data-src":e.img,"data-sub-html":e.desc}},[i("el-tooltip",{attrs:{content:e.caption?e.caption:"No Caption",placement:"top"}},[i("img",{attrs:{className:"img-responsive",src:e.thumb}})])],1)})),0),i("div",{directives:[{name:"show",rawName:"v-show",value:e.busy,expression:"busy"}],staticClass:"loading"},[i("h3",[e._v(e._s(e.msg))])])]),i("el-divider",{directives:[{name:"show",rawName:"v-show",value:e.finished,expression:"finished"}]},[i("i",{staticClass:"el-icon-finished"})])],1)},s=[],l=i("1157"),n=i.n(l),o=i("2690"),r=i("c3c6"),d=i("c79a"),c=i("4dcd"),u=i("c1da"),g=i("5c2b"),h=(i("5abb"),i("5d6f"),i("cfd5"),i("a809"),i("635a"),{name:"GalleryContainer",components:{},props:{items:{type:Array,default:()=>Array(40).fill({}),required:!0},total:{type:Number,default:50,required:!0},title:{type:String,default:"Album",required:!0},busy:{type:Boolean,default:!1,required:!0},finished:{type:Boolean,default:!1,required:!1}},data(){return{msg:"Loading...",intervalId:null}},computed:{},watch:{items(e,t){this.checkDivHeight(),this.$nextTick(()=>{console.log("gallery have been changed"),window.gallery.refresh(),n()("#gallery").justifiedGallery()})}},created(){},mounted(){this.lgInit(),this.justifyInit()},methods:{justifyInit:function(){n()("#gallery").justifiedGallery({captions:!1,lastRow:"left",rowHeight:150,margins:5}).on("jg.complete",(function(){console.log("jg.complete event was trigged")}))},lgInit:function(){const e=document.getElementById("gallery");window.gallery=Object(o["a"])(e,{addClass:"gallery",autoplayFirstVideo:!1,pager:!1,galleryId:"nature",plugins:[r["a"],d["a"],c["a"],u["a"],g["a"]],thumbnail:!0,slideShowInterval:2e3,mobileSettings:{controls:!1,showCloseIcon:!1,download:!1,rotate:!1}})},onChangeDsipType(){this.isDispFace=!this.isDispFace,console.log("onChangeDsipType, current isDispFace: %s",this.isDispFace)},handleShow(e){this.$refs["vabUpload"].handleShow(e)},load(){console.log("infinite loading... ",this.busy),this.busy||this.$emit("load")},checkDivHeight(){if(null===this.intervalId){var e=this.$refs.gallery_container;e&&(this.intervalId=setInterval(()=>{if(this.$refs.gallery_container.style.height="600px",!1===this.busy){var t=e.scrollHeight,i=(e.scrollTop,1e3);if(t>i)clearInterval(this.intervalId),this.intervalId=null,console.log("timer has been closed",t,i);else if(this.finished){clearInterval(this.intervalId),this.intervalId=null;const e=this.$refs.gallery.scrollHeight;this.$refs.gallery_container.style.height=e+"px",console.log("Set the divHeight to match content height:",this.$refs.gallery_container.style.height)}else this.$emit("load")}},1e3))}else console.log("Gallery content: checkDivHeight: intervalId is not null")}}}),m=h,f=(i("e03e"),i("2877")),p=Object(f["a"])(m,a,s,!1,null,"a33c3bd8",null);t["default"]=p.exports},"970f":function(e,t,i){"use strict";i.r(t),i.d(t,"getImg",(function(){return s})),i.d(t,"getImgDetail",(function(){return l})),i.d(t,"getMcs",(function(){return n})),i.d(t,"getTags",(function(){return o})),i.d(t,"getUploadState",(function(){return r})),i.d(t,"getProfile",(function(){return d})),i.d(t,"getProfileDetail",(function(){return c})),i.d(t,"changeFaceAlbumName",(function(){return u})),i.d(t,"clear_face_album",(function(){return g})),i.d(t,"getFace",(function(){return h})),i.d(t,"changeFaceName",(function(){return m})),i.d(t,"getFaceGallery",(function(){return f})),i.d(t,"doEdit",(function(){return p})),i.d(t,"doDelete",(function(){return y})),i.d(t,"upload",(function(){return b})),i.d(t,"getFilterList",(function(){return v})),i.d(t,"getAddress",(function(){return I}));var a=i("b775");function s(e){return Object(a["default"])({url:"/api/img/",method:"get",params:e})}function l(e){return Object(a["default"])({url:"/api/img/"+e+"/",method:"get"})}function n(e){return Object(a["default"])({url:"/api/mcs/"+e.id+"/",method:"get"})}function o(e){return Object(a["default"])({url:"/api/img/"+e.id+" / set_tags/",method:"get"})}function r(e){return Object(a["default"])({url:"/api/img/upload_finished/",method:"get"})}function d(e){return Object(a["default"])({url:"/api/profile/",method:"get",params:e})}function c(e){return Object(a["default"])({url:"/api/profile/"+e.id+"/",method:"get",params:e})}function u(e){return Object(a["default"])({url:"/api/profile/"+e.id+"/",method:"put",data:e})}function g(e){return Object(a["default"])({url:"/api/profile/clear_face_album/",method:"get"})}function h(e){return Object(a["default"])({url:"/api/face/"+e.id+"/",method:"get"})}function m(e){return Object(a["default"])({url:"/api/face/"+e.id+"/",method:"put",data:e})}function f(e){return console.log(e),Object(a["default"])({url:"/api/face/",method:"get",params:e})}function p(e){return Object(a["default"])({url:"/gallery/doEdit",method:"post",data:e})}function y(e){return Object(a["default"])({url:"/gallery/doDelete",method:"post",data:e})}function b(e){return Object(a["default"])({url:"/api/img/",method:"post",data:e})}function v(e){return console.log(e),Object(a["default"])({url:"/api/category/get_filter_list/",method:"get",params:e})}function I(e){return console.log(e),Object(a["default"])({url:"/api/address/",method:"get",params:e})}},a43e:function(e,t,i){},c645:function(e,t,i){"use strict";i.r(t);var a=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",[i("ImgSearch",{on:{handleImgSearch:e.onImgSearch,command:e.onCommand}}),i("GalleryContainer",{attrs:{items:e.imgs.data,total:e.imgs.totalCnt,title:e.imgs.title,busy:e.imgs.loading,finished:e.imgs.finished},on:{load:e.onLoad}}),i("vab-upload",{ref:"vabUpload",attrs:{url:"/api/img/",name:"src",limit:50,size:8}})],1)},s=[],l=i("75b3"),n=i("9d59"),o=i("4360"),r=i("5333"),d=i("635a"),c={name:"Gallery",components:{GalleryContainer:l["default"],ImgSearch:n["default"],VabUpload:d["default"]},directives:{},props:{query:{type:Object,default:null,required:!1}},data:function(){return{imgs:{title:"Img List",loading:!1,finished:!1,checkedId:-1,checkedIndex:-1,totalCnt:0,links:null,curCnt:0,data:[],queryForm:{page:1,size:10,search:"",id:"",fc_nums:-1,fc_name:"",c_img:"",c_fore:"",c_back:"",address__is_located:"",address__city:"",address__longitude__range:"",address__latitude__range:"",user__username:o["default"].getters["user/username"]}}}},watch:{},created(){},mounted(){console.log("Gallery Index: mounted",this.imgs.queryForm),this.fetchImg()},methods:{onRouteJump(e,t){console.log("recieved the child component value %d,%o",e,t),this.imgs.checkedIndex=e,this.imgs.checkedId=t.id||0},async fetchImg(){console.log("Gallery Index: fetchImg"),this.imgs.loading=!0,this.imgs.finished=!1,await Object(r["getImg"])(this.imgs.queryForm).then(e=>{console.log("Gallery Index: getImg",e);const{data:t,totalCnt:i,links:a}=e;this.imgs.data=[...this.imgs.data,...t],this.imgs.curCnt=this.imgs.data.length,this.imgs.totalCnt=i,this.imgs.links=a,null===this.imgs.links.next&&(this.imgs.finished=!0),console.log("Gallery Index: emit imgData"),this.$emit("imgData",this.imgs.data),setTimeout(()=>{this.imgs.loading=!1},2e3)})},onLoad(){console.log("Gallery Index: onLoad, this.imgs.loading",this.imgs.loading),this.imgs.finished?setTimeout(()=>{this.imgs.loading=!1},1e4):(console.log("Gallery Index imgs.queryForm.page: ",this.imgs.queryForm.page),this.imgs.queryForm.page++,this.fetchImg())},onImgSearch(e){console.log("recieve the queryForm info from the search component"),console.log(e),this.imgs.queryForm=e,this.imgs.totalCnt=0,this.imgs.data=[],this.fetchImg()},onCommand(e){console.log("Gallery Index: onCommand",e),"upload"===e&&(console.log("Gallery Index: onCommand: uploading the image...."),this.handleShow({key:"value"}))},handleShow(e){this.$refs["vabUpload"].handleShow(e)}}},u=c,g=i("2877"),h=Object(g["a"])(u,a,s,!1,null,null,null);t["default"]=h.exports},e03e:function(e,t,i){"use strict";i("1372")}}]);