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
/** Procedural albedo on the existing atlas-aligned ground mesh.
 * Repeating world-space detail breaks broad flat-color patches without adding
 * landscape geometry, external imagery, new source locations, or render passes.
 * All material choices remain CANDIDATE_NOT_APPROVED.
 */
function periodicTerrainNoise(u,v,frequency){
 const x=u*frequency,y=v*frequency,ix=Math.floor(x),iy=Math.floor(y);
 const sx=x-ix,sy=y-iy,tx=sx*sx*(3-2*sx),ty=sy*sy*(3-2*sy);
 const sample=(a,b)=>{
  const hX=((a%frequency)+frequency)%frequency,hY=((b%frequency)+frequency)%frequency;
  let h=Math.imul(hX+17,374761393)^Math.imul(hY+31,668265263)^Math.imul(frequency+7,2246822519);
  h=Math.imul(h^(h>>>13),1274126177);
  return ((h^(h>>>16))>>>0)/4294967295;
 };
 const a=sample(ix,iy)*(1-tx)+sample(ix+1,iy)*tx;
 const b=sample(ix,iy+1)*(1-tx)+sample(ix+1,iy+1)*tx;
 return a*(1-ty)+b*ty;
}
export function createTerrainSurfaceTexture(THREE,size=128){
 if(!Number.isInteger(size)||size<32||size>512||(size&(size-1)))throw Error('INVALID_TERRAIN_TEXTURE_SIZE');
 const rgba=new Uint8Array(size*size*4);
 for(let y=0;y<size;y++)for(let x=0;x<size;x++){
  const u=(x+.5)/size,v=(y+.5)/size;
  const broad=periodicTerrainNoise(u,v,4),medium=periodicTerrainNoise(u,v,16),fine=periodicTerrainNoise(u,v,48);
  const tone=.54*broad+.33*medium+.13*fine,soil=Math.max(0,(broad-.56)/.44);
  const base=.84+.24*tone;
  const i=(y*size+x)*4;
  rgba[i]=Math.round(255*Math.min(1,base+.025*soil));
  rgba[i+1]=Math.round(255*Math.min(1,base-.025*soil));
  rgba[i+2]=Math.round(255*Math.min(1,base-.055*soil));
  rgba[i+3]=255;
 }
 const texture=new THREE.DataTexture(rgba,size,size,THREE.RGBAFormat);
 texture.wrapS=THREE.RepeatWrapping;texture.wrapT=THREE.RepeatWrapping;
 texture.minFilter=THREE.LinearMipmapLinearFilter;texture.magFilter=THREE.LinearFilter;
 texture.generateMipmaps=true;texture.colorSpace=THREE.SRGBColorSpace;
 texture.anisotropy=4;texture.needsUpdate=true;
 return texture;
}
export function applyTerrainPlanarUVs(THREE,geometry,tileWorldUnits=64){
 if(!Number.isFinite(tileWorldUnits)||tileWorldUnits<=0)throw Error('INVALID_TERRAIN_TILE_SIZE');
 const position=geometry.getAttribute('position'),uv=new Float32Array(position.count*2);
 for(let i=0;i<position.count;i++){uv[i*2]=position.getX(i)/tileWorldUnits;uv[i*2+1]=position.getZ(i)/tileWorldUnits;}
 geometry.setAttribute('uv',new THREE.BufferAttribute(uv,2));
 return geometry;
}
/** Small, tile-periodic physical-light response on the EXISTING ground.
 * Tangent-space normals derive from deterministic, source-independent noise.
 * No geographic displacement or source/canon data is introduced.
 */
