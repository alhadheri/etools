!function(e){"use strict";var o=e.querySelector("#app");o.baseUrl="/",(""===window.location.port||"8099"===window.location.port)&&(o.baseUrl="/partner/"),o.appData={baseUrl:o.baseUrl,baseSite:window.location.origin,logoutEndpoint:window.location.origin+"/accounts/logout/",userInfoEp:window.location.origin+"/users/api/profile/",userPropertiesEp:window.location.origin+"/partnership/partnerstaffmember/",interventionsEp:[window.location.origin,"partners","api","interventions"].join("/")+"/",getEndpoint:{userProperties:function(e){return[window.location.origin,"partners","api","profile",e].join("/")+"/"}},permissions:{partnerOnlyPermissions:["interventionsMenu","userInfoMenu"],defaultPermissions:["interventionsMenu","userInfoMenu"]}},o.displayInstalledToast=function(){Polymer.dom(e).querySelector("platinum-sw-cache").disabled||Polymer.dom(e).querySelector("#caching-complete").show()},o.addEventListener("dom-change",function(){console.log("Our app is ready to rock!")}),window.addEventListener("WebComponentsReady",function(){}),window.addEventListener("paper-header-transform",function(o){var n=Polymer.dom(e).querySelector("#mainToolbar .app-name"),r=Polymer.dom(e).querySelector("#mainToolbar .middle-container"),a=Polymer.dom(e).querySelector("#mainToolbar .bottom-container"),i=o.detail,t=i.height-i.condensedHeight,s=Math.min(1,i.y/t),l=.5,c=t-i.y,d=t/(1-l),p=Math.max(l,c/d+l),m=1-s;Polymer.Base.transform("translate3d(0,"+100*s+"%,0)",r),Polymer.Base.transform("scale("+m+") translateZ(0)",a),Polymer.Base.transform("scale("+p+") translateZ(0)",n)}),o.scrollPageToTop=function(){o.$.headerPanelMain.scrollToTop(!0)},o.closeDrawer=function(){o.$.paperDrawerPanel.closeDrawer()}}(document);