/** Mature rendering adapter inside the existing observer host.
 * Pinned THREE is injected, as are source-bound geometry and regional assets.
 * Does not determine world state, weather outcomes, location identity or publication.
 */
export function rendererQuality(width,dpr=1){
 if(!Number.isFinite(width)||width<=0||!Number.isFinite(dpr)||dpr<=0)throw Error('INVALID_RENDER_SIZE');
 return {pixelRatio:Math.min(dpr,width<700?1.25:1.5),shadowSize:width<700?1024:2048};
}
/** Shadows are cast by static terrain and architecture, not animated water or reeds.
 * Reuse their depth map while only water/time/weather lighting changes.
 * The directional sun tracks the horizontal Atlas target with fixed elevation.
 */
export function shadowCoverage(c){
 if(!c||!Array.isArray(c.target)||![c.target[0],c.target[2],c.distance].every(Number.isFinite))throw Error('INVALID_SHADOW_COVERAGE');
 const span=Math.min(140,Math.max(20,c.distance*.65));
 return {span,key:JSON.stringify([c.target[0],c.target[2],span])};
}
/** Read-only camera framing from the candidate's real bounds. */
export function siteViewFrames(THREE,locations){
 const result={};for(const l of locations){l.group.updateMatrixWorld(true);const bounds=new THREE.Box3().setFromObject(l.group),sphere=bounds.getBoundingSphere(new THREE.Sphere());if(!Number.isFinite(sphere.radius)||sphere.radius<=0)continue;result[l.id]={target:[l.group.position.x,sphere.center.y,l.group.position.z],distance:Math.max(12,Math.min(80,sphere.radius*3.0+2))};}return result;
}
/** View-responsive optics for the already animated base water plane.
 * The original wave heights and water boundary stay fixed; analytic slopes
 * make light respond to the same physical displacement on ordinary water time.
 * This is candidate rendering only, never an Atlas hydrology claim.
 */