function terrainMicroHeight(u,v){
 return 2.0*(.32*periodicTerrainNoise(u,v,8)+.46*periodicTerrainNoise(u,v,24)+.22*periodicTerrainNoise(u,v,48));
}
export function terrainSurfaceNormal(u,v,size=128,tileWorldUnits=64){
 if(![u,v,tileWorldUnits].every(Number.isFinite)||!Number.isInteger(size)||size<32||size>512||tileWorldUnits<=0)throw Error('INVALID_TERRAIN_NORMAL_SAMPLE');
 const step=1/size;
 const dx=(terrainMicroHeight(u+step,v)-terrainMicroHeight(u-step,v))/(2*step*tileWorldUnits);
 const dz=(terrainMicroHeight(u,v+step)-terrainMicroHeight(u,v-step))/(2*step*tileWorldUnits);
 const length=Math.hypot(dx,dz,1);
 return [-dx/length,-dz/length,1/length];
}
export function createTerrainSurfaceNormalTexture(THREE,size=128,tileWorldUnits=64){
 if(!Number.isInteger(size)||size<32||size>512||(size&(size-1)))throw Error('INVALID_TERRAIN_TEXTURE_SIZE');
 if(!Number.isFinite(tileWorldUnits)||tileWorldUnits<=0)throw Error('INVALID_TERRAIN_TILE_SIZE');
 const rgba=new Uint8Array(size*size*4);
 for(let y=0;y<size;y++)for(let x=0;x<size;x++){
  const n=terrainSurfaceNormal((x+.5)/size,(y+.5)/size,size,tileWorldUnits);
  const i=(y*size+x)*4;
  rgba[i]=Math.round(127.5*(n[0]+1));
  rgba[i+1]=Math.round(127.5*(n[1]+1));
  rgba[i+2]=Math.round(127.5*(n[2]+1));
  rgba[i+3]=255;
 }
 const texture=new THREE.DataTexture(rgba,size,size,THREE.RGBAFormat);
 texture.wrapS=THREE.RepeatWrapping;texture.wrapT=THREE.RepeatWrapping;
 texture.minFilter=THREE.LinearMipmapLinearFilter;texture.magFilter=THREE.LinearFilter;
 texture.generateMipmaps=true;texture.colorSpace=THREE.NoColorSpace;
 texture.anisotropy=4;texture.needsUpdate=true;
 return texture;
}
/** Damp ground contact around the existing Mud Dogs water footprint.
 * A read-only optical vertex tint on terrain triangles only: not a shoreline,
 * water simulation, terrain displacement, hydrology, or canonical state.
 * Existing swamp disc radii (10.5 × 8.2) provide the bounded visual scale.
 */
export function wetlandGroundContactWeight(x,z,anchor){
 if(!Array.isArray(anchor)||anchor.length!==3||![x,z,...anchor].every(Number.isFinite))throw Error('INVALID_WETLAND_CONTACT_ANCHOR');
 const r=Math.hypot((x-anchor[0])/10.5,(z-anchor[2])/8.2);
 const t=Math.max(0,Math.min(1,(1.65-r)/.95));
 return t*t*(3-2*t);
}
export function applyWetlandGroundContact(geometry,anchor,terrainVertexCount){
 const position=geometry?.getAttribute?.('position'),color=geometry?.getAttribute?.('color');
 if(!position||!color||position.count!==color.count||!Number.isInteger(terrainVertexCount)||terrainVertexCount<=0||terrainVertexCount>position.count)throw Error('INVALID_WETLAND_CONTACT_GEOMETRY');
 // Validate source anchor even on a hypothetical mesh entirely outside the region.
 wetlandGroundContactWeight(0,0,anchor);
 let tinted=0;
 for(let i=0;i<terrainVertexCount;i++){
  const x=position.getX(i),z=position.getZ(i);
  const weight=wetlandGroundContactWeight(x,z,anchor);
  if(weight===0)continue;
  // Small deterministic variation avoids a hard circular, uniform color decal.
  const variation=.87+.13*Math.sin(x*.6+z*.23)*Math.cos(x*.3-z*.5);
  const contact=weight*variation;
  color.setXYZ(i,color.getX(i)*(1-.33*contact),color.getY(i)*(1-.22*contact),color.getZ(i)*(1-.21*contact));
  tinted++;
 }
 if(tinted){if(color.data)color.data.needsUpdate=true;else color.needsUpdate=true;}
 return tinted;
}

