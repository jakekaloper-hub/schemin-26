/** Site-specific visualization candidates for the OTHER twenty current Atlas sites.
 * Existing Southern Wetlands models remain owned by regional-assets.mjs.
 * Source IDs, landmarks and positions are inputs. Local materials/shapes are art
 * proposals, NOT approved geography, historical restoration or new world state.
 * No actors, network, world writes or public release authority.
 */
const SITE_IDS = [
 'LOC-TRADE-JEDI-MOUNTAIN-BASE','LOC-ARSENAL-BARBERSHOP','LOC-STORM-BOWL',
 'LOC-LLC-BOARDROOM','LOC-RED-RUINS','LOC-CHILI-STABLE','LOC-BELT-KEEPER-KEEP',
 'LOC-SLOB-FOOTHILL-CAMP','LOC-CHINS-ROAD-COMMONS','LOC-LEAGUE-CHAMBER',
 'LOC-PITTSYS-BOOK','LOC-BRIDGE-MOUNTAIN-LAKE','LOC-DK-MUD-HILL',
 'LOC-RED-SLOB-ALPINE-ROUTE','LOC-SOUTHERN-SPEEDWAY','LOC-LLC-STORM-CITY',
 'LOC-DK-HIGHLAND-STRONGHOLD','LOC-TDS-CHILI-SHARED-MARCH',
 'LOC-COMPACT-NEUTRAL-GROUNDS','LOC-LEAGUE-ARCHIVE'
];
export function supportedAtlasSiteIds(){return [...SITE_IDS];}
export function buildAtlasSiteAssets(THREE,bindings,height){
 if(!THREE||!Array.isArray(bindings)||typeof height!=='function')throw Error('ATLAS_ASSET_INPUT_REQUIRED');
 const seen=new Set();for(const b of bindings){if(!b||seen.has(b.id))throw Error('DUPLICATE_LOCATION');seen.add(b.id);if(!Array.isArray(b.anchor)||b.anchor.length!==3||!b.anchor.every(Number.isFinite))throw Error('INVALID_SITE_ANCHOR');}
 const root=new THREE.Group();root.name='Current Atlas sites · candidate visualizations';
 const locations=[],water=[],motion=[],geometries=new Set(),materials=new Set(),textures=new Set();let disposed=false;
 function texture(kind){const n=64,bytes=new Uint8Array(n*n*4);for(let y=0;y<n;y++)for(let x=0;x<n;x++){const hash=((x*73856093)^(y*19349663))>>>0;let v=215+(hash%29);if(kind==='stone'&&(y%16<1||(x+(Math.floor(y/16)%2)*16)%32<1))v=140;else if(kind==='wood')v-=Math.pow(.5+.5*Math.sin(x*.73+Math.sin(y*.13)),4)*55;const i=(y*n+x)*4;bytes[i]=bytes[i+1]=bytes[i+2]=v;bytes[i+3]=255;}const t=new THREE.DataTexture(bytes,n,n);t.colorSpace=THREE.SRGBColorSpace;t.wrapS=t.wrapT=THREE.RepeatWrapping;t.generateMipmaps=true;t.minFilter=THREE.LinearMipmapLinearFilter;t.magFilter=THREE.LinearFilter;t.needsUpdate=true;textures.add(t);return t;}
 const stoneMap=texture('stone'),woodMap=texture('wood');
 function mat(color,kind='',extra={}){const m=new THREE.MeshStandardMaterial({color,roughness:.88,map:kind==='stone'?stoneMap:kind==='wood'?woodMap:null,...extra});materials.add(m);return m;}
 const M={stone:mat('#c3bda5','stone'),light:mat('#e5d5ae','stone'),dark:mat('#444b58','stone'),slate:mat('#55626c','stone'),sand:mat('#bca176'),wood:mat('#785738','wood'),timber:mat('#4d3528','wood'),red:mat('#a82f38'),gold:mat('#bd9745','',{metalness:.25}),green:mat('#537746'),deepGreen:mat('#275647'),paleGreen:mat('#91a365'),earth:mat('#75634c'),ivory:mat('#e5d8b9'),blue:mat('#2c6a7e'),canvas:mat('#9d7860'),roof:mat('#665957','stone'),snow:mat('#d8e2dc'),glass:mat('#78a4a5','',{roughness:.25}),black:mat('#293336')};
 function mesh(g,geo,m,x=0,y=0,z=0,name=''){geometries.add(geo);const o=new THREE.Mesh(geo,m);o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;o.name=name;g.add(o);return o;}
 const box=(g,x,y,z,w,h,d,m,name='')=>mesh(g,new THREE.BoxGeometry(w,h,d),m,x,y+h/2,z,name);
 const cyl=(g,x,y,z,rt,rb,h,m,n=12,name='')=>mesh(g,new THREE.CylinderGeometry(rt,rb,h,n),m,x,y+h/2,z,name);
 function roof(g,x,y,z,w,d,h,m=M.roof){const o=mesh(g,new THREE.CylinderGeometry(0,1,h,4,1),m,x,y+h/2,z,'Pitched roof candidate');o.scale.set(w/Math.SQRT2,1,d/Math.SQRT2);o.rotation.y=Math.PI/4;return o;}
 function rock(g,x,y,z,sx,sy,sz,m=M.slate){const o=mesh(g,new THREE.IcosahedronGeometry(1,1),m,x,y,z,'Illustrative rock');o.scale.set(sx,sy,sz);o.rotation.set(.13+x*.03,.3+z*.11,.07);return o;}
 function beam(g,a,b,r=.12,m=M.wood,name='Timber brace'){const av=new THREE.Vector3(...a),bv=new THREE.Vector3(...b),d=bv.clone().sub(av);const o=mesh(g,new THREE.CylinderGeometry(r,r,d.length(),6),m,...av.add(bv).multiplyScalar(.5).toArray(),name);o.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());return o;}
 function arch(g,x,y,z,r=1.5,thickness=.45,depth=.7,m=M.stone){const sh=new THREE.Shape();sh.moveTo(-r-thickness,0);sh.lineTo(-r-thickness,r);sh.absarc(0,r,r+thickness,Math.PI,0,true);sh.lineTo(r+thickness,0);sh.lineTo(r,0);sh.lineTo(r,r);sh.absarc(0,r,r,0,Math.PI,false);sh.lineTo(-r,0);sh.closePath();const geo=new THREE.ExtrudeGeometry(sh,{depth,bevelEnabled:false,curveSegments:10});return mesh(g,geo,m,x,y,z-depth/2,'Masonry arch candidate');}
 function posts(g,x,z,w,d,h=2.8,m=M.wood){for(const dx of [-w/2,w/2])for(const dz of [-d/2,d/2])cyl(g,x+dx,.3,z+dz,.14,.2,h,m,8);}
 function pavilion(g,x,z,w=5,d=4,h=3,m=M.roof){const floor=box(g,x,0,z,w+.6,.3,d+.6,M.stone,'Pavilion floor');posts(g,x,z,w,d,h);roof(g,x,h+.3,z,w+1,d+1,1.6,m);return floor;}
 function hall(g,x,z,w=6,d=4,h=3,m=M.stone,rm=M.roof){const body=box(g,x,.35,z,w,h,d,m,'Hall candidate');roof(g,x,h+.35,z,w+.7,d+.7,1.6,rm);box(g,x,.36,z+d/2+.03,1.1,2,.08,M.timber,'Door');for(const dx of [-w*.3,w*.3])box(g,x+dx,1.4,z+d/2+.05,.65,.95,.08,M.glass,'Window');return body;}
 function steps(g,x,z,w,count=5,rise=.18,run=.42,m=M.stone){let first;for(let i=0;i<count;i++)first=box(g,x,0,z-i*run,w,rise*(i+1),run+.02,m,'Approach step');return first;}
 function fence(g,x,z,w,d,m=M.wood){for(const dz of [-d/2,d/2]){for(let i=0;i<=4;i++)box(g,x-w/2+i*w/4,0,z+dz,.16,1.15,.16,m);for(const y of [.43,.86])box(g,x,y,z+dz,w,.12,.13,m);}for(const dx of [-w/2,w/2])for(const y of [.43,.86])box(g,x+dx,y,z,.13,.12,d,m);}
 // Source-exact Red Ruins predator banners: one shared moving cloth treatment.
 // Mast anchors and location stay source-defined; folds are illustration only,
 // not sourced wind, canonical weather, or an enacted world event.
 let ruinBannerMaterial=null;
 function flag(g,x,y,z,color=M.red,animateCloth=false){
  const p=cyl(g,x,y,z,.055,.075,3.8,M.timber,6,'Banner mast');
  if(!animateCloth){box(g,x+.55,y+2.25,z,1.05,1.35,.035,color,'Stationary authored banner');return p;}
  if(!ruinBannerMaterial){
   ruinBannerMaterial=new THREE.ShaderMaterial({uniforms:{uTime:{value:0}},side:THREE.DoubleSide,
    vertexShader:`uniform float uTime;varying vec2 vUv;varying float vFold;
     void main(){
      vUv=uv;vec3 p=position;
      float reach=clamp((position.x+.525)/1.05,0.,1.);
      float low=sin(uTime*.87+position.y*2.2+reach*6.4);
      float high=sin(uTime*1.53-position.y*3.7+reach*12.);
      p.z+=reach*reach*(.085*low+.035*high);
      p.y+=.024*reach*sin(uTime*.89+reach*4.8);
      vFold=.5+.5*high;
      gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.);
     }`,
    fragmentShader:`varying vec2 vUv;varying float vFold;
     void main(){
      float light=.77+.23*vFold;
      float hem=1.-.16*smoothstep(0.,1.,vUv.y);
      vec3 color=vec3(.68,.14,.18)*light*hem;
      gl_FragColor=vec4(color,1.);
      #include <tonemapping_fragment>
      #include <colorspace_fragment>
     }`});
   materials.add(ruinBannerMaterial);motion.push(ruinBannerMaterial);
  }
  // Anchored and tessellated, with no additional mesh or draw call per flag.
  const cloth=mesh(g,new THREE.PlaneGeometry(1.05,1.35,10,6),ruinBannerMaterial,x+.55,y+2.925,z,'Moving predator banner · candidate cloth');
  cloth.castShadow=false;cloth.receiveShadow=false;
  return p;
 }
 function tree(g,x,z,s=1,m=M.deepGreen){cyl(g,x,0,z,.13*s,.25*s,2.3*s,M.timber,6);for(let i=0;i<3;i++)rock(g,x+Math.sin(i*2.1)*.55*s,(2.5+i*.2)*s,z+Math.cos(i*2.1)*.45*s,s,.8*s,s,i===1?M.green:m);}
 // Locally sculpted, presentation-only alpine stone/snow. Site anchor and
 // authoritative summit geometry remain upstream; this adds no world state.
 function alpineSurface(g,x,y,z,sx,sy,sz,snowCap=false){
  const geo=new THREE.IcosahedronGeometry(1,3),position=geo.getAttribute('position'),colors=[];
  for(let i=0;i<position.count;i++){
   const vx=position.getX(i),vy=position.getY(i),vz=position.getZ(i);
   // Bounded (<=2.9%) micro-relief: deterministic, no texture or new draw.
   const grain=Math.sin(vx*19.3+vz*13.7)*Math.cos(vy*17.1-vz*4.6);
   const crack=Math.sin(vx*39.1+vy*27.3+vz*31.7);
   const relief=1+.020*grain+.009*crack;
   position.setXYZ(i,vx*relief,vy*relief,vz*relief);
   const weathering=.5+.5*Math.sin(vx*9.3+vz*5.7)*Math.cos(vy*8.1-vx*3.1);
   const line=Math.max(0,Math.min(1,(vy-.22+grain*.10)*2.7));
   const cover=snowCap?.76+.22*weathering:line*(.68+.22*weathering);
   const shade=.65+.35*weathering;
   const stone=[.18*shade,.23*shade,.26*shade],snow=[.64+.18*weathering,.70+.14*weathering,.71+.16*weathering];
   for(let c=0;c<3;c++)colors.push(stone[c]*(1-cover)+snow[c]*cover);
  }
  geo.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));geo.computeVertexNormals();
  const surface=mat('#ffffff','',{vertexColors:true,roughness:.96,metalness:0});
  const o=mesh(g,geo,surface,x,y,z,snowCap?'Alpine summit snow · candidate':'Alpine summit stone · candidate');
  o.scale.set(sx,sy,sz);o.rotation.set(.13+x*.03,.3+z*.11,.07);
  return o;
 }
 // Exact Trade Jedi Mountain Base ridge: one static replacement, original
 // instance transform. Stone strata are illustrative, not canonical geology.
 function tradeJediHighRidge(g){
  const geo=new THREE.IcosahedronGeometry(1,3),position=geo.getAttribute('position'),colors=[];
  for(let i=0;i<position.count;i++){
   const vx=position.getX(i),vy=position.getY(i),vz=position.getZ(i);
   const grain=Math.sin(vx*17.1+vz*8.3)*Math.cos(vy*11.7-vx*4.6);
   const fissure=Math.sin(vx*30.7+vy*23.1+vz*14.4);
   const relief=1+.016*grain+.008*fissure;
   position.setXYZ(i,vx*relief,vy*relief,vz*relief);
   const band=.5+.5*Math.sin(vy*22.7+vx*1.8+Math.sin(vz*5.4)*.28);
   const mineral=.5+.5*Math.sin(vx*12.7+vz*15.1)*Math.cos(vy*9.9-vz*5.6);
   const shade=.75+.25*mineral;
   colors.push(.23+.105*shade+.04*band,.225+.07*shade+.035*band,.205+.045*shade+.027*band);
  }
  geo.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));geo.computeVertexNormals();
  const stone=mat('#ffffff','',{vertexColors:true,roughness:.98,metalness:0});
  const ridge=mesh(g,geo,stone,0,1.3,0,'Trade Jedi high ridge · candidate');
  ridge.scale.set(7,2.5,5.5);ridge.rotation.set(.13,.3,.07);
  return ridge;
 }
 function conifer(g,x,z,s=1){cyl(g,x,0,z,.12*s,.23*s,3.3*s,M.timber,6);for(let i=0;i<3;i++)cyl(g,x,1.1*s+i*.65*s,z,.04,(1.2-i*.22)*s,1.8*s,M.deepGreen,7);}
 function ring(g,x,y,z,inner,outer,scaleZ=1,m=M.sand){const o=mesh(g,new THREE.RingGeometry(inner,outer,56),m,x,y,z,'Open ring candidate');o.rotation.x=-Math.PI/2;o.scale.y=scaleZ;return o;}
 // Only the source-recorded Southern Speedway receives this candidate dirt surface.
 // Existing oval footprint and height remain unchanged; wear and ruts are not
 // historical tire evidence, course geometry authority or a current race event.
 function speedwayTrack(g){
  const inner=4.2,outer=6.7,geo=new THREE.RingGeometry(inner,outer,144,20);
  const pos=geo.getAttribute('position'),colors=[];
  for(let i=0;i<pos.count;i++){
   const x=pos.getX(i),y=pos.getY(i),radius=Math.hypot(x,y),angle=Math.atan2(y,x);
   const edge=Math.min(1,Math.max(0,(radius-inner)/.25),Math.max(0,(outer-radius)/.25));
   const innerRut=Math.exp(-Math.pow((radius-5.02-.045*Math.sin(angle*3))/.22,2));
   const outerRut=Math.exp(-Math.pow((radius-5.83-.035*Math.sin(angle*4+.4))/.22,2));
   const grit=Math.sin(angle*31+radius*12)*Math.cos(angle*19-radius*17);
   pos.setZ(i,edge*(.009*grit-.043*innerRut-.038*outerRut));
   const shade=Math.max(.42,Math.min(.88,.75-.16*innerRut-.13*outerRut+.06*grit));
   colors.push(.46*shade,.34*shade,.23*shade);
  }
  geo.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));
  geo.computeVertexNormals();geo.computeBoundingSphere();
  const surface=mat('#ffffff','',{vertexColors:true,roughness:.98,metalness:0});
  const course=mesh(g,geo,surface,0,.35,0,'Rutted oval race course · candidate');
  course.rotation.x=-Math.PI/2;course.scale.y=.64;
  return course;
 }

 // Weather exposure is source-recorded for LOC-STORM-BOWL, but the tiny chips
 // and mineral shades below are reversible presentation details, not an event.
 // One existing seat stays one static mesh; existing anchors and box limits
 // remain unchanged, so batching can preserve the original draw budget.
 let stormBowlSeatMaterial=null;
 function stormBowlSeat(g,x,z,angle,index){
  if(!stormBowlSeatMaterial)stormBowlSeatMaterial=mat('#ffffff','',{vertexColors:true,roughness:.97,metalness:0});
  const geo=new THREE.BoxGeometry(1.9,.7,1.4,6,3,4);
  const position=geo.getAttribute('position'),colors=[];
  for(let i=0;i<position.count;i++){
   const vx=position.getX(i),vy=position.getY(i),vz=position.getZ(i);
   const grain=.5+.5*Math.sin(vx*18.3+vz*14.7+index*.81)*Math.cos(vy*15.2-vz*8.1);
   const corner=Math.max(0,Math.min(1,(Math.abs(vx)/.95+Math.abs(vz)/.7-1.30)/.70));
   const fracture=.013+.065*corner*(.4+.6*grain);
   const wornTop=vy>0?.010+.035*grain:0;
   position.setXYZ(i,vx*(1-fracture),vy-wornTop,vz*(1-fracture));
   const mineral=.62+.19*grain-.07*corner;
   colors.push(.56*mineral,.59*mineral,.61*mineral);
  }
  geo.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));
  geo.computeVertexNormals();geo.computeBoundingSphere();
  const seat=mesh(g,geo,stormBowlSeatMaterial,x,.8,z,'Broken-ring seating');
  seat.rotation.y=-angle;
  return seat;
 }
 // Source-exact Highland Stronghold training court: reversible sculpted-sand
 // visualization. No recorded training action, actor or world-state mutation.
 // One subdivided static mesh replaces the existing flat box at identical bounds.
 let highlandCourtMaterial=null;
 function highlandTrainingCourt(g){
  const geo=new THREE.BoxGeometry(7.8,.1,5,48,1,32);
  const p=geo.getAttribute('position'),colors=[];
  for(let i=0;i<p.count;i++){
   const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
   const top=y>.049,edge=Math.max(0,Math.min(1,(3.9-Math.abs(x))/.33,(2.5-Math.abs(z))/.30));
   const laneA=Math.exp(-Math.pow((z+.9+.05*Math.sin(x*1.3))/.34,2));
   const laneB=Math.exp(-Math.pow((z-.9-.04*Math.cos(x*1.2))/.36,2));
   const grain=Math.sin(x*7.8+z*1.9)*Math.cos(z*9.7-x*1.1);
   if(top){
    const relief=edge*(.035*laneA+.031*laneB+.010*(.5+.5*grain));
    p.setY(i,y-relief);
   }
   const tone=top?.84-.19*laneA-.17*laneB+.09*grain:.76;
   colors.push(.68*tone,.55*tone,.35*tone);
  }
  geo.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));
  geo.computeVertexNormals();geo.computeBoundingSphere();
  if(!highlandCourtMaterial)highlandCourtMaterial=mat('#ffffff','',{vertexColors:true,roughness:.99,metalness:0});
  return mesh(g,geo,highlandCourtMaterial,0,.86,1.2,'Training court');
 }
 // Source-exact, provisional Belt Keeper dark keep: one static stone mesh.
 // Recessed mortar courses are bounded presentation relief, not a recorded
 // siege, age, damage event, architectural survey, or canon update.
 let beltKeeperStoneMaterial=null;
 function beltKeeperDarkStone(g){
  const geo=new THREE.BoxGeometry(5.5,6.5,4.8,12,18,10);
  const p=geo.getAttribute('position'),normals=geo.getAttribute('normal'),colors=[];
  const clampEdge=(distance,band)=>Math.max(0,Math.min(1,distance/band));
  for(let i=0;i<p.count;i++){
   const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
   const nx=normals.getX(i),ny=normals.getY(i),nz=normals.getZ(i);
   const vertical=Math.abs(ny)>.5,lateral=Math.abs(nx)>.5;
   const u=vertical?x:lateral?z:x,umax=vertical?2.75:lateral?2.4:2.75;
   const v=vertical?z:y,vmax=vertical?2.4:3.25;
   const edge=clampEdge(umax-Math.abs(u),.27)*clampEdge(vmax-Math.abs(v),.24);
   const course=Math.floor((y+3.25)/.54);
   const horizontal=Math.pow(Math.max(0,1-Math.abs(Math.sin((y+3.25)*Math.PI/.54))),10);
   const staggered=Math.pow(Math.max(0,1-Math.abs(Math.sin((u+(course%2)*.45)*Math.PI/1.1))),12);
   const mortar=Math.max(horizontal,staggered*.8);
   const grain=.5+.5*Math.sin(u*6.1+v*7.9)*Math.cos(y*9.7-u*3.8);
   const inset=edge*(.007+.024*mortar+.010*grain);
   p.setXYZ(i,x-nx*inset,y-ny*inset,z-nz*inset);
   const shade=.75+.18*grain-.12*mortar;
   colors.push(.075*shade,.095*shade,.12*shade);
  }
  geo.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));
  geo.computeVertexNormals();geo.computeBoundingSphere();
  if(!beltKeeperStoneMaterial)beltKeeperStoneMaterial=mat('#ffffff','stone',{vertexColors:true,roughness:.97,metalness:0});
  return mesh(g,geo,beltKeeperStoneMaterial,0,4.45,-.8,'Dark keep');
 }
 function desk(g,x,y,z,w=2.7,m=M.wood){const top=box(g,x,y+1.1,z,w,.15,1.1,m,'Record surface');for(const dx of [-w*.4,w*.4])box(g,x+dx,y,z,.17,1.1,.65,M.timber);return top;}
 function ledger(g,x,y,z){for(let i=0;i<3;i++)box(g,x+i*.18,y+i*.08,z,.7,.08,.55,i===1?M.red:M.ivory,'Unlettered ledger');}
 // Pittsy's Book: unlettered open spread upon the existing settlement desk.
 // Ruled paper / curvature are illustrative only: no odds or historical writes.
 function pittsysOpenLedger(g){
  const geo=new THREE.BufferGeometry(),positions=[],colors=[],indices=[];
  const columns=14,rows=24;
  for(const side of [-1,1]){
   const start=positions.length/3;
   for(let row=0;row<=rows;row++)for(let column=0;column<=columns;column++){
    const u=column/columns,v=row/rows;
    const x=-.07+side*(.025+.705*u),z=1.2+(v-.5)*1.14;
    const y=1.62+.056*Math.pow(u,1.25)-.014*Math.exp(-Math.pow(u/.16,2))+.006*Math.sin(Math.PI*v)*u;
    positions.push(x,y,z);
    const ruled=(row>=4&&row<=20&&row%4===0)?.085:0;
    const tone=.89-.02*u-ruled;
    colors.push(tone,tone*.971,tone*.884);
   }
   for(let row=0;row<rows;row++)for(let col=0;col<columns;col++){
    const a=start+row*(columns+1)+col,b=a+1,c=a+columns+1,d=c+1;
    indices.push(a,b,c,b,d,c);
   }
  }
  geo.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));
  geo.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));
  geo.setIndex(indices);geo.computeVertexNormals();
  const cover=box(g,-.07,1.55,1.2,1.55,.065,1.24,M.deepGreen,'Open ledger cover candidate');
  const leaves=mesh(g,geo,mat('#ffffff','',{vertexColors:true,side:THREE.DoubleSide,roughness:1}),0,0,0,'Open ledger leaves — unlabeled');
  for(const piece of [cover,leaves])piece.userData={...piece.userData,visualAuthority:'CANDIDATE_NOT_APPROVED',contentAuthority:'NONE'};
  return leaves;
 }
 // The four EXISTING other-site water bodies use a finer interior mesh so
 // the environmental clock moves their actual surface, not just painted streaks.
 // All rim vertices remain fixed at the original radius; this is candidate art,
 // not a coastline, water-level, weather or Atlas-topology assertion.
 function existingWaterDisk(){
  const segments=56,rings=7,positions=[0,0,0],uvs=[.5,.5],indices=[];
  for(let ring=1;ring<=rings;ring++)for(let i=0;i<segments;i++){
   const a=i*Math.PI*2/segments,r=ring/rings,x=Math.cos(a)*r,y=Math.sin(a)*r;
   positions.push(x,y,0);uvs.push(.5+x*.5,.5+y*.5);
  }
  for(let i=0;i<segments;i++)indices.push(0,1+i,1+(i+1)%segments);
  for(let ring=1;ring<rings;ring++)for(let i=0;i<segments;i++){
   const p=1+(ring-1)*segments+i,q=1+(ring-1)*segments+(i+1)%segments;
   const n=1+ring*segments+i,m=1+ring*segments+(i+1)%segments;
   indices.push(p,n,m,p,m,q);
  }
  const geo=new THREE.BufferGeometry();geo.name='Candidate existing-water interior';
  geo.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));
  geo.setAttribute('uv',new THREE.Float32BufferAttribute(uvs,2));
  geo.setIndex(indices);geo.computeVertexNormals();geo.computeBoundingSphere();
  return geo;
 }
 function waterSurface(g,x,y,z,rx,rz,kind='lake',color='#366d76'){
  const material=new THREE.ShaderMaterial({uniforms:{uTime:{value:0},uColor:{value:new THREE.Color(color)},uAmplitude:{value:kind==='mountain lake'?.028:kind==='sheltered port'?.021:kind==='mire'?.012:.010},uViewSheen:{value:kind==='mountain lake'?.52:kind==='sheltered port'?.42:kind==='mire'?.12:.24},uCrossing:{value:kind==='watercourse crossing'?1:0},uBridge:{value:kind==='mountain lake'?1:0},uBarrier:{value:kind==='sheltered port'?1:0},uMire:{value:kind==='mire'?1:0},uLakeGlint:{value:kind==='mountain lake'?1:0}},transparent:true,depthWrite:false,side:THREE.DoubleSide,
   vertexShader:`uniform float uTime;uniform float uAmplitude;uniform float uCrossing;uniform float uBridge;uniform float uBarrier;uniform float uMire;varying vec2 vUv;varying vec3 vWorld;
    void main(){
     vUv=uv;vec3 p=position;
     float radius=length(position.xy);
     // Preserve the original footprint and still-shoreline vertices at all times.
     float interior=1.-smoothstep(.58,.95,radius);
     float waveA=sin(position.x*12.7-uTime*1.18+sin(position.y*7.5)*.45);
     float waveB=sin(position.y*10.2+uTime*.74+position.x*3.);
     p.z+=uAmplitude*interior*(.72*waveA+.28*waveB);
     // Candidate crossing-only riffle; its local axis is not canonical hydrology.
     float crossingWave=sin(position.y*18.8-uTime*2.1+sin(position.x*5.)*.55);
     p.z+=uCrossing*uAmplitude*.34*interior*crossingWave;
     // Lake-only candidate bridge-contact wave at the two modeled arch ends.
     // These are presentation geometry coordinates, not surveyed hydrology.
     float bridgeR=min(length(position.xy-vec2(-.39,0.)),length(position.xy-vec2(.39,0.)));
     float bridgeWave=exp(-bridgeR*8.)*sin(bridgeR*24.-uTime*1.7);
     p.z+=uBridge*uAmplitude*.16*interior*bridgeWave;
     // Candidate storm-barrier contact: modeled shape, not surveyed hydrology.
     float barrierAxis=abs(position.y+.016);
     float barrierSpan=smoothstep(-.85,-.62,position.x)*(1.-smoothstep(.45,.65,position.x));
     float barrierBand=exp(-barrierAxis*13.)*barrierSpan;
     float barrierWave=sin(barrierAxis*26.-uTime*1.35+position.x*3.1);
     p.z+=uBarrier*uAmplitude*.20*interior*barrierBand*barrierWave;
     // Candidate-only, slow silt eddies on the original Mire Hill water mesh.
     float mireR=length(position.xy-vec2(.12,-.08));
     float mireBand=exp(-mireR*3.2)*interior;
     float mireWave=sin(mireR*17.-uTime*.81+position.x*4.8-position.y*3.1);
     p.z+=uMire*uAmplitude*.22*mireBand*mireWave;
     vWorld=(modelMatrix*vec4(p,1.)).xyz;
     gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.);
    }`,
   fragmentShader:`uniform float uTime;uniform vec3 uColor;uniform float uViewSheen;uniform float uCrossing;uniform float uBridge;uniform float uBarrier;uniform float uMire;uniform float uLakeGlint;varying vec2 vUv;varying vec3 vWorld;
    void main(){
     float edge=1.-smoothstep(.83,1.,length((vUv-.5)*2.));
     float line=pow(max(sin(vUv.x*52.+sin(vUv.y*19.)*.9-uTime*.7),0.),17.);
     float gap=smoothstep(.2,.85,.5+.5*sin(vUv.y*32.+uTime*.24));
     // Read the actual moving mesh's world-space facing; no static painted normal.
     vec3 faceCross=cross(dFdx(vWorld),dFdy(vWorld));
     float faceSize=length(faceCross);
     vec3 faceNormal=faceSize>.00001?faceCross/faceSize:vec3(0.,1.,0.);
     vec3 eyeRay=normalize(cameraPosition-vWorld);
     float grazing=pow(1.-clamp(abs(dot(faceNormal,eyeRay)),0.,1.),2.);
     vec3 viewTint=vec3(.10,.16,.15)*(uViewSheen*grazing);
     // Candidate-only lake glints follow real displaced-surface derivatives.
     // Fixed illustrative key light: NOT an Eastern solar or weather feed.
     // Uniform branch skips extra work on the other three existing waters.
     float lakeGlint=0.;
     if(uLakeGlint>.5){
       vec3 lakeNormal=faceNormal.y<0.?-faceNormal:faceNormal;
       vec3 lakeSun=normalize(vec3(.43,.79,.37));
       lakeGlint=(1.-smoothstep(.58,.95,length((vUv-.5)*2.)))*pow(max(dot(reflect(-lakeSun,lakeNormal),eyeRay),0.),12.);
     }
     float crossingSheen=uCrossing*pow(max(sin(vUv.y*72.-uTime*2.1+sin(vUv.x*16.)*.55),0.),18.)*(1.-smoothstep(.58,.95,length((vUv-.5)*2.)));
     float bridgeR=min(length((vUv-.5)*2.-vec2(-.39,0.)),length((vUv-.5)*2.-vec2(.39,0.)));
     float bridgeSheen=uBridge*exp(-bridgeR*10.)*pow(max(sin(bridgeR*34.-uTime*1.7),0.),8.)*(1.-smoothstep(.58,.95,length((vUv-.5)*2.)));
     vec2 barrierXY=(vUv-.5)*2.;
     float barrierAxis=abs(barrierXY.y+.016);
     float barrierSpan=smoothstep(-.85,-.62,barrierXY.x)*(1.-smoothstep(.45,.65,barrierXY.x));
     float barrierSheen=uBarrier*exp(-barrierAxis*13.)*barrierSpan*pow(max(sin(barrierAxis*26.-uTime*1.35+barrierXY.x*3.1),0.),8.)*(1.-smoothstep(.58,.95,length(barrierXY)));
     // Source-exact mire tint follows moving vertex eddy phase, never historical state.
     vec2 mireXY=(vUv-.5)*2.;
     float mireR=length(mireXY-vec2(.12,-.08));
     float mireSilt=uMire*exp(-mireR*3.2)*(.5+.5*sin(mireR*17.-uTime*.81+mireXY.x*4.8-mireXY.y*3.1))*(1.-smoothstep(.58,.95,length(mireXY)));
     vec3 c=clamp(uColor+vec3(.09,.15,.14)*line*gap+viewTint,0.,1.);
     c=clamp(c+vec3(.035,.065,.06)*crossingSheen,0.,1.);
     c=clamp(c+vec3(.055,.09,.08)*bridgeSheen,0.,1.);
     c=clamp(c+vec3(.13,.18,.17)*lakeGlint,0.,1.);
     c=clamp(c+vec3(.045,.075,.074)*barrierSheen,0.,1.);
     c=clamp(c+vec3(.052,.034,-.008)*mireSilt,0.,1.);
     gl_FragColor=vec4(c,.87*edge);\n#include <tonemapping_fragment>\n#include <colorspace_fragment>\n}`});materials.add(material);
  const o=mesh(g,existingWaterDisk(),material,x,y,z,'Moving '+kind+' candidate');o.rotation.x=-Math.PI/2;o.scale.set(rx,rz,1);o.castShadow=false;o.receiveShadow=false;water.push({mesh:o,material,kind});return o;
 }
 // Only the source-exact Chili Stable pit uses layered, time-advected wisps.
 // Other existing smoke sites retain their prior shader. Candidate art only;
 // no new geometry/materials, atmospheric authority or world state.
 function smoke(g,x,y,z,layered=false){const material=new THREE.ShaderMaterial({uniforms:{uTime:{value:0}},transparent:true,depthWrite:false,side:THREE.DoubleSide,vertexShader:'varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',fragmentShader:layered?'uniform float uTime;varying vec2 vUv;float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1.,0.)),f.x),mix(hash(i+vec2(0.,1.)),hash(i+vec2(1.,1.)),f.x),f.y);}void main(){float rise=clamp(vUv.y,0.,1.);vec2 adv=vec2(vUv.x*4.2,vUv.y*3.9-uTime*.39);float coarse=noise(adv*1.8),fine=noise(adv*4.1+vec2(11.7,-uTime*.12));float drift=.075*sin(rise*5.7-uTime*.61)+.034*sin(rise*13.1-uTime*.27);float spread=mix(.11,.36,rise);float across=abs(vUv.x-.5-drift);float body=1.-smoothstep(spread*.52,spread,across);float breakup=clamp(.64+.52*(coarse-.5)+.36*(fine-.5),0.,1.);float birth=smoothstep(0.,.12,rise);float fade=1.-smoothstep(.72,1.,rise);float a=min(.22,.22*body*breakup*birth*fade);float grey=mix(.46,.7,rise);gl_FragColor=vec4(vec3(grey*.99,grey*.995,grey),a);}':'uniform float uTime;varying vec2 vUv;void main(){float x=vUv.x-.5-sin(vUv.y*8.-uTime*.65)*.08;float a=exp(-x*x*36.)*sin(vUv.y*3.14159)*(.65+.35*sin(vUv.y*22.-uTime*1.4));gl_FragColor=vec4(.64,.64,.58,a*.2);}'});materials.add(material);for(const yaw of [0,Math.PI/2]){const o=mesh(g,new THREE.PlaneGeometry(2,5),material,x,y+2.5,z,'Authored pit smoke');o.rotation.y=yaw;o.castShadow=false;}motion.push(material);}

 // Source-exact watercourse bank vegetation is an illustrative presentation,
 // never a measured shoreline or a new Atlas location. One combined dynamic draw.
 function crossingBankReeds(g){
  const positions=[],uv=[],phases=[],indices=[];
  for(let bank=0;bank<2;bank++)for(let i=0;i<14;i++){
   const x=-6.2+i*.95;if(Math.abs(x)<1.5)continue; // keep the existing bridge approach clear
   const z=(bank===0?1.04:4.53)+.10*Math.sin(i*1.31+bank);
   const h=.60+.08*((i+bank)%4),phase=i*.79+bank*2.17,first=positions.length/3;
   for(const [rise,width] of [[0,.075],[.52,.050],[1,.012]])for(const side of [-1,1]){
    positions.push(x+side*width,.30+h*rise,z);
    uv.push((side+1)/2,rise);phases.push(phase);
   }
   for(let row=0;row<2;row++){const a=first+row*2;indices.push(a,a+1,a+2,a+1,a+3,a+2);}
  }
  const geo=new THREE.BufferGeometry();geo.name='Shared March bankside reeds · candidate';
  geo.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));
  geo.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));
  geo.setAttribute('aPhase',new THREE.Float32BufferAttribute(phases,1));
  geo.setIndex(indices);geo.computeVertexNormals();geo.computeBoundingSphere();
  const material=new THREE.ShaderMaterial({uniforms:{uTime:{value:0}},
   vertexShader:`uniform float uTime;attribute float aPhase;varying float vRise;varying float vShade;
void main(){float rise=clamp(uv.y,0.,1.);vec3 p=position;
float bend=sin(uTime*.73+aPhase)+.3*sin(uTime*1.21+aPhase*1.73);
p.x+=pow(rise,1.7)*.16*bend;
p.z+=pow(rise,1.6)*.035*sin(uTime*.51+aPhase*1.31);
vRise=rise;vShade=.7+.3*(.5+.5*sin(aPhase+uTime*.18));
gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.);`,
   fragmentShader:`varying float vRise;varying float vShade;
void main(){vec3 base=mix(vec3(.18,.24,.12),vec3(.39,.49,.21),vRise);
gl_FragColor=vec4(base*vShade,1.);
#include <tonemapping_fragment>
#include <colorspace_fragment>
}`,
   side:THREE.DoubleSide,depthWrite:true});
  materials.add(material);motion.push(material);
  const o=mesh(g,geo,material,0,0,0,'Shared March swaying bank reeds · candidate');
  o.castShadow=false;o.receiveShadow=false;
  return o;
 }
 // A definition returns one representative object for each upstream landmark.
 const definitions={
  'LOC-TRADE-JEDI-MOUNTAIN-BASE'(g){const ridge=tradeJediHighRidge(g);for(let i=0;i<3;i++)box(g,0,1.9+i*.27,0,9-i*1.3,.35,6-i*.8,M.stone);const pavilionStart=g.children.length;const view=pavilion(g,0,-.7,5.2,3.4,3.7,M.slate);for(const part of g.children.slice(pavilionStart))part.position.y+=2.1;for(const dx of [-2.6,2.6]){beam(g,[dx,.3,-2.4],[dx,5.8,-2.4],.15,M.stone);flag(g,dx,2.4,-2.5,M.blue);}steps(g,0,4.5,2.7,10,.24);for(const x of [-5,5])conifer(g,x,-2,.8);desk(g,0,2.7,0,3,M.stone);return [ridge,view];},
  'LOC-ARSENAL-BARBERSHOP'(g){box(g,0,0,0,8,.35,6,M.stone);const shell=hall(g,0,-1,6,3.4,3.2,M.light,M.red);box(g,0,.35,1.2,5.4,2.8,.13,M.timber,'Open shop backdrop');const awning=roof(g,0,2.75,2.05,6.4,2.2,.6,M.red);for(const dx of [-2.6,2.6])cyl(g,dx,.3,2.9,.08,.11,2.45,M.ivory,7);cyl(g,0,.4,1.9,.35,.6,.6,M.black);const chair=box(g,0,1.0,1.9,1.25,.27,1.2,M.red,'Barber chair');box(g,0,1.24,1.45,1.25,1.1,.23,M.red);for(const x of [-.8,.8])box(g,x,1.1,1.9,.14,.5,1.2,M.gold);box(g,0,.72,2.85,.8,.14,.4,M.black);for(const x of [-2.2,2.2]){const pole=cyl(g,x,.35,3,.1,.1,2,M.ivory,8);for(let i=0;i<5;i++)cyl(g,x,.4+i*.35,3,.115,.115,.16,M.red,8);pole.name='Shop stripe';}return [chair,awning];},
  'LOC-STORM-BOWL'(g){const field=cyl(g,0,0,0,6.6,6.9,.45,M.sand,36,'Weather-exposed venue');for(let i=0;i<20;i++){const a=i*Math.PI*2/20;if(a>1.1&&a<2.0)continue;const x=Math.cos(a)*6.3,z=Math.sin(a)*6.3;stormBowlSeat(g,x,z,a,i);rock(g,x*1.13,.35,z*1.13,.8,.7,.8,M.dark);}const counter=desk(g,1,.45,7.6,4);pavilion(g,1,7.6,4.6,2.4,2.7,M.blue);for(const x of [-4,4])flag(g,x,.4,-5.4,M.blue);return [field,counter];},
  'LOC-LLC-BOARDROOM'(g){box(g,0,0,0,10,.55,7.5,M.slate);const chamber=hall(g,0,-1.6,8.8,3.6,4.6,M.light,M.slate);for(const x of [-4.2,4.2])cyl(g,x,.55,1.6,.27,.34,3.8,M.stone);const table=desk(g,0,.55,1.45,4.4,M.dark);ledger(g,-1.1,1.85,1.4);ledger(g,.8,1.85,1.4);const ledgers=box(g,-3.6,.55,.4,.7,2.4,1.7,M.timber,'Ledger cabinet');for(let i=0;i<5;i++)box(g,-3.6,1+i*.32,.95,.55,.19,.7,i%2?M.red:M.ivory);const overlook=box(g,0,.65,4.2,10,.2,1.8,M.stone,'Market overlook');for(let i=0;i<9;i++)box(g,-4+i, .85,4.9,.12,.8,.12,M.gold);box(g,0,1.6,4.9,8.3,.1,.1,M.gold);steps(g,0,5.6,3,4,.14);return [chamber,ledgers,overlook];},
  'LOC-RED-RUINS'(g){const terrace=box(g,0,0,0,12,.55,10,M.dark,'Ruined jungle terrace');for(let i=0;i<3;i++)box(g,0,.5+i*.3,-i*.5,11-i*.8,.35,8-i*.7,M.stone);for(const x of [-4,0,4])arch(g,x,1.45,-2.5,1.45,.45,.9);for(const [x,z,h]of [[-5,2,2.9],[4.7,2.4,2],[2,-4,4],[-2.7,-4,2.2]]){cyl(g,x,.5,z,.43,.52,h,M.stone,9);rock(g,x+.4,.6,z+.7,.75,.45,.7);}const banners=flag(g,-4.8,.7,3.2,M.red,true);flag(g,4.8,.7,3.2,M.red,true);steps(g,0,5.4,3.5,6,.25);for(const [x,z]of [[-6,-3],[5.8,-3.6],[-5.9,3.8]])tree(g,x,z,1.15);return [terrace,banners];},
  'LOC-CHILI-STABLE'(g){box(g,0,0,0,13,.2,11,M.sand);const stable=hall(g,-2,-2,8,4.3,3.4,M.wood,M.red);for(const x of [-4,-1,2]){box(g,x,.3,.25,2.1,1.7,.12,M.timber);box(g,x,1.2,.35,2.1,.12,.1,M.gold);}const pit=cyl(g,4,.2,3,1.15,1.3,.7,M.dark,14,'Cooking pit');cyl(g,4,.9,3,.85,.95,.5,M.black,12);smoke(g,4,1.2,3,true);fence(g,-2,3.5,7,3.5);const enclosure=box(g,-2,.22,3.5,6.7,.04,3.3,M.earth,'Dark Horse enclosure — no actor');for(const x of [-5.8,5.6])tree(g,x,-3.7,.8,M.paleGreen);return [stable,pit,enclosure];},
  'LOC-BELT-KEEPER-KEEP'(g){const plinth=rock(g,0,.5,0,7,1.3,6.3,M.dark);box(g,0,.5,0,10,.8,8,M.slate);const keep=beltKeeperDarkStone(g);roof(g,0,7.7,-.8,6,5.3,2.6,M.slate);for(const x of [-4,4])for(const z of [-3,3]){cyl(g,x,1.0,z,1.05,1.2,4.5,M.slate,10);cyl(g,x,5.5,z,1.25,1.25,.6,M.dark,10);for(let i=0;i<6;i++){const a=i*Math.PI/3;box(g,x+Math.cos(a)*1.03,6.1,z+Math.sin(a)*1.03,.45,.65,.45,M.dark);}}const hallObj=box(g,0,1.3,2.3,4.3,3,2.2,M.slate,'Championship hall');arch(g,0,1.3,3.5,1,.3,.3,M.gold);flag(g,-1.5,4.6,2.6,M.red);flag(g,1.5,4.6,2.6,M.red);steps(g,0,6,2.3,5,.26);return [keep,hallObj];},
  'LOC-SLOB-FOOTHILL-CAMP'(g){const yard=box(g,0,0,0,12,.18,10,M.earth,'Tailgate yard');for(const [x,z,w,d]of [[-3,-2,4.5,4.3],[3,-2,3.3,3.5]]){roof(g,x,.3,z,w,d,3.2,M.canvas);beam(g,[x,.3,z+d*.52],[x,3.5,z],.07,M.timber);}desk(g,-2,.2,3,4);for(const x of [-4,0])box(g,x,.2,3.8,1.6,.45,.55,M.wood);const training=box(g,3,.2,2.5,3.7,.1,4,M.sand,'Rough training ground');for(const x of [2,3.5,5])cyl(g,x,.3,1.5,.17,.25,1.6,M.wood,7);for(const x of [-6,6])conifer(g,x,-3,1);return [yard,training];},
  'LOC-CHINS-ROAD-COMMONS'(g){box(g,0,0,0,13,.22,10,M.sand);const hallObj=hall(g,0,-2,8.5,4,3.4,M.wood,M.red);pavilion(g,-3.6,2.3,4,3,2.8,M.canvas);const bbq=cyl(g,-3.6,.25,2.5,.9,1,.65,M.dark,12,'BBQ yard');smoke(g,-3.6,.9,2.5);const court=box(g,3.2,.24,2.5,4,.06,4.5,M.earth,'Caravan court');for(const z of [1,4]){box(g,3.1,.6,z,2.4,.4,1.1,M.wood);for(const x of [2.3,3.9]){const wheel=cyl(g,x,.2,z,.4,.4,.15,M.black,10);wheel.rotation.z=Math.PI/2;}}return [hallObj,bbq,court];},
  'LOC-LEAGUE-CHAMBER'(g){box(g,0,0,0,9,.5,7,M.stone);for(const x of [-4,4])box(g,x,.5,-.3,.6,4,6,M.light);box(g,0,.5,-3,8,4,.5,M.light);roof(g,0,4.5,-1,9,5,1.9,M.blue);const map=box(g,0,1.8,-2.68,4.8,1.85,.07,M.gold,'Map wall');box(g,0,1.9,-2.61,4.55,1.6,.04,M.deepGreen);const record=desk(g,0,.5,.4,4.4);ledger(g,-1,1.8,.4);for(const x of [-3,3])cyl(g,x,.5,2,.24,.34,3.6,M.light,10);steps(g,0,4.3,5,4,.15);return [record,map];},
  'LOC-PITTSYS-BOOK'(g){box(g,0,0,0,8.3,.3,6,M.stone);pavilion(g,0,-.5,7,4,3.8,M.deepGreen);const boards=box(g,0,1,-2.3,6.1,2.7,.22,M.timber,'Ledger boards');for(const x of [-2,0,2]){box(g,x,1.2,-2.15,1.55,2.1,.05,M.ivory);for(let j=0;j<5;j++)box(g,x,1.45+j*.32,-2.1,1.3,.035,.03,M.gold);}const settlement=desk(g,0,.3,1.2,5.9,M.dark);ledger(g,-1.6,1.6,1.2);ledger(g,1.1,1.6,1.2);pittsysOpenLedger(g);flag(g,3.7,.3,2.1,M.deepGreen);return [boards,settlement];},
  'LOC-BRIDGE-MOUNTAIN-LAKE'(g){const lake=waterSurface(g,0,.25,0,8.7,5.9,'mountain lake','#477f89');for(const x of [-6.8,6.8])rock(g,x,.15,0,2.1,1,3.4,M.slate);const span=arch(g,0,.3,0,3.4,.65,2.3,M.stone);box(g,0,4.27,0,9.3,.45,2.6,M.stone);for(const z of [-1.25,1.25]){box(g,0,4.7,z,9.2,.8,.18,M.light);for(let i=0;i<11;i++)box(g,-4.25+i*.85,4.7,z,.12,1,.24,M.stone);}for(const s of [-1,1])for(let i=0;i<6;i++)box(g,s*(4.8+i*.5),0,0,.52,4.7-i*.7,2.8,M.stone);const jump=box(g,2.8,4.7,1.6,1.35,.18,.85,M.light,'Recorded jump-point edge');for(const x of [-7.2,7.2])conifer(g,x,-3.3,.8);return [span,lake,jump];},
  'LOC-DK-MUD-HILL'(g){const hill=rock(g,0,.8,0,6,2.4,4.7,M.earth);for(let i=0;i<7;i++){const a=i*2.1;rock(g,Math.cos(a)*4.4,.25,Math.sin(a)*3.6,1.3,.45,1.1,M.slate);}const mire=waterSurface(g,1,.22,1.3,7.2,5.2,'mire','#515d46');const standards=flag(g,-1.9,2.6,0,M.red);flag(g,1.8,2.6,-.3,M.blue);box(g,0,2.15,2.2,3,.2,1,M.earth,'Worn illustrative ridge');return [hill,mire,standards];},
  'LOC-RED-SLOB-ALPINE-ROUTE'(g){const summit=alpineSurface(g,0,1.4,-1.7,5.5,4.1,4.1);alpineSurface(g,.2,4.2,-1.8,3.8,.85,2.9,true);for(let i=0;i<6;i++){const a=i*.7;rock(g,-5+i*1.8,.3,Math.sin(a)*3.2,1.6,.9,1.2,M.slate);}const camp=roof(g,-3,.4,3.5,3.2,3,2.5,M.red);roof(g,2,.4,4.1,2.6,2.7,2.1,M.canvas);const marker=cyl(g,2.9,2.7,-1,.28,.45,1.9,M.stone,7,'Wager marker');flag(g,3,4.6,-1,M.red);return [summit,camp,marker];},
  'LOC-SOUTHERN-SPEEDWAY'(g){const track=speedwayTrack(g);const inner=cyl(g,0,0,0,4,4,.3,M.green,40,'Racecourse infield');inner.scale.z=.64;for(const z of [-5.7,5.7]){for(let row=0;row<4;row++)box(g,0,.25+row*.36,z+Math.sign(z)*row*.55,8,.4,.55,M.stone,'Grandstand tier');roof(g,0,2.7,z+Math.sign(z)*.7,8.8,2.3,.75,M.red);for(const x of [-3.7,3.7])for(const dz of [-.65,.65])cyl(g,x,.25,z+Math.sign(z)*.7+dz,.1,.14,2.45,M.timber,6);}const stand=g.children.find(o=>o.name==='Grandstand tier');for(const x of [-7.2,7.2])flag(g,x,.3,0,M.red);return [track,stand];},
  'LOC-LLC-STORM-CITY'(g){waterSurface(g,1,.22,3.9,10,6.2,'sheltered port','#356572');box(g,0,.3,-.7,13,.65,9,M.slate);let tower;for(const [x,z,h]of [[-4,-3,6],[0,-3.5,8],[4,-3,5.6],[-3,0,4],[2,0,4.7]]){const body=box(g,x,.95,z,2.7,h,2.5,M.light,'Mercantile tower');roof(g,x,h+.95,z,3.2,3,1.4,M.blue);for(let j=0;j<3;j++)box(g,x,2.1+j*1.2,z+1.27,1,.5,.04,M.glass);tower??=body;}const barriers=box(g,0,.9,4,13,1.35,.55,M.dark,'Storm barrier');for(let i=0;i<7;i++)box(g,-6+i*2,1.7,4,.3,1.05,.85,M.stone);steps(g,5,6.1,1.5,6,.16);return [tower,barriers];},
  'LOC-DK-HIGHLAND-STRONGHOLD'(g){box(g,0,0,0,13,.8,11,M.slate);const stronghold=hall(g,0,-3,8,4,4.6,M.stone,M.red);for(const x of [-5.4,5.4]){box(g,x,.8,0,1,3.3,8,M.stone);cyl(g,x,.8,3.8,1,1.2,4.9,M.slate,8);roof(g,x,5.7,3.8,2.6,2.6,1.5,M.red);}const court=highlandTrainingCourt(g);for(const x of [-2.5,2.5]){beam(g,[x,.9,1.1],[x,2.7,1.1],.15,M.wood);beam(g,[x-.6,2.3,1.1],[x+.6,2.3,1.1],.1,M.wood);}const road=steps(g,0,6.3,3.2,5,.17);for(const x of [-3.8,3.8])flag(g,x,.8,3.4,M.red);return [stronghold,court,road];},
  'LOC-TDS-CHILI-SHARED-MARCH'(g){box(g,0,0,0,13,.2,11,M.earth);const settlement=pavilion(g,-3.2,-1.5,4.7,3.8,3,M.deepGreen);pavilion(g,3.4,-2,4,3.4,2.8,M.red);waterSurface(g,0,.25,2.8,7.8,1.5,'watercourse crossing','#46766c');const crossing=box(g,0,.5,2.8,2.3,.3,4.3,M.wood,'Watercourse crossing');for(const x of [-1.1,1.1])box(g,x,.8,2.8,.12,.75,4.1,M.wood);const quarter=hall(g,-3.4,-4.1,4.6,2.8,2.8,M.wood,M.canvas);desk(g,3.3,.2,-.8,3.5);fence(g,4.7,3.2,3.5,3);for(const x of [-6,6])tree(g,x,-4.2,.7,M.paleGreen);crossingBankReeds(g);return [settlement,crossing,quarter];},
  'LOC-COMPACT-NEUTRAL-GROUNDS'(g){const field=cyl(g,0,0,0,6.5,6.8,.25,M.green,40,'Open ceremonial field');const pav=pavilion(g,0,-4.7,5,3,3.4,M.ivory);for(const x of [-4.5,4.5])flag(g,x,.25,-2,M.ivory);const roads=box(g,0,.26,4.7,2.3,.04,5.2,M.sand,'Arrival-road presentation');for(const sign of [-1,1]){const path=box(g,sign*4.3,.27,2.4,2,.03,5.3,M.sand);path.rotation.y=sign*.8;}for(const x of [-2.7,2.7])for(const z of [-.8,1.2])box(g,x,.25,z,1.5,.4,.5,M.stone);return [field,pav,roads];},
  'LOC-LEAGUE-ARCHIVE'(g){box(g,0,0,0,12,.45,10,M.stone);const halls=hall(g,0,-2.8,9,3.6,4.5,M.light,M.blue);for(const x of [-4.2,4.2])hall(g,x,.6,2.5,5.1,3.4,M.stone,M.blue);const vault=arch(g,0,.45,-.85,1.2,.45,.65,M.gold);box(g,0,.45,-1,2.25,2.1,.2,M.timber,'Ledger vault doors');const court=box(g,0,.46,2.1,5.8,.1,4.3,M.sand,'Courier court');for(const x of [-2.5,2.5]){cyl(g,x,.45,3.8,.17,.25,2.6,M.light,9);box(g,x,2.9,3.8,.6,.6,.6,M.gold);}desk(g,0,.55,1.1,2.6);ledger(g,0,1.8,1.1);steps(g,0,5.5,4,3,.17);return [halls,vault,court];}
 };
 for(const b of bindings){const define=definitions[b.id];if(!define)continue;
  const g=new THREE.Group();g.name=b.name||b.id;g.userData={locationId:b.id,canonStatus:b.canonStatus,visualAuthority:'CANDIDATE_NOT_APPROVED',currentStateClaim:false,sourceLandmarks:[...(b.landmarks||[])],sourcePath:'world/data/locations.json'};
  const landmarkObjects=define(g);for(let i=0;i<(b.landmarks||[]).length;i++){const o=landmarkObjects[i];if(!o)throw Error('MISSING_LANDMARK_GEOMETRY:'+b.id);o.userData={...o.userData,sourceLandmark:b.landmarks[i],visualAuthority:'CANDIDATE_NOT_APPROVED'};}
  g.updateMatrixWorld(true);const box3=new THREE.Box3().setFromObject(g);const radius=Math.max(...[box3.min.x,box3.max.x].flatMap(x=>[box3.min.z,box3.max.z].map(z=>Math.hypot(x,z))));
  const nearest=Math.min(...bindings.filter(p=>p.id!==b.id).map(p=>Math.hypot(p.anchor[0]-b.anchor[0],p.anchor[2]-b.anchor[2])));
  const scale=Math.min(1,nearest*.44/Math.max(radius,.001));if(!(scale>0&&Number.isFinite(scale)))throw Error('COINCIDENT_SITE_ANCHORS');
  g.scale.setScalar(scale);
  // Fit the illustrative level floor above this preview's terrain, not into it.
  // Only vertical presentation placement changes; source anchors/geography do not.
  const fitRadius=radius*scale*.65;
  const xs=[box3.min.x,(box3.min.x+box3.max.x)/2,box3.max.x],zs=[box3.min.z,(box3.min.z+box3.max.z)/2,box3.max.z];
  const sampled=[...[-fitRadius,0,fitRadius].flatMap(dx=>[-fitRadius,0,fitRadius].map(dz=>height(b.anchor[0]+dx,b.anchor[2]+dz))),...xs.flatMap(x=>zs.map(z=>height(b.anchor[0]+x*scale,b.anchor[2]+z*scale)))];
  if(!sampled.every(Number.isFinite))throw Error('INVALID_SITE_HEIGHT');
  const floor=Math.max(.65,...sampled)+.08;
  g.position.set(b.anchor[0],floor,b.anchor[2]);g.userData.presentationScale=scale;
  // Candidate retaining skirt meets the existing illustrative terrain; it does
  // not write elevations, shoreline or architectural canon back to the Atlas.
  const outline=[[xs[0],zs[0]],[xs[1],zs[0]],[xs[2],zs[0]],[xs[2],zs[1]],[xs[2],zs[2]],[xs[1],zs[2]],[xs[0],zs[2]],[xs[0],zs[1]]];
  const values=[],uv=[];
  for(let i=0;i<outline.length;i++){
   const a=outline[i],b2=outline[(i+1)%outline.length];
   const ah=(height(b.anchor[0]+a[0]*scale,b.anchor[2]+a[1]*scale)-.06-floor)/scale;
   const bh=(height(b.anchor[0]+b2[0]*scale,b.anchor[2]+b2[1]*scale)-.06-floor)/scale;
   values.push(a[0],.015,a[1],a[0],ah,a[1],b2[0],bh,b2[1],a[0],.015,a[1],b2[0],bh,b2[1],b2[0],.015,b2[1]);
   uv.push(0,1,0,0,1,0,0,1,1,0,1,1);
  }
  const skirt=new THREE.BufferGeometry();skirt.setAttribute('position',new THREE.Float32BufferAttribute(values,3));skirt.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));skirt.computeVertexNormals();
  mesh(g,skirt,M.slate,0,0,0,'Terrain-contact presentation skirt');root.add(g);
  locations.push({id:b.id,group:g,sourceLandmarks:[...(b.landmarks||[])],visualAuthority:'CANDIDATE_NOT_APPROVED',presentationRadius:radius*scale});
 }
 function tick(time,{paused=false}={}){if(disposed||paused)return;if(!Number.isFinite(time))throw Error('INVALID_ANIMATION_TIME');for(const w of water)w.material.uniforms.uTime.value=time;for(const m of motion)m.uniforms.uTime.value=time;}
 function dispose(){if(disposed)return;disposed=true;for(const g of geometries)g.dispose();for(const m of materials)m.dispose();for(const t of textures)t.dispose();root.clear();}
 return {root,locations,water,tick,dispose,worldMutationAllowed:false,weatherMutationAllowed:false,principalCharacters:[]};
}
