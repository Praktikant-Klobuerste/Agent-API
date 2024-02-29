"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[461],{1668:(e,r,n)=>{n.r(r),n.d(r,{assets:()=>p,contentTitle:()=>a,default:()=>m,frontMatter:()=>i,metadata:()=>o,toc:()=>c});var t=n(4848),s=n(8453);const i={sidebar_position:2},a="schemas.py",o={id:"schemas_py",title:"schemas.py",description:"",source:"@site/docs/01_schemas_py.md",sourceDirName:".",slug:"/schemas_py",permalink:"/Agent-API/docs/schemas_py",draft:!1,unlisted:!1,editUrl:"https://github.com/Praktikant-Klobuerste/Agent-API/tree/main/docusaurus/docs/01_schemas_py.md",tags:[],version:"current",sidebarPosition:2,frontMatter:{sidebar_position:2},sidebar:"tutorialSidebar",previous:{title:"team.py",permalink:"/Agent-API/docs/resources/team_py"}},p={},c=[];function u(e){const r={code:"code",h1:"h1",pre:"pre",...(0,s.R)(),...e.components};return(0,t.jsxs)(t.Fragment,{children:[(0,t.jsx)(r.h1,{id:"schemaspy",children:"schemas.py"}),"\n",(0,t.jsx)(r.pre,{children:(0,t.jsx)(r.code,{className:"language-python",children:'from flask import Flask\r\nfrom flask_smorest import Api\r\n\r\nfrom resources.agent import blp as AgentBlueprint\r\nfrom resources.lair import blp as LairBlueprint\r\nfrom resources.team import blp as TeamBlueprint\r\n\r\napp = Flask(__name__)\r\n\r\napp.config["PROPAGATE_EXCEPTIONS"] = True\r\napp.config["API_TITLE"] = "Agent API"\r\napp.config["API_VERSION"] = "v1"\r\napp.config["OPENAPI_VERSION"] = "3.0.3"\r\napp.config["OPENAPI_URL_PREFIX"] = "/"\r\napp.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"\r\napp.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"\r\n\r\napi = Api(app)\r\n\r\napi.register_blueprint(AgentBlueprint)\r\napi.register_blueprint(LairBlueprint)\r\napi.register_blueprint(TeamBlueprint)\r\n\r\nif __name__ == "__main__":\r\n    app.run(debug=True)\n'})})]})}function m(e={}){const{wrapper:r}={...(0,s.R)(),...e.components};return r?(0,t.jsx)(r,{...e,children:(0,t.jsx)(u,{...e})}):u(e)}},8453:(e,r,n)=>{n.d(r,{R:()=>a,x:()=>o});var t=n(6540);const s={},i=t.createContext(s);function a(e){const r=t.useContext(i);return t.useMemo((function(){return"function"==typeof e?e(r):{...r,...e}}),[r,e])}function o(e){let r;return r=e.disableParentContext?"function"==typeof e.components?e.components(s):e.components||s:a(e.components),t.createElement(i.Provider,{value:r},e.children)}}}]);