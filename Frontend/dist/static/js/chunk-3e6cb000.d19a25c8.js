/*!
 *  build: vue-admin-better 
 *  vue-admin-beautiful.com 
 *  https://gitee.com/chu1204505056/vue-admin-better 
 *  time: 2023-9-12 21:12:51
 */
(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-3e6cb000"],{"0528":function(e,t,a){},"195d":function(e,t,a){"use strict";a("0528")},"1add":function(e,t,a){},"239a":function(e,t,a){"use strict";a.r(t);var o=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",{staticClass:"edit-list"},[a("span",[e._v("与我的关系")]),e.isHaveTag?a("el-tag",{attrs:{closable:"","disable-transitions":!1},on:{close:function(t){return e.onTagDelete(e.selectedTag)}}},[e._v(" "+e._s(e.selectedTag)+" ")]):e._e()],1),a("el-radio-group",{on:{input:e.onRelationChoosed},model:{value:e.selectedTag,callback:function(t){e.selectedTag=t},expression:"selectedTag"}},e._l(e.dynamicTags,(function(t){return a("el-radio-button",{key:t,attrs:{label:t}},[e._v(" "+e._s(t)+" ")])})),1),e.inputVisible?a("el-input",{ref:"saveTagInput",staticClass:"input-new-tag",attrs:{size:"small"},on:{blur:e.handleInputConfirm},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleInputConfirm.apply(null,arguments)}},model:{value:e.inputValue,callback:function(t){e.inputValue=t},expression:"inputValue"}}):a("el-button",{staticClass:"button-new-tag",attrs:{size:"small"},on:{click:e.showInput}},[e._v(" + New Tag ")])],1)},i=[],n={name:"ProfileRelationTags",props:{relation:{type:String,default:"",required:!1}},data(){return{dynamicTags:["我","妻子","丈夫","儿子","女儿","爸爸","妈妈","爷爷","奶奶","外公","外婆","家人","哥哥","姐姐","弟弟","妹妹","亲戚","男朋友","女朋友","同事","朋友","同学","闺蜜","客户","供应商","合作伙伴","其他"],inputVisible:!1,inputValue:"",selectedTag:"",isHaveTag:!1}},watch:{relation(e,t){console.log("ProfileRelationTags: relation",e,t),this.selectedTag=e}},mounted(){""===this.relation?this.isHaveTag=!1:(this.isHaveTag=!0,this.selectedTag=this.relation),console.log("ProfileRelationTags: mounted",this.selectedTag)},methods:{handleClose(e){this.dynamicTags.splice(this.dynamicTags.indexOf(e),1)},showInput(){this.inputVisible=!0,this.$nextTick(e=>{this.$refs.saveTagInput.$refs.input.focus()})},handleInputConfirm(){let e=this.inputValue;e&&this.dynamicTags.push(e),this.inputVisible=!1,this.inputValue=""},onTagDelete(e){console.log("ProfileRelationTags: onTagDelete",e),this.isHaveTag=!1},onRelationChoosed(e){console.log("ProfileRelationTags: onRelationChoosed",this.selectedTag,e),this.isHaveTag=!0,this.$emit("relationChoosed",this.selectedTag)}}},l=n,s=(a("195d"),a("2877")),r=Object(s["a"])(l,o,i,!1,null,null,null);t["default"]=r.exports},3273:function(e,t,a){"use strict";a.r(t);var o=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"edit-container"},[a("el-drawer",{attrs:{title:e.title,visible:e.drawer,"with-header":!0,"before-close":e.handleClose},on:{"update:visible":function(t){e.drawer=t}}},[a("EditAvatar",{attrs:{id:e.profileNew.id,avatar:e.profileNew.avatar},on:{confirmAvatar:e.onConfirmAvatar}}),a("Rename",{attrs:{name:e.profileNew.name},on:{confirmRename:e.onConfirmRename}}),a("ProfileRelationTags",{attrs:{relation:e.profileNew.relation},on:{relationChoosed:e.onRelationChoosed}}),a("div",[a("el-button",{staticClass:"dialog-footer",attrs:{type:"primary",loading:e.loading},on:{click:e.onProcessEdit}},[e._v(" "+e._s(e.loading?"提交中 ...":"确 定")+" ")])],1)],1)],1)},i=[],n=a("239a"),l=a("a17a"),s=a("4b8e"),r=a("7f87"),c={name:"ProfileEdit",components:{ProfileRelationTags:n["default"],Rename:l["default"],EditAvatar:s["default"]},props:{title:{type:String,default:"人脸详情",required:!0},edit:{type:Boolean,default:!1,required:!0},profile:{type:Object,default:null,required:!0}},data(){return{drawer:!1,loading:!1,dialogVisible:!1,isHaveTag:!0,newRelation:"",profileNew:{avatar:"https://cube.elemecdn.com/6/7b/03f0a0a0b0e2f6b5b6b5e2f0a0e0b0a0.jpeg",name:"DeepDiary",relation:""},fetchParams:{id:0,name:""}}},watch:{edit(e,t){this.drawer=e,e&&console.log("ProfileEdit: watch edit changed",e)},profile(e,t){this.profileNew=e,console.log("ProfileEdit: watch profile changed",e)}},mounted(){this.profileNew=this.profile,console.log("ProfileEdit: mounted",this.profile,this.profileNew)},methods:{onCancel(){console.log("ProfileEdit: onCancel"),this.$emit("cancel")},onConfirm(){console.log("ProfileEdit: onConfirm"),this.$emit("confirm")},handleClose(e){console.log("ProfileEdit: handleClose"),e(),this.$emit("close")},onChooseAvatar(){console.log("ProfileEdit: onChooseAvatar"),this.$emit("chooseAvatar")},onConfirmAvatar(e){console.log("ProfileEdit: onConfirmAvatar",e),this.profileNew.avatar=e.thumb,this.fetchParams.id=e.id},onConfirmRename(e){console.log(`ProfileEdit: handleConfirmName, new name: ${e}, old name: ${this.profile.name}`),this.fetchParams.name=e},onRelationChoosed(e){this.newRelation=e,this.isHaveTag=!0,console.log("ProfileEdit: onRelationChoosed, newRelation ",this.newRelation)},async onProcessEdit(){console.log("ProfileEdit: onProcessEdit",`新名称：${this.fetchParams.name}, 老名称为:${this.profile.name}`),this.loading=!0,await Object(r["patchProfile"])(this.fetchParams,this.profile.id).then(e=>{console.log("ProfileEdit: patchProfile",e),this.loading=!1,this.fetchParams.name="",this.$emit("close"),this.$message({message:"修改成功，修改后的名称是："+e.data.name,type:"success"})})}}},d=c,u=(a("80bd"),a("2877")),f=Object(u["a"])(d,o,i,!1,null,null,null);t["default"]=f.exports},"3e07":function(e,t,a){"use strict";a.r(t);var o=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"header-container"},[a("el-page-header",{attrs:{content:e.content},on:{back:e.goBack}}),a("el-dropdown",{on:{command:e.handleCommand}},[a("span",{staticClass:"el-dropdown-link"},[e._v(" 菜单 "),a("i",{staticClass:"el-icon-arrow-down el-icon--right"})]),a("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[a("el-dropdown-item",{attrs:{command:"edit"}},[e._v("人物信息编辑")]),a("el-dropdown-item",{attrs:{command:"remove"}},[e._v("移除该人物")])],1)],1)],1)},i=[],n={name:"DetailHead",components:{},props:{content:{type:String,default:"人脸详情",required:!0}},methods:{goBack(){console.log("go back"),this.$router.go(-1)},handleCommand(e){this.$message("click on item "+e),this.$emit(e)}}},l=n,s=(a("4ae9"),a("2877")),r=Object(s["a"])(l,o,i,!1,null,null,null);t["default"]=r.exports},"3ef0":function(e,t,a){},4021:function(e,t,a){},"4ae9":function(e,t,a){"use strict";a("1add")},"4b8e":function(e,t,a){"use strict";a.r(t);var o=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"reanme-container"},[a("div",{staticClass:"edit-list",on:{click:e.onChangeAvatarReq}},[a("img",{staticClass:"user-avatar",attrs:{src:e.avatar,alt:""}}),a("span",[e._v("选择封面>")])]),a("el-dialog",{attrs:{title:"选择封面",visible:e.dialogVisible,width:"30%",modal:!1},on:{"update:visible":function(t){e.dialogVisible=t}}},[e.isMounted?a("FaceList",{attrs:{query:e.FaceQueryForm},on:{choosed:e.onChoosed}}):e._e(),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){e.dialogVisible=!1}}},[e._v("取 消")]),a("el-button",{attrs:{type:"primary"},on:{click:e.onConfirmAvatar}},[e._v("确 定")])],1)],1)],1)},i=[],n=a("f5d0"),l={name:"EditAvatar",components:{FaceList:n["default"]},props:{avatar:{type:String,default:"未命名",required:!0},id:{type:Number,default:0,required:!0}},data(){return{dialogVisible:!1,isMounted:!1,choosedFace:null,newAvatar:"",FaceQueryForm:{page:1,size:20,profile:1,det_score__gt:.7}}},watch:{},mounted(){console.log("EditAvatar: mounted",this.avatar),this.newAvatar=this.avatar},methods:{onChangeAvatarReq(){this.dialogVisible=!0,this.FaceQueryForm.profile=this.id,this.isMounted=!0,console.log("EditAvatar: onChangeAvatarReq, this.FaceQueryForm.id",this.FaceQueryForm.profile)},onChoosed(e){this.choosedFace=e,console.log("EditAvatar: onChoosed",this.newAvatar)},onConfirmAvatar(e){console.log("EditAvatar: onConfirmAvatar",this.newAvatar),this.dialogVisible=!1,this.newAvatar=this.choosedFace.thumb,this.$emit("confirmAvatar",this.choosedFace)}}},s=l,r=(a("4eb6"),a("2877")),c=Object(r["a"])(s,o,i,!1,null,null,null);t["default"]=c.exports},"4eb6":function(e,t,a){"use strict";a("3ef0")},"80bd":function(e,t,a){"use strict";a("fc94")},a17a:function(e,t,a){"use strict";a.r(t);var o=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"reanme-container"},[a("div",{staticClass:"edit-list",on:{click:e.onRenameReq}},[a("span",[e._v("人物命名")]),a("span",[e._v(e._s(e.newName)+">")])]),a("el-dialog",{attrs:{title:"重命名",visible:e.dialogVisible,width:"30%",modal:!1},on:{"update:visible":function(t){e.dialogVisible=t}}},[a("el-form",[a("el-form-item",{attrs:{label:"姓名","label-width":"120px"}},[a("el-input",{attrs:{autocomplete:"off",placeholder:"请输入新名字"},model:{value:e.newName,callback:function(t){e.newName=t},expression:"newName"}})],1)],1),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){e.dialogVisible=!1}}},[e._v("取 消")]),a("el-button",{attrs:{type:"primary"},on:{click:e.onConfirmRename}},[e._v("确 定")])],1)],1)],1)},i=[],n={name:"Rename",components:{},props:{name:{type:String,default:"未命名",required:!0}},data(){return{dialogVisible:!1,newName:""}},watch:{name(e,t){console.log("Rename: watch name",e),this.newName=e}},mounted(){console.log("Rename: mounted",this.name),this.newName=this.name},methods:{onRenameReq(){this.dialogVisible=!0,console.log("Rename: onRenameReq"),this.$emit("rename")},onConfirmRename(e){console.log("Rename: handleConfirmName",this.newName),this.dialogVisible=!1,this.$emit("confirmRename",this.newName)}}},l=n,s=(a("f8d63"),a("2877")),r=Object(s["a"])(l,o,i,!1,null,null,null);t["default"]=r.exports},b97e:function(e,t,a){"use strict";a.r(t);var o=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("DetailHead",{attrs:{content:"人脸详情"},on:{edit:e.onEdit,remove:e.onRemove}}),e.isShowCarosel?a("Carosel",{attrs:{title:"照片",items:e.faces.data}}):e._e(),e.isGetRoutePrarms?a("FaceListGallery",{attrs:{query:e.faces.query},on:{faceData:e.onFaceData}}):e._e(),a("ProfileEdit",{attrs:{profile:e.profileDetail.data,edit:e.isDoEdit,title:"编辑人物信息"},on:{close:e.onClose}})],1)},i=[],n=(a("63a6"),a("c067")),l=(a("970f"),a("7f87")),s=a("3e07"),r=a("3273"),c=a("71d9"),d={name:"ProfileDetail",components:{DetailHead:s["default"],FaceListGallery:c["default"],Carosel:n["default"],ProfileEdit:r["default"]},data(){return{isGetRoutePrarms:!1,isShowCarosel:!1,isDoEdit:!1,faces:{query:{page:1,size:40,profile:30,det_score__gt:.7,pose_x__gt:0},data:[]},profileDetail:{data:{},query:{id:-1}}}},computed:{},watch:{"profileDetail.query.id"(e,t){console.log("this.profileDetail.query.id have bee changed: %d --\x3e %d",t,e),this.fetchProfileDetail()}},created(){console.log("component have been created --")},mounted(){console.log("component have been mounted --")},activated(){this.profileDetail.query.id=parseInt(this.$route.query.id),this.faces.query.profile=this.profileDetail.query.id,this.faces.query.page=1,this.isGetRoutePrarms=!0,console.log("ProfileDetail: the face component is activated",this.faces.query.profile)},deactivated(){console.log("the face component is deactivated")},methods:{async fetchProfileDetail(){console.log("start to get the fetchProfileDetail...",this.profileDetail.query.id);const{data:e}=await Object(l["getProfileDetail"])(this.profileDetail.query);console.log("getProfileDetail: ",e),this.profileDetail.data=e},beforeRouteEnter(e,t,a){console.log("beforeRouteEnter....")},beforeRouteLeave(e,t,a){console.log("beforeRouteLeave....")},onEdit(){console.log("ProfileDetail: onEdit"),this.isDoEdit=!0},onRemove(){console.log("ProfileDetail: onRemove")},onClose(){console.log("ProfileDetail: onClose"),this.isDoEdit=!1},onFaceData(e){console.log("ProfileDetail: onFaceData",e),this.faces.data=e,this.isShowCarosel=!0}}},u=d,f=a("2877"),h=Object(f["a"])(u,o,i,!1,null,null,null);t["default"]=h.exports},c067:function(e,t,a){"use strict";a.r(t);var o=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"gallery-container"},[a("el-carousel",{attrs:{interval:2e3,"indicator-position":"none",arrow:"always",height:"300px",type:"card"},on:{change:e.carouselChange}},e._l(e.items,(function(e){return a("el-carousel-item",{key:e.id},[a("el-row",{attrs:{gutter:12}},[a("el-col",{staticStyle:{height:"400px","margin-bottom":"20px display: flex","align-items":"center","justify-content":"center"}},[a("img",{ref:"banner",refInFor:!0,staticStyle:{"max-width":"100%","max-height":"100%","object-fit":"contain"},attrs:{src:e.thumb,alt:""}})])],1)],1)})),1)],1)},i=[],n={name:"Carosel",components:{},props:{items:{type:Array,default:()=>[],required:!0},title:{type:String,default:"deep-diary",required:!1}},data(){return{bannerHeight:""}},watch:{items(e,t){console.log("Carosel: watch items changed",e)}},created(){},mounted(){},methods:{carouselChange:function(e,t){}}},l=n,s=a("2877"),r=Object(s["a"])(l,o,i,!1,null,"4fef49c5",null);t["default"]=r.exports},f8d63:function(e,t,a){"use strict";a("4021")},fc94:function(e,t,a){}}]);