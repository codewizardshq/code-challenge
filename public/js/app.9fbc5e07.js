(function(e){function t(t){for(var n,o,i=t[0],u=t[1],s=t[2],l=0,p=[];l<i.length;l++)o=i[l],Object.prototype.hasOwnProperty.call(a,o)&&a[o]&&p.push(a[o][0]),a[o]=0;for(n in u)Object.prototype.hasOwnProperty.call(u,n)&&(e[n]=u[n]);f&&f(t);while(p.length)p.shift()();return c.push.apply(c,s||[]),r()}function r(){for(var e,t=0;t<c.length;t++){for(var r=c[t],n=!0,o=1;o<r.length;o++){var i=r[o];0!==a[i]&&(n=!1)}n&&(c.splice(t--,1),e=u(u.s=r[0]))}return e}var n={},o={app:0},a={app:0},c=[];function i(e){return u.p+"js/"+({}[e]||e)+"."+{"chunk-2d21a3d2":"0f26d0fb","chunk-2d22d746":"f49a57de","chunk-3ce6ca78":"4dd45276","chunk-00b4e06c":"4d95fadc","chunk-21b12f7c":"82ae4479","chunk-8edd607a":"92299f07"}[e]+".js"}function u(t){if(n[t])return n[t].exports;var r=n[t]={i:t,l:!1,exports:{}};return e[t].call(r.exports,r,r.exports,u),r.l=!0,r.exports}u.e=function(e){var t=[],r={"chunk-3ce6ca78":1,"chunk-8edd607a":1};o[e]?t.push(o[e]):0!==o[e]&&r[e]&&t.push(o[e]=new Promise((function(t,r){for(var n="css/"+({}[e]||e)+"."+{"chunk-2d21a3d2":"31d6cfe0","chunk-2d22d746":"31d6cfe0","chunk-3ce6ca78":"914d76ea","chunk-00b4e06c":"31d6cfe0","chunk-21b12f7c":"31d6cfe0","chunk-8edd607a":"52330ed3"}[e]+".css",a=u.p+n,c=document.getElementsByTagName("link"),i=0;i<c.length;i++){var s=c[i],l=s.getAttribute("data-href")||s.getAttribute("href");if("stylesheet"===s.rel&&(l===n||l===a))return t()}var p=document.getElementsByTagName("style");for(i=0;i<p.length;i++){s=p[i],l=s.getAttribute("data-href");if(l===n||l===a)return t()}var f=document.createElement("link");f.rel="stylesheet",f.type="text/css",f.onload=t,f.onerror=function(t){var n=t&&t.target&&t.target.src||a,c=new Error("Loading CSS chunk "+e+" failed.\n("+n+")");c.code="CSS_CHUNK_LOAD_FAILED",c.request=n,delete o[e],f.parentNode.removeChild(f),r(c)},f.href=a;var b=document.getElementsByTagName("head")[0];b.appendChild(f)})).then((function(){o[e]=0})));var n=a[e];if(0!==n)if(n)t.push(n[2]);else{var c=new Promise((function(t,r){n=a[e]=[t,r]}));t.push(n[2]=c);var s,l=document.createElement("script");l.charset="utf-8",l.timeout=120,u.nc&&l.setAttribute("nonce",u.nc),l.src=i(e);var p=new Error;s=function(t){l.onerror=l.onload=null,clearTimeout(f);var r=a[e];if(0!==r){if(r){var n=t&&("load"===t.type?"missing":t.type),o=t&&t.target&&t.target.src;p.message="Loading chunk "+e+" failed.\n("+n+": "+o+")",p.name="ChunkLoadError",p.type=n,p.request=o,r[1](p)}a[e]=void 0}};var f=setTimeout((function(){s({type:"timeout",target:l})}),12e4);l.onerror=l.onload=s,document.head.appendChild(l)}return Promise.all(t)},u.m=e,u.c=n,u.d=function(e,t,r){u.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:r})},u.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},u.t=function(e,t){if(1&t&&(e=u(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(u.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var n in e)u.d(r,n,function(t){return e[t]}.bind(null,n));return r},u.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return u.d(t,"a",t),t},u.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},u.p="/",u.oe=function(e){throw console.error(e),e};var s=window["webpackJsonp"]=window["webpackJsonp"]||[],l=s.push.bind(s);s.push=t,s=s.slice();for(var p=0;p<s.length;p++)t(s[p]);var f=l;c.push([0,"chunk-vendors"]),r()})({0:function(e,t,r){e.exports=r("56d7")},"3c61":function(e,t,r){},4360:function(e,t,r){"use strict";var n=r("2b0e"),o=r("2f62"),a=(r("a4d3"),r("4de4"),r("4160"),r("e439"),r("dbb4"),r("b64b"),r("159b"),r("2fa7"));function c(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?c(r,!0).forEach((function(t){Object(a["a"])(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):c(r).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}var u="User";function s(){return{username:"",name:"",isAuthroized:!1}}var l=i({},s()),p={namespaced:!0,name:u,state:l,mapState:function(){return Object(o["b"])([u])}};function f(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function b(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?f(r,!0).forEach((function(t){Object(a["a"])(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):f(r).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}var d="Progress";function h(){return{rank:21}}var m=b({},h()),v={namespaced:!0,name:d,state:m,mapState:function(){return Object(o["b"])([d])}};r.d(t,"b",(function(){return p})),r.d(t,"a",(function(){return v})),n["a"].use(o["a"]);t["c"]=new o["a"].Store({state:{},mutations:{},actions:{},modules:{User:p,Progress:v}})},"56d7":function(e,t,r){"use strict";r.r(t);r("e260"),r("e6cf"),r("cca6"),r("a79d");var n=r("2b0e"),o=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-app",[r("app-bar"),r("quiz-bar"),r("v-content",[r("router-view")],1)],1)},a=[],c=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-app-bar",{attrs:{color:"dark",flat:"",dark:"","max-height":"80"}},[n("div",{staticClass:"d-flex align-center"},[n("v-img",{attrs:{alt:"CodewizardsHQ Logo",contain:"",src:r("96eb"),transition:"scale-transition"}})],1),n("v-spacer"),n("v-btn",e._b({attrs:{to:{name:"home"}}},"v-btn",e.buttonProps,!1),[e._v(" Home ")]),n("v-btn",e._b({attrs:{to:{name:"quiz"}}},"v-btn",e.buttonProps,!1),[e._v(" Quiz ")]),n("v-btn",e._b({attrs:{to:{name:"about"}}},"v-btn",e.buttonProps,!1),[e._v(" About ")]),n("v-btn",e._b({on:{click:e.getHelp}},"v-btn",e.buttonProps,!1),[e._v(" Get Help ")]),e.User.isAuthenticated?e._e():n("v-btn",e._b({attrs:{to:{name:"login"}}},"v-btn",e.buttonProps,!1),[e._v(" Sign In ")]),e.User.isAuthenticated?e._e():n("v-btn",e._b({attrs:{to:{name:"register"}}},"v-btn",e.buttonProps,!1),[e._v(" Create Account ")]),e.User.isAuthenticated?n("v-btn",e._b({attrs:{to:{name:"about"}}},"v-btn",e.buttonProps,!1),[e._v(" Sign Out ")]):e._e()],1)},i=[],u=(r("a4d3"),r("4de4"),r("4160"),r("e439"),r("dbb4"),r("b64b"),r("159b"),r("2fa7")),s=r("4360");function l(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function p(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?l(r,!0).forEach((function(t){Object(u["a"])(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):l(r).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}var f={name:"appBar",computed:p({},s["b"].mapState()),data:function(){return{buttonProps:{text:!0}}},methods:{getHelp:function(){}}},b=f,d=r("2877"),h=r("6544"),m=r.n(h),v=r("40dc"),g=r("8336"),y=r("adda"),O=r("2fa4"),C=Object(d["a"])(b,c,i,!1,null,null,null),w=C.exports;m()(C,{VAppBar:v["a"],VBtn:g["a"],VImg:y["a"],VSpacer:O["a"]});var j=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-toolbar",{staticClass:"secondary--text",attrs:{color:"dark2",flat:"","max-height":"60"}},[r("quiz-bar-rank",{attrs:{rank:e.Progress.rank}}),e.User.isAuthorized?r("span",[e._v(" Welcome pilgrim "+e._s(e.User.username)+" ")]):r("v-btn",{attrs:{color:"secondary",text:"",to:{name:"register"}}},[e._v(" Start your journey ")]),r("v-spacer"),r("v-btn",{attrs:{text:"",color:"secondary"}},[e._v(" Get your friends in on it "),r("v-icon",[e._v(" mdi-open-in-new ")])],1)],1)},P=[],k=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"quiz-bar-rank"},[r("div",{staticClass:"title"},[e._v("Level")]),r("svg",{staticStyle:{"fill-rule":"evenodd","clip-rule":"evenodd","stroke-linejoin":"round","stroke-miterlimit":"2"},attrs:{width:"100%",height:"100%",viewBox:"0 0 71 96",version:"1.1",xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink","xml:space":"preserve","xmlns:serif":"http://www.serif.com/"}},[r("g",{attrs:{id:"Layer_1-2"}},[r("path",{staticStyle:{fill:"rgb(0,134,100)","fill-rule":"nonzero"},attrs:{d:"M70,10.46C69.947,10.131 69.733,9.849 69.43,9.71C58.143,6.47 46.857,3.253 35.57,0.06C35.384,0.011 35.192,-0.01 35,0L35,8.76C35.223,8.734 35.447,8.734 35.67,8.76C38.54,9.35 41.33,10.32 44.16,11.12C46.57,11.8 48.98,12.45 51.39,13.12C53.8,13.79 56.07,14.48 58.39,15.12L64.71,17C66.32,17.45 67.93,17.89 69.54,18.31C69.66,18.31 69.98,18.12 69.98,18.01L69.98,10.48"}}),r("path",{staticStyle:{fill:"rgb(15,173,128)","fill-rule":"nonzero"},attrs:{d:"M34.55,0.06C32.55,0.6 30.55,1.18 28.6,1.74C19.227,4.38 9.853,7.023 0.48,9.67C0.24,9.788 0.071,10.016 0.03,10.28L0.03,17.82C0.03,18.4 0.28,18.47 0.76,18.3C1.24,18.13 2,17.9 2.63,17.72L9.75,15.72L15.75,14C17.81,13.42 19.87,12.86 21.93,12.28C23.99,11.7 25.75,11.15 27.67,10.61C29.13,10.19 30.59,9.77 32.07,9.42C33.023,9.104 34.004,8.879 35,8.75L35,0C34.845,0.002 34.69,0.022 34.54,0.06"}}),r("path",{staticStyle:{fill:"rgb(0,134,100)","fill-rule":"nonzero"},attrs:{d:"M37.18,95L37.18,94.2C37.18,94.2 37.27,94.5 37.37,94.56C37.49,94.619 37.63,94.619 37.75,94.56L46.65,88.4C49.84,86.19 53.05,83.99 56.22,81.75C57.95,80.53 59.7,79.32 61.32,77.97C62.477,77.021 63.508,75.929 64.39,74.72C65.851,72.707 67.187,70.607 68.39,68.43C69.436,66.442 69.976,64.226 69.96,61.98C70,48.84 70,35.73 70,22.63C70,20.98 70,21 68.4,20.57C65.4,19.76 61.7,18.7 61.7,18.7C61.7,18.7 61.59,33.77 61.59,36.7L61.59,61.06C61.505,62.902 60.958,64.694 60,66.27C58.796,68.614 57.088,70.663 55,72.27C52.66,74.04 50.23,75.68 47.84,77.37C47.21,77.82 37.09,84.15 37.09,84.15L37.09,95"}}),r("path",{staticStyle:{fill:"rgb(15,173,128)","fill-rule":"nonzero"},attrs:{d:"M32.83,95L32.83,94.2C32.83,94.2 32.74,94.5 32.64,94.56C32.523,94.616 32.387,94.616 32.27,94.56L23.37,88.4C20.16,86.16 17,84 13.78,81.72C12,80.5 10.3,79.29 8.68,77.94C7.523,76.991 6.492,75.899 5.61,74.69C4.149,72.677 2.813,70.577 1.61,68.4C0.576,66.406 0.05,64.186 0.08,61.94C0,48.84 0,35.73 0,22.63C0,21 0,21 1.6,20.57C4.6,19.76 8.3,18.7 8.3,18.7C8.3,18.7 8.41,33.77 8.41,36.7L8.41,61.06C8.495,62.902 9.042,64.694 10,66.27C11.204,68.614 12.912,70.663 15,72.27C17.34,74.04 19.77,75.68 22.16,77.37C22.79,77.82 32.91,84.15 32.91,84.15L32.91,95"}}),r("g",{attrs:{transform:"matrix(1,0,0,1,-16.323,12.1487)"}},[r("text",{staticStyle:{"font-family":"'Barrow2Bold', 'Barrow2'","font-weight":"700","font-size":"42px",fill:"rgb(0,134,100)"},attrs:{x:"32.827px",y:"50.734px"}},[e._v(e._s(e.rank))])])])])])},_=[],S=(r("a9e3"),{props:{rank:{type:Number,default:0}}}),x=S,L=Object(d["a"])(x,k,_,!1,null,null,null),E=L.exports;function z(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function D(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?z(r,!0).forEach((function(t){Object(u["a"])(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):z(r).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}var A={name:"quizBar",components:{QuizBarRank:E},computed:D({},s["b"].mapState(),{},s["a"].mapState()),methods:{getHelp:function(){}}},B=A,V=r("132d"),q=r("71d9"),T=Object(d["a"])(B,j,P,!1,null,null,null),M=T.exports;m()(T,{VBtn:g["a"],VIcon:V["a"],VSpacer:O["a"],VToolbar:q["a"]});var U={name:"App",components:{AppBar:w,QuizBar:M}},H=U,N=r("7496"),$=r("a75b"),I=Object(d["a"])(H,o,a,!1,null,null,null),Q=I.exports;m()(I,{VApp:N["a"],VContent:$["a"]});r("d3b7");var G=r("8c4f");n["a"].use(G["a"]);var J=[{path:"/home",name:"home",component:function(){return r.e("chunk-2d21a3d2").then(r.bind(null,"bb51"))}},{path:"/about",name:"about",component:function(){return r.e("chunk-2d22d746").then(r.bind(null,"f820"))}},{path:"/login",name:"login",component:function(){return Promise.all([r.e("chunk-3ce6ca78"),r.e("chunk-00b4e06c")]).then(r.bind(null,"a55b"))}},{path:"/logout",name:"logout",component:function(){return Promise.all([r.e("chunk-3ce6ca78"),r.e("chunk-00b4e06c")]).then(r.bind(null,"a55b"))}},{path:"/create-account",name:"register",component:function(){return Promise.all([r.e("chunk-3ce6ca78"),r.e("chunk-8edd607a")]).then(r.bind(null,"73cf"))}},{path:"/quiz",name:"quiz",component:function(){return Promise.all([r.e("chunk-3ce6ca78"),r.e("chunk-21b12f7c")]).then(r.bind(null,"2e44"))}},{path:"*",name:"redirect",redirect:{name:"home"}}],F=new G["a"]({mode:"history",routes:J}),K=F,R=r("f309");n["a"].use(R["a"]);var W=new R["a"]({theme:{dark:!0,flat:!0,themes:{dark:{primary:"#fdc743",secondary:"#0fad80",dark:"#353535",dark2:"#333131"}}}});r("3c61");n["a"].config.productionTip=!1,new n["a"]({router:K,store:s["c"],vuetify:W,render:function(e){return e(Q)}}).$mount("#app")},"96eb":function(e,t,r){e.exports=r.p+"img/logo-small.a031fc3f.png"}});
//# sourceMappingURL=app.9fbc5e07.js.map