/** Shallow-water optical mask derived ONLY from existing terrain height.
 * Disposable, read-only lighting cue for the original water plane:
 * not hydrological topology, an Atlas river edit, or a canonical shoreline.
 */
export function shorelineOpticalStrength(height,x,z,waterLevel=-.4){
 if(typeof height!=='function'||![x,z,waterLevel].every(Number.isFinite))throw Error('INVALID_SHORELINE_SAMPLE');
 const elevation=height(x,z);
 if(!Number.isFinite(elevation))throw Error('INVALID_SHORELINE_HEIGHT');
 const depth=waterLevel-elevation;
 return depth>0?Math.max(0,1-depth/1.6):0;
}
export function createWaterShorelineTexture(THREE,height,size=256){
 if(!Number.isInteger(size)||size<32||size>512||(size&(size-1)))throw Error('INVALID_SHORELINE_TEXTURE_SIZE');
 if(typeof height!=='function')throw Error('INVALID_SHORELINE_HEIGHT_PROVIDER');
 const rgba=new Uint8Array(size*size*4);
 for(let z=0;z<size;z++)for(let x=0;x<size;x++){
  const worldX=-110+(x+.5)*220/size,worldZ=-110+(z+.5)*220/size;
  const shore=shorelineOpticalStrength(height,worldX,worldZ);
  const i=(z*size+x)*4;
  rgba[i]=Math.round(255*shore);rgba[i+1]=0;rgba[i+2]=0;rgba[i+3]=255;
 }
 const texture=new THREE.DataTexture(rgba,size,size,THREE.RGBAFormat);
 texture.wrapS=THREE.ClampToEdgeWrapping;texture.wrapT=THREE.ClampToEdgeWrapping;
 texture.minFilter=THREE.LinearFilter;texture.magFilter=THREE.LinearFilter;
 texture.generateMipmaps=false;texture.colorSpace=THREE.NoColorSpace;texture.needsUpdate=true;
 texture.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',provenance:'existing-terrain-height',status:'OPTICAL_ONLY'};
 return texture;
}

/** View-responsive optics for the already animated base water plane.
 * The original wave heights and water boundary stay fixed; analytic slopes
 * make light respond to the same physical displacement on ordinary water time.
 * Reuse the scene's existing Three.js fog to align distant water with terrain.
 * This is candidate rendering only, never an Atlas hydrology claim.
 */
