/** Native WebGL spatial study. All relief/building shapes are explicitly unapproved massing.
 * No libraries, network, live data, world writes or character generation. */
const TAU=Math.PI*2;
/** Secondary native-WebGL water uses the observer's ordinary clock, not weather. */
export function nextWaterPhase(previous,time,paused=false){
 if(!Number.isFinite(previous)||!Number.isFinite(time))throw Error('INVALID_WATER_PHASE');
 return paused?previous:time;
}
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const mix=(a,b,t)=>a+(b-a)*t;
const norm=v=>{const l=Math.hypot(...v)||1;return v.map(n=>n/l);};
const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const sub=(a,b)=>a.map((x,i)=>x-b[i]);
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
function multiply(a,b){const r=new Float32Array(16);for(let c=0;c<4;c++)for(let row=0;row<4;row++)for(let k=0;k<4;k++)r[c*4+row]+=a[k*4+row]*b[c*4+k];return r;}
function perspective(fov,aspect,near,far){const f=1/Math.tan(fov/2),r=new Float32Array(16);r[0]=f/aspect;r[5]=f;r[10]=(far+near)/(near-far);r[11]=-1;r[14]=2*far*near/(near-far);return r;}
function lookAt(eye,target,up=[0,1,0]){const z=norm(sub(eye,target)),x=norm(cross(up,z)),y=cross(z,x);return new Float32Array([x[0],y[0],z[0],0,x[1],y[1],z[1],0,x[2],y[2],z[2],0,-dot(x,eye),-dot(y,eye),-dot(z,eye),1]);}
function ortho(l,r,b,t,n,f){return new Float32Array([2/(r-l),0,0,0,0,2/(t-b),0,0,0,0,-2/(f-n),0,-(r+l)/(r-l),-(t+b)/(t-b),-(f+n)/(f-n),1]);}
function rng(seed){return ()=>{seed|=0;seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return ((t^t>>>14)>>>0)/4294967296;};}
const hash=(x,y)=>{const v=Math.sin(x*127.1+y*311.7)*43758.5453;return v-Math.floor(v);};
/** Low-cost illustrative movement of existing fallback-water highlights, never geography. */
export function waterSheenDrift(index,ordinaryTime){
 if(!Number.isInteger(index)||index<0||!Number.isFinite(ordinaryTime))throw Error('INVALID_WATER_SHEEN_PHASE');
 return Math.sin(ordinaryTime*.75+hash(index,13)*TAU)*.65;
}
/** Canvas compatibility uses the same bounded ordinary-time water displacement as
 * the existing native WebGL vertex shader; no weather or source inputs apply. */
