/*!
 *  build: vue-admin-better 
 *  vue-admin-beautiful.com 
 *  https://gitee.com/chu1204505056/vue-admin-better 
 *  time: 2022-8-30 07:03:59
 */
(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-9dd8a12c"],{"0bd5":function(e,t,i){"use strict";i("fd23")},"13f2":function(e,t,i){"use strict";i("c0b7")},3206:function(e,t,i){"use strict";i.r(t);var a=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{staticClass:"gallery-container"},[i("vab-upload",{ref:"vabUpload",attrs:{url:"/api/img/",name:"src",limit:50,size:8}}),i("el-card",{staticClass:"box-card"},[i("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[i("span",[e._v(e._s(e.title))]),e.albumName?i("span",[e._v("> "+e._s(e.albumName))]):e._e(),e._e(),i("el-button-group",{staticStyle:{float:"right"}},[i("el-button",{attrs:{type:"primary",icon:"el-icon-plus"}}),i("el-button",{attrs:{type:"primary",icon:"el-icon-edit"}}),i("el-button",{attrs:{type:"primary",icon:"el-icon-map-location"}}),i("el-button",{attrs:{type:"primary",icon:"el-icon-user-solid"},on:{click:function(t){return e.onChangeDetailType("album")}}}),i("el-button",{attrs:{type:"primary",icon:"el-icon-picture"},on:{click:function(t){return e.onChangeDetailType("face-img")}}}),i("el-button",{attrs:{type:"primary",icon:"el-icon-upload"},on:{click:function(t){return e.handleShow({key:"value"})}}})],1)],1),i("div",{ref:"album",attrs:{id:"album"}},e._l(e.items,(function(t,a){return i("div",{key:t.id,attrs:{"class-name":"album-item"},on:{click:function(i){return e.onAlbumChoose(i,a,t)},dblclick:function(i){return e.onDoubleClick(i,a,t)}}},[i("img",{class:e.checkedIndex===a?"img-checked":"img-unchecked",attrs:{className:"img-responsive",src:t.src,alt:t.name,title:t.name}})])})),0)])],1)},l=[],s=i("1157"),r=i.n(s),n=(i("cfd5"),i("a809"),i("635a")),o={name:"Album",components:{VabUpload:n["default"]},props:{items:{type:Array,default:()=>[],required:!0},title:{type:String,default:"88888888888888",required:!0},type:{type:String,default:"face",required:!1},route:{type:String,default:"Face_detail",required:!1},limit:{type:Number,default:50,required:!1},size:{type:Number,default:8,required:!1}},data(){return{drawer:!1,direction:"rtl",plugin:null,elementLoadingText:"正在加载...",msg:"",queryForm:{page:1,pageSize:10,search:""},albumLoading:!1,totalAlbumCnt:0,curAlbumCnt:0,checkedIndex:"0",checkedId:"0",albumName:""}},watch:{items(e,t){this.$nextTick(()=>{console.log("onAlbumChoose have been changed",e),r()("#album").justifiedGallery()})}},created(){},mounted(){this.justifyInit()},methods:{justifyInit:function(){r()("[id=album]").justifiedGallery({captions:!0,lastRow:"left",rowHeight:150,margins:5}).on("jg.complete",(function(){console.log("jg.complete event was trigged")}))},onAlbumChoose(e,t,i){console.log("单击事件"),this.checkedIndex=t,this.drawer=!0,"face"===this.type&&(this.checkedId=i.face_album,this.routeName="FaceGallery",this.albumName=i.name),"personal"===this.type&&(this.checkedId=i.id,this.routeName="FaceGallery",this.albumName=i.name),"collection"===this.type&&(this.checkedId=i.id,this.routeName="Img",this.albumName=i.filename),console.log(this.checkedIndex,this.checkedId),this.$emit("albumClick",t,this.checkedId)},onDoubleClick(e,t,i){console.log("双击事件"),this.$router.push({name:this.routeName,query:{id:this.checkedId,title:i.name}})}}},u=o,c=(i("13f2"),i("2877")),d=Object(c["a"])(u,a,l,!1,null,"0e99555a",null);t["default"]=d.exports},"635a":function(e,t,i){"use strict";i.r(t);var a=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("el-dialog",{attrs:{"before-close":e.handleClose,"close-on-click-modal":!1,title:e.title,visible:e.dialogFormVisible,width:"909px"},on:{"update:visible":function(t){e.dialogFormVisible=t}}},[i("div",{staticClass:"upload"},[i("el-alert",{attrs:{closable:!1,title:"支持jpg、jpeg、png格式，单次可最多选择"+e.limit+"张图片，每张不可大于"+e.size+"M，如果大于"+e.size+"M会自动为您过滤",type:"info"}}),i("br"),i("el-upload",{ref:"upload",staticClass:"upload-content",attrs:{action:e.action,"auto-upload":!1,"close-on-click-modal":!1,data:e.data,"file-list":e.fileList,headers:e.headers,limit:e.limit,multiple:!0,name:e.name,"on-change":e.handleChange,"on-error":e.handleError,"on-exceed":e.handleExceed,"on-preview":e.handlePreview,"on-progress":e.handleProgress,"on-remove":e.handleRemove,"on-success":e.handleSuccess,accept:"image/png, image/jpeg","list-type":"picture-card"}},[i("i",{staticClass:"el-icon-plus",attrs:{slot:"trigger"},slot:"trigger"}),i("el-dialog",{attrs:{visible:e.dialogVisible,"append-to-body":"",title:"查看大图"},on:{"update:visible":function(t){e.dialogVisible=t}}},[i("div",[i("img",{attrs:{src:e.dialogImageUrl,alt:"",width:"100%"}})])])],1)],1),i("div",{staticClass:"dialog-footer",staticStyle:{position:"relative","padding-right":"15px","text-align":"right"},attrs:{slot:"footer"},slot:"footer"},[e.show?i("div",{staticStyle:{position:"absolute",top:"10px",left:"15px",color:"#999"}},[e._v(" 正在上传中... 当前上传成功数:"+e._s(e.imgSuccessNum)+"张 当前上传失败数:"+e._s(e.imgErrorNum)+"张 ")]):e._e(),i("el-button",{attrs:{type:"primary"},on:{click:e.handleClose}},[e._v("关闭")]),i("el-button",{staticStyle:{"margin-left":"10px"},attrs:{loading:e.loading,size:"small",type:"success"},on:{click:e.submitUpload}},[e._v(" 开始上传 ")])],1)])},l=[],s=(i("f121"),i("4360")),r={name:"Upload",props:{url:{type:String,default:"api/img/",required:!0},name:{type:String,default:"src",required:!0},limit:{type:Number,default:50,required:!0},size:{type:Number,default:8,required:!0}},data(){return{show:!1,loading:!1,dialogVisible:!1,dialogImageUrl:"",action:"http://localhost:8000/api/img/",headers:{Authorization:"Bearer "+s["default"].getters["user/accessToken"]},fileList:[],picture:"picture",imgNum:0,imgSuccessNum:0,imgErrorNum:0,typeList:null,title:"上传",dialogFormVisible:!1,data:{}}},computed:{percentage(){return 0==this.allImgNum?0:100*this.$baseLodash.round(this.imgNum/this.allImgNum,2)}},methods:{submitUpload(){this.$refs.upload.submit()},handleProgress(e,t,i){this.loading=!0,this.show=!0},handleChange(e,t){e.size>1048576*this.size?(t.map((i,a)=>{i===e&&t.splice(a,1)}),this.fileList=t):this.allImgNum=t.length},handleSuccess(e,t,i){this.imgNum=this.imgNum+1,this.imgSuccessNum=this.imgSuccessNum+1,i.length===this.imgNum&&setTimeout(()=>{this.$baseMessage(`上传完成! 共上传${i.length}张图片`,"success")},1e3),setTimeout(()=>{this.loading=!1,this.show=!1},1e3)},handleError(e,t,i){this.imgNum=this.imgNum+1,this.imgErrorNum=this.imgErrorNum+1,this.$baseMessage(`文件[${t.raw.name}]上传失败,文件大小为${this.$baseLodash.round(t.raw.size/1024,0)}KB`,"error"),setTimeout(()=>{this.loading=!1,this.show=!1},1e3)},handleRemove(e,t){this.imgNum=this.imgNum-1,this.allNum=this.allNum-1},handlePreview(e){this.dialogImageUrl=e.url,this.dialogVisible=!0},handleExceed(e,t){this.$baseMessage(`当前限制选择 ${this.limit} 个文件，本次选择了\n           ${e.length}\n           个文件`,"error")},handleShow(e){this.title="上传",this.data=e,this.dialogFormVisible=!0},handleClose(){this.fileList=[],this.picture="picture",this.allImgNum=0,this.imgNum=0,this.imgSuccessNum=0,this.imgErrorNum=0,this.dialogFormVisible=!1}}},n=r,o=(i("0bd5"),i("2877")),u=Object(o["a"])(n,a,l,!1,null,"a9a08f94",null);t["default"]=u.exports},"970f":function(e,t,i){"use strict";i.r(t),i.d(t,"getAlbum",(function(){return l})),i.d(t,"getGallery",(function(){return s})),i.d(t,"getImg",(function(){return r})),i.d(t,"checkImgMcs",(function(){return n})),i.d(t,"getFaceAlbum",(function(){return o})),i.d(t,"getFaceAlbumDetail",(function(){return u})),i.d(t,"getFaceGallery",(function(){return c})),i.d(t,"doEdit",(function(){return d})),i.d(t,"doDelete",(function(){return m})),i.d(t,"upload",(function(){return h}));var a=i("b775");function l(e){return Object(a["default"])({url:"/api/img/",method:"get",params:e})}function s(e){return Object(a["default"])({url:"/api/img/",method:"get",params:e})}function r(e){return Object(a["default"])({url:"/api/img/"+e.id+"/",method:"get"})}function n(e){return Object(a["default"])({url:"/api/img/"+e.id+"/check_mcs/",method:"get"})}function o(e){return Object(a["default"])({url:"/api/faces/",method:"get",params:e})}function u(e){return Object(a["default"])({url:"/api/faces/"+e.id+"/",method:"get",params:e})}function c(e){return console.log(e),Object(a["default"])({url:"/api/face/",method:"get",params:e})}function d(e){return Object(a["default"])({url:"/gallery/doEdit",method:"post",data:e})}function m(e){return Object(a["default"])({url:"/gallery/doDelete",method:"post",data:e})}function h(e){return Object(a["default"])({url:"/api/img/",method:"post",data:e})}},c0b7:function(e,t,i){},c75b:function(e,t,i){"use strict";i.r(t);var a=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",[i("Album",{ref:"album",attrs:{title:"人脸相册",type:"personal",items:e.albums},on:{albumClick:e.onGetAlbumId}}),i("br")],1)},l=[],s=(i("1157"),i("3206")),r=i("970f"),n={name:"PgFacePersonal",components:{Album:s["default"]},data:function(){return{faceAlbumQueryForm:{page:1,pageSize:10,search:"",faceAlumId:1,faces__id__gte:0},albums:[],albumLoading:!1,totalAlbumCnt:0,curAlbumCnt:0,checkedIndex:-1,checkedId:-1}},created(){this.fetchFaceAlbum()},mounted(){},methods:{onGetAlbumId(e,t){console.log("recieved the child component value %d,%d",e,t),this.checkedIndex=e,this.checkedId=t},async fetchFaceAlbum(){if(!this.albumLoading&&(this.albumLoading=!0,this.curAlbumCnt<this.totalAlbumCnt||0===this.totalAlbumCnt)){console.log("start to get the album...");const{data:e,totalCount:t}=await Object(r["getFaceAlbum"])(this.faceAlbumQueryForm);if(0===t)return;console.log("get img api result, data is %o, total is %d",e,t),this.albums=[...this.albums,...e],this.curAlbumCnt=this.albums.length,this.totalAlbumCnt=t,setTimeout(()=>{this.albumLoading=!1},300)}}}},o=n,u=i("2877"),c=Object(u["a"])(o,a,l,!1,null,null,null);t["default"]=c.exports},fd23:function(e,t,i){}}]);