export function createBaseWaterMaterial(THREE,shorelineTexture=null){
 // Fog uses native engine uniforms; the sampler retains its texture identity.
 const uniforms=THREE.UniformsUtils.merge([THREE.UniformsLib.fog,{uTime:{value:0},uStrength:{value:1},uStorm:{value:0}}]);
 uniforms.uShoreMask={value:shorelineTexture};
 return new THREE.ShaderMaterial({uniforms,
  vertexShader:`uniform float uTime;
   varying vec3 vP;varying vec3 vWaveNormal;
   #include <fog_pars_vertex>
   void main(){
    vec3 p=position;
    float phaseX=p.x*.17+uTime*.6;
    float phaseY=p.y*.21-uTime*.39;
    p.z+=sin(phaseX)*.07+sin(phaseY)*.05;
    // Derivatives of the displaced local plane; not an invented water current.
    vec3 localNormal=normalize(vec3(-.07*.17*cos(phaseX),-.05*.21*cos(phaseY),1.));
    vWaveNormal=normalize(mat3(modelMatrix)*localNormal);
    vP=(modelMatrix*vec4(p,1.)).xyz;
    vec4 mvPosition=modelViewMatrix*vec4(p,1.);
    gl_Position=projectionMatrix*mvPosition;
    #include <fog_vertex>
   }`,
  fragmentShader:`uniform float uTime;uniform float uStrength;uniform float uStorm;
   uniform sampler2D uShoreMask;
   varying vec3 vP;varying vec3 vWaveNormal;
   #include <fog_pars_fragment>
   void main(){
    float opticalPhaseA=vP.x*1.7+sin(vP.z*.7)+uTime*.65;
    float opticalPhaseB=vP.z*2.1-uTime*.41;
    float w=sin(opticalPhaseA)*sin(opticalPhaseB);
    // Suppress subpixel glitter without slowing the physical water beneath it.
    float opticalPixelSpan=max(fwidth(opticalPhaseA),fwidth(opticalPhaseB));
    float fineDetailFade=1.-smoothstep(.5,2.,opticalPixelSpan);
    float s=pow(max(w,0.),9.)*fineDetailFade;
    vec3 col=mix(vec3(.065,.24,.235),vec3(.18,.42,.38),.5+.5*sin(vP.x*.014+vP.z*.012));
    col+=vec3(.23,.3,.24)*s*.45;
    // Small optical normals add fine water sheen without extra geometry/draws.
    vec3 n=normalize(vWaveNormal+fineDetailFade*vec3(.021*cos(vP.x*.71+uTime*.49),0.,.024*sin(vP.z*.63-uTime*.38)));
    vec3 viewDir=normalize(cameraPosition-vP);
    vec3 sunDir=normalize(vec3(-.6,.9,.36));
    float fresnel=pow(1.-max(dot(n,viewDir),0.),3.);
    float glint=pow(max(dot(reflect(-sunDir,n),viewDir),0.),64.);
    col=mix(col,vec3(.36,.47,.47),(.10+.27*fresnel));
    // Match the sky solar halo: night retains ambient water optics, not direct sunlight.
    float solarDaylight=clamp((uStrength-.32)/.68,0.,1.);
    col+=vec3(.38,.34,.21)*glint*.35*solarDaylight;
    // Existing terrain determines shallows; normal uTime drives highlights.
    vec2 shoreUV=(vP.xz+vec2(110.))/220.;
    float within=step(0.,shoreUV.x)*step(shoreUV.x,1.)*step(0.,shoreUV.y)*step(shoreUV.y,1.);
    float shallows=texture2D(uShoreMask,clamp(shoreUV,0.,1.)).r*within;
    float breaking=pow(max(sin(vP.x*3.1+uTime*.8)*sin(vP.z*2.8-uTime*.71),0.),6.)*fineDetailFade;
    col=mix(col,vec3(.22,.4,.35),shallows*.28);
    col+=vec3(.33,.31,.24)*shallows*breaking*.25;
    col*=.45+.55*uStrength;
    gl_FragColor=vec4(col,1.);
    #include <tonemapping_fragment>
    #include <colorspace_fragment>
    #include <fog_fragment>
   }`,side:THREE.DoubleSide,fog:true});
}
/** Sky-only candidate: one camera-centered sphere and no weather/canon producer.
 * The existing fog color owns the horizon; light strength only controls the
 * optical gradient and sun halo. No cloud/storm or world-state inference.
 */
export function createAtmosphericSky(THREE){
 const geometry=new THREE.SphereGeometry(1,24,12);
 const material=new THREE.ShaderMaterial({
  uniforms:{uHorizon:{value:new THREE.Color('#bed1cf')},uDaylight:{value:1}},
  vertexShader:`varying vec3 vSkyDirection;
   void main(){
    vSkyDirection=position;
    gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);
   }`,
  fragmentShader:`uniform vec3 uHorizon;uniform float uDaylight;
   varying vec3 vSkyDirection;
   void main(){
    vec3 ray=normalize(vSkyDirection);
    float upper=smoothstep(.015,.72,max(ray.y,0.));
    float light=clamp(uDaylight,0.,1.);
    vec3 zenith=mix(vec3(.012,.025,.052),vec3(.28,.43,.53),light);
    vec3 col=mix(uHorizon,zenith,.72*upper);
    // The candidate solar halo follows the existing directional-light vector.
    float halo=pow(max(dot(ray,normalize(vec3(-95.,150.,60.))),0.),22.);
    col+=vec3(.55,.42,.24)*halo*.21*light*upper;
    gl_FragColor=vec4(col,1.);
    #include <colorspace_fragment>
   }`,
  side:THREE.BackSide,depthTest:false,depthWrite:false,fog:false,toneMapped:false
 });
 const sky=new THREE.Mesh(geometry,material);
 sky.name='Source-neutral atmosphere · candidate';
 sky.scale.setScalar(1000);sky.renderOrder=-1000;sky.frustumCulled=false;
 sky.userData={visualAuthority:'CANDIDATE_NOT_APPROVED'};
 return sky;
}
/** Use the existing illustrative clock floor (.32), not a second clock or
 * weather input. Keep noon colors and fog/horizon continuity; only optical
 * daylight goes to zero at night, leaving terrain and water lighting intact.
 */
