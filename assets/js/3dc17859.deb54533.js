"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[461],{1668:(e,r,n)=>{n.r(r),n.d(r,{assets:()=>i,contentTitle:()=>c,default:()=>m,frontMatter:()=>o,metadata:()=>a,toc:()=>u});var s=n(4848),t=n(8453);const o={sidebar_position:2},c="schemas.py",a={id:"schemas_py",title:"schemas.py",description:"",source:"@site/docs/01_schemas_py.md",sourceDirName:".",slug:"/schemas_py",permalink:"/Agent-API/docs/schemas_py",draft:!1,unlisted:!1,editUrl:"https://github.com/Praktikant-Klobuerste/Agent-API/tree/main/docusaurus/docs/01_schemas_py.md",tags:[],version:"current",sidebarPosition:2,frontMatter:{sidebar_position:2},sidebar:"tutorialSidebar",previous:{title:"team.py",permalink:"/Agent-API/docs/resources/team_py"}},i={},u=[];function d(e){const r={code:"code",h1:"h1",pre:"pre",...(0,t.R)(),...e.components};return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(r.h1,{id:"schemaspy",children:"schemas.py"}),"\n",(0,s.jsx)(r.pre,{children:(0,s.jsx)(r.code,{className:"language-python",children:"from marshmallow import Schema, fields\r\n\r\n\r\nclass AgentSchema(Schema):\r\n    code = fields.Int(dump_only=True)\r\n    name = fields.Str(required=True)\r\n    eye_color = fields.Str(required=True)\r\n\r\n\r\nclass LairSchema(Schema):\r\n    id = fields.Int(dump_only=True)\r\n    secret = fields.Bool(dump_only=True)\r\n    name = fields.Str(required=True)\r\n    cap = fields.Int(required=True)\n"})})]})}function m(e={}){const{wrapper:r}={...(0,t.R)(),...e.components};return r?(0,s.jsx)(r,{...e,children:(0,s.jsx)(d,{...e})}):d(e)}},8453:(e,r,n)=>{n.d(r,{R:()=>c,x:()=>a});var s=n(6540);const t={},o=s.createContext(t);function c(e){const r=s.useContext(o);return s.useMemo((function(){return"function"==typeof e?e(r):{...r,...e}}),[r,e])}function a(e){let r;return r=e.disableParentContext?"function"==typeof e.components?e.components(t):e.components||t:c(e.components),s.createElement(o.Provider,{value:r},e.children)}}}]);