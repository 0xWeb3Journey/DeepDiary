/*!
 *  build: vue-admin-better 
 *  vue-admin-beautiful.com 
 *  https://gitee.com/chu1204505056/vue-admin-better 
 *  time: 2023-11-20 22:24:12
 */
(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2b4a9e00"],{"310f":function(e,t,a){"use strict";a.r(t);var l=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"search-container"},[a("el-input",{attrs:{clearable:"",placeholder:"Please input what you want"},on:{change:e.onSearch},model:{value:e.faceQuery.search,callback:function(t){e.$set(e.faceQuery,"search",t)},expression:"faceQuery.search"}},[a("i",{staticClass:"el-input__icon el-icon-search",attrs:{slot:"prefix"},on:{click:e.advancedSearch},slot:"prefix"}),a("el-dropdown",{attrs:{slot:"append",icon:"el-icon-delete"},on:{command:e.handleCommand},slot:"append"},[a("span",{staticClass:"el-dropdown-link"},[a("i",{staticClass:"el-icon-menu el-icon--right"})]),a("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[a("el-dropdown-item",{attrs:{command:"edit"}},[a("i",{staticClass:"el-icon-edit"}),e._v(" Edit ")]),a("el-dropdown-item",{attrs:{command:"view"}},[a("i",{staticClass:"el-icon-view"}),e._v(" View ")]),a("el-dropdown-item",{attrs:{command:"delete"}},[a("i",{staticClass:"el-icon-delete"}),e._v(" Reset ")]),a("el-dropdown-item",{attrs:{command:"setting"}},[a("i",{staticClass:"el-icon-setting"}),e._v(" Setting ")])],1)],1)],1),e.advanced?a("div",{staticClass:"advancedSearch"},[a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Is Confirmed?",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.confirmed,callback:function(t){e.$set(e.faceQuery,"confirmed",t)},expression:"faceQuery.confirmed"}},e._l(e.filterList.confirmed,(function(t){return a("el-option",{key:t.name,attrs:{label:t.name,value:t.value,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t.name))])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Relation to Me",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.relation,callback:function(t){e.$set(e.faceQuery,"relation",t)},expression:"faceQuery.relation"}},e._l(e.filterList.relation,(function(t){return a("el-option",{key:t,attrs:{label:t,value:t,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t))])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Friend Name",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.profile__name,callback:function(t){e.$set(e.faceQuery,"profile__name",t)},expression:"faceQuery.profile__name"}},e._l(e.filterList.profile__name,(function(t){return a("el-option",{key:t.name,attrs:{label:t.name,value:t.name,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t.name))]),a("span",{staticStyle:{float:"right",color:"#8492a6","font-size":"13px"}},[e._v(" "+e._s(t.value)+" ")])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Named Face or not",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.profile__isnull,callback:function(t){e.$set(e.faceQuery,"profile__isnull",t)},expression:"faceQuery.profile__isnull"}},e._l(e.filterList.profile__isnull,(function(t){return a("el-option",{key:t.name,attrs:{label:t.name,value:t.value,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t.name))])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Det Score Bigger Then",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.det_score__gt,callback:function(t){e.$set(e.faceQuery,"det_score__gt",t)},expression:"faceQuery.det_score__gt"}},e._l(e.filterList.det_score__gt,(function(t){return a("el-option",{key:t,attrs:{label:t,value:t,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t))]),a("span",{staticStyle:{float:"right",color:"#8492a6","font-size":"13px"}},[e._v(" "+e._s(t.value)+" ")])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Det Score Smaller Then",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.det_score__lt,callback:function(t){e.$set(e.faceQuery,"det_score__lt",t)},expression:"faceQuery.det_score__lt"}},e._l(e.filterList.det_score__lt,(function(t){return a("el-option",{key:t,attrs:{label:t,value:t,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t))]),a("span",{staticStyle:{float:"right",color:"#8492a6","font-size":"13px"}},[e._v(" "+e._s(t.value)+" ")])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Face Score Bigger Then",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.face_score__gt,callback:function(t){e.$set(e.faceQuery,"face_score__gt",t)},expression:"faceQuery.face_score__gt"}},e._l(e.filterList.face_score__gt,(function(t){return a("el-option",{key:t,attrs:{label:t,value:t,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t))])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Face Score Smaller Then",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.face_score__lt,callback:function(t){e.$set(e.faceQuery,"face_score__lt",t)},expression:"faceQuery.face_score__lt"}},e._l(e.filterList.face_score__lt,(function(t){return a("el-option",{key:t,attrs:{label:t,value:t,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t))])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Gender",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.gender,callback:function(t){e.$set(e.faceQuery,"gender",t)},expression:"faceQuery.gender"}},e._l(e.filterList.gender,(function(t){return a("el-option",{key:t.name,attrs:{label:t.name,value:t.value,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t.name))])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Look Up",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.pose_x__gt,callback:function(t){e.$set(e.faceQuery,"pose_x__gt",t)},expression:"faceQuery.pose_x__gt"}},e._l(e.filterList.pose_x__gt,(function(t){return a("el-option",{key:t,attrs:{label:t,value:t,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t))])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Look Down",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.pose_x__lt,callback:function(t){e.$set(e.faceQuery,"pose_x__lt",t)},expression:"faceQuery.pose_x__lt"}},e._l(e.filterList.pose_x__lt,(function(t){return a("el-option",{key:t,attrs:{label:t,value:t,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t))])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Look Right",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.pose_y__gt,callback:function(t){e.$set(e.faceQuery,"pose_y__gt",t)},expression:"faceQuery.pose_y__gt"}},e._l(e.filterList.pose_y__gt,(function(t){return a("el-option",{key:t,attrs:{label:t,value:t,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t))])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Look Left",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.pose_y__lt,callback:function(t){e.$set(e.faceQuery,"pose_y__lt",t)},expression:"faceQuery.pose_y__lt"}},e._l(e.filterList.pose_y__lt,(function(t){return a("el-option",{key:t,attrs:{label:t,value:t,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t))])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Rotate Right",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.pose_z__gt,callback:function(t){e.$set(e.faceQuery,"pose_z__gt",t)},expression:"faceQuery.pose_z__gt"}},e._l(e.filterList.pose_z__gt,(function(t){return a("el-option",{key:t,attrs:{label:t,value:t,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t))])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Rotate Left",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.pose_z__lt,callback:function(t){e.$set(e.faceQuery,"pose_z__lt",t)},expression:"faceQuery.pose_z__lt"}},e._l(e.filterList.pose_z__lt,(function(t){return a("el-option",{key:t,attrs:{label:t,value:t,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t))])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Width Bigger Then",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.wid__gt,callback:function(t){e.$set(e.faceQuery,"wid__gt",t)},expression:"faceQuery.wid__gt"}},e._l(e.filterList.wid__gt,(function(t){return a("el-option",{key:t,attrs:{label:t,value:t,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t))])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"Width Smaller Then",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.wid__lt,callback:function(t){e.$set(e.faceQuery,"wid__lt",t)},expression:"faceQuery.wid__lt"}},e._l(e.filterList.wid__lt,(function(t){return a("el-option",{key:t,attrs:{label:t,value:t,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t))])])})),1),a("el-select",{attrs:{clearable:"",filterable:"","default-first-option":"",placeholder:"State",loading:e.loading},on:{change:e.onSearch},model:{value:e.faceQuery.state,callback:function(t){e.$set(e.faceQuery,"state",t)},expression:"faceQuery.state"}},e._l(e.filterList.state,(function(t){return a("el-option",{key:t.name,attrs:{label:t.name,value:t.value,disabled:!1}},[a("span",{staticStyle:{float:"left",color:"#8492a6"}},[e._v(e._s(t.name))])])})),1)],1):e._e()],1)},i=[],s=a("e21c"),n={name:"FaceSearch",components:{},props:{filteredList:{type:Object,default:function(){return{face_color:["skin","black","grey","blue","light grey"],fore_color:["light brown","beige","light blue"],back_color:["black","blue","light grey"]}},required:!1}},data(){return{faceQuery:{page:1,size:25,search:"",confirmed:1,profile__isnull:"",profile__name:"",profile:"",det_score__gt:"",det_score__lt:"",face_score__gt:"",face_score__lt:"",age__gt:"",age__lt:"",gender:"",pose_x__gt:"",pose_x__lt:"",pose_y__gt:"",pose_y__lt:"",pose_z__gt:"",pose_z__lt:"",wid__gt:"",wid__lt:"",state:"",relation:""},checked_fcGroup:"",filterList:{confirmed:[{name:"Unconfirmed",value:0},{name:"Confirmed",value:1}],profile__name:[{name:"葛维冬",value:501},{name:"葛昱琛",value:457},{name:"韩莉",value:332},{name:"unknown",value:279},{name:"叶四妹",value:68},{name:"葛顺法",value:63},{name:"马成学",value:59},{name:"张立华",value:56},{name:"葛菊英",value:40},{name:"葛丰炳",value:33},{name:"王呐",value:30},{name:"赵妮",value:15},{name:"刘欢",value:14}],profile__isnull:[{name:"Has Related Profile",value:0},{name:"No Related Profile",value:1}],det_score__gt:[.9,.8,.7,.6,.5],det_score__lt:[.4,.5,.6,.7,.8],face_score__gt:[.9,.8,.7,.6,.5],face_score__lt:[.4,.5,.6,.7,.8],gender:[{name:"Female",value:0},{name:"Male",value:1}],pose_x__gt:[-20,-10,0,10,20],pose_x__lt:[-20,-10,0,10,20],pose_y__gt:[-20,-10,0,10,20],pose_y__lt:[-20,-10,0,10,20],pose_z__gt:[-20,-10,0,10,20],pose_z__lt:[-20,-10,0,10,20],wid__gt:[1e3,800,600,400,200],wid__lt:[1e3,800,600,400,200],state:[{name:"Normal",value:0},{name:"Forbidden",value:1},{name:"Deleted",value:9}],relation:[]},list:[],loading:!1,states:[],ratingColors:["#99A9BF","#F7BA2A","#FF9900"],advanced:!1}},watch:{},created(){},mounted(){this.fetchCategory()},methods:{onSearch(){this.faceQuery.page=1;let e=Object.assign({},this.faceQuery);for(let t in this.faceQuery)Array.isArray(this.faceQuery[t])&&(e[t]=this.faceQuery[t].toString());console.log("onCateSearch",this.faceQuery,e),this.$emit("handleFaceSearch",e),this.fetchCategory(e)},onCateSearch(e){this.faceQuery.page=1;let t=Object.assign({},this.faceQuery);t.categories__name=e,this.$emit("handlefaceSearch",t),this.fetchCategory(t)},async fetchCategory(e){console.log("start to get the Category list...");const{data:t}=await Object(s["getFilterList"])(e);this.filterList=t,console.log("this.filterList",this.filterList,t)},reset_search(){console.log(this.$data),console.log(this.$options.data()),Object.assign(this.$data,this.$options.data()),this.fetchCategory(),this.onSearch()},advancedSearch(){console.log("advancedSearch"),this.advanced=!this.advanced},handleCommand(e){this.$message("click on item "+e),"reset"===e?this.reset_search():this.$emit(e)}}},o=n,r=a("2877"),c=Object(r["a"])(o,l,i,!1,null,"3d6d16bc",null);t["default"]=c.exports},"41cf":function(e,t,a){"use strict";a.r(t);var l=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"album_container"},[a("div",{directives:[{name:"infinite-scroll",rawName:"v-infinite-scroll",value:e.load,expression:"load"}],ref:"album_container",staticClass:"content",attrs:{id:"album_container","infinite-scroll-disabled":"busy","infinite-scroll-distance":"400","infinite-scroll-immediate-check":"true","force-use-infinite-wrapper":!0}},[e._l(e.items,(function(t,l){return a("div",{key:t.id,on:{click:function(a){return e.onClick(a,l,t)},dblclick:function(a){return e.onDoubleClick(a,l,t)}}},[a("img",{class:e.checkedIndex===l?"img-checked hvr-pulse grow":"img-unchecked hvr-pulse grow",attrs:{className:"img-responsive",src:t.thumb,alt:t.name}}),a("div",{staticClass:"jg-caption"},[a("el-badge",{staticClass:"item",attrs:{value:t.value,max:99,type:"primary"}},[a("el-input",{staticClass:"item-name",staticStyle:{float:"left","font-size":"8px"},attrs:{size:"small",placeholder:"Change the Name"},on:{blur:function(a){return e.changeName(t.name,t)}},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.enterBlur(t)}},model:{value:t.name,callback:function(a){e.$set(t,"name",a)},expression:"item.name"}})],1)],1)])})),a("div",{directives:[{name:"show",rawName:"v-show",value:e.busy,expression:"busy"}],staticClass:"loading"},[a("h3",[e._v(e._s(e.msg))])])],2),a("el-divider",{directives:[{name:"show",rawName:"v-show",value:e.finished,expression:"finished"}]},[a("i",{staticClass:"el-icon-finished"})])],1)},i=[],s=a("1157"),n=a.n(s),o=(a("cfd5"),a("a809"),a("487a")),r=a.n(o),c=(a("2cab"),{name:"AlbumContainer",directives:{infiniteScroll:r.a},props:{items:{type:Array,default:()=>Array(40).fill({}),required:!0},total:{type:Number,default:50,required:!0},title:{type:String,default:"Album",required:!0},busy:{type:Boolean,default:!1,required:!0},finished:{type:Boolean,default:!1,required:!1}},data(){return{msg:"正在加载...",intervalId:null,checkedIndex:-1,checkedId:0}},watch:{items(e,t){console.log("Album.content: Album numbers have been changed",e.length,this.total,this.msg),this.$nextTick(()=>{n()("#album_container").justifiedGallery()}),this.checkDivHeight()}},created(){console.log("Album.content: Album component created")},mounted(){this.justifyInit()},activated(){console.log("Album contetn: activated"),this.checkDivHeight()},deactivated(){console.log("Album contetn: deactivated"),clearInterval(this.intervalId),this.intervalId=null},methods:{justifyInit:function(){n()("[id=album_container]").justifiedGallery({captions:!0,lastRow:"left",rowHeight:150,margins:5}).on("jg.complete",(function(){console.log("Album.content: jg.complete event was trigged")}))},onClick(e,t,a){console.log("Album.content: onClick: ",a),this.checkedIndex=t,t<0||null!==a&&(this.checkedId=a.id,this.$emit("albumClick",t,a))},onDoubleClick(e,t,a){console.log("Album.content: onDoubleClick"),this.$emit("doubleClick",t,a)},changeName(e,t){console.log("Album.content: changeName"),this.$emit("changeName",e,t)},enterBlur(e){console.log("Album.content: enterBlur"),e.target.blur()},load(){console.log("infinite loading... ",this.busy),this.busy||this.$emit("load")},checkDivHeight(){if(null===this.intervalId){var e=this.$refs.album_container;e&&(this.intervalId=setInterval(()=>{if(!1===this.busy){var t=e.scrollHeight,a=e.scrollTop,l=1e3;console.log("Gallery Contetn: checkDivHeight:divElement: The div is not filled.",a,t,l,this.finished),t>l||this.finished?(clearInterval(this.intervalId),this.intervalId=null,console.log("timer has been closed")):this.$emit("load")}},1e3))}else console.log("Gallery content: checkDivHeight: intervalId is not null")}}}),d=c,u=(a("d890"),a("2877")),f=Object(u["a"])(d,l,i,!1,null,"795ced1c",null);t["default"]=f.exports},"56bb":function(e,t,a){},"5efe":function(e,t,a){},"635a":function(e,t,a){"use strict";a.r(t);var l=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("el-dialog",{attrs:{"before-close":e.handleClose,"close-on-click-modal":!1,title:e.title,visible:e.dialogFormVisible,width:"909px"},on:{"update:visible":function(t){e.dialogFormVisible=t}}},[a("div",{staticClass:"upload"},[a("el-alert",{attrs:{closable:!1,title:"支持jpg、jpeg、png格式，单次可最多选择"+e.limit+"张图片，每张不可大于"+e.size+"M，如果大于"+e.size+"M会自动为您过滤",type:"info"}}),a("br"),a("el-upload",{ref:"upload",staticClass:"upload-content",attrs:{action:e.action,"auto-upload":!1,"close-on-click-modal":!1,data:e.data,"file-list":e.fileList,headers:e.headers,limit:e.limit,multiple:!0,name:e.name,"on-change":e.handleChange,"on-error":e.handleError,"on-exceed":e.handleExceed,"on-preview":e.handlePreview,"on-progress":e.handleProgress,"on-remove":e.handleRemove,"on-success":e.handleSuccess,accept:"image/png, image/jpeg","list-type":"picture-card"}},[a("i",{staticClass:"el-icon-plus",attrs:{slot:"trigger"},slot:"trigger"}),a("el-dialog",{attrs:{visible:e.dialogVisible,"append-to-body":"",title:"查看大图"},on:{"update:visible":function(t){e.dialogVisible=t}}},[a("div",[a("img",{attrs:{src:e.dialogImageUrl,alt:"",width:"100%"}})])])],1)],1),a("div",{staticClass:"dialog-footer",staticStyle:{position:"relative","padding-right":"15px","text-align":"right"},attrs:{slot:"footer"},slot:"footer"},[e.show?a("div",{staticStyle:{position:"absolute",top:"10px",left:"15px",color:"#999"}},[e._v(" 正在上传中... 当前上传成功数:"+e._s(e.imgSuccessNum)+"张 当前上传失败数:"+e._s(e.imgErrorNum)+"张 ")]):e._e(),a("el-button",{attrs:{type:"primary"},on:{click:e.handleClose}},[e._v("关闭")]),a("el-button",{staticStyle:{"margin-left":"10px"},attrs:{loading:e.loading,size:"small",type:"success"},on:{click:e.submitUpload}},[e._v(" 开始上传 ")])],1)])},i=[],s=a("f121"),n=a("4360"),o=a("970f"),r={name:"Upload",props:{url:{type:String,default:"api/img/",required:!0},name:{type:String,default:"src",required:!0},limit:{type:Number,default:500,required:!0},size:{type:Number,default:8,required:!0}},data(){return{show:!1,loading:!1,dialogVisible:!1,dialogImageUrl:"",action:s["baseURL"]+this.url,headers:{Authorization:"Bearer "+n["default"].getters["user/accessToken"]},fileList:[],picture:"picture",imgNum:0,imgSuccessNum:0,imgErrorNum:0,typeList:null,title:"上传",dialogFormVisible:!1,data:{}}},computed:{percentage(){return 0==this.allImgNum?0:100*this.$baseLodash.round(this.imgNum/this.allImgNum,2)}},methods:{submitUpload(){this.api=`${window.location.protocol}//${window.location.host}`,this.action=this.api+this.url,console.log("this.action:",this.action,"production",s["baseURL"]),this.$refs.upload.submit()},handleProgress(e,t,a){this.loading=!0,this.show=!0},handleChange(e,t){e.size>1048576*this.size?(t.map((a,l)=>{a===e&&t.splice(l,1)}),this.fileList=t):this.allImgNum=t.length},handleSuccess(e,t,a){this.imgNum=this.imgNum+1,this.imgSuccessNum=this.imgSuccessNum+1,a.length===this.imgNum&&setTimeout(()=>{this.$baseMessage(`上传完成! 共上传${a.length}张图片`,"success")},1e3),setTimeout(()=>{this.loading=!1,this.show=!1},1e3)},handleError(e,t,a){this.imgNum=this.imgNum+1,this.imgErrorNum=this.imgErrorNum+1,this.$baseMessage(`文件[${t.raw.name}]上传失败,文件大小为${this.$baseLodash.round(t.raw.size/1024,0)}KB`,"error"),setTimeout(()=>{this.loading=!1,this.show=!1},1e3)},handleRemove(e,t){this.imgNum=this.imgNum-1,this.allNum=this.allNum-1},handlePreview(e){this.dialogImageUrl=e.url,this.dialogVisible=!0},handleExceed(e,t){this.$baseMessage(`当前限制选择 ${this.limit} 个文件，本次选择了\n           ${e.length}\n           个文件`,"error")},handleShow(e){this.title="上传",this.data=e,this.dialogFormVisible=!0},handleClose(){this.fileList=[],this.picture="picture",this.allImgNum=0,this.imgNum=0,this.imgSuccessNum=0,this.imgErrorNum=0,this.uploadFinished(),this.dialogFormVisible=!1},async uploadFinished(){console.log("handleClose");const{msg:e}=await Object(o["getUploadState"])("");this.$message({message:e,type:"success"})}}},c=r,d=(a("73d2"),a("2877")),u=Object(d["a"])(c,l,i,!1,null,"2c7c9ebb",null);t["default"]=u.exports},"63a6":function(e,t,a){"use strict";a.r(t);var l=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"gallery-container"},[a("vab-upload",{ref:"vabUpload",attrs:{url:"/api/img/",name:"src",limit:50,size:8}}),a("el-card",{staticClass:"box-card"},[a("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[a("span",[e._v(e._s(e.name)+"("+e._s(e.items.length)+" / "+e._s(e.total)+")")]),a("el-button-group",{staticStyle:{float:"right"}},[a("el-button",{attrs:{type:"primary",icon:"el-icon-edit"},on:{click:e.onChangeDsipType}}),a("el-button",{attrs:{type:"primary",icon:"el-icon-upload"},on:{click:function(t){return e.handleShow({key:"value"})}}})],1)],1),a("div",{directives:[{name:"infinite-scroll",rawName:"v-infinite-scroll",value:e.load,expression:"load"}],ref:"gallery",staticClass:"infinite-list",staticStyle:{overflow:"auto"},attrs:{id:"gallery"}},e._l(e.items,(function(t){return a("a",{key:t.id,staticClass:"gallery infinite-list-item",attrs:{className:"gallery-item","data-src":"oss"===e.storageType?t.img:t.mcs.nft_url,"data-sub-html":t.desc}},[a("img",{attrs:{className:"img-responsive",src:!0===e.isDispFace?t.thumb_face:t.thumb}})])})),0)])],1)},i=[],s=a("1157"),n=a.n(s),o=a("2690"),r=a("c3c6"),c=a("c79a"),d=a("4dcd"),u=a("c1da"),f=a("5c2b"),h=(a("5abb"),a("5d6f"),a("cfd5"),a("a809"),a("635a")),g={name:"Gallery",components:{VabUpload:h["default"]},props:{items:{type:Array,default:()=>[],required:!0},name:{type:String,default:"88888888888888",required:!0},total:{type:Number,default:50,required:!0},dispType:{type:String,default:"face",required:!0},storageType:{type:String,default:"oss",required:!1},limit:{type:Number,default:50,required:!1},size:{type:Number,default:8,required:!1}},data(){return{isDispFace:"face"===this.dispType}},computed:{},watch:{items(e,t){this.$nextTick(()=>{console.log("gallery have been changed"),window.gallery.refresh(),n()("#gallery").justifiedGallery()})}},created(){},mounted(){this.lgInit(),this.justifyInit()},methods:{justifyInit:function(){n()("#gallery").justifiedGallery({captions:!1,lastRow:"left",rowHeight:150,margins:5}).on("jg.complete",(function(){console.log("jg.complete event was trigged")}))},lgInit:function(){const e=document.getElementById("gallery");window.gallery=Object(o["a"])(e,{addClass:"gallery",autoplayFirstVideo:!1,pager:!1,galleryId:"nature",plugins:[r["a"],c["a"],d["a"],u["a"],f["a"]],thumbnail:!0,slideShowInterval:2e3,mobileSettings:{controls:!1,showCloseIcon:!1,download:!1,rotate:!1}})},onChangeDsipType(){this.isDispFace=!this.isDispFace,console.log("onChangeDsipType, current isDispFace: %s",this.isDispFace)},handleShow(e){this.$refs["vabUpload"].handleShow(e)},load(){console.log("loading...")}}},m=g,p=a("2877"),_=Object(p["a"])(m,l,i,!1,null,"d29b2178",null);t["default"]=_.exports},"71d9":function(e,t,a){"use strict";a.r(t);var l=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[e.searchable?a("FaceSearch",{on:{handleFaceSearch:e.onFaceSearch}}):e._e(),a("GalleryContainer",{attrs:{items:e.faces.data,total:e.faces.totalCnt,title:e.faces.title,busy:e.faces.loading,finished:e.faces.finished},on:{load:e.onLoad}})],1)},i=[],s=a("75b3"),n=(a("63a6"),a("e21c")),o=a("310f"),r={name:"FaceListGallery",components:{GalleryContainer:s["default"],FaceSearch:o["default"]},directives:{},props:{query:{type:Object,default:null,required:!1},searchable:{type:Boolean,default:!0,required:!1},id:{type:Number,default:null,required:!1}},data:function(){return{faces:{title:"Face List",loading:!1,finished:!1,checkedId:-1,checkedIndex:-1,totalCnt:0,links:null,curCnt:0,data:[],queryForm:{page:1,size:25,profile:""}}}},watch:{id(e,t){console.log("FaceListGallery: watch: query.profile",e),this.faces.queryForm.profile=e,this.faces.queryForm.page=1,this.faces.data=[],this.fetchFace()}},created(){},mounted(){console.log("FaceListGallery: mounted",this.faces.queryForm),this.faces.queryForm.profile=this.id,console.log("FaceListGallery: mounted",this.faces.queryForm),this.fetchFace()},methods:{onRouteJump(e,t){console.log("recieved the child component value %d,%o",e,t),this.faces.checkedIndex=e,this.faces.checkedId=t.id||0},async fetchFace(){this.faces.loading=!0,this.faces.finished=!1,await Object(n["getFace"])(this.faces.queryForm).then(e=>{console.log("FaceListGallery: getFace",e);const{data:t,totalCnt:a,links:l}=e;this.faces.data=[...this.faces.data,...t],this.faces.curCnt=this.faces.data.length,this.faces.totalCnt=a,this.faces.links=l,null===this.faces.links.next&&(this.faces.finished=!0,console.log("FaceListGallery: fetchFace: no more data-----------------")),console.log("FaceListGallery: emit faceData"),this.$emit("faceData",this.faces)}),setTimeout(()=>{this.faces.loading=!1},300)},onLoad(){console.log("FaceListGallery: onLoad",this.faces.loading,this.faces.finished),this.faces.loading||(this.faces.finished?setTimeout(()=>{this.faces.loading=!1},3e3):(this.faces.queryForm.page++,this.fetchFace()))},onFaceSearch(e){console.log("recieve the queryForm info from the search component"),console.log(e),this.faces.queryForm=e,this.faces.totalCnt=0,this.faces.data=[],this.fetchFace()}}},c=r,d=a("2877"),u=Object(d["a"])(c,l,i,!1,null,null,null);t["default"]=u.exports},"73d2":function(e,t,a){"use strict";a("db9f")},"75b3":function(e,t,a){"use strict";a.r(t);var l=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"gallery-container"},[a("div",{directives:[{name:"infinite-scroll",rawName:"v-infinite-scroll",value:e.load,expression:"load"}],ref:"gallery_container",staticClass:"gallery_container",attrs:{id:"gallery_container","infinite-scroll-disabled":"busy","infinite-scroll-distance":"50","infinite-scroll-immediate-check":"true","force-use-infinite-wrapper":!0}},[a("div",{ref:"gallery",staticClass:"infinite-list",staticStyle:{overflow:"auto"},attrs:{id:"gallery"}},e._l(e.items,(function(e){return a("a",{key:e.id,staticClass:"gallery infinite-list-item hvr-pulse grow",attrs:{className:"gallery-item","data-src":e.img,"data-lg-size":e.size,"data-sub-html":e.desc}},[a("img",{attrs:{className:"img-responsive",src:e.thumb}})])})),0),a("div",{directives:[{name:"show",rawName:"v-show",value:e.busy,expression:"busy"}],staticClass:"loading"},[a("h3",[e._v(e._s(e.msg))])])]),a("el-divider",{directives:[{name:"show",rawName:"v-show",value:e.finished,expression:"finished"}]},[a("i",{staticClass:"el-icon-finished"})])],1)},i=[],s=a("1157"),n=a.n(s),o=a("2690"),r=a("c3c6"),c=a("c79a"),d=a("4dcd"),u=a("c1da"),f=a("5c2b"),h=(a("5abb"),a("5d6f"),a("cfd5"),a("a809"),a("2cab"),a("635a"),{name:"GalleryContainer",components:{},props:{items:{type:Array,default:()=>Array(40).fill({}),required:!0},total:{type:Number,default:50,required:!0},title:{type:String,default:"Album",required:!0},busy:{type:Boolean,default:!1,required:!0},finished:{type:Boolean,default:!1,required:!1}},data(){return{msg:"Loading...",intervalId:null}},computed:{},watch:{items(e,t){this.checkDivHeight(),this.$nextTick(()=>{console.log("gallery have been changed"),window.gallery.refresh(),n()("#gallery").justifiedGallery()})}},created(){},mounted(){this.lgInit(),this.justifyInit()},activated(){console.log("Gallery contetn: activated"),this.checkDivHeight()},deactivated(){console.log("Gallery contetn: deactivated"),clearInterval(this.intervalId),this.intervalId=null},methods:{justifyInit:function(){n()("#gallery").justifiedGallery({captions:!1,lastRow:"left",rowHeight:150,margins:5}).on("jg.complete",(function(){console.log("jg.complete event was trigged")}))},lgInit:function(){const e=document.getElementById("gallery");window.gallery=Object(o["a"])(e,{addClass:"gallery",subHtmlSelectorRelative:!0,autoplayFirstVideo:!1,pager:!1,galleryId:"nature",plugins:[r["a"],c["a"],d["a"],u["a"],f["a"]],thumbnail:!0,slideShowInterval:2e3,speed:500,mode:"lg-slide",appendSubHtmlTo:".lg-item",slideDelay:0,mobileSettings:{controls:!0,showCloseIcon:!0,download:!0,rotate:!0}})},onChangeDsipType(){this.isDispFace=!this.isDispFace,console.log("onChangeDsipType, current isDispFace: %s",this.isDispFace)},handleShow(e){this.$refs["vabUpload"].handleShow(e)},load(){console.log("infinite loading... ",this.busy),this.busy||this.$emit("load")},checkDivHeight(){if(null===this.intervalId){var e=this.$refs.gallery_container;e&&(this.intervalId=setInterval(()=>{if(this.$refs.gallery_container.style.height="1000px",!1===this.busy){var t=e.scrollHeight,a=(e.scrollTop,1e3);if(t>a)clearInterval(this.intervalId),this.intervalId=null,console.log("timer has been closed",t,a);else if(this.finished){clearInterval(this.intervalId),this.intervalId=null;const e=this.$refs.gallery.scrollHeight;this.$refs.gallery_container.style.height=e+"px",console.log("Set the divHeight to match content height:",this.$refs.gallery_container.style.height)}else this.$emit("load")}},1e3))}else console.log("Gallery content: checkDivHeight: intervalId is not null")}}}),g=h,m=(a("c7f7"),a("2877")),p=Object(m["a"])(g,l,i,!1,null,"4ae5c714",null);t["default"]=p.exports},"7f87":function(e,t,a){"use strict";a.r(t),a.d(t,"getProfile",(function(){return i})),a.d(t,"getProfileDetail",(function(){return s})),a.d(t,"patchProfile",(function(){return n})),a.d(t,"getProfileChangeAvatar",(function(){return o})),a.d(t,"changeFaceAlbumName",(function(){return r})),a.d(t,"clear_face_album",(function(){return c})),a.d(t,"getFilterList",(function(){return d}));var l=a("b775");function i(e){return Object(l["default"])({url:"/api/profile/",method:"get",params:e})}function s(e){return Object(l["default"])({url:"/api/profile/"+e.id+"/",method:"get",params:e})}function n(e,t){return Object(l["default"])({url:"/api/profile/"+t+"/",method:"patch",data:e})}function o(e,t){return Object(l["default"])({url:"/api/profile/"+t+"/change_avatar/",method:"get",params:e})}function r(e){return Object(l["default"])({url:"/api/profile/"+e.id+"/",method:"put",data:e})}function c(e){return Object(l["default"])({url:"/api/profile/clear_face_album/",method:"get"})}function d(e){return Object(l["default"])({url:"/api/profile/get_filtered_list/",method:"get",params:e})}},"970f":function(e,t,a){"use strict";a.r(t),a.d(t,"getImg",(function(){return i})),a.d(t,"getImgDetail",(function(){return s})),a.d(t,"getMcs",(function(){return n})),a.d(t,"getTags",(function(){return o})),a.d(t,"getUploadState",(function(){return r})),a.d(t,"getProfile",(function(){return c})),a.d(t,"getProfileDetail",(function(){return d})),a.d(t,"changeFaceAlbumName",(function(){return u})),a.d(t,"clear_face_album",(function(){return f})),a.d(t,"getFace",(function(){return h})),a.d(t,"changeFaceName",(function(){return g})),a.d(t,"getFaceGallery",(function(){return m})),a.d(t,"doEdit",(function(){return p})),a.d(t,"doDelete",(function(){return _})),a.d(t,"upload",(function(){return y})),a.d(t,"getFilterList",(function(){return b})),a.d(t,"getAddress",(function(){return v}));var l=a("b775");function i(e){return Object(l["default"])({url:"/api/img/",method:"get",params:e})}function s(e){return Object(l["default"])({url:"/api/img/"+e+"/",method:"get"})}function n(e){return Object(l["default"])({url:"/api/mcs/"+e.id+"/",method:"get"})}function o(e){return Object(l["default"])({url:"/api/img/"+e.id+" / set_tags/",method:"get"})}function r(e){return Object(l["default"])({url:"/api/img/upload_finished/",method:"get"})}function c(e){return Object(l["default"])({url:"/api/profile/",method:"get",params:e})}function d(e){return Object(l["default"])({url:"/api/profile/"+e.id+"/",method:"get",params:e})}function u(e){return Object(l["default"])({url:"/api/profile/"+e.id+"/",method:"put",data:e})}function f(e){return Object(l["default"])({url:"/api/profile/clear_face_album/",method:"get"})}function h(e){return Object(l["default"])({url:"/api/face/"+e.id+"/",method:"get"})}function g(e){return Object(l["default"])({url:"/api/face/"+e.id+"/",method:"put",data:e})}function m(e){return console.log(e),Object(l["default"])({url:"/api/face/",method:"get",params:e})}function p(e){return Object(l["default"])({url:"/gallery/doEdit",method:"post",data:e})}function _(e){return Object(l["default"])({url:"/gallery/doDelete",method:"post",data:e})}function y(e){return Object(l["default"])({url:"/api/img/",method:"post",data:e})}function b(e){return console.log(e),Object(l["default"])({url:"/api/category/get_filter_list/",method:"get",params:e})}function v(e){return console.log(e),Object(l["default"])({url:"/api/address/",method:"get",params:e})}},c7f7:function(e,t,a){"use strict";a("56bb")},d890:function(e,t,a){"use strict";a("5efe")},db9f:function(e,t,a){},e21c:function(e,t,a){"use strict";a.r(t),a.d(t,"getFace",(function(){return i})),a.d(t,"changeFaceName",(function(){return s})),a.d(t,"getFilterList",(function(){return n}));var l=a("b775");function i(e){return Object(l["default"])({url:"/api/face/",method:"get",params:e})}function s(e){return Object(l["default"])({url:"/api/face/"+e.id+"/",method:"put",data:e})}function n(e){return console.log(e),Object(l["default"])({url:"/api/face/get_filtered_list/",method:"get",params:e})}},f5d0:function(e,t,a){"use strict";a.r(t);var l=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[e.searchable?a("FaceSearch",{on:{handleFaceSearch:e.onFaceSearch}}):e._e(),a("AlbumContainer",{attrs:{items:e.faces.data,total:e.faces.totalCnt,title:e.faces.title,busy:e.faces.loading,finished:e.faces.finished},on:{albumClick:e.onClick,load:e.onLoad,changeName:e.onChangeName}})],1)},i=[],s=a("41cf"),n=a("e21c"),o=a("310f"),r={name:"FaceList",components:{AlbumContainer:s["default"],FaceSearch:o["default"]},directives:{},props:{query:{type:Object,default:null,required:!1},searchable:{type:Boolean,default:!0,required:!1},id:{type:Number,default:null,required:!1}},data:function(){return{faces:{title:"Face List",loading:!1,finished:!1,checkedId:-1,checkedIndex:-1,totalCnt:0,links:null,curCnt:0,data:[],queryForm:{page:1,size:25,confirmed:"1"}},patchParams:{id:0,name:""}}},watch:{id(e,t){console.log("FaceListGallery: watch: query.profile",e),this.faces.queryForm.profile=e,this.faces.queryForm.page=1,this.faces.data=[],this.fetchFace()}},created(){},mounted(){console.log("FaceList: mounted"),this.faces.queryForm.profile=this.id,this.fetchFace()},methods:{onClick(e,t){console.log("recieved the child component value %d,%o",e,t),this.faces.checkedIndex=e,this.faces.checkedId=t.id||0,this.$emit("choosed",t)},async fetchFace(){this.faces.loading=!0,this.faces.finished=!1,await Object(n["getFace"])(this.faces.queryForm).then(e=>{console.log("getFaceChangeAvatar",e);const{data:t,totalCnt:a,links:l}=e;this.faces.data=[...this.faces.data,...t],this.faces.curCnt=this.faces.data.length,this.faces.totalCnt=a,this.faces.links=l,null===this.faces.links.next&&(this.faces.finished=!0,console.log("FaceList: fetchFace: no more data------------")),this.$emit("faceData",this.faces.data)}),setTimeout(()=>{this.faces.loading=!1},500)},onLoad(){if(console.log("FaceList: onLoad:loading:",this.faces.loading),!0!==this.faces.loading){if(this.faces.finished)return console.log("FaceList: onLoad: faces.links.next is null, finished:",this.faces.finished),void setTimeout(()=>{this.faces.loading=!1},3e3);this.faces.queryForm.page++,this.fetchFace()}},onChangeName(e,t){console.log("FaceList: onChangeName",e,t),this.patchParams.id=t.id,this.patchParams.name=e,this.onProcessEdit()},async onProcessEdit(){console.log("faceList: onProcessEdit","新名称："+this.patchParams.name),await Object(n["changeFaceName"])(this.patchParams).then(e=>{console.log("faceList: changeFaceName",e),this.patchParams.name="",this.$message({message:"修改成功",type:"success"})})},onFaceSearch(e){console.log("recieve the queryForm info from the search component"),console.log(e),this.faces.queryForm=e,this.faces.totalCnt=0,this.faces.data=[],this.fetchFace()}}},c=r,d=a("2877"),u=Object(d["a"])(c,l,i,!1,null,null,null);t["default"]=u.exports}}]);