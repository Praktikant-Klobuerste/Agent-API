"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[960],{4318:(e,r,t)=>{t.r(r),t.d(r,{assets:()=>d,contentTitle:()=>s,default:()=>u,frontMatter:()=>c,metadata:()=>i,toc:()=>a});var n=t(4848),o=t(8453);const c={sidebar_position:1},s="Dockerfile",i={id:"docker/dockerfile",title:"Dockerfile",description:"",source:"@site/docs/01_docker/00_dockerfile.md",sourceDirName:"01_docker",slug:"/docker/dockerfile",permalink:"/Agent-API/docs/docker/dockerfile",draft:!1,unlisted:!1,editUrl:"https://github.com/Praktikant-Klobuerste/Agent-API/tree/main/docusaurus/docs/01_docker/00_dockerfile.md",tags:[],version:"current",sidebarPosition:1,frontMatter:{sidebar_position:1},sidebar:"tutorialSidebar",previous:{title:"Docker",permalink:"/Agent-API/docs/category/docker"},next:{title:"Docker Befehle",permalink:"/Agent-API/docs/docker/docker_befehle"}},d={},a=[];function l(e){const r={code:"code",h1:"h1",pre:"pre",...(0,o.R)(),...e.components};return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(r.h1,{id:"dockerfile",children:"Dockerfile"}),"\n",(0,n.jsx)(r.pre,{children:(0,n.jsx)(r.code,{className:"language-shell",metastring:'title="Dockerfile"',children:'FROM python:3.10\r\nEXPOSE 5000\r\nWORKDIR /app\r\nCOPY ./requirements.txt requirements.txt\r\nRUN pip install --no-cache-dir --upgrade -r requirements.txt\r\nCOPY . .\r\nCMD ["flask", "run", "--host", "0.0.0.0"]\r\n\n'})})]})}function u(e={}){const{wrapper:r}={...(0,o.R)(),...e.components};return r?(0,n.jsx)(r,{...e,children:(0,n.jsx)(l,{...e})}):l(e)}},8453:(e,r,t)=>{t.d(r,{R:()=>s,x:()=>i});var n=t(6540);const o={},c=n.createContext(o);function s(e){const r=n.useContext(c);return n.useMemo((function(){return"function"==typeof e?e(r):{...r,...e}}),[r,e])}function i(e){let r;return r=e.disableParentContext?"function"==typeof e.components?e.components(o):e.components||o:s(e.components),n.createElement(c.Provider,{value:r},e.children)}}}]);