export function canvasWaterDisplacement(x,z,ordinaryTime){
 if(![x,z,ordinaryTime].every(Number.isFinite))throw Error('INVALID_CANVAS_WATER_POSITION');
 return Math.sin(x*.21+ordinaryTime*.55)*.11+Math.sin(z*.31+ordinaryTime*.34)*.07;
}
function noise(x,y){const a=Math.floor(x),b=Math.floor(y),tx=x-a,ty=y-b,s=tx*tx*(3-2*tx),t=ty*ty*(3-2*ty);return mix(mix(hash(a,b),hash(a+1,b),s),mix(hash(a,b+1),hash(a+1,b+1),s),t);}
const fbm=(x,z)=>noise(x,z)*.58+noise(x*2.03,z*2.03)*.28+noise(x*4.13,z*4.13)*.14;
const gauss=(x,z,cx,cz,sx,sz)=>Math.exp(-((x-cx)**2/(sx*sx)+(z-cz)**2/(sz*sz)));
function rawHeight(x,z){
 const north=-z;
 let h=2.4+3.4*fbm(x*.055,z*.055);
 // Physical zone types/bounds guide candidate relief, not surveyed elevation.
 h+=30*gauss(x,z,-16,-72,47,17)*(0.35+fbm(x*.14,z*.14));
 h+=22*gauss(x,z,14,-80,20,13)*(0.3+fbm(x*.19,z*.19));
 h+=10*gauss(x,z,15,-42,58,20)*fbm(x*.085,z*.085);
 h+=9*gauss(x,z,62,-20,22,56)*(0.3+fbm(x*.1,z*.1));
 h+=6*gauss(x,z,-62,0,25,55);
 // Illustrative river corridor; its exact course is not canonical.
 const rx=7+7*Math.sin(z*.034)+3*Math.sin(z*.091),rd=Math.abs(x-rx);
 if(z>-54){const bed=Math.exp(-(rd*rd)/24);h=mix(h,-1.4,Math.min(1,bed*1.6));}
 if(z>32&&x>-47&&x<48)h-=1.6*noise(x*.16,z*.12);
 const edge=1-Math.pow(Math.abs(x+2)/107,2.65)-Math.pow(Math.abs(z+3)/108,2.65);
 h*=clamp(edge*5,0,1);h-=Math.max(0,.07-edge)*65;
 if(x>66&&z>46)h-=((x-66)+(z-46))*.13;
 return h;
}
function terrainColor(x,y,z){
 const wet=clamp((z-20)/35,0,1),west=clamp((-x-15)/45,0,1),east=clamp((x-20)/40,0,1);
 let c=[.36,.48,.29];c=c.map((v,i)=>mix(v,[.49,.48,.29][i],west*.8));c=c.map((v,i)=>mix(v,[.20,.37,.29][i],east*.8));c=c.map((v,i)=>mix(v,[.26,.41,.32][i],wet*.65));
 const v=.94+fbm(x*.18,z*.18)*.14;c=c.map(q=>q*v);
 if(y<1.1)c=c.map((v,i)=>mix(v,[.58,.55,.37][i],clamp((1.1-y)/1.5,0,1)));
 if(y>14)c=c.map((v,i)=>mix(v,[.50,.52,.46][i],clamp((y-14)/12,0,1)));
 if(y>22)c=c.map((v,i)=>mix(v,[.91,.92,.86][i],clamp((y-22)/8,0,1)));
 return c;
}
class MeshBuilder{
 constructor(){this.values=[];}
 tri(a,b,c,color,normal=null){let n=normal||norm(cross(sub(b,a),sub(c,a)));for(const p of [a,b,c])this.values.push(...p,...n,...color);}
 triSmooth(a,b,c,colorA,na,nb,nc,colorB=colorA,colorC=colorA){for(const [p,n,color] of [[a,na,colorA],[b,nb,colorB],[c,nc,colorC]])this.values.push(...p,...n,...color);}
 quad(a,b,c,d,color){this.tri(a,b,c,color);this.tri(a,c,d,color);}
 box(x,y,z,w,h,d,color){const a=[x-w/2,y,z-d/2],b=[x+w/2,y,z-d/2],c=[x+w/2,y,z+d/2],d0=[x-w/2,y,z+d/2];const A=[a[0],y+h,a[2]],B=[b[0],y+h,b[2]],C=[c[0],y+h,c[2]],D=[d0[0],y+h,d0[2]];this.quad(A,D,C,B,color);this.quad(a,A,B,b,color);this.quad(b,B,C,c,color);this.quad(c,C,D,d0,color);this.quad(d0,D,A,a,color);}
 cone(x,y,z,r,h,color,sides=6){for(let i=0;i<sides;i++){const a=i*TAU/sides,b=(i+1)*TAU/sides;this.tri([x+Math.cos(a)*r,y,z+Math.sin(a)*r],[x,y+h,z],[x+Math.cos(b)*r,y,z+Math.sin(b)*r],color);}}
 roof(x,y,z,w,h,d,col){const a=[x-w/2,y,z-d/2],b=[x+w/2,y,z-d/2],c=[x+w/2,y,z+d/2],dd=[x-w/2,y,z+d/2],e=[x,y+h,z-d/2],f=[x,y+h,z+d/2];this.quad(a,dd,f,e,col);this.quad(e,f,c,b,col);this.tri(a,e,b,col);this.tri(dd,c,f,col);}
}
const VS=`attribute vec3 aPosition;attribute vec3 aNormal;attribute vec3 aColor;uniform mat4 uVP;uniform mat4 uLightVP;uniform float uTime;uniform float uWater;varying vec3 vColor;varying vec3 vNormal;varying vec3 vWorld;varying vec4 vShadow;void main(){vec3 p=aPosition;if(uWater>.5)p.y+=sin(p.x*.21+uTime*.55)*.11+sin(p.z*.31+uTime*.34)*.07;vWorld=p;vNormal=aNormal;vColor=aColor;vShadow=uLightVP*vec4(p,1.);gl_Position=uVP*vec4(p,1.);}`;
const FS=`precision highp float;varying vec3 vColor;varying vec3 vNormal;varying vec3 vWorld;varying vec4 vShadow;uniform sampler2D uShadow;uniform vec3 uEye;uniform vec3 uSun;uniform vec3 uSky;uniform float uStrength;uniform float uTime;uniform float uWater;uniform float uStorm;uniform float uNight;float unpack(vec4 v){return dot(v,vec4(1./(256.*256.*256.),1./(256.*256.),1./256.,1.));}float shadow(){vec3 sc=vShadow.xyz/vShadow.w*.5+.5;if(sc.x<0.||sc.y<0.||sc.x>1.||sc.y>1.)return 1.;float s=0.;for(int x=-1;x<=1;x++)for(int y=-1;y<=1;y++){float depth=unpack(texture2D(uShadow,sc.xy+vec2(float(x),float(y))/1536.));s+=sc.z-.0016>depth?.58:1.;}return s/9.;}void main(){vec3 n=normalize(vNormal);if(uWater>.5){float slopeX=.11*.21*cos(vWorld.x*.21+uTime*.55);float slopeZ=.07*.31*cos(vWorld.z*.31+uTime*.34);n=normalize(vec3(-slopeX,1.,-slopeZ));}float dif=max(0.,dot(n,normalize(uSun)));float shade=shadow();vec3 color=vColor*(.42+dif*.7*shade)*uStrength;float stormMask=0.;if(uStorm>0.5){stormMask=smoothstep(26.,46.,vWorld.x);if(uStorm>1.5)stormMask=max(stormMask,smoothstep(34.,56.,vWorld.z));if(uStorm>2.5)stormMask=max(stormMask,(1.-smoothstep(38.,58.,abs(vWorld.x)))*(1.-smoothstep(20.,40.,abs(vWorld.z))));}color*=1.-stormMask*.29;if(uWater>.5){vec3 view=normalize(uEye-vWorld);float fres=pow(1.-max(0.,dot(view,n)),3.);color=mix(color,uSky*.8,.12+fres*.34);float sparkle=pow(max(0.,dot(reflect(-normalize(uSun),n),view)),86.);color+=vec3(.9,.73,.42)*sparkle*.55*uStrength;}else{color+=vec3(.07,.05,.018)*dif*uStrength;}float dist=length(vWorld-uEye);float fog=1.-exp(-dist*.0023);color=mix(color,uSky,clamp(fog,0.,.55));color=pow(max(color,vec3(0.)),vec3(.86));gl_FragColor=vec4(color,1.);}`;
const SV=`attribute vec3 aPosition;uniform mat4 uVP;void main(){gl_Position=uVP*vec4(aPosition,1.);}`;
const SF=`precision highp float;void main(){vec4 enc=fract(gl_FragCoord.z*vec4(256.*256.*256.,256.*256.,256.,1.));enc-=enc.xxyz*vec4(0.,1./256.,1./256.,1./256.);gl_FragColor=enc;}`;
function program(gl,v,f){const build=(type,s)=>{const x=gl.createShader(type);gl.shaderSource(x,s);gl.compileShader(x);if(!gl.getShaderParameter(x,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(x));return x;};const p=gl.createProgram();gl.attachShader(p,build(gl.VERTEX_SHADER,v));gl.attachShader(p,build(gl.FRAGMENT_SHADER,f));gl.linkProgram(p);if(!gl.getProgramParameter(p,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(p));return p;}

export function buildWorldGeometry(bindings,grid=200,treeCount=4300,{skipLandmarkIds=[]}={}){
 const rand=rng(20261115),mesh=new MeshBuilder(),water=new MeshBuilder();
 function height(x,z){let h=rawHeight(x,z);for(const p of bindings){const d=Math.hypot(x-p.anchor[0],z-p.anchor[2]);if(d<3.2)h=mix(h,Math.max(2.6,rawHeight(p.anchor[0],p.anchor[2])),Math.pow(1-d/3.2,.6));}return h;}
 const N=grid,step=220/N,terrainVertices=new Map();
 // Shared vertex samples preserve the original height field and triangle footprint,
 // but interpolate terrain normals smoothly rather than flat-shading each cell.
 function terrainVertex(ix,iz){
  const key=ix*(N+1)+iz;
  if(terrainVertices.has(key))return terrainVertices.get(key);
  const x=-110+ix*step,z=-110+iz*step,y=height(x,z);
  const normal=norm([height(x-.5,z)-height(x+.5,z),1,height(x,z-.5)-height(x,z+.5)]);
  const vertex={position:[x,y,z],normal,color:terrainColor(x,y,z)};
  terrainVertices.set(key,vertex);
  return vertex;
 }
 for(let ix=0;ix<N;ix++)for(let iz=0;iz<N;iz++){
  const a=terrainVertex(ix,iz),b=terrainVertex(ix+1,iz),
   c=terrainVertex(ix+1,iz+1),d=terrainVertex(ix,iz+1);
  mesh.triSmooth(a.position,c.position,b.position,a.color,a.normal,c.normal,b.normal,c.color,b.color);
  mesh.triSmooth(a.position,d.position,c.position,a.color,a.normal,d.normal,c.normal,d.color,c.color);
 }
 const stone=[.63,.60,.49],roof=[.23,.27,.25],gold=[.57,.43,.22],chalk=[.82,.77,.61];
 function house(x,y,z,w=2,h=1.6,d=2,color=stone){mesh.box(x,y,z,w,h,d,color);mesh.roof(x,y+h,z,w*1.1,h*.65,d*1.1,roof);}
 function tower(x,y,z,h=4){mesh.box(x,y,z,1.2,h,1.2,stone);for(let i=0;i<4;i++)mesh.box(x+(i%2-.5)*.85,y+h,z+(Math.floor(i/2)-.5)*.85,.32,.35,.32,chalk);}
 for(const p of bindings){const [x,,z]=p.anchor,y=height(x,z);p.renderAnchor=[x,y+1.3,z];const id=p.id;if(skipLandmarkIds.includes(id))continue;
  if(/MOUNTAIN-BASE|STRONGHOLD|KEEP|RUINS/.test(id)){mesh.box(x,y,z,4.5,.6,3.8,stone);mesh.box(x,y+.6,z,2.6,3.4,2.2,id.includes('KEEP')?[.27,.3,.3]:stone);for(const [dx,dz]of[[-2,-1.4],[2,-1.4],[-2,1.4],[2,1.4]])tower(x+dx,y,z+dz,id.includes('RUINS')?1.7:4.1);if(!id.includes('RUINS'))mesh.roof(x,y+4,z,3,1.4,2.7,roof);}
  else if(id.includes('WATERFALL')){for(let i=0;i<4;i++)mesh.box(x,y+i*.6,z,5-i,.6,4-i*.65,stone);for(let j=-1;j<=1;j++)mesh.box(x+j*1.1,y+2.4,z,.3,1.6,.3,chalk);mesh.roof(x,y+4,z,3.6,1.2,2.3,[.25,.32,.29]);}
  else if(id.includes('JACKSON')){house(x,y,z,5,2,2.8,chalk);house(x-3,y,z,1.8,1.4,2.2,chalk);house(x+3,y,z,1.8,1.4,2.2,chalk);for(let j=0;j<3;j++){mesh.box(x+j*1.6-1.5,y+.08,z+4,1.3,.04,2.2,[.32,.47,.25]);mesh.box(x+j*1.6-1.5,y,z+4,.07,1.2,.07,stone);mesh.tri([x+j*1.6-1.5,y+1.2,z+4],[x+j*1.6-.9,y+1.05,z+4],[x+j*1.6-1.5,y+.92,z+4],[.68,.38,.23]);}}
  else if(id.includes('BRIDGE')){mesh.box(x,y,z,5,.6,1.3,stone);mesh.box(x,y+.6,z-.7,5,.4,.18,chalk);mesh.box(x,y+.6,z+.7,5,.4,.18,chalk);}
  else if(id.includes('SPEEDWAY')||id.includes('BOWL')||id.includes('GROUNDS')){for(let i=0;i<28;i++){const t=i/28*TAU;mesh.box(x+Math.cos(t)*3,y,z+Math.sin(t)*2,.65,id.includes('BOWL')?1.6:.5,.6,stone);}house(x-3.5,y,z,1.2,1.8,2,stone);}
  else if(/CAMP|SWAMP|STABLE|MARCH/.test(id)){for(let i=0;i<4;i++)house(x+(i%2)*2.4-1.2,y,z+Math.floor(i/2)*2.4-1.2,1.8,1.2,2.1,[.43,.36,.25]);}
  else{house(x,y,z,3.5,2.5,2.7,chalk);for(let i=0;i<3;i++)house(x+(i-1)*1.7,y,z+2.8,1.2,1.5,1.3,stone);if(/ARCHIVE|CITY|BOARDROOM/.test(id))tower(x+1.6,y,z-1.8,4.8);}
 }
 // Deterministic generic vegetation, not principal characters or authored settlements.
 for(let i=0;i<treeCount;i++){const x=rand()*197-98,z=rand()*194-98,y=height(x,z);if(y<1.8||y>20||bindings.some(p=>Math.hypot(x-p.anchor[0],z-p.anchor[2])<(skipLandmarkIds.includes(p.id)?12:5)))continue;
  const density=x>30?.88:z>26?.58:x<-35?.17:.48;if(rand()>density||noise(x*.035,z*.035)<.31)continue;
  const h=(1.2+rand()*2.3)*(z<-35?1.1:.85),r=h*.35;
  mesh.box(x,y,z,.17,h*.43,.17,[.24,.21,.14]);
  const c=x<-25?[.28+rand()*.07,.31+rand()*.08,.17]:[.10+rand()*.07,.24+rand()*.10,.18+rand()*.06];
  mesh.cone(x,y+h*.15,z,r,h*.85,c,5);mesh.cone(x,y+h*.42,z,r*.78,h*.72,c.map(v=>v*1.06),5);
 }
 for(let x=-320;x<320;x+=16)for(let z=-320;z<320;z+=16)water.quad([x,-.4,z],[x,-.4,z+16],[x+16,-.4,z+16],[x+16,-.4,z],[.115,.29,.31]);

return {mesh,water,height};
}
export function createWorldRenderer(canvas,bindings,{onContextLost=()=>{}}={}){
 const gl=canvas.getContext('webgl',{antialias:true,alpha:false,preserveDrawingBuffer:true});if(!gl)return createSoftwareRenderer(canvas,bindings,{onContextLost});
 const {mesh,water,height}=buildWorldGeometry(bindings);
 const P=program(gl,VS,FS),S=program(gl,SV,SF);
 const upload=m=>{const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(m.values),gl.STATIC_DRAW);return {buffer:b,count:m.values.length/9};};
 const terrain=upload(mesh),ocean=upload(water);mesh.values=null;water.values=null;
 const attrs=p=>['aPosition','aNormal','aColor'].map(n=>gl.getAttribLocation(p,n));const loc=Object.fromEntries(['uVP','uLightVP','uEye','uSun','uSky','uStrength','uTime','uWater','uStorm','uNight','uShadow'].map(n=>[n,gl.getUniformLocation(P,n)]));
 const shadowTex=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,shadowTex);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,1536,1536,0,gl.RGBA,gl.UNSIGNED_BYTE,null);for(const [a,b]of[[gl.TEXTURE_MIN_FILTER,gl.NEAREST],[gl.TEXTURE_MAG_FILTER,gl.NEAREST],[gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE],[gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE]])gl.texParameteri(gl.TEXTURE_2D,a,b);
 const depth=gl.createRenderbuffer();gl.bindRenderbuffer(gl.RENDERBUFFER,depth);gl.renderbufferStorage(gl.RENDERBUFFER,gl.DEPTH_COMPONENT16,1536,1536);const fb=gl.createFramebuffer();gl.bindFramebuffer(gl.FRAMEBUFFER,fb);gl.framebufferTexture2D(gl.FRAMEBUFFER,gl.COLOR_ATTACHMENT0,gl.TEXTURE_2D,shadowTex,0);gl.framebufferRenderbuffer(gl.FRAMEBUFFER,gl.DEPTH_ATTACHMENT,gl.RENDERBUFFER,depth);
 const lightVP=multiply(ortho(-165,165,-165,165,1,600),lookAt([-150,230,90],[0,0,0]));
 function bind(p,m){gl.bindBuffer(gl.ARRAY_BUFFER,m.buffer);attrs(p).forEach((a,i)=>{if(a>=0){gl.enableVertexAttribArray(a);gl.vertexAttribPointer(a,3,gl.FLOAT,false,36,i*12);}});}
 gl.enable(gl.DEPTH_TEST);gl.disable(gl.CULL_FACE);gl.viewport(0,0,1536,1536);gl.clearColor(1,1,1,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.useProgram(S);gl.uniformMatrix4fv(gl.getUniformLocation(S,'uVP'),false,lightVP);bind(S,terrain);gl.drawArrays(gl.TRIANGLES,0,terrain.count);gl.bindFramebuffer(gl.FRAMEBUFFER,null);
 let vp,eye,disposed=false,waterTime=0;const contextLost=e=>{e.preventDefault();onContextLost();};canvas.addEventListener('webglcontextlost',contextLost);
 function render(c,time,{strength=1,storm=0,paused=false}={}){if(disposed||gl.isContextLost())return;waterTime=nextWaterPhase(waterTime,time,paused);const ratio=Math.min(devicePixelRatio||1,1.6),w=Math.floor(canvas.clientWidth*ratio),h=Math.floor(canvas.clientHeight*ratio);if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;}gl.viewport(0,0,w,h);
  const aspect=w/h,fit=Math.max(1,1.25/aspect),distance=c.distance*(c.distance>100?fit:Math.min(fit,1.25)),t=c.target;eye=[t[0]+Math.sin(c.yaw)*Math.cos(c.pitch)*distance,t[1]+Math.sin(c.pitch)*distance,t[2]+Math.cos(c.yaw)*Math.cos(c.pitch)*distance];vp=multiply(perspective(.72,w/h,.2,1900),lookAt(eye,t));
  const sky=[.63,.72,.72].map(v=>v*(.58+.42*strength));gl.clearColor(...sky,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.useProgram(P);gl.uniformMatrix4fv(loc.uVP,false,vp);gl.uniformMatrix4fv(loc.uLightVP,false,lightVP);gl.uniform3fv(loc.uEye,eye);gl.uniform3fv(loc.uSun,[-.6,.9,.36]);gl.uniform3fv(loc.uSky,sky);gl.uniform1f(loc.uStrength,strength);gl.uniform1f(loc.uTime,waterTime);gl.uniform1f(loc.uStorm,storm);gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,shadowTex);gl.uniform1i(loc.uShadow,0);gl.uniform1f(loc.uWater,0);bind(P,terrain);gl.drawArrays(gl.TRIANGLES,0,terrain.count);gl.uniform1f(loc.uWater,1);bind(P,ocean);gl.drawArrays(gl.TRIANGLES,0,ocean.count);
 }
 function project(p){if(!vp)return null;const v=[...p,1],o=[0,0,0,0];for(let r=0;r<4;r++)for(let c=0;c<4;c++)o[r]+=vp[c*4+r]*v[c];if(o[3]<=0)return null;return {x:(o[0]/o[3]*.5+.5)*canvas.clientWidth,y:(-.5*o[1]/o[3]+.5)*canvas.clientHeight,depth:o[2]/o[3]};}
 function pick(x,y){let best=null,dist=30;for(const p of bindings){const q=project(p.renderAnchor);if(!q||q.depth>1)continue;const d=Math.hypot(q.x-x,q.y-y);if(d<dist){dist=d;best=p;}}return best;}
 return {render,project,pick,height,stats:{vertices:terrain.count,locations:bindings.length,renderer:'native-webgl',geometry:'PROCEDURAL_MASSING_NOT_APPROVED_ART'},loseContext(){gl.getExtension('WEBGL_lose_context')?.loseContext();},dispose(){disposed=true;canvas.removeEventListener('webglcontextlost',contextLost);gl.deleteBuffer(terrain.buffer);gl.deleteBuffer(ocean.buffer);gl.deleteTexture(shadowTex);gl.deleteRenderbuffer(depth);gl.deleteFramebuffer(fb);gl.deleteProgram(P);gl.deleteProgram(S);}};
}