export function applyAtmosphereLighting(sky,background,fogColor,strength){
 const daylight=Math.max(0,Math.min(1,(strength-.32)/.68));
 background.setRGB(.055+daylight*.445,.085+daylight*.545,.13+daylight*.51);
 fogColor.copy(background);
 sky.material.uniforms.uHorizon.value.copy(fogColor);
 sky.material.uniforms.uDaylight.value=daylight;
}
/** A source-identified, local water-haze candidate over the existing Mud Dogs
 * swamp disc. This is illustrative optical depth, not a storm, weather event,
 * water boundary, resident, or geographic source record. No external texture.
 */
export function createWetlandWaterHaze(THREE){
 const count=96,positions=new Float32Array(count*3),phases=new Float32Array(count);
 for(let i=0;i<count;i++){
  const a=i*2.399963229728653,r=Math.sqrt((i+.5)/count)*.84;
  positions[3*i]=10.5*r*Math.cos(a);
  positions[3*i+1]=.28+.07*(i%7)+.035*Math.sin(i*1.37);
  positions[3*i+2]=8.2*r*Math.sin(a);
  phases[i]=i*.79;
 }
 const geometry=new THREE.BufferGeometry();
 geometry.setAttribute('position',new THREE.BufferAttribute(positions,3));
 geometry.setAttribute('aPhase',new THREE.BufferAttribute(phases,1));
 geometry.computeBoundingSphere();
 const material=new THREE.ShaderMaterial({
  uniforms:{uTime:{value:0},uLightLevel:{value:1}},
  transparent:true,depthTest:true,depthWrite:false,fog:false,
  vertexShader:`uniform float uTime;attribute float aPhase;varying float vOpacity;
   void main(){
    vec3 p=position;
    // Small bounded optical drift on ordinary independent animation time.
    p.x+=.23*sin(uTime*.19+aPhase);
    p.z+=.19*cos(uTime*.17+aPhase*1.3);
    p.y+=.035*sin(uTime*.29+aPhase);
    vec4 mvPosition=modelViewMatrix*vec4(p,1.);
    gl_Position=projectionMatrix*mvPosition;
    gl_PointSize=clamp(2600./max(1.,-mvPosition.z),2.,64.);
    // Optical extinction: avoid near-camera sprites and distant world-view fog.
    // This is independent of weather and does not change the source footprint.
    float viewDepth=max(0.,-mvPosition.z);
    float nearVisibility=smoothstep(4.,14.,viewDepth);
    float farVisibility=1.-smoothstep(95.,165.,viewDepth);
    vOpacity=(.13+.055*(.5+.5*sin(uTime*.21+aPhase)))*nearVisibility*farVisibility;
   }`,
  fragmentShader:`uniform float uLightLevel;varying float vOpacity;
   void main(){
    vec2 p=(gl_PointCoord*2.-1.)*vec2(1.,2.1);
    float r=length(p);
    float halo=exp(-4.0*r*r)*(1.-smoothstep(.72,1.,r));
    // Same shared-clock light as the terrain and sky; opacity and drift are unchanged.
    float light=clamp(uLightLevel,0.,1.);
    vec3 radiance=vec3(.69,.80,.73)*mix(.30,1.,light);
    gl_FragColor=vec4(radiance,vOpacity*halo);
    #include <tonemapping_fragment>
    #include <colorspace_fragment>
   }`
 });
 const points=new THREE.Points(geometry,material);
 points.name='Mud Dogs water-haze · optical candidate';
 points.renderOrder=3;
 points.frustumCulled=false;
 points.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',locationId:'LOC-MUD-DOGS-SWAMP',sourceEnvironment:['existing swamp water disc'],waterAndWeatherAuthority:'NONE',navigable:false};
 return points;
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
 const sky=createAtmosphericSky(THREE);scene.add(sky);
 const hemisphere=new THREE.HemisphereLight('#e3ecdf','#657256',1.4);scene.add(hemisphere);
 const sun=new THREE.DirectionalLight('#ffe7b3',2.5);sun.position.set(-95,150,60);sun.castShadow=true;
 const quality=rendererQuality(canvas.clientWidth||1280,globalThis.devicePixelRatio||1);
 sun.shadow.mapSize.set(quality.shadowSize,quality.shadowSize);Object.assign(sun.shadow.camera,{left:-140,right:140,top:140,bottom:-140,near:1,far:420});sun.shadow.bias=-.00035;sun.shadow.normalBias=.1;scene.add(sun);scene.add(sun.target);
 const specialIds=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON',...(buildAtlasSiteAssets?atlasSiteIds:[])];
 const terrainGrid=160;
 const {mesh,water:oldWater,height}=buildWorldGeometry(bindings,terrainGrid,2600,{skipLandmarkIds:specialIds});
 const geometry=new THREE.BufferGeometry(),interleaved=new THREE.InterleavedBuffer(new Float32Array(mesh.values),9);
 const color=new THREE.Color();for(let i=0;i<interleaved.array.length;i+=9){color.setRGB(interleaved.array[i+6],interleaved.array[i+7],interleaved.array[i+8],THREE.SRGBColorSpace);interleaved.array[i+6]=color.r;interleaved.array[i+7]=color.g;interleaved.array[i+8]=color.b;}
 geometry.setAttribute('position',new THREE.InterleavedBufferAttribute(interleaved,3,0));geometry.setAttribute('normal',new THREE.InterleavedBufferAttribute(interleaved,3,3));geometry.setAttribute('color',new THREE.InterleavedBufferAttribute(interleaved,3,6));
 const swampBinding=bindings.find(b=>b.id==='LOC-MUD-DOGS-SWAMP');
 if(swampBinding)applyWetlandGroundContact(geometry,swampBinding.anchor,terrainGrid*terrainGrid*6);
 geometry.computeBoundingSphere();
 applyTerrainPlanarUVs(THREE,geometry);
 const terrainTexture=createTerrainSurfaceTexture(THREE);
 const terrainNormalTexture=createTerrainSurfaceNormalTexture(THREE);
 const terrainMaterial=new THREE.MeshStandardMaterial({map:terrainTexture,normalMap:terrainNormalTexture,normalScale:new THREE.Vector2(.7,.7),vertexColors:true,roughness:.93,side:THREE.DoubleSide});
 const terrain=new THREE.Mesh(geometry,terrainMaterial);terrain.castShadow=true;terrain.receiveShadow=true;terrain.name='Atlas-aligned provisional terrain';scene.add(terrain);mesh.values=null;oldWater.values=null;
 const regional=buildRegionalAssets(THREE,bindings,height);scene.add(regional.root);
 const atlasSites=buildAtlasSiteAssets?buildAtlasSiteAssets(THREE,bindings,height):null;if(atlasSites)scene.add(atlasSites.root);
 const siteLocations=[...regional.locations,...(atlasSites?.locations||[])];
 const siteIds=siteLocations.map(l=>l.id);if(new Set(siteIds).size!==siteIds.length)throw Error('DUPLICATE_RENDERED_SITE');
 const framesBySite=siteViewFrames(THREE,siteLocations);
 const batches=siteLocations.flatMap(l=>batchStaticGeometry(THREE,l.group).geometries);
 const templeMist=regional.locations.find(l=>l.id==='LOC-TDS-WATERFALL-TEMPLE')?.group.getObjectByName('Candidate waterfall plunge mist');
 const swampSite=regional.locations.find(l=>l.id==='LOC-MUD-DOGS-SWAMP');
 const swampHaze=swampSite?createWetlandWaterHaze(THREE):null;
 if(swampHaze)swampSite.group.add(swampHaze);
 const shorelineTexture=createWaterShorelineTexture(THREE,height);
 const oceanMaterial=createBaseWaterMaterial(THREE,shorelineTexture);
 const oceanGeo=new THREE.PlaneGeometry(800,800,70,70),ocean=new THREE.Mesh(oceanGeo,oceanMaterial);ocean.rotation.x=-Math.PI/2;ocean.position.y=-.4;ocean.name='Moving base water';scene.add(ocean);
 let disposed=false,prepared=false,lastSignature='',lastShadowKey='',frames=0,lastTime=0,lastWidth=0,lastHeight=0;
 const debugExt=context.getExtension('WEBGL_debug_renderer_info');
 const stats={renderer:'three-webgl2',engine:'three@'+THREE.REVISION,locations:bindings.length,regionalLocations:regional.locations.length,siteLocations:siteLocations.length,siteIds:[...siteIds],genericLandmarks:bindings.filter(b=>!siteIds.includes(b.id)).length,geometry:'SOURCE_BOUND_CANDIDATE_NOT_APPROVED',gpuRenderer:debugExt?context.getParameter(debugExt.UNMASKED_RENDERER_WEBGL):'UNAVAILABLE',prepared:false,frames:0,waterTime:0,shadowRefreshes:0};
 function setCamera(c){
  const w=Math.max(1,canvas.clientWidth),h=Math.max(1,canvas.clientHeight),aspect=w/h,fit=Math.max(1,1.25/aspect),d=c.distance*(c.distance>100?fit:Math.min(fit,1.25)),t=c.target;
  if(w!==lastWidth||h!==lastHeight){const q=rendererQuality(w,globalThis.devicePixelRatio||1);renderer.setPixelRatio(q.pixelRatio);renderer.setSize(w,h,false);camera.aspect=aspect;camera.updateProjectionMatrix();lastWidth=w;lastHeight=h;}
  camera.position.set(t[0]+Math.sin(c.yaw)*Math.cos(c.pitch)*d,t[1]+Math.sin(c.pitch)*d,t[2]+Math.cos(c.yaw)*Math.cos(c.pitch)*d);camera.lookAt(...t);camera.updateMatrixWorld(true);sky.position.copy(camera.position);
 }
 async function prepare(c){setCamera(c);await renderer.compileAsync(scene,camera);renderer.shadowMap.needsUpdate=true;prepared=true;stats.prepared=true;}
 function render(c,time,{strength=1,storm=0,paused=false}={}){
  if(disposed||context.isContextLost())return;
  if(!Number.isFinite(time)||!Number.isFinite(strength))throw Error('INVALID_RENDER_TIME');
  const signature=JSON.stringify([c,paused?lastTime:time,strength,storm,canvas.clientWidth,canvas.clientHeight]);if(signature===lastSignature)return;lastSignature=signature;setCamera(c);
  if(!paused)lastTime=time;regional.tick(lastTime,{paused});atlasSites?.tick(lastTime,{paused});oceanMaterial.uniforms.uTime.value=lastTime;if(swampHaze){swampHaze.material.uniforms.uTime.value=lastTime;swampHaze.material.uniforms.uLightLevel.value=strength;}oceanMaterial.uniforms.uStrength.value=strength;oceanMaterial.uniforms.uStorm.value=storm;
  if(templeMist)templeMist.material.uniforms.uLightLevel.value=strength;
  for(const w of regional.water)w.material.uniforms.uLightLevel.value=strength;
  for(const w of atlasSites?.water||[])w.material.uniforms.uLightLevel.value=strength;
  const {span,key:shadowKey}=shadowCoverage(c);
  if(shadowKey!==lastShadowKey){
   sun.position.set(c.target[0]-95,150,c.target[2]+60);sun.target.position.set(c.target[0],0,c.target[2]);
   Object.assign(sun.shadow.camera,{left:-span,right:span,top:span,bottom:-span});
   sun.shadow.camera.updateProjectionMatrix();renderer.shadowMap.needsUpdate=true;
   lastShadowKey=shadowKey;stats.shadowRefreshes++;
  }
  sun.intensity=.35+strength*2.15;hemisphere.intensity=.45+strength*.95;applyAtmosphereLighting(sky,scene.background,scene.fog.color,strength);
  renderer.render(scene,camera);stats.frames=++frames;stats.waterTime=lastTime;stats.triangles=renderer.info.render.triangles;stats.drawCalls=renderer.info.render.calls;stats.memory={...renderer.info.memory};
 }
 function project(p){if(disposed)return null;const v=new THREE.Vector3(...p).project(camera);if(v.z<-1||v.z>1)return null;return {x:(v.x*.5+.5)*canvas.clientWidth,y:(.5-v.y*.5)*canvas.clientHeight,depth:v.z};}
 function pick(clientX,clientY){const r=canvas.getBoundingClientRect(),x=clientX-r.left,y=clientY-r.top;let best=null,distance=32;for(const p of bindings){const q=project(framesBySite[p.id]?.target||p.renderAnchor||[p.anchor[0],height(p.anchor[0],p.anchor[2])+2,p.anchor[2]]);if(!q)continue;const d=Math.hypot(q.x-x,q.y-y);if(d<distance){best=p;distance=d;}}return best;}
 const lost=e=>{e.preventDefault();onContextLost();};canvas.addEventListener('webglcontextlost',lost);
 return {prepare,render,project,pick,height,stats,siteView(id){return framesBySite[id]?structuredClone(framesBySite[id]):null;},
  loseContext(){renderer.forceContextLoss();},
  dispose(){if(disposed)return;disposed=true;canvas.removeEventListener('webglcontextlost',lost);regional.dispose();atlasSites?.dispose();for(const g of batches)g.dispose();geometry.dispose();terrainMaterial.dispose();terrainTexture.dispose();terrainNormalTexture.dispose();oceanGeo.dispose();oceanMaterial.dispose();shorelineTexture.dispose();if(swampHaze){swampHaze.geometry.dispose();swampHaze.material.dispose();}sky.geometry.dispose();sky.material.dispose();sun.shadow.map?.dispose();renderer.dispose();scene.clear();stats.disposed=true;}
 };
}