export function createBaseWaterMaterial(THREE){
 return new THREE.ShaderMaterial({uniforms:{uTime:{value:0},uStrength:{value:1},uStorm:{value:0}},
  vertexShader:`uniform float uTime;
   varying vec3 vP;varying vec3 vWaveNormal;
   void main(){
    vec3 p=position;
    float phaseX=p.x*.17+uTime*.6;
    float phaseY=p.y*.21-uTime*.39;
    p.z+=sin(phaseX)*.07+sin(phaseY)*.05;
    // Derivatives of the displaced local plane; not an invented water current.
    vec3 localNormal=normalize(vec3(-.07*.17*cos(phaseX),-.05*.21*cos(phaseY),1.));
    vWaveNormal=normalize(mat3(modelMatrix)*localNormal);
    vP=(modelMatrix*vec4(p,1.)).xyz;
    gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.);
   }`,
  fragmentShader:`uniform float uTime;uniform float uStrength;uniform float uStorm;
   varying vec3 vP;varying vec3 vWaveNormal;
   void main(){
    float w=sin(vP.x*1.7+sin(vP.z*.7)+uTime*.65)*sin(vP.z*2.1-uTime*.41);
    float s=pow(max(w,0.),9.);
    vec3 col=mix(vec3(.065,.24,.235),vec3(.18,.42,.38),.5+.5*sin(vP.x*.014+vP.z*.012));
    col+=vec3(.23,.3,.24)*s*.45;
    // Small optical normals add fine water sheen without extra geometry/draws.
    vec3 n=normalize(vWaveNormal+vec3(.021*cos(vP.x*.71+uTime*.49),0.,.024*sin(vP.z*.63-uTime*.38)));
    vec3 viewDir=normalize(cameraPosition-vP);
    vec3 sunDir=normalize(vec3(-.6,.9,.36));
    float fresnel=pow(1.-max(dot(n,viewDir),0.),3.);
    float glint=pow(max(dot(reflect(-sunDir,n),viewDir),0.),64.);
    col=mix(col,vec3(.36,.47,.47),(.10+.27*fresnel));
    col+=vec3(.38,.34,.21)*glint*.35;
    col*=.45+.55*uStrength;
    gl_FragColor=vec4(col,1.);
    #include <tonemapping_fragment>
    #include <colorspace_fragment>
   }`,side:THREE.DoubleSide});
}
export function createThreeWorldRenderer(THREE,canvas,bindings,{buildWorldGeometry,buildRegionalAssets,buildAtlasSiteAssets=null,atlasSiteIds=[],onContextLost=()=>{}}={}){
 if(!THREE||typeof buildWorldGeometry!=='function'||typeof buildRegionalAssets!=='function')throw Error('RENDERER_DEPENDENCY_REQUIRED');
 const context=canvas.getContext('webgl2',{alpha:false,antialias:true,powerPreference:'low-power'});
 if(!context)throw Error('WEBGL2_UNAVAILABLE');
 const renderer=new THREE.WebGLRenderer({canvas,context,antialias:true,alpha:false});
 renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.1;
 renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.shadowMap.autoUpdate=false;
 const scene=new THREE.Scene();scene.background=new THREE.Color('#bed1cf');scene.fog=new THREE.FogExp2('#bed1cf',.0018);
 const camera=new THREE.PerspectiveCamera(41.25,1,.2,1900);
 const hemisphere=new THREE.HemisphereLight('#e3ecdf','#657256',1.4);scene.add(hemisphere);
 const sun=new THREE.DirectionalLight('#ffe7b3',2.5);sun.position.set(-95,150,60);sun.castShadow=true;
 const quality=rendererQuality(canvas.clientWidth||1280,globalThis.devicePixelRatio||1);
 sun.shadow.mapSize.set(quality.shadowSize,quality.shadowSize);Object.assign(sun.shadow.camera,{left:-140,right:140,top:140,bottom:-140,near:1,far:420});sun.shadow.bias=-.00035;sun.shadow.normalBias=.1;scene.add(sun);scene.add(sun.target);
 const specialIds=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON',...(buildAtlasSiteAssets?atlasSiteIds:[])];
 const {mesh,water:oldWater,height}=buildWorldGeometry(bindings,160,2600,{skipLandmarkIds:specialIds});
 const geometry=new THREE.BufferGeometry(),interleaved=new THREE.InterleavedBuffer(new Float32Array(mesh.values),9);
 const color=new THREE.Color();for(let i=0;i<interleaved.array.length;i+=9){color.setRGB(interleaved.array[i+6],interleaved.array[i+7],interleaved.array[i+8],THREE.SRGBColorSpace);interleaved.array[i+6]=color.r;interleaved.array[i+7]=color.g;interleaved.array[i+8]=color.b;}
 geometry.setAttribute('position',new THREE.InterleavedBufferAttribute(interleaved,3,0));geometry.setAttribute('normal',new THREE.InterleavedBufferAttribute(interleaved,3,3));geometry.setAttribute('color',new THREE.InterleavedBufferAttribute(interleaved,3,6));geometry.computeBoundingSphere();
 const terrainMaterial=new THREE.MeshStandardMaterial({vertexColors:true,roughness:.93,side:THREE.DoubleSide});
 const terrain=new THREE.Mesh(geometry,terrainMaterial);terrain.castShadow=true;terrain.receiveShadow=true;terrain.name='Atlas-aligned provisional terrain';scene.add(terrain);mesh.values=null;oldWater.values=null;
 const regional=buildRegionalAssets(THREE,bindings,height);scene.add(regional.root);
 const atlasSites=buildAtlasSiteAssets?buildAtlasSiteAssets(THREE,bindings,height):null;if(atlasSites)scene.add(atlasSites.root);
 const siteLocations=[...regional.locations,...(atlasSites?.locations||[])];
 const siteIds=siteLocations.map(l=>l.id);if(new Set(siteIds).size!==siteIds.length)throw Error('DUPLICATE_RENDERED_SITE');
 const framesBySite=siteViewFrames(THREE,siteLocations);
 const batches=siteLocations.flatMap(l=>batchStaticGeometry(THREE,l.group).geometries);
 const oceanMaterial=createBaseWaterMaterial(THREE);
 const oceanGeo=new THREE.PlaneGeometry(800,800,70,70),ocean=new THREE.Mesh(oceanGeo,oceanMaterial);ocean.rotation.x=-Math.PI/2;ocean.position.y=-.4;ocean.name='Moving base water';scene.add(ocean);
 let disposed=false,prepared=false,lastSignature='',lastShadowKey='',frames=0,lastTime=0,lastWidth=0,lastHeight=0;
 const debugExt=context.getExtension('WEBGL_debug_renderer_info');
 const stats={renderer:'three-webgl2',engine:'three@'+THREE.REVISION,locations:bindings.length,regionalLocations:regional.locations.length,siteLocations:siteLocations.length,siteIds:[...siteIds],genericLandmarks:bindings.filter(b=>!siteIds.includes(b.id)).length,geometry:'SOURCE_BOUND_CANDIDATE_NOT_APPROVED',gpuRenderer:debugExt?context.getParameter(debugExt.UNMASKED_RENDERER_WEBGL):'UNAVAILABLE',prepared:false,frames:0,waterTime:0,shadowRefreshes:0};
 function setCamera(c){
  const w=Math.max(1,canvas.clientWidth),h=Math.max(1,canvas.clientHeight),aspect=w/h,fit=Math.max(1,1.25/aspect),d=c.distance*(c.distance>100?fit:Math.min(fit,1.25)),t=c.target;
  if(w!==lastWidth||h!==lastHeight){const q=rendererQuality(w,globalThis.devicePixelRatio||1);renderer.setPixelRatio(q.pixelRatio);renderer.setSize(w,h,false);camera.aspect=aspect;camera.updateProjectionMatrix();lastWidth=w;lastHeight=h;}
  camera.position.set(t[0]+Math.sin(c.yaw)*Math.cos(c.pitch)*d,t[1]+Math.sin(c.pitch)*d,t[2]+Math.cos(c.yaw)*Math.cos(c.pitch)*d);camera.lookAt(...t);camera.updateMatrixWorld(true);
 }
 async function prepare(c){setCamera(c);await renderer.compileAsync(scene,camera);renderer.shadowMap.needsUpdate=true;prepared=true;stats.prepared=true;}
 function render(c,time,{strength=1,storm=0,paused=false}={}){
  if(disposed||context.isContextLost())return;
  if(!Number.isFinite(time)||!Number.isFinite(strength))throw Error('INVALID_RENDER_TIME');
  const signature=JSON.stringify([c,paused?lastTime:time,strength,storm,canvas.clientWidth,canvas.clientHeight]);if(signature===lastSignature)return;lastSignature=signature;setCamera(c);
  if(!paused)lastTime=time;regional.tick(lastTime,{paused});atlasSites?.tick(lastTime,{paused});oceanMaterial.uniforms.uTime.value=lastTime;oceanMaterial.uniforms.uStrength.value=strength;oceanMaterial.uniforms.uStorm.value=storm;
  const {span,key:shadowKey}=shadowCoverage(c);
  if(shadowKey!==lastShadowKey){
   sun.position.set(c.target[0]-95,150,c.target[2]+60);sun.target.position.set(c.target[0],0,c.target[2]);
   Object.assign(sun.shadow.camera,{left:-span,right:span,top:span,bottom:-span});
   sun.shadow.camera.updateProjectionMatrix();renderer.shadowMap.needsUpdate=true;
   lastShadowKey=shadowKey;stats.shadowRefreshes++;
  }
  sun.intensity=.35+strength*2.15;hemisphere.intensity=.45+strength*.95;scene.background.setRGB(.39+strength*.11,.49+strength*.14,.50+strength*.14);scene.fog.color.copy(scene.background);
  renderer.render(scene,camera);stats.frames=++frames;stats.waterTime=lastTime;stats.triangles=renderer.info.render.triangles;stats.drawCalls=renderer.info.render.calls;stats.memory={...renderer.info.memory};
 }
 function project(p){if(disposed)return null;const v=new THREE.Vector3(...p).project(camera);if(v.z<-1||v.z>1)return null;return {x:(v.x*.5+.5)*canvas.clientWidth,y:(.5-v.y*.5)*canvas.clientHeight,depth:v.z};}
 function pick(clientX,clientY){const r=canvas.getBoundingClientRect(),x=clientX-r.left,y=clientY-r.top;let best=null,distance=32;for(const p of bindings){const q=project(framesBySite[p.id]?.target||p.renderAnchor||[p.anchor[0],height(p.anchor[0],p.anchor[2])+2,p.anchor[2]]);if(!q)continue;const d=Math.hypot(q.x-x,q.y-y);if(d<distance){best=p;distance=d;}}return best;}
 const lost=e=>{e.preventDefault();onContextLost();};canvas.addEventListener('webglcontextlost',lost);
 return {prepare,render,project,pick,height,stats,siteView(id){return framesBySite[id]?structuredClone(framesBySite[id]):null;},
  loseContext(){renderer.forceContextLoss();},
  dispose(){if(disposed)return;disposed=true;canvas.removeEventListener('webglcontextlost',lost);regional.dispose();atlasSites?.dispose();for(const g of batches)g.dispose();geometry.dispose();terrainMaterial.dispose();oceanGeo.dispose();oceanMaterial.dispose();sun.shadow.map?.dispose();renderer.dispose();scene.clear();stats.disposed=true;}
 };
}