/** Canvas fallback uses the same source-bound 3D geometry/camera, with painter ordering.
 * It is a deliberately lower-detail renderer, not a substitute canon or a blank screen. */
function createSoftwareRenderer(canvas,bindings,{onContextLost}){
 const ctx=canvas.getContext('2d',{alpha:false});if(!ctx)throw Error('CANVAS_UNAVAILABLE');
 const {mesh,water,height}=buildWorldGeometry(bindings,100,7000),values=mesh.values,triangles=[],waterTriangles=[];
 for(let i=0;i<values.length;i+=27){const pts=[values.slice(i,i+3),values.slice(i+9,i+12),values.slice(i+18,i+21)];if(pts.every(p=>p[1]<-.35))continue;const normal=values.slice(i+3,i+6),col=values.slice(i+6,i+9);const sun=norm([-.6,.9,.36]);const diffuse=Math.max(0,dot(normal,sun));let shade=.72+diffuse*.43;const center=pts[0].map((_,j)=>(pts[0][j]+pts[1][j]+pts[2][j])/3);for(let d=4;d<24;d+=5){if(height(center[0]+sun[0]*d,center[2]+sun[2]*d)>center[1]+sun[1]*d+1){shade*=.74;break;}}triangles.push({pts,col:col.map(v=>v*shade),center});}
 // Reuse the EXISTING water grid, not a new shoreline, river or place.
 // The painter projects bounded moving vertices each 1/8 second fallback frame.
 for(let i=0;i<water.values.length;i+=27){
  const pts=[water.values.slice(i,i+3),water.values.slice(i+9,i+12),water.values.slice(i+18,i+21)];
  const center=pts[0].map((_,j)=>(pts[0][j]+pts[1][j]+pts[2][j])/3);
  waterTriangles.push({pts,center,water:true});
 }
 mesh.values=null;water.values=null;let eye,view,vp,width=0,heightPx=0,signature='',lastWater=0,disposed=false,drawCount=0;
 const project=p=>{if(!vp)return null;const v=[...p,1],o=[0,0,0,0];for(let r=0;r<4;r++)for(let c=0;c<4;c++)o[r]+=vp[c*4+r]*v[c];if(o[3]<=.1)return null;return {x:(o[0]/o[3]*.5+.5)*width,y:(-.5*o[1]/o[3]+.5)*heightPx,depth:o[2]/o[3],distance:o[3]};};
 function render(c,time,{strength=1,storm=0,paused=false}={}){if(disposed)return;
   lastWater=nextWaterPhase(lastWater,time,paused);
   // At most eight fallback redraws/sec for ordinary water; explicit pause holds exact pixels.
   const waterFrame=Math.floor(lastWater*8)/8;
   const w=canvas.clientWidth,h=canvas.clientHeight;const current=JSON.stringify([w,h,c.target.map(x=>Math.round(x*20)/20),Math.round(c.distance*20),Math.round(c.yaw*500),Math.round(c.pitch*500),Math.round(strength*100),storm,waterFrame]);if(signature===current)return;signature=current;drawCount++;
  width=w;heightPx=h;const ratio=Math.min(devicePixelRatio||1,1.5);if(canvas.width!==Math.floor(w*ratio)||canvas.height!==Math.floor(h*ratio)){canvas.width=w*ratio;canvas.height=h*ratio;}ctx.setTransform(ratio,0,0,ratio,0,0);
  const aspect=w/h,fit=Math.max(1,1.25/aspect),distance=c.distance*(c.distance>100?fit:Math.min(fit,1.25)),t=c.target;eye=[t[0]+Math.sin(c.yaw)*Math.cos(c.pitch)*distance,t[1]+Math.sin(c.pitch)*distance,t[2]+Math.cos(c.yaw)*Math.cos(c.pitch)*distance];view=lookAt(eye,t);vp=multiply(perspective(.72,aspect,.2,1900),view);
  const grad=ctx.createLinearGradient(0,0,0,h);grad.addColorStop(0,`rgb(${Math.round(126*strength+20)},${Math.round(153*strength+20)},${Math.round(155*strength+20)})`);grad.addColorStop(.5,`rgb(${Math.round(48*strength+20)},${Math.round(103*strength+15)},${Math.round(109*strength+15)})`);grad.addColorStop(1,`rgb(${Math.round(22*strength+14)},${Math.round(65*strength+14)},${Math.round(72*strength+14)})`);ctx.fillStyle=grad;ctx.fillRect(0,0,w,h);
  const ordered=[];for(const tri of triangles){const p=tri.pts.map(project);if(p.some(x=>!x))continue;if(p.every(x=>x.x<0)||p.every(x=>x.x>w)||p.every(x=>x.y<0)||p.every(x=>x.y>h))continue;ordered.push({tri,p,d:p.reduce((s,x)=>s+x.distance,0)/3});}
  for(const tri of waterTriangles){
   const moving=tri.pts.map(p=>[p[0],p[1]+canvasWaterDisplacement(p[0],p[2],waterFrame),p[2]]);
   const p=moving.map(project);if(p.some(x=>!x))continue;
   if(p.every(x=>x.x<0)||p.every(x=>x.x>w)||p.every(x=>x.y<0)||p.every(x=>x.y>h))continue;
   ordered.push({tri,p,d:p.reduce((s,x)=>s+x.distance,0)/3});
  }
  ordered.sort((a,b)=>b.d-a.d);
  for(const {tri,p,d}of ordered){const fog=clamp((d-distance*.65)/400,0,.28);let dark=1;if(storm){if(tri.center[0]>36)dark=.65;if(storm>=2&&tri.center[2]>40)dark=.67;if(storm>=3&&Math.abs(tri.center[0])<44&&Math.abs(tri.center[2])<32)dark=.7;}const col=(tri.water?(()=>{
   const x=tri.center[0],z=tri.center[2];
   const slopeX=.11*.21*Math.cos(x*.21+waterFrame*.55),slopeZ=.07*.31*Math.cos(z*.31+waterFrame*.34);
   const n=norm([-slopeX,1,-slopeZ]),sun=norm([-.6,.9,.36]);
   const diffuse=Math.max(0,dot(n,sun));
   const view=norm(sub(eye,[x,-.4,z])),fresnel=Math.pow(1-Math.max(0,dot(view,n)),3);
   return [.115,.29,.31].map((base,i)=>Math.round(clamp(Math.pow(mix(base*(.72+diffuse*.4)*(.7+.3*strength)*dark,[.59,.69,.64][i],.08+fresnel*.28+fog),.84)*255,0,255)));
  })():tri.col.map((v,i)=>Math.round(clamp(Math.pow(mix(v*(.7+.3*strength)*dark,[.59,.69,.64][i],fog),.84)*255,0,255))));ctx.fillStyle=`rgb(${col.join(',')})`;ctx.strokeStyle=ctx.fillStyle;ctx.lineWidth=.55;ctx.beginPath();ctx.moveTo(p[0].x,p[0].y);ctx.lineTo(p[1].x,p[1].y);ctx.lineTo(p[2].x,p[2].y);ctx.closePath();ctx.fill();ctx.stroke();}
  // Restrained water sheen: illustrative non-weather surface lighting.
  // Gentle time-dependent surface glints on existing river samples. No new water geometry.
   ctx.strokeStyle=`rgba(216,219,190,${.08*strength})`;ctx.lineWidth=.6;
   for(let i=0;i<110;i++){const bankX=(hash(i,7)*250)-125,z=hash(i,11)*170+35;if(height(bankX,z)>-.3)continue;const x=bankX+waterSheenDrift(i,waterFrame);const a=project([x,-.3,z]),b=project([x+1+hash(i,1)*2,-.3,z]);if(a&&b){ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();}}
 }
 function pick(x,y){let best=null,dist=30;for(const p of bindings){const q=project(p.renderAnchor);if(!q||q.depth>1)continue;const d=Math.hypot(q.x-x,q.y-y);if(d<dist){dist=d;best=p;}}return best;}
 return {render,project,pick,height,stats:{triangles:triangles.length,waterTriangles:waterTriangles.length,locations:bindings.length,renderer:'canvas2d-spatial-fallback',geometry:'PROCEDURAL_MASSING_NOT_APPROVED_ART'},loseContext(){onContextLost();},dispose(){disposed=true;}};
}
