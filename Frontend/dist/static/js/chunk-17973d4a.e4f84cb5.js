/*!
 *  build: vue-admin-better 
 *  vue-admin-beautiful.com 
 *  https://gitee.com/chu1204505056/vue-admin-better 
 *  time: 2023-10-6 15:18:13
 */
(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-17973d4a"],{"07c4":function(e,t,o){},"0fb0":function(e,t,o){"use strict";o.r(t);var a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",[o("el-dialog",{attrs:{title:"Add Demand",visible:e.dialogFormVisible},on:{"update:visible":function(t){e.dialogFormVisible=t}}},[o("el-form",{attrs:{model:e.form}},[o("el-form-item",{attrs:{label:"Profile","label-width":e.formLabelWidth}},[o("el-select",{attrs:{filterable:"",clearable:"",placeholder:"Please Choose a Person"},model:{value:e.form.profile,callback:function(t){e.$set(e.form,"profile",t)},expression:"form.profile"}},[o("el-option",{attrs:{label:"葛维冬",value:1}}),o("el-option",{attrs:{label:"韩莉",value:5}}),o("el-option",{attrs:{label:"葛丰炳",value:33}})],1)],1),o("el-form-item",{attrs:{label:"Title","label-width":e.formLabelWidth}},[o("el-input",{attrs:{autocomplete:"off"},model:{value:e.form.name,callback:function(t){e.$set(e.form,"name",t)},expression:"form.name"}})],1),o("el-form-item",{attrs:{label:"Desc.","label-width":e.formLabelWidth}},[o("el-input",{attrs:{autocomplete:"off"},model:{value:e.form.desc,callback:function(t){e.$set(e.form,"desc",t)},expression:"form.desc"}})],1)],1),o("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[o("el-button",{on:{click:e.onCancel}},[e._v("取 消")]),o("el-button",{attrs:{type:"primary"},on:{click:e.onConfirm}},[e._v("确 定")])],1)],1)],1)},i=[],n=o("2b26"),s={name:"DemandAdd",components:{},props:{visible:{type:Boolean,default:!1,required:!0}},data(){return{dialogFormVisible:!1,form:{name:"",profile:"",desc:""},formLabelWidth:"120px"}},computed:{},watch:{visible(e,t){console.log("demandAdd: watch visible",e),this.dialogFormVisible=e}},created(){console.log("demandAdd: component has been created --")},mounted(){console.log("demandAdd: component has been mounted --"),this.dialogFormVisible=this.isVisible},activated(){console.log("demandAdd: component has been activated --")},deactivated(){console.log("demandAdd: component has been deactivated -- ")},methods:{beforeRouteEnter(e,t,o){console.log("demandAdd: component has been beforeRouteEnter -- ")},beforeRouteLeave(e,t,o){console.log("demandAdd: component has been beforeRouteLeave -- ")},onCancel(){console.log("demandAdd: onCancel"),this.$emit("done","cancel")},onConfirm(){console.log("demandAdd: onConfirm",this.form),this.onAddDemand(),this.$emit("done","confirm")},async onAddDemand(){await Object(n["addDemand"])(this.form).then(e=>{console.log("demandAdd: addDemand",e,e.id),this.$message({message:`创建成功, name is ${e.name}, id is ${e.id}`,type:"success"})})}}},l=s,r=o("2877"),c=Object(r["a"])(l,a,i,!1,null,null,null);t["default"]=c.exports},1602:function(e,t,o){"use strict";o.r(t);var a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"edit-container"},[o("el-drawer",{attrs:{title:e.title,visible:e.drawer,"with-header":!0,"before-close":e.handleClose},on:{"update:visible":function(t){e.drawer=t}}},[o("EditAvatar",{attrs:{id:e.profileNew.id,avatar:e.profileNew.avatar},on:{confirmAvatar:e.onConfirmAvatar}}),o("Rename",{attrs:{name:e.profileNew.name},on:{confirmRename:e.onConfirmRename}}),o("ProfileRelationTags",{attrs:{relation:e.profileNew.relation},on:{relationChoosed:e.onRelationChoosed}}),o("div",[o("el-button",{staticClass:"dialog-footer",attrs:{type:"primary",loading:e.loading},on:{click:e.onProcessEdit}},[e._v(" "+e._s(e.loading?"提交中 ...":"确 定")+" ")])],1)],1)],1)},i=[],n=o("871d"),s=o("8d44"),l=o("c49f"),r=o("7f87"),c={name:"ProfileEdit",components:{ProfileRelationTags:n["default"],Rename:s["default"],EditAvatar:l["default"]},props:{title:{type:String,default:"人脸详情",required:!0},edit:{type:Boolean,default:!1,required:!0},profile:{type:Object,default:null,required:!0}},data(){return{drawer:!1,loading:!1,dialogVisible:!1,isHaveTag:!0,newRelation:"",profileNew:{avatar:"https://cube.elemecdn.com/6/7b/03f0a0a0b0e2f6b5b6b5e2f0a0e0b0a0.jpeg",name:"DeepDiary",relation:""},fetchParams:{id:0,name:"",re_from:"",relation:""}}},watch:{edit(e,t){this.drawer=e,e&&console.log("ProfileEdit: watch edit changed",e)},profile(e,t){this.profileNew=e,console.log("ProfileEdit: watch profile changed",e)}},mounted(){this.profileNew=this.profile,console.log("ProfileEdit: mounted",this.profile,this.profileNew)},methods:{onCancel(){console.log("ProfileEdit: onCancel"),this.$emit("cancel")},onConfirm(){console.log("ProfileEdit: onConfirm"),this.$emit("confirm")},handleClose(e){console.log("ProfileEdit: handleClose"),e(),this.$emit("close")},onChooseAvatar(){console.log("ProfileEdit: onChooseAvatar"),this.$emit("chooseAvatar")},onConfirmAvatar(e){console.log("ProfileEdit: onConfirmAvatar",e),this.profileNew.avatar=e.thumb,this.fetchParams.id=e.id},onConfirmRename(e){console.log(`ProfileEdit: handleConfirmName, new name: ${e}, old name: ${this.profile.name}`),this.fetchParams.name=e},onRelationChoosed(e){this.newRelation=e,this.isHaveTag=!0,this.fetchParams.re_from=this.profile.id,this.fetchParams.relation=e,console.log("ProfileEdit: onRelationChoosed, newRelation ",this.newRelation)},async onProcessEdit(){console.log("ProfileEdit: onProcessEdit",`新名称：${this.fetchParams.name}, 老名称为:${this.profile.name}`),this.loading=!0,await Object(r["patchProfile"])(this.fetchParams,this.profile.id).then(e=>{console.log("ProfileEdit: patchProfile",e),this.loading=!1,this.fetchParams.name="",this.$emit("close"),this.$message({message:`修改成功，修改后的名称是：${e.data.name}, 修改后的关系是：${e.data.relation}`,type:"success"})})}}},d=c,m=(o("4d66"),o("2877")),u=Object(m["a"])(d,a,i,!1,null,null,null);t["default"]=u.exports},"19c5":function(e,t,o){},"1add":function(e,t,o){},"2b26":function(e,t,o){"use strict";o.r(t),o.d(t,"getDemand",(function(){return i})),o.d(t,"addDemand",(function(){return n})),o.d(t,"changeDemand",(function(){return s}));var a=o("b775");function i(e){return Object(a["default"])({url:"/api/demand/",method:"get",params:e})}function n(e){return Object(a["default"])({url:"/api/demand/",method:"post",data:e})}function s(e,t){return Object(a["default"])({url:"/api/demand/"+t+"/",method:"put",data:e})}},"3e05":function(e,t,o){"use strict";o.r(t);var a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",[o("DetailHead",{attrs:{content:"人物详情 | "+e.profileDetail.data.name+" | "+e.profileDetail.data.relation+" | 共计"+e.faces.totalCnt+"张照片 "},on:{edit:e.onEdit,remove:e.onRemove}}),e.isShowCarosel?o("Carosel",{attrs:{title:"照片",items:e.faces.data}}):e._e(),e.isGetRoutePrarms?o("FaceListGallery",{attrs:{id:e.profileDetail.query.id,searchable:!1},on:{faceData:e.onFaceData}}):e._e(),o("el-collapse",{attrs:{accordion:""},model:{value:e.activeName,callback:function(t){e.activeName=t},expression:"activeName"}},[o("el-collapse-item",{attrs:{name:"resources"}},[o("template",{slot:"title"},[e._v("三大资源 Resources")]),o("ResourceDemand",{attrs:{items:e.profileDetail.data.resources,type:"resource"}})],2),o("el-collapse-item",{attrs:{title:"三大需求 Demands",name:"demands"}},[o("ResourceDemand",{attrs:{items:e.profileDetail.data.demands,type:"demand"}})],1),o("el-collapse-item",{attrs:{title:"工作经历 Experiences",name:"experience"}},[o("Experience",{attrs:{items:e.profileDetail.data.experiences}})],1)],1),o("ProfileEdit",{attrs:{profile:e.profileDetail.data,edit:e.isDoEdit,title:"编辑人物信息"},on:{close:e.onClose}})],1)},i=[],n=o("c067"),s=o("7f87"),l=o("3e07"),r=o("1602"),c=o("71d9"),d=o("ad02"),m=o("6e96"),u=(o("ff49"),{name:"ProfileDetail",components:{DetailHead:l["default"],FaceListGallery:c["default"],Carosel:n["default"],ProfileEdit:r["default"],ResourceDemand:d["default"],Experience:m["default"]},data(){return{isGetRoutePrarms:!1,isShowCarosel:!1,isDoEdit:!1,faces:{data:[]},profileDetail:{data:{},query:{id:-1}},activeName:"faces"}},computed:{},watch:{"profileDetail.query.id"(e,t){console.log("this.profileDetail.query.id have bee changed: %d --\x3e %d",t,e),this.faces.data=[],this.fetchProfileDetail()}},created(){console.log("profileDetail component have been created --")},mounted(){console.log("profileDetail component have been mounted --")},activated(){console.log("profileDetail component have been activated --"),this.profileDetail.query.id=parseInt(this.$route.query.id),this.isGetRoutePrarms=!0},deactivated(){console.log("profileDetail: the face component is deactivated")},methods:{async fetchProfileDetail(){console.log("start to get the fetchProfileDetail...",this.profileDetail.query.id);const{data:e}=await Object(s["getProfileDetail"])(this.profileDetail.query);console.log("getProfileDetail: ",e),this.profileDetail.data=e},beforeRouteEnter(e,t,o){console.log("beforeRouteEnter....")},beforeRouteLeave(e,t,o){console.log("beforeRouteLeave....")},onEdit(){console.log("ProfileDetail: onEdit"),this.isDoEdit=!0},onRemove(){console.log("ProfileDetail: onRemove")},onClose(){console.log("ProfileDetail: onClose"),this.isDoEdit=!1},onFaceData(e){this.faces=e,this.isShowCarosel=!0}}}),f=u,h=o("2877"),p=Object(h["a"])(f,a,i,!1,null,null,null);t["default"]=p.exports},"3e07":function(e,t,o){"use strict";o.r(t);var a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"header-container"},[o("el-page-header",{attrs:{content:e.content},on:{back:e.goBack}}),o("el-dropdown",{on:{command:e.handleCommand}},[o("span",{staticClass:"el-dropdown-link"},[e._v(" 菜单 "),o("i",{staticClass:"el-icon-arrow-down el-icon--right"})]),o("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[o("el-dropdown-item",{attrs:{command:"edit"}},[e._v("人物信息编辑")]),o("el-dropdown-item",{attrs:{command:"remove"}},[e._v("移除该人物")])],1)],1)],1)},i=[],n={name:"DetailHead",components:{},props:{content:{type:String,default:"人脸详情",required:!0}},methods:{goBack(){console.log("go back"),this.$router.go(-1)},handleCommand(e){this.$message("click on item "+e),this.$emit(e)}}},s=n,l=(o("4ae9"),o("2877")),r=Object(l["a"])(s,a,i,!1,null,null,null);t["default"]=r.exports},"47a1":function(e,t,o){"use strict";o("b667")},"48c8":function(e,t,o){},"4ae9":function(e,t,o){"use strict";o("1add")},"4d66":function(e,t,o){"use strict";o("926f")},"6c6e":function(e,t,o){"use strict";o.r(t),o.d(t,"getResource",(function(){return i})),o.d(t,"addResource",(function(){return n})),o.d(t,"changeResource",(function(){return s}));var a=o("b775");function i(e){return Object(a["default"])({url:"/api/resource/",method:"get",params:e})}function n(e){return Object(a["default"])({url:"/api/resource/",method:"post",data:e})}function s(e,t){return Object(a["default"])({url:"/api/resource/"+t+"/",method:"put",data:e})}},"6e96":function(e,t,o){"use strict";o.r(t);var a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",[o("el-row",{staticClass:"row-bg",attrs:{gutter:12,type:"flex",justify:"space-around"}},e._l(e.items,(function(e){return o("el-col",{key:e.id,attrs:{xs:24,sm:12,md:12,lg:8,xl:6}},[o("experienceItem",{attrs:{item:e}})],1)})),1),e.isNoResourceDemand?o("el-empty",{attrs:{image:"https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png",description:"No Data"}},[o("el-button",{attrs:{type:"primary"},on:{click:e.onAdd}},[e._v("Add")])],1):e._e()],1)},i=[],n=o("fd15"),s={name:"Experience",components:{ExperienceItem:n["default"]},props:{items:{type:Array,default:()=>[],required:!1}},data(){return{isNoResourceDemand:!1}},computed:{},watch:{items(e,t){console.log("Experience: items have bee changed: ",e),0===e.length?this.isNoResourceDemand=!0:this.isNoResourceDemand=!1}},created(){console.log("Experience: component has been created --")},mounted(){console.log("Experience: component has been mounted --")},activated(){console.log("Experience: component has been activated --")},deactivated(){console.log("Experience: component has been deactivated -- ")},methods:{beforeRouteEnter(e,t,o){console.log("Experience: component has been beforeRouteEnter -- ")},beforeRouteLeave(e,t,o){console.log("Experience: component has been beforeRouteLeave -- ")},onAdd(){console.log("ResourceDemand: onAdd"),this.$router.push({name:"ResourceDemandAdd"})}}},l=s,r=o("2877"),c=Object(r["a"])(l,a,i,!1,null,null,null);t["default"]=c.exports},7485:function(e,t,o){"use strict";o.r(t);var a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",[o("el-card",{attrs:{shadow:"hover"}},[o("div",{staticClass:"header",attrs:{slot:"header"},slot:"header"},[o("span",[e._v(e._s(e.itemLocal.name))]),o("Menu",{staticClass:"menu-right",attrs:{menus:e.menus},on:{command:e.handleCommand}})],1),o("div",{staticClass:"text item"},[e._v(" "+e._s(e.itemLocal.desc)+" ")]),o("el-carousel",{attrs:{height:"200px"}},e._l(e.itemLocal.images,(function(t){return o("el-carousel-item",{key:t.id},[o("el-image",{staticStyle:{width:"100%"},attrs:{src:t.thumb,fit:"cover","preview-src-list":e.srcList}})],1)})),1)],1)],1)},i=[],n=o("ff49"),s={name:"ResourceDemandItem",components:{Menu:n["default"]},props:{item:{type:Object,default:()=>({id:1,name:"英语",desc:"TEM8, 英语可以作为工作语言",images:[{id:1,src:"https://deep-diary.oss-accelerate.aliyuncs.com/media/user_info_img/%E5%9C%B0%E5%9B%BE%E6%98%BE%E7%A4%BA.png",thumb:"https://deep-diary.oss-accelerate.aliyuncs.com/media/CACHE/images/user_info_img/%E5%9C%B0%E5%9B%BE%E6%98%BE%E7%A4%BA/1ed8b21aca917ed0e325c8571f207821.jpg"},{id:5,src:"https://deep-diary.oss-accelerate.aliyuncs.com/media/user_info_img/deep-diary_cover.png",thumb:"https://deep-diary.oss-accelerate.aliyuncs.com/media/CACHE/images/user_info_img/deep-diary_cover/69e150672e13b78f12fc3edb4ed1c43c.jpg"}]}),required:!0}},data(){return{itemLocal:this.item,srcList:[],menus:[{icon:"el-icon-circle-plus",text:"Add"},{icon:"el-icon-remove",text:"Remove"},{icon:"el-icon-edit",text:"Edit"},{icon:"el-icon-view",text:"View"},{icon:"el-icon-delete",text:"Reset"},{icon:"el-icon-upload",text:"Upload"},{icon:"el-icon-setting",text:"Setting"}]}},computed:{},watch:{item:{handler:function(e,t){console.log("ResourceDemandItem: item has been changed -- "),this.itemLocal=e,console.log(this.itemLocal.images.length,"-------------------"),0===this.itemLocal.images.length&&(console.log("ResourceDemandItem: item.images is empty -- "),this.itemLocal.images=[{id:1,src:"https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png",thumb:"https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png"}],console.log("ResourceDemandItem: this.itemLocal.images is -- ",this.itemLocal.images)),this.srcList=this.itemLocal.images.map(e=>e.src)},deep:!0}},created(){console.log("ResourceDemandItem: component has been created --")},mounted(){console.log("ResourceDemandItem: component has been mounted --"),this.itemLocal=this.item,0===this.itemLocal.images.length&&(this.itemLocal.images=[{id:1,src:"https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png",thumb:"https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png"}]),this.srcList=this.itemLocal.images.map(e=>e.src)},activated(){console.log("ResourceDemandItem: component has been activated --")},deactivated(){console.log("ResourceDemandItem: component has been deactivated -- ")},methods:{beforeRouteEnter(e,t,o){console.log("ResourceDemandItem: component has been beforeRouteEnter -- ")},beforeRouteLeave(e,t,o){console.log("ResourceDemandItem: component has been beforeRouteLeave -- ")},handleCommand(e){this.$message("click on item "+e),this.$emit("command",e)}}},l=s,r=(o("47a1"),o("2877")),c=Object(r["a"])(l,a,i,!1,null,null,null);t["default"]=c.exports},"871d":function(e,t,o){"use strict";o.r(t);var a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",[o("div",{staticClass:"edit-list"},[o("span",[e._v("与我的关系")]),e.isHaveTag?o("el-tag",{attrs:{closable:"","disable-transitions":!1},on:{close:function(t){return e.onTagDelete(e.selectedTag)}}},[e._v(" "+e._s(e.selectedTag)+" ")]):e._e()],1),o("el-radio-group",{on:{input:e.onRelationChoosed},model:{value:e.selectedTag,callback:function(t){e.selectedTag=t},expression:"selectedTag"}},e._l(e.dynamicTags,(function(t,a){return o("el-radio-button",{key:a,attrs:{label:t}},[e._v(" "+e._s(t)+" ")])})),1),e.inputVisible?o("el-input",{ref:"saveTagInput",staticClass:"input-new-tag",attrs:{size:"small"},on:{blur:e.handleInputConfirm},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleInputConfirm.apply(null,arguments)}},model:{value:e.inputValue,callback:function(t){e.inputValue=t},expression:"inputValue"}}):o("el-button",{staticClass:"button-new-tag",attrs:{size:"small"},on:{click:e.showInput}},[e._v(" + New Tag ")])],1)},i=[],n={name:"ProfileRelationTags",props:{relation:{type:String,default:"",required:!1}},data(){return{dynamicTags:["我","妻子","丈夫","儿子","女儿","爸爸","妈妈","爷爷","奶奶","外公","外婆","家人","哥哥","姐姐","弟弟","妹妹","亲戚","男朋友","女朋友","同事","朋友","同学","闺蜜","客户","供应商","合作伙伴","其他"],inputVisible:!1,inputValue:"",selectedTag:"",isHaveTag:!1}},watch:{relation(e,t){console.log("ProfileRelationTags: relation",e,t),this.selectedTag=e}},mounted(){""===this.relation?this.isHaveTag=!1:(this.isHaveTag=!0,this.selectedTag=this.relation),console.log("ProfileRelationTags: mounted",this.selectedTag)},methods:{handleClose(e){this.dynamicTags.splice(this.dynamicTags.indexOf(e),1)},showInput(){this.inputVisible=!0,this.$nextTick(e=>{this.$refs.saveTagInput.$refs.input.focus()})},handleInputConfirm(){let e=this.inputValue;e&&this.dynamicTags.push(e),this.inputVisible=!1,this.inputValue=""},onTagDelete(e){console.log("ProfileRelationTags: onTagDelete",e),this.isHaveTag=!1},onRelationChoosed(e){console.log("ProfileRelationTags: onRelationChoosed",this.selectedTag,e),this.isHaveTag=!0,this.$emit("relationChoosed",this.selectedTag)}}},s=n,l=(o("c0ea"),o("2877")),r=Object(l["a"])(s,a,i,!1,null,null,null);t["default"]=r.exports},"8b38":function(e,t,o){"use strict";o("07c4")},"8d44":function(e,t,o){"use strict";o.r(t);var a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"reanme-container"},[o("div",{staticClass:"edit-list",on:{click:e.onRenameReq}},[o("span",[e._v("人物命名")]),o("span",[e._v(e._s(e.newName)+">")])]),o("el-dialog",{attrs:{title:"重命名",visible:e.dialogVisible,width:"30%",modal:!1},on:{"update:visible":function(t){e.dialogVisible=t}}},[o("el-form",[o("el-form-item",{attrs:{label:"姓名","label-width":"120px"}},[o("el-input",{attrs:{autocomplete:"off",placeholder:"请输入新名字"},model:{value:e.newName,callback:function(t){e.newName=t},expression:"newName"}})],1)],1),o("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[o("el-button",{on:{click:function(t){e.dialogVisible=!1}}},[e._v("取 消")]),o("el-button",{attrs:{type:"primary"},on:{click:e.onConfirmRename}},[e._v("确 定")])],1)],1)],1)},i=[],n={name:"Rename",components:{},props:{name:{type:String,default:"未命名",required:!0}},data(){return{dialogVisible:!1,newName:""}},watch:{name(e,t){console.log("Rename: watch name",e),this.newName=e}},mounted(){console.log("Rename: mounted",this.name),this.newName=this.name},methods:{onRenameReq(){this.dialogVisible=!0,console.log("Rename: onRenameReq"),this.$emit("rename")},onConfirmRename(e){console.log("Rename: handleConfirmName",this.newName),this.dialogVisible=!1,this.$emit("confirmRename",this.newName)}}},s=n,l=(o("8b38"),o("2877")),r=Object(l["a"])(s,a,i,!1,null,null,null);t["default"]=r.exports},"926f":function(e,t,o){},9982:function(e,t,o){"use strict";o("be72")},a7e4:function(e,t,o){"use strict";o.r(t);var a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",[o("el-dialog",{attrs:{title:"Add Resource",visible:e.dialogFormVisible},on:{"update:visible":function(t){e.dialogFormVisible=t}}},[o("el-form",{attrs:{model:e.form}},[o("el-form-item",{attrs:{label:"Profile","label-width":e.formLabelWidth}},[o("el-select",{attrs:{filterable:"",clearable:"",placeholder:"Please Choose a Person"},model:{value:e.form.profile,callback:function(t){e.$set(e.form,"profile",t)},expression:"form.profile"}},[o("el-option",{attrs:{label:"葛维冬",value:1}}),o("el-option",{attrs:{label:"韩莉",value:5}}),o("el-option",{attrs:{label:"葛丰炳",value:33}})],1)],1),o("el-form-item",{attrs:{label:"Title","label-width":e.formLabelWidth}},[o("el-input",{attrs:{autocomplete:"off"},model:{value:e.form.name,callback:function(t){e.$set(e.form,"name",t)},expression:"form.name"}})],1),o("el-form-item",{attrs:{label:"Desc.","label-width":e.formLabelWidth}},[o("el-input",{attrs:{autocomplete:"off"},model:{value:e.form.desc,callback:function(t){e.$set(e.form,"desc",t)},expression:"form.desc"}})],1)],1),o("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[o("el-button",{on:{click:e.onCancel}},[e._v("取 消")]),o("el-button",{attrs:{type:"primary"},on:{click:e.onConfirm}},[e._v("确 定")])],1)],1)],1)},i=[],n=o("6c6e"),s={name:"ResourceAdd",components:{},props:{visible:{type:Boolean,default:!1,required:!0}},data(){return{dialogFormVisible:!1,form:{name:"",profile:"",desc:""},formLabelWidth:"120px"}},computed:{},watch:{visible(e,t){console.log("ResourceDemandAdd: watch visible",e),this.dialogFormVisible=e}},created(){console.log("ResourceDemandAdd: component has been created --")},mounted(){console.log("ResourceDemandAdd: component has been mounted --"),this.dialogFormVisible=this.isVisible},activated(){console.log("ResourceDemandAdd: component has been activated --")},deactivated(){console.log("ResourceDemandAdd: component has been deactivated -- ")},methods:{beforeRouteEnter(e,t,o){console.log("ResourceDemandAdd: component has been beforeRouteEnter -- ")},beforeRouteLeave(e,t,o){console.log("ResourceDemandAdd: component has been beforeRouteLeave -- ")},onCancel(){console.log("ResourceDemandAdd: onCancel"),this.$emit("done","cancel")},onConfirm(){console.log("ResourceDemandAdd: onConfirm",this.form),this.onAddResource(),this.$emit("done","confirm")},async onAddResource(){await Object(n["addResource"])(this.form).then(e=>{console.log("ResourceDemandAdd: addResource",e,e.id),this.$message({message:`创建成功, name is ${e.name}, id is ${e.id}`,type:"success"})})}}},l=s,r=o("2877"),c=Object(r["a"])(l,a,i,!1,null,null,null);t["default"]=c.exports},ad02:function(e,t,o){"use strict";o.r(t);var a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",[o("el-row",{staticClass:"row-bg",attrs:{gutter:12,type:"flex",justify:"space-around"}},e._l(e.items,(function(t){return o("el-col",{key:t.id,attrs:{xs:24,sm:12,md:12,lg:8,xl:6}},[o("resourceDemandItem",{attrs:{item:t},on:{command:e.onHandleCommand}})],1)})),1),e.isNoResourceDemand?o("el-empty",{attrs:{image:"https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png",description:"No Data"}},[o("el-button",{attrs:{type:"primary"},on:{click:e.onAdd}},[e._v("Add")])],1):e._e(),o("ResourceAdd",{attrs:{visible:e.dialogResourceVisible},on:{done:e.onConfirmAdd}}),o("DemandAdd",{attrs:{visible:e.dialogDemandVisible},on:{done:e.onConfirmAdd}})],1)},i=[],n=o("7485"),s=o("a7e4"),l=o("0fb0"),r={name:"ResourceDemand",components:{resourceDemandItem:n["default"],ResourceAdd:s["default"],DemandAdd:l["default"]},props:{items:{type:Array,default:()=>[],required:!1},type:{type:String,default:"resource",required:!1}},data(){return{isNoResourceDemand:!1,dialogResourceVisible:!1,dialogDemandVisible:!1}},computed:{},watch:{items(e,t){console.log("ResourceDemand: items have bee changed: ",e),0===e.length?this.isNoResourceDemand=!0:this.isNoResourceDemand=!1}},created(){console.log("ResourceDemand: component has been created --")},mounted(){console.log("ResourceDemand: component has been mounted --",this.items.length)},activated(){console.log("ResourceDemand: component has been activated --")},deactivated(){console.log("ResourceDemand: component has been deactivated -- ")},methods:{beforeRouteEnter(e,t,o){console.log("ResourceDemand: component has been beforeRouteEnter -- ")},beforeRouteLeave(e,t,o){console.log("ResourceDemand: component has been beforeRouteLeave -- ")},onAdd(){console.log("ResourceDemand: onAdd, item length and type is:",this.items.length,this.type),this.items.length<3?"resource"===this.type?this.dialogResourceVisible=!0:"demand"===this.type&&(this.dialogDemandVisible=!0):this.$message({message:"最多只能添加3个资源需求",type:"warning"})},onConfirmAdd(e){this.dialogResourceVisible=!1,this.dialogDemandVisible=!1},onHandleCommand(e){switch(console.log("ResourceDemand: onHandleCommand",e),e){case"add":this.onAdd();break;case"delete":break;default:break}}}},c=r,d=o("2877"),m=Object(d["a"])(c,a,i,!1,null,null,null);t["default"]=m.exports},b667:function(e,t,o){},bc56:function(e,t,o){"use strict";o("48c8")},be72:function(e,t,o){},c067:function(e,t,o){"use strict";o.r(t);var a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"gallery-container"},[o("el-carousel",{attrs:{interval:2e3,"indicator-position":"none",arrow:"always",height:"300px",type:"card"},on:{change:e.carouselChange}},e._l(e.items,(function(e){return o("el-carousel-item",{key:e.id},[o("el-row",{attrs:{gutter:12}},[o("el-col",{staticStyle:{height:"400px","margin-bottom":"20px display: flex","align-items":"center","justify-content":"center"}},[o("img",{ref:"banner",refInFor:!0,staticStyle:{"max-width":"100%","max-height":"100%","object-fit":"contain"},attrs:{src:e.thumb,alt:""}})])],1)],1)})),1)],1)},i=[],n={name:"Carosel",components:{},props:{items:{type:Array,default:()=>[],required:!0},title:{type:String,default:"deep-diary",required:!1}},data(){return{bannerHeight:""}},watch:{items(e,t){console.log("Carosel: watch items changed",e)}},created(){},mounted(){},methods:{carouselChange:function(e,t){}}},s=n,l=o("2877"),r=Object(l["a"])(s,a,i,!1,null,"4fef49c5",null);t["default"]=r.exports},c0ea:function(e,t,o){"use strict";o("19c5")},c49f:function(e,t,o){"use strict";o.r(t);var a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"reanme-container"},[o("div",{staticClass:"edit-list",on:{click:e.onChangeAvatarReq}},[o("img",{staticClass:"user-avatar",attrs:{src:e.avatar,alt:""}}),o("span",[e._v("选择封面>")])]),o("el-dialog",{attrs:{title:"选择封面",visible:e.dialogVisible,width:"30%",modal:!1},on:{"update:visible":function(t){e.dialogVisible=t}}},[e.isMounted?o("FaceList",{attrs:{id:e.FaceQueryForm.profile},on:{choosed:e.onChoosed}}):e._e(),o("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[o("el-button",{on:{click:function(t){e.dialogVisible=!1}}},[e._v("取 消")]),o("el-button",{attrs:{type:"primary"},on:{click:e.onConfirmAvatar}},[e._v("确 定")])],1)],1)],1)},i=[],n=o("f5d0"),s={name:"EditAvatar",components:{FaceList:n["default"]},props:{avatar:{type:String,default:"未命名",required:!0},id:{type:Number,default:0,required:!0}},data(){return{dialogVisible:!1,isMounted:!1,choosedFace:null,newAvatar:"",FaceQueryForm:{page:1,size:20,profile:1,det_score__gt:.7}}},watch:{},mounted(){console.log("EditAvatar: mounted",this.avatar),this.newAvatar=this.avatar},methods:{onChangeAvatarReq(){this.dialogVisible=!0,this.FaceQueryForm.profile=this.id,this.isMounted=!0,console.log("EditAvatar: onChangeAvatarReq, this.FaceQueryForm.id",this.FaceQueryForm.profile)},onChoosed(e){this.choosedFace=e,console.log("EditAvatar: onChoosed",this.newAvatar)},onConfirmAvatar(e){console.log("EditAvatar: onConfirmAvatar",this.newAvatar),this.dialogVisible=!1,this.newAvatar=this.choosedFace.thumb,this.$emit("confirmAvatar",this.choosedFace)}}},l=s,r=(o("9982"),o("2877")),c=Object(r["a"])(l,a,i,!1,null,null,null);t["default"]=c.exports},fd15:function(e,t,o){"use strict";o.r(t);var a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",[o("el-card",{attrs:{shadow:"hover"}},[o("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[o("span",[e._v(e._s(e.itemLocal.name))]),o("Menu",{attrs:{menus:e.menus},on:{command:e.handleCommand}})],1),o("div",{staticClass:"text item"},[e._v(" "+e._s(e.itemLocal.desc)+" ")]),o("el-carousel",{attrs:{height:"200px"}},e._l(e.itemLocal.images,(function(t){return o("el-carousel-item",{key:t.id},[o("el-image",{staticStyle:{width:"100%"},attrs:{src:t.thumb,fit:"cover","preview-src-list":e.srcList}})],1)})),1)],1)],1)},i=[],n=o("ff49"),s={name:"ExperienceItem",components:{Menu:n["default"]},props:{item:{type:Object,default:()=>({id:1,company:"宁波福尔达智能科技股份有限公司",company_PyInitial:"nbfedznkjgfyxgs",images:[{id:6,src:"https://deep-diary.oss-accelerate.aliyuncs.com/media/user_info_img/avatar.jpg",thumb:"https://deep-diary.oss-accelerate.aliyuncs.com/media/CACHE/images/user_info_img/avatar/d5e22908141f1dca9b7144e4d08c25d8.jpg"},{id:7,src:"https://deep-diary.oss-accelerate.aliyuncs.com/media/user_info_img/IMG_20210909_194805.jpg",thumb:"https://deep-diary.oss-accelerate.aliyuncs.com/media/CACHE/images/user_info_img/IMG_20210909_194805/409854c23b91bb02ca91b98ff4114721.jpg"}],position:"项目经理",start_date:"2021-10-08",end_date:"2023-09-27",name:"SE336出风口",desc:"内叶片自动关风为导向传统出风口,出口安通林与HBPO终端客户为西班牙西亚特",duty:"1.全面主持项目日常管理工作，按照计划组织日常工作，同时进行全面管理及过程监督， \t\t保证进度，质量，控成本完成项目 \t2.参加设计评审会议，模具工装等评审会议，主持日常技术交流会议 \t3.基于公司经营项目制定的目标预算，利用产线合并，降低费用支出，严控预算使用风险 4.跟踪把控产品质量，外购标准件采购进度等，有效实施过程质量监控 5．根据进度节点制定上报计划及设置进度提醒机制，审核工、模、检等进度计划，对各个模块定期检查、分析进度完成情况",achievement:"1. 通过TR交流赢得客户认可，促进项目定点；2. 按时完成客户要求的节点并按时完成第一次产品交样"}),required:!0}},data(){return{itemLocal:this.item,srcList:[],menus:[{icon:"el-icon-circle-plus",text:"Add"},{icon:"el-icon-remove",text:"Remove"},{icon:"el-icon-edit",text:"Edit"},{icon:"el-icon-view",text:"View"},{icon:"el-icon-delete",text:"Reset"},{icon:"el-icon-upload",text:"Upload"},{icon:"el-icon-setting",text:"Setting"}]}},computed:{},watch:{item:{handler:function(e,t){console.log("ExperienceItem: item has been changed -- "),this.itemLocal=e,0===this.itemLocal.images.length&&(console.log("ExperienceItem: item.images is empty -- "),this.itemLocal.images=[{id:1,src:"https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png",thumb:"https://deep-diary.oss-accelerate.aliyuncs.com/media/sys_img/logo_lg.png"}]),this.srcList=this.itemLocal.images.map(e=>e.src)},deep:!0}},created(){console.log("ExperienceItem: component has been created --")},mounted(){console.log("ExperienceItem: component has been mounted --"),console.log("ExperienceItem: item = ",this.item)},activated(){console.log("ExperienceItem: component has been activated --")},deactivated(){console.log("ExperienceItem: component has been deactivated -- ")},methods:{beforeRouteEnter(e,t,o){console.log("ExperienceItem: component has been beforeRouteEnter -- ")},beforeRouteLeave(e,t,o){console.log("ExperienceItem: component has been beforeRouteLeave -- ")},handleCommand(e){this.$message("click on item "+e),this.$emit("command",e)}}},l=s,r=(o("bc56"),o("2877")),c=Object(r["a"])(l,a,i,!1,null,null,null);t["default"]=c.exports},ff49:function(e,t,o){"use strict";o.r(t);var a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{staticClass:"menu-container"},[o("el-dropdown",{on:{command:e.handleCommand}},[o("span",{staticClass:"el-dropdown-link"},[o("i",{staticClass:"el-icon-menu el-icon--right"})]),o("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},e._l(e.menus,(function(t){return o("el-dropdown-item",{key:t.text,attrs:{command:t.text.toLowerCase()}},[o("i",{class:t.icon}),e._v(" "+e._s(t.text)+" ")])})),1)],1)],1)},i=[],n={name:"Menu",components:{},props:{menus:{type:Array,default:()=>[{icon:"el-icon-circle-plus",text:"Add"},{icon:"el-icon-remove",text:"Remove"},{icon:"el-icon-edit",text:"Edit"},{icon:"el-icon-view",text:"View"},{icon:"el-icon-delete",text:"Reset"},{icon:"el-icon-upload",text:"Upload"},{icon:"el-icon-setting",text:"Setting"}],required:!1}},data(){return{}},watch:{},created(){},mounted(){},methods:{handleCommand(e){this.$message("click on item "+e),this.$emit("command",e)}}},s=n,l=o("2877"),r=Object(l["a"])(s,a,i,!1,null,"7c247514",null);t["default"]=r.exports}}]);