/** Batch opaque static meshes by material, leaving animated water intact. */
export function batchStaticGeometry(THREE,root){
 const groups=new Map(),geometries=[];for(const o of [...root.children]){if(!o.isMesh||o.material?.isShaderMaterial||o.material?.transparent)continue;o.updateMatrix();const g=(o.geometry.index?o.geometry.toNonIndexed():o.geometry.clone()).applyMatrix4(o.matrix);const key=o.material.uuid;if(!groups.has(key))groups.set(key,{material:o.material,items:[]});groups.get(key).items.push({object:o,geometry:g});}
 for(const {material,items} of groups.values()){const result=new THREE.BufferGeometry();for(const name of ['position','normal','uv',...(material.vertexColors?['color']:[])]){if(!items.every(x=>x.geometry.attributes[name]))continue;const size=items[0].geometry.attributes[name].itemSize,values=[];for(const item of items)values.push(...item.geometry.attributes[name].array);result.setAttribute(name,new THREE.Float32BufferAttribute(values,size));}if(material.vertexColors&&!result.getAttribute('color'))throw Error('BATCH_VERTEX_COLORS_MISSING');result.computeBoundingSphere();const batch=new THREE.Mesh(result,material);if(material.vertexColors){batch.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',compiledFrom:items.map(x=>x.object.name).filter(Boolean)};}batch.renderOrder=Math.min(...items.map(x=>x.object.renderOrder));batch.castShadow=true;batch.receiveShadow=true;root.add(batch);geometries.push(result);for(const item of items){root.remove(item.object);item.geometry.dispose();}}
 return {geometries};
}
