import {T} from './stadium_scene.js?v=4';
const {THREE,scene}=T;let graphGroup;
function dispose(group){group.traverse(o=>{o.geometry?.dispose();if(o.material)o.material.dispose()});scene.remove(group)}
window.addEventListener('twin-data',e=>{
 if(graphGroup)dispose(graphGroup);graphGroup=new THREE.Group();scene.add(graphGroup);
 T.labels.filter(l=>l.node).forEach(l=>l.el.remove());T.labels=T.labels.filter(l=>!l.node);T.nodeMeshes.clear();
 for(const n of e.detail.nodes){const d=T.heatMode==='predicted'?n.predicted_density:n.density;
 const m=new THREE.Mesh(n.kind==='zone'?new THREE.CylinderGeometry(1.7,1.7,.35,16):new THREE.BoxGeometry(1.3,1.4,1.3),new THREE.MeshStandardMaterial({color:n.blocked||d>=.85?0xc40000:d>=.65?0x555555:0xffffff}));m.position.copy(T.position(n));m.userData.node=n;graphGroup.add(m);T.nodeMeshes.set(n.id,m);
 const p=T.position(n);p.y+=1.5;const l=T.label(T.name(n),p,n.blocked);l.node=true;l.el.onclick=()=>T.inspect(n);
 }
 for(const edge of e.detail.edges){const a=T.position(T.data.nodes.find(n=>n.id===edge.source)),b=T.position(T.data.nodes.find(n=>n.id===edge.target));const curve=new THREE.LineCurve3(a,b);graphGroup.add(new THREE.Mesh(new THREE.TubeGeometry(curve,1,.13,5,false),new THREE.MeshStandardMaterial({color:edge.blocked?0xc40000:0x888888})))}
 for(const id of ['sim-source','sim-destination','element']){const el=document.getElementById(id),old=el.value;el.innerHTML=T.data.nodes.map(n=>'<option value="'+n.id+'">'+T.name(n)+' ('+n.id+')</option>').join('');if(old)el.value=old;else if(id==='sim-destination')el.value='E2'}
 document.getElementById('gate-list').innerHTML=T.data.nodes.filter(n=>n.kind==='gate').map(n=>'<p class="'+(n.blocked?'status-critical':'')+'">'+T.name(n)+' · '+(n.blocked?'Blocked':'Open')+' · '+n.crowd+' people</p>').join('');
 document.getElementById('live-state').textContent=(T.data.running?'RUNNING':'PAUSED')+' · Step '+T.data.tick+' · '+T.data.nodes.reduce((s,n)=>s+n.crowd,0).toLocaleString()+' spectators';
});
document.getElementById('heatmap').onclick=async e=>{try{T.heatMode=T.heatMode==='current'?'predicted':'current';if(T.heatMode==='predicted')await T.api('/api/predict',{method:'POST',body:JSON.stringify({horizon:3})});e.target.textContent=T.heatMode==='current'?'Show Predicted Heatmap':'Show Current Heatmap';document.getElementById('density-mode').textContent=T.heatMode==='current'?'Current density':'Predicted +3 minute density';await T.refresh()}catch(e){document.getElementById('sim-error').textContent=e.message}};