/** Batch opaque static meshes by material, leaving animated water intact. */
export function batchStaticGeometry(THREE,root){
 const groups=new Map(),geometries=[];for(const o of [...root.children]){if(!o.isMesh||o.material?.isShaderMaterial||o.material?.transparent)continue;o.updateMatrix();const g=(o.geometry.index?o.geometry.toNonIndexed():o.geometry.clone()).applyMatrix4(o.matrix);const key=o.material.uuid;if(!groups.has(key))groups.set(key,{material:o.material,items:[]});groups.get(key).items.push({object:o,geometry:g});}
 for(const {material,items} of groups.values()){const result=new THREE.BufferGeometry();for(const name of ['position','normal','uv',...(material.vertexColors?['color']:[])]){if(!items.every(x=>x.geometry.attributes[name]))continue;const size=items[0].geometry.attributes[name].itemSize,values=[];for(const item of items)values.push(...item.geometry.attributes[name].array);result.setAttribute(name,new THREE.Float32BufferAttribute(values,size));}if(material.vertexColors&&!result.getAttribute('color'))throw Error('BATCH_VERTEX_COLORS_MISSING');result.computeBoundingSphere();const batch=new THREE.Mesh(result,material);if(material.vertexColors){batch.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',compiledFrom:items.map(x=>x.object.name).filter(Boolean)};}batch.renderOrder=Math.min(...items.map(x=>x.object.renderOrder));batch.castShadow=true;batch.receiveShadow=true;root.add(batch);geometries.push(result);for(const item of items){root.remove(item.object);item.geometry.dispose();}}
 return {geometries};
}
