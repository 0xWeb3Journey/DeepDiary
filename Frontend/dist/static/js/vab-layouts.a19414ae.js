/*!
 *  build: vue-admin-better 
 *  vue-admin-beautiful.com 
 *  https://gitee.com/chu1204505056/vue-admin-better 
 *  time: 2023-11-1 08:58:33
 */
(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["vab-layouts"],{1396:function(e,t,a){},"1e68":function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"nav-bar-container"},[a("el-row",{attrs:{gutter:15}},[a("el-col",{attrs:{xs:4,sm:12,md:12,lg:12,xl:12}},[a("div",{staticClass:"left-panel"},[a("i",{staticClass:"fold-unfold",class:e.collapse?"el-icon-s-unfold":"el-icon-s-fold",attrs:{title:e.collapse?"展开":"收起"},on:{click:e.handleCollapse}}),a("vab-breadcrumb",{staticClass:"hidden-xs-only"})],1)]),a("el-col",{attrs:{xs:20,sm:12,md:12,lg:12,xl:12}},[a("div",{staticClass:"right-panel"},[a("vab-error-log"),a("vab-full-screen-bar",{on:{refresh:e.refreshRoute}}),a("vab-theme-bar",{staticClass:"hidden-xs-only"}),a("vab-icon",{attrs:{title:"重载所有路由",pulse:e.pulse,icon:["fas","redo"]},on:{click:e.refreshRoute}}),a("vab-avatar")],1)])],1)],1)},i=[],n=a("2f62"),o={name:"VabNavBar",data(){return{pulse:!1}},computed:{...Object(n["c"])({collapse:"settings/collapse",visitedRoutes:"tabsBar/visitedRoutes",device:"settings/device",routes:"routes/routes"})},methods:{...Object(n["b"])({changeCollapse:"settings/changeCollapse"}),handleCollapse(){this.changeCollapse()},async refreshRoute(){this.$baseEventBus.$emit("reload-router-view"),this.pulse=!0,setTimeout(()=>{this.pulse=!1},1e3)}}},r=o,l=(a("9300"),a("2877")),c=Object(l["a"])(r,s,i,!1,null,"63690af4",null);t["default"]=c.exports},"21e1":function(e,t,a){},"397a":function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return e.routerView?a("div",{staticClass:"app-main-container"},[a("transition",{attrs:{mode:"out-in",name:"fade-transform"}},[a("keep-alive",{attrs:{include:e.cachedRoutes,max:e.keepAliveMaxNum}},[a("router-view",{key:e.key,staticClass:"app-main-height"})],1)],1),a("footer",{directives:[{name:"show",rawName:"v-show",value:e.footerCopyright,expression:"footerCopyright"}],staticClass:"footer-copyright"},[e._v(" Copyright "),a("vab-icon",{attrs:{icon:["fas","copyright"]}}),e._v(" deep-diary "+e._s(e.fullYear)+" "),a("vab-icon",{attrs:{icon:["fas","envelope-open-text"]}}),e._v(" 浙ICP备2022003145号 ")],1)],1):e._e()},i=[],n=a("2f62"),o=a("f121"),r={name:"VabAppMain",data(){return{show:!1,fullYear:(new Date).getFullYear(),copyright:o["copyright"],title:o["title"],keepAliveMaxNum:o["keepAliveMaxNum"],routerView:!0,footerCopyright:o["footerCopyright"]}},computed:{...Object(n["c"])({visitedRoutes:"tabsBar/visitedRoutes",device:"settings/device"}),cachedRoutes(){const e=[];return this.visitedRoutes.forEach(t=>{t.meta.noKeepAlive||e.push(t.name)}),e},key(){return this.$route.path}},watch:{$route:{handler(e){"mobile"===this.device&&this.foldSideBar()},immediate:!0}},created(){this.$baseEventBus.$on("reload-router-view",()=>{this.routerView=!1,this.$nextTick(()=>{this.routerView=!0})})},mounted(){},methods:{...Object(n["b"])({foldSideBar:"settings/foldSideBar"})}},l=r,c=(a("ebe6"),a("2877")),u=Object(c["a"])(l,s,i,!1,null,"1a5bbd56",null);t["default"]=u.exports},"3ab0":function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"vue-admin-beautiful-wrapper",class:e.classObj},["horizontal"===e.layout?a("div",{staticClass:"layout-container-horizontal",class:{fixed:"fixed"===e.header,"no-tabs-bar":"false"===e.tabsBar||!1===e.tabsBar}},[a("div",{class:"fixed"===e.header?"fixed-header":""},[a("vab-top-bar"),"true"===e.tabsBar||!0===e.tabsBar?a("div",{class:{"tag-view-show":e.tabsBar}},[a("div",{staticClass:"vab-main"},[a("vab-tabs-bar")],1)]):e._e()],1),a("div",{staticClass:"vab-main main-padding"},[a("vab-ad"),a("vab-app-main")],1)]):a("div",{staticClass:"layout-container-vertical",class:{fixed:"fixed"===e.header,"no-tabs-bar":"false"===e.tabsBar||!1===e.tabsBar}},["mobile"===e.device&&!1===e.collapse?a("div",{staticClass:"mask",on:{click:e.handleFoldSideBar}}):e._e(),a("vab-side-bar"),a("div",{staticClass:"vab-main",class:e.collapse?"is-collapse-main":""},[a("div",{class:"fixed"===e.header?"fixed-header":""},[a("vab-nav-bar"),"true"===e.tabsBar||!0===e.tabsBar?a("vab-tabs-bar"):e._e()],1),a("vab-ad"),a("vab-app-main")],1)],1),a("el-backtop")],1)},i=[],n=(a("caad"),a("2f62")),o=a("f121"),r={name:"Layout",data(){return{oldLayout:""}},computed:{...Object(n["c"])({layout:"settings/layout",tabsBar:"settings/tabsBar",collapse:"settings/collapse",header:"settings/header",device:"settings/device"}),classObj(){return{mobile:"mobile"===this.device}}},beforeMount(){window.addEventListener("resize",this.handleResize)},beforeDestroy(){window.removeEventListener("resize",this.handleResize)},mounted(){this.oldLayout=this.layout;const e=navigator.userAgent;e.includes("Juejin")&&this.$baseAlert("vue-admin-beautiful不支持在掘金内置浏览器演示，请手动复制以下地址到浏览器中查看http://mpfhrd48.sanxing.uz7.cn/vue-admin-beautiful");const t=this.handleIsMobile();t?(t?this.$store.dispatch("settings/changeLayout","vertical"):this.$store.dispatch("settings/changeLayout",this.oldLayout),this.$store.dispatch("settings/toggleDevice","mobile"),setTimeout(()=>{this.$store.dispatch("settings/foldSideBar")},2e3)):this.$store.dispatch("settings/openSideBar"),this.$nextTick(()=>{window.addEventListener("storage",e=>{e.key!==o["tokenName"]&&null!==e.key||window.location.reload(),e.key===o["tokenName"]&&null===e.value&&window.location.reload()},!1)})},methods:{...Object(n["b"])({handleFoldSideBar:"settings/foldSideBar"}),handleIsMobile(){return document.body.getBoundingClientRect().width-1<992},handleResize(){if(!document.hidden){const e=this.handleIsMobile();e?this.$store.dispatch("settings/changeLayout","vertical"):this.$store.dispatch("settings/changeLayout",this.oldLayout),this.$store.dispatch("settings/toggleDevice",e?"mobile":"desktop")}}}},l=r,c=(a("d849"),a("2877")),u=Object(c["a"])(l,s,i,!1,null,"a1e859d6",null);t["default"]=u.exports},"4d1b":function(e,t,a){e.exports={"menu-color":"rgba(255,255,255,.95)","menu-color-active":"rgba(255,255,255,.95)","menu-background":"#21252b"}},"5f5f":function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("router-view")},i=[],n=a("2877"),o={},r=Object(n["a"])(o,s,i,!1,null,null,null);t["default"]=r.exports},6997:function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("el-breadcrumb",{staticClass:"breadcrumb-container",attrs:{separator:">"}},e._l(e.list,(function(t){return a("el-breadcrumb-item",{key:t.path},[e._v(" "+e._s(t.meta.title)+" ")])})),1)},i=[],n={name:"VabBreadcrumb",data(){return{list:this.getBreadcrumb()}},watch:{$route(){this.list=this.getBreadcrumb()}},methods:{getBreadcrumb(){return this.$route.matched.filter(e=>e.name&&e.meta.title)}}},o=n,r=(a("8a85"),a("2877")),l=Object(r["a"])(o,s,i,!1,null,"2b4cacba",null);t["default"]=l.exports},"6c36":function(e,t,a){},"756a":function(e,t,a){},8034:function(e,t,a){},"803c":function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return e.themeBar?a("span",[a("vab-icon",{attrs:{title:"Theme",icon:["fas","palette"]},on:{click:e.handleOpenThemeBar}}),a("div",{staticClass:"theme-bar-setting"},[a("div",{on:{click:e.handleOpenThemeBar}},[a("vab-icon",{attrs:{icon:["fas","palette"]}}),a("p",[e._v("Theme")])],1)]),a("el-drawer",{attrs:{title:"Theme",visible:e.drawerVisible,direction:"rtl","append-to-body":"",size:"300px"},on:{"update:visible":function(t){e.drawerVisible=t}}},[a("el-scrollbar",{staticStyle:{height:"80vh",overflow:"hidden"}},[a("div",{staticClass:"el-drawer__body"},[a("el-form",{ref:"form",attrs:{model:e.theme,"label-position":"top"}},[a("el-form-item",{attrs:{label:"主题"}},[a("el-radio-group",{model:{value:e.theme.name,callback:function(t){e.$set(e.theme,"name",t)},expression:"theme.name"}},[a("el-radio-button",{attrs:{label:"default"}},[e._v("默认")]),a("el-radio-button",{attrs:{label:"green"}},[e._v("绿荫草场")]),a("el-radio-button",{attrs:{label:"glory"}},[e._v("荣耀典藏")])],1)],1),a("el-form-item",{attrs:{label:"布局"}},[a("el-radio-group",{model:{value:e.theme.layout,callback:function(t){e.$set(e.theme,"layout",t)},expression:"theme.layout"}},[a("el-radio-button",{attrs:{label:"vertical"}},[e._v("纵向布局")]),a("el-radio-button",{attrs:{label:"horizontal"}},[e._v("横向布局")])],1)],1),a("el-form-item",{attrs:{label:"头部"}},[a("el-radio-group",{model:{value:e.theme.header,callback:function(t){e.$set(e.theme,"header",t)},expression:"theme.header"}},[a("el-radio-button",{attrs:{label:"fixed"}},[e._v("固定头部")]),a("el-radio-button",{attrs:{label:"noFixed"}},[e._v("不固定头部")])],1)],1),a("el-form-item",{attrs:{label:"多标签"}},[a("el-radio-group",{model:{value:e.theme.tabsBar,callback:function(t){e.$set(e.theme,"tabsBar",t)},expression:"theme.tabsBar"}},[a("el-radio-button",{attrs:{label:"true"}},[e._v("开启")]),a("el-radio-button",{attrs:{label:"false"}},[e._v("不开启")])],1)],1)],1)],1)]),a("div",{staticClass:"el-drawer__footer"},[a("el-button",{attrs:{type:"primary"},on:{click:e.handleSaveTheme}},[e._v("保存")]),a("el-button",{attrs:{type:""},on:{click:function(t){e.drawerVisible=!1}}},[e._v("取消")])],1)],1)],1):e._e()},i=[],n=a("2f62"),o=a("f121"),r={name:"VabThemeBar",data(){return{drawerVisible:!1,theme:{name:"default",layout:"",header:"fixed",tabsBar:""}}},computed:{...Object(n["c"])({layout:"settings/layout",header:"settings/header",tabsBar:"settings/tabsBar",themeBar:"settings/themeBar"})},created(){this.$baseEventBus.$on("theme",()=>{this.handleOpenThemeBar()});const e=localStorage.getItem("vue-admin-beautiful-theme");null!==e?(this.theme=JSON.parse(e),this.handleSetTheme()):(this.theme.layout=this.layout,this.theme.header=this.header,this.theme.tabsBar=this.tabsBar)},methods:{...Object(n["b"])({changeLayout:"settings/changeLayout",changeHeader:"settings/changeHeader",changeTabsBar:"settings/changeTabsBar"}),handleIsMobile(){return document.body.getBoundingClientRect().width-1<992},handleOpenThemeBar(){this.drawerVisible=!0},handleSetTheme(){let{name:e,layout:t,header:a,tabsBar:s}=this.theme;localStorage.setItem("vue-admin-beautiful-theme",`{\n          "name":"${e}",\n          "layout":"${t}",\n          "header":"${a}",\n          "tabsBar":"${s}"\n        }`),this.handleIsMobile()||this.changeLayout(t),this.changeHeader(a),this.changeTabsBar(s),document.getElementsByTagName("body")[0].className="vue-admin-beautiful-theme-"+e,this.drawerVisible=!1},handleSaveTheme(){this.handleSetTheme()},handleSetDfaultTheme(){let{name:e}=this.theme;document.getElementsByTagName("body")[0].classList.remove("vue-admin-beautiful-theme-"+e),localStorage.removeItem("vue-admin-beautiful-theme"),this.$refs["form"].resetFields(),Object.assign(this.$data,this.$options.data()),this.changeHeader(o["layout"]),this.theme.name="default",this.theme.layout=this.layout,this.theme.header=this.header,this.theme.tabsBar=this.tabsBar,this.drawerVisible=!1,location.reload()},handleGetCode(){const e="https://github.com/chuzhixin/vue-admin-beautiful/tree/master/src/views";let t=this.$route.path+"/index.vue";"/vab/menu1/menu1-1/menu1-1-1/index.vue"===t&&(t="/vab/nested/menu1/menu1-1/menu1-1-1/index.vue"),"/vab/icon/awesomeIcon/index.vue"===t&&(t="/vab/icon/index.vue"),"/vab/icon/remixIcon/index.vue"===t&&(t="/vab/icon/remixIcon.vue"),"/vab/icon/colorfulIcon/index.vue"===t&&(t="/vab/icon/colorfulIcon.vue"),"/vab/table/comprehensiveTable/index.vue"===t&&(t="/vab/table/index.vue"),"/vab/table/inlineEditTable/index.vue"===t&&(t="/vab/table/inlineEditTable.vue"),window.open(e+t)}}},l=r,c=(a("85bd"),a("ad67"),a("2877")),u=Object(c["a"])(l,s,i,!1,null,"20a3927d",null);t["default"]=u.exports},"84c8":function(e,t,a){"use strict";a.r(t);var s=a("a026");const i=a("f192");i.keys().forEach(e=>{const t=i(e),a=t.default.name;s["default"].component(a,t.default||t)});const n=a("e114");n.keys().forEach(e=>{const t=n(e),a=t.default.name;s["default"].component(a,t.default||t)});const o=a("1654");o.keys().forEach(e=>{a("e8cc")("./"+e.slice(2))})},"85bd":function(e,t,a){"use strict";a("8833")},8833:function(e,t,a){},"89bf":function(e,t,a){},"8a85":function(e,t,a){"use strict";a("89bf")},9300:function(e,t,a){"use strict";a("8034")},"9b65":function(e,t,a){"use strict";a("1396")},"9c80":function(e,t,a){},ab5f:function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{class:"logo-container-"+e.layout},[a("router-link",{attrs:{to:"/"}},[e.logo?a("vab-remix-icon",{staticClass:"logo",attrs:{"icon-class":e.logo}}):e._e(),a("span",{staticClass:"title",class:{"hidden-xs-only":"horizontal"===e.layout},attrs:{title:e.title}},[e._v(" "+e._s(e.title)+" ")])],1)],1)},i=[],n=a("2f62"),o={name:"VabLogo",data(){return{title:this.$baseTitle}},computed:{...Object(n["c"])({logo:"settings/logo",layout:"settings/layout"})}},r=o,l=(a("9b65"),a("2877")),c=Object(l["a"])(r,s,i,!1,null,"9789ca38",null);t["default"]=c.exports},abf6:function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"vab-ad"},[e.adList?a("el-carousel",{attrs:{height:"30px",direction:"vertical",autoplay:!0,interval:3e3,"indicator-position":"none"}},e._l(e.adList,(function(t,s){return a("el-carousel-item",{key:s},[a("el-tag",{attrs:{type:"warning"}},[e._v("Ad")]),a("a",{attrs:{target:"_blank",href:t.url}},[e._v(e._s(t.title))])],1)})),1):e._e()],1)},i=[],n=a("ff02"),o={name:"VabAd",data(){return{nodeEnv:"production",adList:[]}},created(){this.fetchData()},methods:{async fetchData(){const{data:e}=await Object(n["getList"])();console.log("### this is the ad info: %o",e),this.adList=e}}},r=o,l=(a("d2fd"),a("2877")),c=Object(l["a"])(r,s,i,!1,null,"29c56bf7",null);t["default"]=c.exports},ad67:function(e,t,a){"use strict";a("4d1b")},cbe4:function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("el-dropdown",{on:{command:e.handleCommand}},[a("span",{staticClass:"avatar-dropdown"},[a("img",{staticClass:"user-avatar",attrs:{src:e.avatar,alt:""}}),a("div",{staticClass:"user-name"},[e._v(" "+e._s(e.username)+" "),a("i",{staticClass:"el-icon-arrow-down el-icon--right"})])]),a("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[a("el-dropdown-item",{attrs:{command:"logout",divided:""}},[e._v("退出登录")])],1)],1)},i=[],n=a("2f62"),o=a("f121"),r={name:"VabAvatar",computed:{...Object(n["c"])({avatar:"user/avatar",username:"user/username"})},methods:{handleCommand(e){switch(e){case"logout":this.logout();break;case"personalCenter":this.personalCenter();break;case"github":window.open("https://github.com/chuzhixin/vue-admin-beautiful");break;case"gitee":window.open("https://gitee.com/chu1204505056/vue-admin-beautiful");break;case"pro":window.open("https://vue-admin-beautiful.com/admin-pro/?hmsr=homeAd&hmpl=&hmcu=&hmkw=&hmci=");break;case"plus":window.open("https://vue-admin-beautiful.com/admin-plus/?hmsr=homeAd&hmpl=&hmcu=&hmkw=&hmci=")}},personalCenter(){this.$router.push("/personalCenter/personalCenter")},logout(){this.$baseConfirm("您确定要退出"+this.$baseTitle+"吗?",null,async()=>{if(await this.$store.dispatch("user/logout"),o["recordRoute"]){const e=this.$route.fullPath;this.$router.push("/login?redirect="+e)}else this.$router.push("/login")})}}},l=r,c=(a("fa3c"),a("2877")),u=Object(c["a"])(l,s,i,!1,null,"88f1a36e",null);t["default"]=u.exports},d2fd:function(e,t,a){"use strict";a("21e1")},d849:function(e,t,a){"use strict";a("9c80")},ebe6:function(e,t,a){"use strict";a("6c36")},fa3c:function(e,t,a){"use strict";a("756a")}}]);