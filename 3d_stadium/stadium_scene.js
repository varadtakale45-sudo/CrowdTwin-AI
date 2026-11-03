import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
const host=document.getElementById('stadium-canvas'),scene=new THREE.Scene();scene.background=new THREE.Color(0xeeeeee);
const camera=new THREE.PerspectiveCamera(48,1,.1,500);camera.position.set(40,42,42);
const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));host.appendChild(renderer.domElement);
const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.maxPolarAngle=Math.PI*.48;controls.minDistance=20;controls.maxDistance=110;
scene.add(new THREE.HemisphereLight(0xffffff,0x666666,2));const light=new THREE.DirectionalLight(0xffffff,2);light.position.set(20,40,20);scene.add(light);
function mesh(geometry,color,x=0,y=0,z=0){const m=new THREE.Mesh(geometry,new THREE.MeshStandardMaterial({color,side:THREE.DoubleSide,roughness:.85}));m.position.set(x,y,z);scene.add(m);return m}
const ground=mesh(new THREE.CircleGeometry(16,96),0xbbbbbb,0,.01,0);ground.rotation.x=-Math.PI/2;ground.scale.y=.72;
function ovalLine(radius,height,color){const p=[];for(let i=0;i<=128;i++){const a=i/128*Math.PI*2;p.push(new THREE.Vector3(Math.cos(a)*radius,height,Math.sin(a)*radius*.72))}scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(p),new THREE.LineBasicMaterial({color})))}
ovalLine(15.5,.09,0xffffff);ovalLine(16,.08,0x111111);
mesh(new THREE.BoxGeometry(2,.06,7),0xffffff,0,.07,0);for(const z of [-2.8,2.8]){mesh(new THREE.BoxGeometry(3,.03,.08),0x111111,0,.12,z);for(const x of [-.12,0,.12])mesh(new THREE.CylinderGeometry(.025,.025,.45,5),0x111111,x,.3,z)}
// Stepped seating sectors and segmented roof canopies preserve open access aisles.
for(let sector=0;sector<8;sector++){const angle=sector*Math.PI/4+.05;for(let row=0;row<12;row++){const band=mesh(new THREE.RingGeometry(17+row*.48,17.44+row*.48,24,1,angle,Math.PI/4-.1),row%2?0xeeeeee:0x555555,0,.5+row*.42,0);band.rotation.x=-Math.PI/2;band.scale.y=.72}const roof=mesh(new THREE.RingGeometry(20,24.5,24,1,angle,Math.PI/4-.1),0xffffff,0,7,0);roof.rotation.x=-Math.PI/2;roof.scale.y=.72;for(const a of [angle,angle+.62])mesh(new THREE.CylinderGeometry(.12,.12,7,6),0x333333,Math.cos(a)*23,3.5,Math.sin(a)*23*.72)}
const walk=mesh(new THREE.RingGeometry(24.5,27,96),0xdddddd,0,.03,0);walk.rotation.x=-Math.PI/2;walk.scale.y=.72;
const api=async(url,options={})=>{const r=await fetch(url,{headers:{'Content-Type':'application/json'},...options});const d=await r.json();if(!r.ok)throw Error(typeof d.detail==='string'?d.detail:JSON.stringify(d.detail));return d};
export const T=window.CrowdTwin={THREE,scene,camera,renderer,controls,api,nodeMeshes:new Map(),data:null,route:null,heatMode:'current',crowdVisible:true,animations:[],labels:[]};
T.position=n=>new THREE.Vector3(n.x*(n.kind==='zone'?1.12:1.45),n.kind==='zone'?3.2:.5,n.z*(n.kind==='zone'?1.12:1.45));
T.name=n=>n.kind.toUpperCase()+' '+n.id.replace(/^\D+/,'').padStart(2,'0');
T.label=(text,position,critical=false)=>{const el=document.createElement('button');el.className='node-label'+(critical?' blocked':'');el.textContent=text;host.appendChild(el);const label={el,position};T.labels.push(label);return label};
T.inspect=n=>{document.getElementById('tooltip').innerHTML='<strong>'+T.name(n)+'</strong><br>Capacity '+n.capacity.toLocaleString()+'<br>Current crowd '+n.crowd.toLocaleString()+'<br>Predicted crowd '+Math.round(n.predicted_density*n.capacity).toLocaleString()+'<br>Queue '+n.queue+'<br>'+(n.blocked?'BLOCKED':n.predicted_density>=.85?'CRITICAL':n.density>=.7?'HIGH LOAD':'OPEN')};
const raycaster=new THREE.Raycaster(),pointer=new THREE.Vector2();renderer.domElement.addEventListener('click',e=>{const r=renderer.domElement.getBoundingClientRect();pointer.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);raycaster.setFromCamera(pointer,camera);const hit=raycaster.intersectObjects([...T.nodeMeshes.values()])[0];if(hit)T.inspect(hit.object.userData.node)});
document.getElementById('camera').onclick=()=>{camera.position.set(40,42,42);controls.target.set(0,0,0);controls.update()};
function resize(){camera.aspect=host.clientWidth/host.clientHeight;camera.updateProjectionMatrix();renderer.setSize(host.clientWidth,host.clientHeight)}new ResizeObserver(resize).observe(host);resize();
T.refresh=async()=>{T.data=await api('/api/stadium');window.dispatchEvent(new CustomEvent('twin-data',{detail:T.data}));return T.data};
function animate(t){requestAnimationFrame(animate);controls.update();const placed=[];for(const l of [...T.labels].sort((a,b)=>Number(!!b.route)-Number(!!a.route))){const p=l.position.clone().project(camera);l.el.style.display=p.z>1?'none':'';let x=Math.max(75,Math.min(host.clientWidth-75,(p.x*.5+.5)*host.clientWidth)),y=(-p.y*.5+.5)*host.clientHeight;const w=l.el.offsetWidth||140;for(let attempt=0;attempt<20&&placed.some(q=>Math.abs(q.x-x)<(q.w+w)/2+6&&Math.abs(q.y-y)<32);attempt++)y+=34;placed.push({x,y,w});l.el.style.left=x+'px';l.el.style.top=y+'px'}T.animations.forEach(fn=>fn(t));renderer.render(scene,camera)}requestAnimationFrame(animate);
