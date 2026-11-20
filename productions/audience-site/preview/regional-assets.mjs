/** Authored regional visualization candidates. No new locations, characters or canon.
 * Geometry is local to existing Atlas anchors; all dimensions remain illustrative.
 * THREE is injected so the same asset code can be inspected in Node and rendered offline.
 */
export function buildRegionalAssets(THREE, bindings, height) {
  const root=new THREE.Group(); root.name='Southern Wetlands · candidate environment';
  const locations=[],water=[],ambientMotion=[],materials=new Map(),geometries=new Set(),textures=new Set(); let disposed=false;
  function texture(kind){const n=128,a=new Uint8Array(n*n*4);for(let y=0;y<n;y++)for(let x=0;x<n;x++){const noise=(Math.sin(x*31.71+y*17.19)*437.3)%1;let v=220+noise*16;if(kind==='stone'){const row=Math.floor(y/32),xx=(x+(row%2)*32)%64;if(y%32<2||xx<2)v=128+noise*10;}else if(kind==='wood')v-=Math.pow(.5+.5*Math.sin(x*.9+Math.sin(y*.1)*1.2),7)*48;const i=(y*n+x)*4;a[i]=a[i+1]=a[i+2]=Math.max(0,Math.min(255,v));a[i+3]=255;}const t=new THREE.DataTexture(a,n,n);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(2,2);t.magFilter=THREE.LinearFilter;t.minFilter=THREE.LinearMipmapLinearFilter;t.generateMipmaps=true;t.colorSpace=THREE.SRGBColorSpace;t.needsUpdate=true;textures.add(t);return t;}
  const stoneTexture=texture('stone'),woodTexture=texture('wood');
  const mat=(color,roughness=.88)=>{const key=color+':'+roughness;if(!materials.has(key)){const stoneColors=['#b4ad89','#ddd2a6','#e4d8b3','#997856'];const woody=['#6b4c33','#665340'];const t=stoneColors.includes(color)?stoneTexture:woody.includes(color)?woodTexture:null;materials.set(key,new THREE.MeshStandardMaterial({color,roughness,metalness:0,map:t,bumpMap:t,bumpScale:t?.08:0}));}return materials.get(key);};
  const stone=mat('#b4ad89'),edge=mat('#ddd2a6'),moss=mat('#4d6d3b'),dark=mat('#54604a'),wood=mat('#6b4c33'),trunk=mat('#665340'),leaf=mat('#35684a'),leafLight=mat('#77944b'),leafDark=mat('#234d43');
  const mesh=(g,geo,material,x,y,z)=>{geometries.add(geo);const o=new THREE.Mesh(geo,material);o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;g.add(o);return o;};
  const box=(g,x,y,z,w,h,d,m)=>mesh(g,new THREE.BoxGeometry(w,h,d),m,x,y+h/2,z);
  const cyl=(g,x,y,z,r1,r2,h,m,n=10)=>mesh(g,new THREE.CylinderGeometry(r1,r2,h,n),m,x,y+h/2,z);
  const rock=(g,x,y,z,sx,sy,sz,m=stone)=>{const o=mesh(g,new THREE.IcosahedronGeometry(1,2),m,x,y,z);o.scale.set(sx,sy,sz);o.rotation.set(.19+x*.07,z*.16,.1);return o;};
  const branch=(g,a,b,r,m=trunk)=>{const av=new THREE.Vector3(...a),bv=new THREE.Vector3(...b),v=bv.clone().sub(av);const o=mesh(g,new THREE.CylinderGeometry(r*.62,r,v.length(),7),m,...av.clone().add(bv).multiplyScalar(.5).toArray());o.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),v.normalize());return o;};
  function canopy(g,x,y,z,scale=1,tint=leaf){
    cyl(g,x,y,z,.15*scale,.30*scale,2.5*scale,trunk,7);
    for(let j=0;j<3;j++){const a=j*2.1+.3;branch(g,[x,y+1.5*scale,z],[x+Math.cos(a)*.7*scale,y+2.7*scale,z+Math.sin(a)*.7*scale],.09*scale);rock(g,x+Math.cos(a)*.65*scale,y+3.05*scale,z+Math.sin(a)*.65*scale,1.1*scale,.75*scale,.95*scale,j===1?leafLight:tint);}
  }
  function waterMaterial(kind,color){
    // Local candidate current direction/speed: visualization only, no new hydrology canon.
    const wetland=kind==='swamp'||kind==='channel';
    const flow=kind==='channel'?new THREE.Vector2(-.034,.013):kind==='swamp'?new THREE.Vector2(.012,-.009):new THREE.Vector2(0,0);
    const m=new THREE.ShaderMaterial({uniforms:{uTime:{value:0},uColor:{value:new THREE.Color(color)},uFall:{value:kind==='waterfall'?1:0},uRiver:{value:kind==='river'?1:0},uWetland:{value:wetland?1:0},uChannel:{value:kind==='channel'?1:0},uPond:{value:kind==='pond'?1:0},uPlunge:{value:kind==='pool'?1:0},uFlow:{value:flow},uSheenGain:{value:kind==='swamp'?.42:kind==='channel'?.62:0},uBankContact:{value:kind==='swamp'?.76:kind==='channel'?.42:0},uRootSiteCount:{value:0},uRootSites:{value:Array.from({length:5},()=>new THREE.Vector2(0,0))},uPadSiteCount:{value:0},uPadSites:{value:Array.from({length:12},()=>new THREE.Vector2(0,0))},uIslandSiteCount:{value:0},uIslandSites:{value:Array.from({length:4},()=>new THREE.Vector4(0,0,0,0))}},transparent:true,depthWrite:false,side:THREE.DoubleSide,
      vertexShader:`uniform float uTime;uniform float uWetland;uniform float uFall;uniform float uRiver;uniform float uPlunge;uniform float uPond;uniform float uChannel;uniform float uRootSiteCount;uniform vec2 uRootSites[5];uniform float uPadSiteCount;uniform vec2 uPadSites[12];uniform float uIslandSiteCount;uniform vec4 uIslandSites[4];uniform vec2 uFlow;varying vec2 vUv;varying vec3 vWorld;
        void main(){
          vec3 p=position;
          if(uFall>.5){
            // Flex the EXISTING falling sheet without moving source-bounded edges.
            float sideHold=sin(uv.x*3.14159265);
            float endHold=sin(uv.y*3.14159265);
            float folds=sin(uv.x*17.-uTime*2.2+uv.y*7.8)
              +.38*sin(uv.x*29.+uTime*1.45-uv.y*9.3);
            p.z+=.10*sideHold*endHold*folds;
          }
          if(uWetland>.5){
            // Animated surface relief, NOT a storm or revised current/topology claim.
            vec2 heading=normalize(uFlow+vec2(.0001,.0001));
            float phase=dot(uv-vec2(.5),heading)*30.-uTime*1.16;
            float crest=sin(phase)+.35*sin((uv.x+uv.y)*57.+uTime*.71);
            float shoreHold=1.-smoothstep(.65,.96,length((uv-vec2(.5))*2.));
            p.z+=crest*.018*shoreHold;
            // Existing channel flow ribbons now have a restrained moving surface.
            // Edge falloff retains the old water disk and unchanged shoreline.
            if(uChannel>.5){
              vec2 channelAlong=normalize(uFlow);
              vec2 channelAcross=vec2(-channelAlong.y,channelAlong.x);
              vec2 channelP=(uv-vec2(.5))*2.;
              float channelDistance=length(channelP);
              float channelLong=dot(channelP,channelAlong);
              float channelCross=dot(channelP,channelAcross);
              float channelBend=sin(channelLong*8.-uTime*.26)*.036;
              float channelPhase=(channelCross+channelBend)*31.
                +channelLong*7.-uTime*.90;
              float channelShear=smoothstep(.12,.68,abs(channelCross))
                *(1.-smoothstep(.75,.98,channelDistance));
              p.z+=.009*sin(channelPhase)*channelShear*shoreHold;
            }
            // Root ripples physically affect only the existing swamp mesh.
            // Reuse the five tree-wake sites, phase and perimeter fade; no added surface.
            if(uRootSiteCount>.5){
              float rootRelief=0.;
              for(int i=0;i<5;i++){
                if(float(i)>=uRootSiteCount)break;
                float rootDistance=length((uv-uRootSites[i])*vec2(21.,16.4));
                float rootFade=1.-smoothstep(.55,3.25,rootDistance);
                float rootPulse=pow(max(sin(rootDistance*7.1-uTime*1.6),0.),6.);
                rootRelief=max(rootRelief,rootPulse*rootFade);
              }
              p.z+=.006*rootRelief*shoreHold;
            }
            // Existing twelve drifting foliage pads also disturb the same swamp
            // water vertices; the pad centers and pulse phase are shared with
            // fragment-stage contact light. No new surface, shoreline or weather.
            if(uPadSiteCount>.5){
              float padRelief=0.;
              for(int i=0;i<12;i++){
                if(float(i)>=uPadSiteCount)break;
                float padDistance=length((uv-uPadSites[i])*vec2(21.,16.4));
                if(padDistance<1.05){
                  float padInterior=1.-smoothstep(.32,1.05,padDistance);
                  float padCrest=pow(max(sin(padDistance*12.-uTime*2.05),0.),8.);
                  padRelief=max(padRelief,padInterior*padCrest);
                }
              }
              p.z+=.0045*padRelief*shoreHold;
            }
            // Four inherited raised-ground banks disturb only adjacent existing water.
            // The footprint and island centers come directly from the local relief mesh.
            if(uIslandSiteCount>.5){
              float islandLap=0.;
              for(int i=0;i<4;i++){
                if(float(i)>=uIslandSiteCount)break;
                vec2 delta=(uv-uIslandSites[i].xy)/max(uIslandSites[i].zw,vec2(.00001));
                float islandRadius=length(delta);
                float contactBand=smoothstep(.86,.97,islandRadius)
                  *(1.-smoothstep(1.04,1.22,islandRadius));
                float lapPhase=islandRadius*24.-uTime*1.85+atan(delta.y,delta.x)*2.;
                islandLap=max(islandLap,contactBand*pow(max(sin(lapPhase),0.),4.));
              }
              p.z+=.007*islandLap*shoreHold;
            }
          }
          if(uRiver>.5){
            // Low-amplitude running surface on the EXISTING Temple upstream disc.
            // Physical motion fades before the unchanged source-bounded perimeter.
            float riverRadius=length((uv-vec2(.5))*2.);
            float riverHold=1.-smoothstep(.68,.96,riverRadius);
            float riverPhase=sin(uv.y*26.-uTime*1.9+sin(uv.x*8.)*.35);
            float riverCross=sin((uv.x+uv.y)*35.-uTime*2.2);
            p.z+=(.026*riverPhase+.009*riverCross)*riverHold;
          }
          if(uPlunge>.5){
            // Subtle water relief within the EXISTING Temple receiving-pool disc.
            // Rim vertices stay fixed: scenic motion, not new shoreline geometry.
            float plungeRadius=length((uv-vec2(.5))*2.);
            float plungeHold=1.-smoothstep(.64,.96,plungeRadius);
            float plungeWave=sin(plungeRadius*29.-uTime*1.75+sin(uv.x*13.)*.23);
            float plungeCross=sin((uv.x*16.-uv.y*12.)+uTime*.88);
            p.z+=(.017*plungeWave+.006*plungeCross)*plungeHold;
          }
          if(uPond>.5){
            // Existing Country Club Jackson pond; keep the inherited circular bank fixed.
            // The two already visible radial ripples now move interior vertices as water.
            vec2 pondP=(uv-vec2(.5))*2.;
            float pondRadius=length(pondP);
            float pondHold=1.-smoothstep(.66,.97,pondRadius);
            float pondA=sin(length((pondP-vec2(-.19,.08))*vec2(1.,1.25))*33.-uTime*2.4);
            float pondB=sin(length((pondP-vec2(.25,-.18))*vec2(1.2,1.))*25.-uTime*1.75);
            p.z+=(.012*pondA+.007*pondB)*pondHold;
            // Two existing illustrated Week 9 bridge facades meet this same pond:
            // candidate local x=-.88,+.71, inherited pond radius x=3.8 and z=2.3.
            // Their subtle contact wavelets do not infer actual bridge foundations.
            vec2 bridgeA=vec2(-.88/3.8,0.);
            vec2 bridgeB=vec2(.71/3.8,0.);
            float bridgeDistA=length((pondP-bridgeA)*vec2(1.,1.28));
            float bridgeDistB=length((pondP-bridgeB)*vec2(1.,1.28));
            float bridgeHoldA=1.-smoothstep(.08,.39,bridgeDistA);
            float bridgeHoldB=1.-smoothstep(.08,.39,bridgeDistB);
            float bridgePulseA=sin(bridgeDistA*37.-uTime*2.05);
            float bridgePulseB=sin(bridgeDistB*33.-uTime*1.82+1.2);
            p.z+=.0035*(bridgePulseA*bridgeHoldA+bridgePulseB*bridgeHoldB)*pondHold;
          }
          vUv=uv;vWorld=(modelMatrix*vec4(p,1.)).xyz;
          gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.);
        }`,
      fragmentShader:`uniform float uTime;uniform vec3 uColor;uniform float uFall;uniform float uRiver;uniform float uWetland;uniform float uChannel;uniform float uPond;uniform float uPlunge;uniform vec2 uFlow;uniform float uSheenGain;uniform float uBankContact;uniform float uRootSiteCount;uniform vec2 uRootSites[5];uniform float uPadSiteCount;uniform vec2 uPadSites[12];uniform float uIslandSiteCount;uniform vec4 uIslandSites[4];varying vec2 vUv;varying vec3 vWorld;void main(){float stripe;if(uFall>.5){
        stripe=pow(.5+.5*sin(vUv.x*21.+sin(vUv.y*9.-uTime*3.8)*1.9),3.);
        float foam=pow(.5+.5*sin(vUv.y*35.+uTime*9.+sin(vUv.x*13.)),4.);
        // The EXISTING physically displaced sheet now shades from its real screen-space
        // geometry. No new lighting or climate authority: only a restrained candidate
        // view response to folding, with no added geometry or transparency layers.
        vec3 faceCross=cross(dFdx(vWorld),dFdy(vWorld));
        float faceSize=length(faceCross);
        vec3 sheetNormal=faceSize>.00001?faceCross/faceSize:vec3(0.,0.,1.);
        vec3 eyeRay=normalize(cameraPosition-vWorld);
        float grazing=pow(1.-clamp(abs(dot(sheetNormal,eyeRay)),0.,1.),3.);
        float foldFacet=clamp(abs(sheetNormal.z),0.,1.);
        vec3 fallBase=mix(uColor,vec3(.84,.96,.89),.27+stripe*.14+foam*.17);
        vec3 fallTint=clamp(fallBase*(.945+.055*foldFacet)+vec3(.08,.10,.08)*(grazing*.32),0.,1.);
        // Narrow foam threads travel over the EXISTING folded falling sheet.
        // Bounded visual turbulence; no invented watercourse or climate input.
        float threadCoordinate=vUv.x*47.+sin(vUv.y*13.-uTime*1.17)*1.1;
        float foamThread=pow(max(sin(threadCoordinate),0.),10.);
        float brokenThread=.5+.5*sin(vUv.y*25.-uTime*3.6+vUv.x*8.);
        float sideFade=smoothstep(.02,.13,vUv.x)*(1.-smoothstep(.87,.98,vUv.x));
        float endFade=smoothstep(.025,.16,vUv.y)*(1.-smoothstep(.86,.985,vUv.y));
        float threadLight=foamThread*brokenThread*sideFade*endFade;
        fallTint=clamp(fallTint+vec3(.055,.071,.061)*threadLight,0.,1.);
        gl_FragColor=vec4(fallTint,.88);
      }else if(uWetland>.5){
      // Broken, low-contrast elongated reflections rather than high-frequency luminous grids.
      vec2 wetlandUv = vUv + uFlow * uTime;
      float meander=sin(wetlandUv.y*10.+sin(wetlandUv.x*6.)*.5)*.024;
      float breakup=.5+.5*sin(wetlandUv.y*17.+sin(wetlandUv.x*13.)*1.2);
      float currentPattern=sin((wetlandUv.x+meander)*44.+wetlandUv.y*11.+sin(wetlandUv.x*9.)*.8);
      float currentSheen=pow(max(currentPattern,0.),13.)*smoothstep(.45,.9,breakup);
      float eddy=pow(max(sin(length((wetlandUv-vec2(.52,.44))*vec2(1.,1.4))*30.-uTime*.15),0.),12.);
      float eddyFade=1.-smoothstep(.12,.42,length(wetlandUv-vec2(.52,.44)));
      float sediment=.5+.5*sin((wetlandUv.x-wetlandUv.y)*10.+sin(wetlandUv.y*6.)*.6);
      vec3 waterTint=mix(uColor,uColor*vec3(.84,.92,.80),sediment*.13);
      vec3 lowSheen=vec3(.13,.16,.14)*(currentSheen * uSheenGain);
      vec3 quietEddy=vec3(.04,.06,.05)*(eddy*eddyFade*.5*uSheenGain);
      // Local wavelets respond to five pre-existing illustrated tree stands.
      // Their size and phase remain scenic candidates; no extra water surface or flow.
      float rootWake=0.;
      // Five already illustrated root/stand anchors also project broken, subtle
      // canopy-tone patches onto the EXISTING swamp disc. Water-fragmented shade
      // is only scenic rendering; it is not measured light, wind or new ecology.
      float canopyShade=0.;
      for(int i=0;i<5;i++){
        if(float(i)>=uRootSiteCount)break;
        vec2 delta=(vUv-uRootSites[i])*vec2(21.,16.4);
        float rootDistance=length(delta);
        float wakeFade=1.-smoothstep(.55,3.25,rootDistance);
        float wakeCrest=pow(max(sin(rootDistance*7.1-uTime*1.6),0.),6.);
        rootWake=max(rootWake,wakeFade*wakeCrest);
        // The channel has no stand anchors; only the Mud Dogs swamp is affected.
        float canopyFade=1.-smoothstep(1.05,2.50,rootDistance);
        float wateryBreakup=.5+.5*sin(delta.x*3.8-uTime*.27)
                           *sin(delta.y*4.4+uTime*.21);
        canopyShade=max(canopyShade,canopyFade*(.66+.34*wateryBreakup));
      }
      float bankFade=1.-smoothstep(.78,.99,length((vUv-vec2(.5))*2.));
      // Water contact wakes follow the EXISTING twelve drifting foliage discs.
      // This is a scenic water shader response, not new source hydrology.
      float padContactWake=0.;
      if(uPadSiteCount>.5){
        for(int i=0;i<12;i++){
          if(float(i)>=uPadSiteCount)break;
          vec2 padDelta=(vUv-uPadSites[i])*vec2(21.,16.4);
          float padDistance=length(padDelta);
          if(padDistance<1.05){
            float padInterior=1.-smoothstep(.32,1.05,padDistance);
            float padCrest=pow(max(sin(padDistance*12.-uTime*2.05),0.),8.);
            padContactWake=max(padContactWake,padInterior*padCrest);
          }
        }
      }
      vec3 padContactSheen=vec3(.10,.14,.11)*(padContactWake*.42*bankFade);
      vec3 rootSheen=vec3(.13,.17,.13)*(rootWake*.68*bankFade);
      // Match the same four local raised-ground margins and vertex wave phases.
      // This modest animated contact light never creates a new shoreline.
      float islandLap=0.;
      if(uIslandSiteCount>.5){
        for(int i=0;i<4;i++){
          if(float(i)>=uIslandSiteCount)break;
          vec2 delta=(vUv-uIslandSites[i].xy)/max(uIslandSites[i].zw,vec2(.00001));
          float islandRadius=length(delta);
          float contactBand=smoothstep(.86,.97,islandRadius)
            *(1.-smoothstep(1.04,1.22,islandRadius));
          float lapPhase=islandRadius*24.-uTime*1.85+atan(delta.y,delta.x)*2.;
          islandLap=max(islandLap,contactBand*pow(max(sin(lapPhase),0.),4.));
        }
      }
      vec3 islandSheen=vec3(.095,.13,.10)*(islandLap*.30*bankFade);
      // Candidate moving channel-only glints, aligned to the EXISTING illustrative
      // flow vector. Water footprint, shoreline and topology remain unchanged.
      float channelRibbons=0.;
      if(uChannel>.5){
        vec2 alongAxis=normalize(uFlow);
        vec2 crossAxis=vec2(-alongAxis.y,alongAxis.x);
        vec2 p=(vUv-vec2(.5))*2.;
        float across=dot(p,crossAxis);
        float along=dot(p,alongAxis);
        float bend=sin(along*8.-uTime*.26)*.036;
        float fineLine=pow(max(sin((across+bend)*31.+along*7.-uTime*.90),0.),12.);
        float gaps=.5+.5*sin(along*23.-uTime*.53+sin(across*11.)*.72);
        float interior=1.-smoothstep(.70,.98,length(p));
        channelRibbons=fineLine*smoothstep(.34,.80,gaps)*interior;
      }
      vec3 channelSheen=vec3(.12,.17,.13)*(channelRibbons*.75);
      // Broken near-bank lapping light, confined to the existing wetland disc.
      // This is candidate visual depth, not a new shoreline or current record.
      float bankRadius=length((vUv-vec2(.5))*2.);
      float bankAngle=atan(vUv.y-.5,vUv.x-.5);
      float bankWobble=sin(bankAngle*9.+uTime*.31)*.009
                     +sin(bankAngle*17.-uTime*.20)*.006;
      float bankCrest=1.-smoothstep(.0,.022,abs(bankRadius-(.90+bankWobble)));
      float bankBreakup=.45+.55*(.5+.5*sin(bankAngle*13.+uTime*.63));
      float bankMask=smoothstep(.73,.84,bankRadius)
                     *(1.-smoothstep(.955,.995,bankRadius));
      float bankShelf=smoothstep(.79,.95,bankRadius)
                      *(1.-smoothstep(.965,1.,bankRadius));
      vec3 contactTint=waterTint*(1.-.055*bankShelf*uBankContact);
      // A shallow, bounded shadow-tone variation from EXISTING tree positions.
      // Keep the old water footprint and root-wake/perimeter masks unchanged.
      contactTint*=1.-.072*canopyShade*bankFade;
      vec3 contactLight=vec3(.09,.12,.073)*bankCrest*bankBreakup*bankMask*uBankContact;
      // Illustrative surface reflectance grows at grazing view angles.
      // Camera-facing tint affects only the EXISTING wetland material branch;
      // no water boundary, current, clock input, or lighting authority changes.
      vec3 viewToEye=normalize(cameraPosition-vWorld);
      float viewIncidence=clamp(abs(viewToEye.y),0.,1.);
      float grazingGain=.035+.21*pow(1.-viewIncidence,2.);
      contactTint=mix(contactTint,vec3(.31,.41,.37),grazingGain);
      // Existing moving surface now contributes restrained geometry-derived light.
      // Local relief does not interpret source climate, topology or light authority.
      // Use world-space derivatives of the *displaced* vertices; sign-independent
      // orientation also handles two-sided water and varying camera handedness.
      vec3 wetlandFace=cross(dFdx(vWorld),dFdy(vWorld));
      float wetlandFaceSize=length(wetlandFace);
      vec3 wetlandNormal=wetlandFaceSize>.00001?wetlandFace/wetlandFaceSize:vec3(0.,1.,0.);
      float reliefSlope=clamp((1.-clamp(abs(wetlandNormal.y),0.,1.))*14.,0.,.42);
      float reliefFacing=clamp(abs(dot(wetlandNormal,normalize(vec3(.30,.91,.27)))),0.,1.);
      vec3 reliefLight=vec3(.10,.15,.12)*reliefSlope*(.4+.6*reliefFacing)*bankFade;
      contactTint+=reliefLight+padContactSheen+islandSheen;
      gl_FragColor=vec4(contactTint+lowSheen+quietEddy+rootSheen+contactLight+channelSheen,.92);
      }else if(uRiver>.5){
       // Broken light on the EXISTING upstream sheet, not a flow/topology record.
       vec2 runningUv=vUv+vec2(0.,-uTime*.023);
       float broken=sin(runningUv.y*44.+sin(runningUv.x*11.)*1.15);
       float runGlint=pow(max(broken,0.),11.);
       float riverInterior=1.-smoothstep(.72,.96,length((vUv-vec2(.5))*2.));
       // Geometry-informed, two-sided glints follow the EXISTING displaced water.
        // This changes no river boundary or authoritative physical flow.
        vec3 riverFace=cross(dFdx(vWorld),dFdy(vWorld));
        float riverFaceSize=length(riverFace);
        vec3 riverNormal=riverFaceSize>.00001?riverFace/riverFaceSize:vec3(0.,1.,0.);
        float riverSlope=clamp((1.-clamp(abs(riverNormal.y),0.,1.))*12.,0.,.32);
        vec3 riverEye=normalize(cameraPosition-vWorld);
        float riverGrazing=pow(1.-clamp(abs(dot(riverNormal,riverEye)),0.,1.),2.);
        // Narrow broken foam lines move with inherited ordinary water time;
        // keep both existing water geometry and the quiet shoreline untouched.
        float riverFoamLine=pow(max(sin(runningUv.x*42.+sin(runningUv.y*13.)*.7),0.),14.);
        float riverFoamBreak=smoothstep(.47,.86,.5+.5*sin(runningUv.y*29.+vUv.x*6.-uTime*.72));
        float riverFoam=riverFoamLine*riverFoamBreak*riverInterior;
        vec3 riverOptics=vec3(.06,.085,.07)*riverFoam
          +vec3(.055,.075,.062)*(riverSlope*(.45+.55*riverGrazing)*riverInterior);
        gl_FragColor=vec4(clamp(uColor+vec3(.10,.15,.13)*(runGlint*riverInterior)+riverOptics,0.,1.),.88);
       }else if(uPond>.5){
      // Two gently expanding wave trains on the existing pond; no new source hydrology.
      vec2 p=(vUv-vec2(.5))*2.;
      float r1=length((p-vec2(-.19,.08))*vec2(1.,1.25));
      float r2=length((p-vec2(.25,-.18))*vec2(1.2,1.));
      float wave1=pow(max(sin(r1*33.0-uTime*2.4),0.),12.);
      float wave2=pow(max(sin(r2*25.0-uTime*1.75),0.),12.);
      float bank=1.-smoothstep(.68,.95,length(p));
      float ripple=(wave1*.6+wave2*.4)*bank;
      float micro=.5+.5*sin(p.x*7.3+sin(p.y*8.2+uTime*.17));
      vec3 pondTint=mix(uColor*.98,uColor*1.02,micro);
      // Low-intensity view response derives from the SAME displaced pond surface.
      // No new light source, current, shoreline or second water body.
      vec3 pondCross=cross(dFdx(vWorld),dFdy(vWorld));
      float pondCrossSize=length(pondCross);
      vec3 pondNormal=pondCrossSize>.00001?pondCross/pondCrossSize:vec3(0.,1.,0.);
      float pondRelief=clamp((1.-clamp(abs(pondNormal.y),0.,1.))*18.,0.,.34);
      vec3 pondLight=vec3(.08,.12,.10)*pondRelief*bank;
      // Narrow broken contact light follows the same two candidate masonry
      // arch bases, with the SAME local transforms as the physical wavelets.
      // No new light source, waterbody, current, shoreline or climate input.
      vec2 bridgeA=vec2(-.88/3.8,0.);
      vec2 bridgeB=vec2(.71/3.8,0.);
      float bridgeDistA=length((p-bridgeA)*vec2(1.,1.28));
      float bridgeDistB=length((p-bridgeB)*vec2(1.,1.28));
      float bridgeCrestA=(1.-smoothstep(.08,.43,bridgeDistA))
        *pow(max(sin(bridgeDistA*37.-uTime*2.05),0.),10.);
      float bridgeCrestB=(1.-smoothstep(.08,.43,bridgeDistB))
        *pow(max(sin(bridgeDistB*33.-uTime*1.82+1.2),0.),10.);
      float bridgeBreak=.5+.5*sin(p.y*27.+uTime*.68+p.x*11.);
      float bridgeContact=clamp((bridgeCrestA+bridgeCrestB)*bridgeBreak*bank,0.,1.);
      vec3 pondBridgeLight=vec3(.042,.061,.052)*bridgeContact;
      gl_FragColor=vec4(clamp(pondTint+vec3(.09,.13,.11)*ripple+pondLight+pondBridgeLight,0.,1.),.88);
      }else if(uPlunge>.5){
      // Small moving eddies beneath the EXISTING Temple plunge; not a new waterbody.
      vec2 p=(vUv-vec2(.5))*2.;
      float r=length(p*vec2(1.,1.16));
      float moving=sin(r*31.-uTime*2.1+.7*sin(vUv.x*14.+uTime*.35));
      float ring=pow(max(moving,0.),10.);
      float plungeCore=1.-smoothstep(.08,.45,r);
      float scatter=.5+.5*sin(p.x*34.+uTime*1.1)*sin(p.y*29.-uTime*.87);
      float foam=pow(scatter,3.)*plungeCore;
      float boundary=1.-smoothstep(.63,.94,length(p));
      // Local candidate impact follows the EXISTING falling sheet, landing
      // rings and receiving pool; it does not establish new water geography.
      // Broken moving foam stays within the original plunge-water footprint.
      vec2 impactUv=vec2(.5,.554);
      vec2 impactOffset=(vUv-impactUv)*vec2(2.,2.2);
      float impactRadius=length(impactOffset);
      float impactField=1.-smoothstep(.13,.52,impactRadius);
      float impactCrest=pow(max(sin(impactRadius*34.-uTime*2.8+sin(vUv.x*19.+uTime*.3)*.28),0.),9.);
      float impactBreakup=.45+.55*(.5+.5*sin(vUv.x*27.-vUv.y*17.+uTime*.57));
      float impactFoam=impactCrest*impactBreakup*impactField;
      vec3 plungeTint=uColor+vec3(.10,.14,.12)*(ring*.55+foam*.45)*boundary
        +vec3(.10,.15,.13)*impactFoam*boundary;
      // Optics follow the existing physically displaced receiving pool, not climate.
      vec3 plungeFace=cross(dFdx(vWorld),dFdy(vWorld));
      float plungeFaceSize=length(plungeFace);
      vec3 plungeNormal=plungeFaceSize>.00001?plungeFace/plungeFaceSize:vec3(0.,1.,0.);
      float plungeSlope=clamp((1.-clamp(abs(plungeNormal.y),0.,1.))*15.,0.,.34);
      vec3 plungeEye=normalize(cameraPosition-vWorld);
      float plungeGrazing=pow(1.-clamp(abs(dot(plungeNormal,plungeEye)),0.,1.),2.);
      float plungeFacet=plungeSlope*(.35+.65*plungeGrazing)*boundary;
      // Narrow, broken wake light follows the already-modeled waterfall impact.
      // Rim and bank remain dark; no new water mesh or hydrological path.
      vec2 wakeUv=(vUv-impactUv)*vec2(2.,2.2);
      float wakeSpoke=pow(max(sin(atan(wakeUv.y,wakeUv.x)*6.+impactRadius*28.-uTime*1.64),0.),12.);
      float wakeBreak=.5+.5*sin(impactRadius*37.-uTime*2.28+vUv.x*19.);
      float wakeField=smoothstep(.20,.34,impactRadius)
        *(1.-smoothstep(.59,.76,impactRadius))*boundary;
      float wakeGlint=wakeSpoke*sqrt(wakeBreak)*wakeField;
      plungeTint=clamp(plungeTint+vec3(.062,.088,.074)*plungeFacet
        +vec3(.042,.063,.052)*wakeGlint,0.,1.);
      gl_FragColor=vec4(plungeTint,.88);
      }else{float a=sin(vWorld.x*3.+uTime*.6+sin(vWorld.z*2.2))*sin(vWorld.z*3.8-uTime*.34);float rim=pow(clamp(a,0.,1.),6.);gl_FragColor=vec4(uColor+vec3(.25,.34,.24)*rim,.88);}}`});
    materials.set('water-'+water.length,m);return m;
  }
  function wetlandWaterDisk(name='Candidate wetland water surface',segments=48){
    // Reversible candidate mesh: exact same unit-circle perimeter, denser interior.
    // The edge is stationary under displacement so source-bound water footprints stay put.
    const rings=8,position=[0,0,0],uv=[.5,.5],indices=[];
    for(let r=1;r<=rings;r++)for(let i=0;i<segments;i++){
      const angle=i*2*Math.PI/segments,radius=r/rings;
      const x=radius*Math.cos(angle),y=radius*Math.sin(angle);
      position.push(x,y,0);uv.push(.5+.5*x,.5+.5*y);
    }
    for(let i=0;i<segments;i++)indices.push(0,1+i,1+(i+1)%segments);
    for(let r=1;r<rings;r++)for(let i=0;i<segments;i++){
      const next=(i+1)%segments;
      const a=1+(r-1)*segments+i,b=1+(r-1)*segments+next;
      const c=1+r*segments+i,d=1+r*segments+next;
      indices.push(a,c,d,a,d,b);
    }
    const geometry=new THREE.BufferGeometry();
    geometry.name=name;
    geometry.setAttribute('position',new THREE.Float32BufferAttribute(position,3));
    geometry.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));
    geometry.setIndex(indices);geometry.computeVertexNormals();geometry.computeBoundingSphere();
    return geometry;
  }
  function pool(g,kind,x,y,z,rx,rz,color='#387e75'){
    const m=waterMaterial(kind,color);
    const geometry=kind==='swamp'||kind==='channel'?wetlandWaterDisk():kind==='river'?wetlandWaterDisk('Candidate Temple upstream river surface'):kind==='pool'?wetlandWaterDisk('Candidate Temple plunge pool surface',40):kind==='pond'?wetlandWaterDisk('Candidate Country Club pond surface',40):new THREE.CircleGeometry(1,40);
    const o=mesh(g,geometry,m,x,y,z);o.rotation.x=-Math.PI/2;o.scale.set(rx,rz,1);o.castShadow=false;o.renderOrder=2;water.push({kind,material:m,mesh:o});return o;
  }
  function waterfall(g,x,y,z,width,drop){
    const m=waterMaterial('waterfall','#67aaa0'),o=mesh(g,new THREE.PlaneGeometry(width,drop,24,32),m,x,y-drop/2,z);o.castShadow=false;o.renderOrder=2;water.push({kind:'waterfall',material:m,mesh:o});
    // Moving landing ripples, not frozen metallic-looking torus props.
    // Candidate local detail only: no claim about actual approved hydrology geometry.
    for(let i=0;i<4;i++){
      const m=new THREE.ShaderMaterial({uniforms:{uTime:{value:0},uPhase:{value:i/4}},transparent:true,depthWrite:false,side:THREE.DoubleSide,
        vertexShader:`uniform float uTime;uniform float uPhase;varying float vFade;void main(){float progress=fract(uTime*.19+uPhase);vec3 p=position;p.xy*=.55+progress*2.65;vFade=pow(1.-progress,1.5);gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.);}`,
        fragmentShader:`varying float vFade;void main(){gl_FragColor=vec4(.75,.95,.83,.43*vFade);}`});
      materials.set('landing-ripple-'+i,m);
      const ring=mesh(g,new THREE.RingGeometry(.89,1,48),m,x,y-drop+.10+i*.008,z+.9);
      ring.rotation.x=-Math.PI/2;ring.castShadow=false;ring.receiveShadow=false;ring.renderOrder=3;
      water.push({kind:'landing-ripple',material:m,mesh:ring});
    }
  }
  function waterfallMist(g,x,y,z,drop){
    // Diffuse spray at the EXISTING candidate waterfall plunge, not a weather storm.
    // Illustrative environmental detail: no new watercourse, climate fact, or Atlas geometry.
    const pos=[],phase=[],drift=[];
    for(let i=0;i<144;i++){
      const a=i*2.39996323,spread=.16+.83*(.5+.5*Math.sin(i*7.37));
      const dx=Math.cos(a)*spread*1.46,dz=Math.sin(a)*spread*1.02;
      pos.push(x+dx, y-drop+.20+.62*(.5+.5*Math.sin(i*3.13)),z+.83+dz);
      phase.push((i*.61803398875)%1);
      drift.push(Math.sin(i*1.73),.5+.5*Math.cos(i*2.11),Math.cos(i*.97));
    }
    const geo=new THREE.BufferGeometry();
    geo.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));
    geo.setAttribute('aPhase',new THREE.Float32BufferAttribute(phase,1));
    geo.setAttribute('aDrift',new THREE.Float32BufferAttribute(drift,3));
    geo.computeBoundingSphere();geometries.add(geo);
    const m=new THREE.ShaderMaterial({
      uniforms:{uTime:{value:0}},transparent:true,depthWrite:false,blending:THREE.NormalBlending,
      vertexShader:`uniform float uTime;attribute float aPhase;attribute vec3 aDrift;varying float vOpacity;
        void main(){
          float age=fract(aPhase+uTime*(.105+.048*aDrift.y));
          vec3 p=position;
          // Existing plunge spray follows a small rise-and-fall arc instead of
          // rising forever. All motion is local to the existing emitter.
          // Driven only by inherited uTime; no additional input or object.
          float launch=age*(.95+.35*aDrift.y);
          float fall=age*age*(.90+.20*aDrift.y);
          p.x+=aDrift.x*age*(.12+.34*age)
            +sin(uTime*.31+aPhase*35.)*.08*age;
          p.y+=launch-fall;
          p.z+=aDrift.z*age*(.10+.32*age);
          vec4 view=modelViewMatrix*vec4(p,1.);
          gl_PointSize=clamp(650./max(12.,-view.z),2.4,25.)*(1.-age*.22);
          gl_Position=projectionMatrix*view;
          vOpacity=pow(max(sin(age*3.14159265),0.),.75)*(.50+.38*aDrift.y);
        }`,
      fragmentShader:`varying float vOpacity;
        void main(){
          float radial=length(gl_PointCoord-vec2(.5));
          float feather=1.-smoothstep(.08,.49,radial);
          gl_FragColor=vec4(.75,.85,.78,feather*vOpacity*.22);
        }`
    });
    materials.set('candidate-temple-plunge-mist',m);ambientMotion.push(m);
    const o=new THREE.Points(geo,m);o.name='Candidate waterfall plunge mist';
    o.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',sourceLandmark:'waterfall',navigable:false,routeIds:[]};
    o.frustumCulled=false;o.renderOrder=4;g.add(o);
  }
  function templeStoneTread(g,j){
    // Sculpt ONLY the nine pre-existing Temple stair treads, not their footprint,
    // elevation, materials, circulation, chronology or any Atlas topology.
    const width=2.8,thickness=.24,depth=.55;
    const geometry=new THREE.BoxGeometry(width,thickness,depth,28,1,8);
    geometry.name='Candidate Temple recessed stone stair tread';
    const position=geometry.getAttribute('position');
    for(let i=0;i<position.count;i++){
      const x=position.getX(i),y=position.getY(i),z=position.getZ(i);
      // All top/perimeter edges and the complete bottom remain identical.
      if(y<thickness/2-.000001||Math.abs(x)>=width/2-.000001||Math.abs(z)>=depth/2-.000001)continue;
      const seamDistance=Math.min(Math.abs(x+.9),Math.abs(x),Math.abs(x-.9));
      const joint=Math.max(0,1.-seamDistance/.12);
      const mineralWear=.0035*(.5+.5*Math.sin(x*19.1+j*1.7)*Math.sin(z*23.8-j*.93));
      position.setY(i,y-Math.min(.026,.021*joint+mineralWear));
    }
    position.needsUpdate=true;
    geometry.computeVertexNormals();geometry.computeBoundingSphere();
    const tread=mesh(g,geometry,j%2?stone:edge,1,j*.24+thickness/2,5.3-j*.43);
    tread.name='Candidate Temple stone tread relief';
    tread.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',sourceLandmark:'temple stone',
      originalDimensions:[width,thickness,depth],originalStepIndex:j,
      staticRelief:true,navigable:false,routeIds:[],principalCharacters:[]};
    return tread;
  }
  function templeCliff(g,x,y,z,sx,sy,sz,m,index){
    // Sculpt ONLY the three existing Temple cliff rocks. Retain each original
    // transform, material and enclosing unit-sphere footprint (inward cuts only).
    // Bedding is illustrative relief, not a geological or new-landmark claim.
    const geo=new THREE.IcosahedronGeometry(1,4);
    geo.name='Candidate Temple cliff strata geometry';
    const p=geo.getAttribute('position');
    for(let i=0;i<p.count;i++){
      const px=p.getX(i),py=p.getY(i),pz=p.getZ(i);
      const bedding=(py+.08*Math.sin(px*5.+pz*2.3+index*.4))*22.;
      const seam=Math.pow(Math.max(0,Math.cos(bedding)),10);
      const chipped=.5+.5*Math.sin(px*11.7+py*8.9+pz*13.5+index*1.5);
      const inset=.009+.048*seam+.013*chipped;
      const radius=1-inset;
      p.setXYZ(i,px*radius,py*radius,pz*radius);
    }
    p.needsUpdate=true;geo.computeVertexNormals();geo.computeBoundingSphere();
    const o=mesh(g,geo,m,x,y,z);
    o.scale.set(sx,sy,sz);o.rotation.set(.19+x*.07,z*.16,.1);
    o.name='Candidate Temple cliff strata relief';
    o.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',sourceLandmark:'waterfall',
      originalDimensions:[sx,sy,sz],originalCliffIndex:index,
      staticRelief:true,navigable:false,routeIds:[],principalCharacters:[]};
    return o;
  }
  function templeFlutedPillar(g,i){
    // Existing five Temple shafts only: original stone material, location,
    // height, capitals and enclosing radii. Scenic sculpting, not new canon.
    const h=3.1,top=.23,base=.29;
    const geometry=new THREE.CylinderGeometry(top,base,h,32,8);
    geometry.name='Candidate Temple fluted stone pillar geometry';
    const position=geometry.getAttribute('position');
    for(let j=0;j<position.count;j++){
      const x=position.getX(j),y=position.getY(j),z=position.getZ(j);
      // Preserve both original end rings and caps without modification.
      if(Math.abs(y)>=h/2-.000001)continue;
      const angle=Math.atan2(z,x);
      const flute=Math.pow(.5+.5*Math.cos(angle*8+i*.15),6);
      const endHold=Math.pow(Math.sin(Math.PI*(y/h+.5)),2);
      const depth=.046*flute*endHold*(.82+.18*(.5+.5*Math.sin(y*7+i)));
      position.setXYZ(j,x*(1-depth),y,z*(1-depth));
    }
    position.needsUpdate=true;geometry.computeVertexNormals();geometry.computeBoundingSphere();
    const o=mesh(g,geometry,stone,1+i*1.05,2.3+h/2,1.1);
    o.name='Candidate Temple fluted stone pillar';
    o.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',sourceLandmark:'temple stone',
      originalDimensions:[top,base,h],originalPillarIndex:i,staticRelief:true,
      navigable:false,routeIds:[],principalCharacters:[]};
    return o;
  }
  function temple(g){
    // Source-supported raised stone temple, vegetation and falling water; exact forms are candidates.
    templeCliff(g,-6,3,-3,4,6,3,mat('#677163'),0);templeCliff(g,-8,2,-4,3.6,4.8,3.2,mat('#777b6a'),1);templeCliff(g,-5,1,-5,4,4,3.6,mat('#596955'),2);
    for(let j=0;j<4;j++)box(g,1,j*.58,-.8,9-j*1.1,.58,7-j*.75,j%2?edge:stone);
    for(let j=0;j<9;j++)templeStoneTread(g,j);
    box(g,1,2.3,-1,5.2,2.8,3.6,dark);
    for(let i=-2;i<=2;i++){templeFlutedPillar(g,i);box(g,1+i*1.05,5.34,1.1,.7,.22,.65,edge);}
    box(g,1,5.5,-.1,6.7,.4,5,edge);box(g,1,5.9,-.1,6.1,.32,4.5,stone);box(g,1,6.22,-.1,5.2,.3,3.9,dark);
    box(g,1,2.32,1.02,1.25,2.3,.15,mat('#263c35'));
    for(let i=0;i<15;i++)box(g,-2.1+i*.44,5.52,2.43,.16,.25,.15,dark);
    for(let i=0;i<12;i++){const a=i*2.399;rock(g,Math.cos(a)*(5+i%3),.3,Math.sin(a)*(4+i%2),.7,.45,.6,i%3?stone:moss);}
    pool(g,'river',-5.8,7.2,-1.5,2.2,2.6,'#458c7d');waterfall(g,-5.8,7.2,1.8,2.15,6.9);pool(g,'pool',-5.8,.30,3,3.8,2.8,'#3b8c7e');waterfallMist(g,-5.8,7.2,1.8,6.9);
    for(const [x,z,s]of[[-10,-1,1.5],[-9,5,1.25],[-2,-6,1.4],[6,-4,1.5],[7,1,1.3],[6,6,1.1],[-2,7,.9]])canopy(g,x,0,z,s);
    box(g,2.7,2.31,1.9,.8,.05,.6,moss);box(g,-1.8,1.16,2.2,1.1,.04,.8,moss);
  }
  function wetlandShoreline(g,landformMaterial){
    // Source supports mud channels, raised ground and cypress-like wetlands.
    // This bank is ONLY a local candidate transition around the existing visual pool:
    // it creates no river/shoreline topology and deliberately leaves the water ellipse visible.
    const sides=96,rings=3,positions=[],colors=[],faces=[];
    const tones=['#414c3a','#5e6547','#354d39'].map(c=>new THREE.Color(c));
    for(let i=0;i<=sides;i++){
      const a=i/sides*Math.PI*2;
      const waviness=Math.sin(a*7+.3)*.018+Math.sin(a*13-.8)*.009;
      const radii=[1.019+Math.sin(a*11)*.006,1.079+waviness,1.188+waviness*1.6+Math.sin(a*5)*.012];
      const levels=[.102,.235+Math.sin(a*9)*.018,.105+Math.cos(a*6)*.018];
      for(let j=0;j<rings;j++){
        const r=radii[j];positions.push(Math.cos(a)*10.5*r,levels[j],Math.sin(a)*8.2*r);
        const tone=tones[j].clone().multiplyScalar(.965+.035*Math.sin(a*8+.8));
        colors.push(tone.r,tone.g,tone.b);
      }
      if(i<sides)for(let j=0;j<rings-1;j++){
        const p=i*rings+j,q=p+rings;faces.push(p,p+1,q,p+1,q+1,q);
      }
    }
    const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));
    geo.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));geo.setIndex(faces);geo.computeVertexNormals();
    // Opaque shared vertex-color material: landform depth and palettes survive batching.
    const bank=mesh(g,geo,landformMaterial,0,0,0);bank.name='Candidate wetland shoreline transition';
    bank.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',sourceLandmarks:['mud channels','raised ground']};
    bank.castShadow=false;bank.renderOrder=1;
  }
  function wetlandEmergentVegetation(g){
    // Read-only visualization of vegetation on the EXISTING candidate bank.
    // No new botanical species, river boundary, crossing, named landmark or canon.
    // Individual blade triangles share one GPU draw; roots stay fixed as tips sway.
    const pos=[],sway=[],tints=[];
    const palette=['#496944','#65815a','#55754b','#778962','#5b7657'].map(c=>new THREE.Color(c));
    const bladesPerTuft=4,tufts=96;
    for(let i=0;i<tufts;i++){
      const patch=Math.floor(i/6),within=i%6;
      const a=patch/16*Math.PI*2+(within-2.5)*.033+Math.sin(i*7.17)*.009;
      const r=1.105+.067*(.5+.5*Math.sin(i*2.19));
      const x=Math.cos(a)*10.5*r,z=Math.sin(a)*8.2*r;
      const y=.175+.042*(.5+.5*Math.sin(a*9.));
      for(let j=0;j<bladesPerTuft;j++){
        const phase=i*2.399+j*2.04;
        const b=a+j*2.094+Math.sin(i*.82)*.25;
        const dx=Math.cos(b),dz=Math.sin(b);
        const h=.38+((i*13+j*7)%19)*.043;
        const width=.047+(i+j*3)%5*.012;
        const tipX=x+Math.sin(b*2.+i)*.10,tipZ=z+Math.cos(b*2.+i)*.07;
        const tint=palette[(i+j)%palette.length];
        const verts=[x-dx*width,y,z-dz*width,x+dx*width,y,z+dz*width,tipX,y+h,tipZ];
        pos.push(...verts);
        sway.push(phase,0,phase,0,phase,1);
        for(let k=0;k<3;k++)tints.push(tint.r,tint.g,tint.b);
      }
    }
    const geo=new THREE.BufferGeometry();
    geo.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));
    geo.setAttribute('aSway',new THREE.Float32BufferAttribute(sway,2));
    geo.setAttribute('aTint',new THREE.Float32BufferAttribute(tints,3));
    geo.computeVertexNormals();geo.computeBoundingSphere();
    const m=new THREE.ShaderMaterial({
      uniforms:{uTime:{value:0}},side:THREE.DoubleSide,depthWrite:true,
      vertexShader:`uniform float uTime;attribute vec2 aSway;attribute vec3 aTint;varying vec3 vTint;varying float vHeight;
      void main(){vTint=aTint;vHeight=aSway.y;
      float flutter=sin(uTime*.77+aSway.x)+.32*sin(uTime*1.29+aSway.x*1.41);
      vec3 p=position;p.x+=flutter*aSway.y*.16;p.z+=flutter*aSway.y*.07;
      gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.);}`,
      fragmentShader:`varying vec3 vTint;varying float vHeight;
      void main(){gl_FragColor=vec4(vTint*(.78+.16*vHeight),1.);
      #include <tonemapping_fragment>
      #include <colorspace_fragment>
      }`
    });
    materials.set('candidate-wetland-emergent',m);ambientMotion.push(m);
    const o=mesh(g,geo,m,0,0,0);o.name='Candidate wetland emergent vegetation';
    o.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',sourceEnvironment:['cypress-like wetlands','raised ground'],navigable:false,routeIds:[]};
    o.castShadow=false;o.receiveShadow=false;
  }
  function wetlandRaisedGround(g,islands,landformMaterial){
    // Source: permanent Mud Dogs raised ground and Southern Wetlands mudflats.
    // Only the pre-existing FOUR local illustrative island footprints are sculpted;
    // this creates no canonical shoreline, path, travel route or new waterway.
    const sides=28,radii=[.27,.53,.77,.955],heights=[.88,.73,.36,-.12];
    const positions=[],colors=[],islandIds=[],faces=[];
    const strata=['#697456','#626952','#555844','#393e35'].map(v=>new THREE.Color(v));
    // Scenic material transitions on the SAME four raised-ground footprints.
    // Lower shelves retain a dark wet-mud wash; higher terraces show broken silt.
    const marginMud=new THREE.Color('#26382d'),siltDust=new THREE.Color('#84775b');
    islands.forEach(([cx,cy,cz,sx,sy,sz],island)=>{
      const start=positions.length/3;
      function vertex(x,y,z,color){positions.push(x,y,z);colors.push(color.r,color.g,color.b);islandIds.push(island);}
      vertex(cx,cy+sy*(1.03+.035*Math.sin(island*3.3)),cz,strata[0]);
      for(let r=0;r<radii.length;r++)for(let i=0;i<sides;i++){
        const theta=i*2*Math.PI/sides;
        const jostle=1+Math.sin(theta*5+island*1.4)*.038+Math.sin(theta*9-island*.8)*.021;
        const radial=radii[r]*jostle;
        const yVariation=(Math.sin(theta*4+island*.7)*.046+Math.cos(theta*7-island*1.2)*.029)*(1-r*.20);
        const elevation=cy+sy*(heights[r]+yVariation);
        const wetWeight=(r===3?.34:r===2?.15:0)*(.86+.14*Math.sin(theta*6.8+island*.91));
        const siltWeight=(r===1?.12:r===2?.085:0)*(.5+.5*Math.sin(theta*11.+island*1.3));
        const tint=strata[r].clone().lerp(marginMud,wetWeight).lerp(siltDust,siltWeight)
          .multiplyScalar(.90+.095*(.5+.5*Math.sin(theta*8+island+r)));
        vertex(cx+Math.cos(theta)*sx*radial,elevation,cz+Math.sin(theta)*sz*radial,tint);
      }
      for(let i=0;i<sides;i++)faces.push(start,start+1+(i+1)%sides,start+1+i);
      for(let r=0;r<radii.length-1;r++)for(let i=0;i<sides;i++){
        const a=start+1+r*sides+i,b=start+1+r*sides+(i+1)%sides;
        const c=a+sides,d=b+sides;faces.push(a,b,c,b,d,c);
      }
    });
    const geo=new THREE.BufferGeometry();
    geo.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));
    geo.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));
    geo.setAttribute('aIsland',new THREE.Float32BufferAttribute(islandIds,1));
    geo.setIndex(faces);geo.computeVertexNormals();geo.computeBoundingSphere();
    // Color strata are compiled with the shoreline in the opaque vertex-color pass.
    const relief=mesh(g,geo,landformMaterial,0,0,0);
    relief.name='Candidate wetland raised-ground relief';
    relief.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',sourceEnvironment:['raised ground','mudflats'],
      islandCount:islands.length,routeIds:[],navigable:false};
    relief.renderOrder=1;
  }
  function wetlandWaterlineRoots(g,stands){
    // Candidate tapering root projections around ONLY existing illustrated tree stands.
    // This is not a species identification, new hydrological feature or navigable ground.
    const positions=[],uv=[],indices=[],sides=7,rings=3;let rootCount=0;
    for(let i=0;i<stands.length;i++){
      const [cx,cz]=stands[i];
      for(let j=0;j<5;j++){
        const a=j/5*Math.PI*2+i*.39,reach=.53+.17*((i+j)%4);
        const x=cx+Math.cos(a)*reach,z=cz+Math.sin(a)*reach;
        // Keep all projected roots INSIDE the existing illustrative swamp-water rim.
        if(Math.hypot(x/10.5,z/8.2)>.91)continue;
        const start=positions.length/3,h=.35+.065*((i*3+j)%6);
        const broad=.11+.02*(i%3);
        for(let r=0;r<rings;r++){
          const t=r/(rings-1),radius=r===0?broad:r===1?broad*.73:.008;
          const bend=.045*t*t;
          for(let k=0;k<sides;k++){
            const theta=k/sides*Math.PI*2;
            positions.push(x+Math.cos(theta)*radius+Math.cos(a+.7)*bend,
              .105+h*t,z+Math.sin(theta)*radius+Math.sin(a+.7)*bend);
            uv.push(k/sides,t);
          }
        }
        for(let r=0;r<rings-1;r++)for(let k=0;k<sides;k++){
          const next=(k+1)%sides,a0=start+r*sides+k,b0=start+r*sides+next;
          const c0=a0+sides,d0=b0+sides;
          indices.push(a0,c0,b0,b0,c0,d0);
        }
        rootCount++;
      }
    }
    const geo=new THREE.BufferGeometry();
    geo.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));
    geo.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));
    geo.setIndex(indices);geo.computeVertexNormals();geo.computeBoundingSphere();
    // Existing trunk material/UVs let the static batcher reuse an existing draw group.
    const knees=mesh(g,geo,trunk,0,0,0);
    knees.name='Candidate wetland waterline root knees';
    knees.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',
      sourceEnvironment:['cypress-like wetlands','mud channels'],
      sourceStands:stands.length,rootCount,navigable:false,routeIds:[]};
    return knees;
  }
  function wetlandCanopyFringe(g,crowns){
    // Read-only hanging fringe of the SAME 14 illustrated Mud Dogs tree crowns.
    // Foliage profile is a local scenic candidate, not a plant species or ecology claim.
    // Opaque ribbons reuse existing foliage material and the static foliage draw batch.
    const positions=[],uv=[],indices=[],sway=[];let strands=0;
    for(const {i,x,y,z,h} of crowns){
      for(let k=0;k<4;k++){
        const a=k*Math.PI/2+i*.31+.18,r=.84+.06*((k+i)%3);
        const cx=x+Math.cos(a)*r,cz=z+Math.sin(a)*r;
        const top=y+h-.22+.10*(k%2),length=1.08+.12*((k+2*i)%5);
        const phase=i*1.17+k*2.399;
        // Two crossed planes, each with a separately wound front and back.
        // This avoids changing the shared foliage material's face-culling contract.
        for(let plane=0;plane<2;plane++)for(let face=0;face<2;face++){
          const axis=a+plane*Math.PI/2+.37,dx=Math.cos(axis),dz=Math.sin(axis);
          const nx=-dz,nz=dx,offset=(face===0?1:-1)*.003;
          const start=positions.length/3;
          for(let row=0;row<4;row++){
            const t=row/3,bend=.085*Math.sin(t*Math.PI)+.035*t*t;
            const bx=cx+Math.cos(a+Math.PI/2)*bend+nx*offset;
            const bz=cz+Math.sin(a+Math.PI/2)*bend+nz*offset;
            const width=(.18+.024*((i+k)%3))*(1-.80*t)*(row===2?1.12:1);
            const yy=top-length*t;
            positions.push(bx-dx*width,yy,bz-dz*width,bx+dx*width,yy,bz+dz*width);
            uv.push(0,1-t,1,1-t);
            sway.push(phase,t,phase,t);
          }
          for(let row=0;row<3;row++){
            const p=start+row*2,q=p+2;
            if(face===0)indices.push(p,q,p+1,p+1,q,q+1);
            else indices.push(p,p+1,q,p+1,q+1,q);
          }
        }
        strands++;
      }
    }
    const geo=new THREE.BufferGeometry();
    geo.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));
    geo.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));
    geo.setAttribute('aSway',new THREE.Float32BufferAttribute(sway,2));
    geo.setIndex(indices);geo.computeVertexNormals();geo.computeBoundingSphere();
    // Preserve GPU culling even as hanging tips lean within their inherited crown area.
    geo.boundingSphere.radius+=.22;
    // One independent GPU animated mesh for the PRE-EXISTING 56 strands.
    // The former static foliage batch remains unchanged; this adds exactly one
    // deliberately budgeted draw instead of reauthoring the 14 tree crowns.
    const fringeMaterial=new THREE.ShaderMaterial({
      uniforms:{uTime:{value:0},uFoliage:{value:new THREE.Color('#607b54')}},
      side:THREE.DoubleSide,transparent:false,depthWrite:true,
      vertexShader:`uniform float uTime;attribute vec2 aSway;varying float vLower;
        void main(){
          vLower=aSway.y;
          vec3 p=position;
          // Top row remains stationary. Ordinary ambient motion is NOT storm-driven.
          float tipWeight=aSway.y*aSway.y;
          float oscillation=.12*sin(uTime*.62+aSway.x)
                           +.04*sin(uTime*1.07+aSway.x*1.57);
          p.x+=oscillation*tipWeight;
          p.z+=oscillation*tipWeight*.62;
          gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.);
        }`,
      fragmentShader:`uniform vec3 uFoliage;varying float vLower;
        void main(){gl_FragColor=vec4(uFoliage*(.94-.10*vLower),1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }`
    });
    materials.set('candidate-wetland-canopy-fringe',fringeMaterial);
    ambientMotion.push(fringeMaterial);
    const fringe=mesh(g,geo,fringeMaterial,0,0,0);
    // Dynamic vegetation must not claim a refreshed static shadow map each tick.
    fringe.castShadow=false;fringe.receiveShadow=false;
    fringe.name='Candidate Mud Dogs canopy fringe';
    fringe.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',sourceStands:crowns.length,
      strands,triangles:indices.length/3,navigable:false,routeIds:[],principalCharacters:[],
      ambientClock:'ORDINARY_ENVIRONMENT',illustrativeMaxTipDisplacement:.19,drawBudgetDelta:1};
    return fringe;
  }


  function wetlandWaterlineStems(g){
    // Animate only the 26 pre-existing, green cylindrical waterline stems.
    // Keep every established illustrative root, height, radius and 4-sided tube.
    const positions=[],normals=[],sway=[],faces=[],count=26;
    for(let i=0;i<count;i++){
      const a=i*2.399,r=6.8+Math.sin(i)*.8,x=Math.cos(a)*r,z=Math.sin(a)*r;
      const h=.55+(i%3)*.15,base=.1,phase=i*2.399;
      const original=new THREE.CylinderGeometry(.04,.06,h,4);
      const p=original.getAttribute('position'),n=original.getAttribute('normal'),idx=original.getIndex();
      const start=positions.length/3;
      for(let j=0;j<p.count;j++){
        const y=p.getY(j),weight=Math.max(0,Math.min(1,(y+h/2)/h));
        positions.push(p.getX(j)+x,base+h/2+y,p.getZ(j)+z);
        normals.push(n.getX(j),n.getY(j),n.getZ(j));
        sway.push(phase,weight);
      }
      for(let j=0;j<idx.count;j++)faces.push(start+idx.getX(j));
      original.dispose();
    }
    const geo=new THREE.BufferGeometry();
    geo.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));
    geo.setAttribute('normal',new THREE.Float32BufferAttribute(normals,3));
    geo.setAttribute('aSway',new THREE.Float32BufferAttribute(sway,2));
    geo.setIndex(faces);geo.computeBoundingSphere();
    // Maximum tip sway < .091 local units, so retain a .10 culling envelope.
    geo.boundingSphere.radius+=.10;
    const m=new THREE.ShaderMaterial({
      uniforms:{uTime:{value:0},uStem:{value:new THREE.Color('#77944b')}},
      transparent:false,depthWrite:true,side:THREE.DoubleSide,
      vertexShader:`uniform float uTime;attribute vec2 aSway;varying float vTip;
        void main(){
          vTip=aSway.y;vec3 p=position;
          float bend=.060*sin(uTime*.65+aSway.x)+.018*sin(uTime*1.17+aSway.x*1.33);
          float rooted=aSway.y*aSway.y;
          p.x+=bend*rooted;p.z+=bend*rooted*.58;
          gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.);
        }`,
      fragmentShader:`uniform vec3 uStem;varying float vTip;
        void main(){gl_FragColor=vec4(uStem*(.90+.08*vTip),1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }`
    });
    materials.set('candidate-wetland-waterline-stems',m);ambientMotion.push(m);
    const stems=mesh(g,geo,m,0,0,0);
    stems.castShadow=false;stems.receiveShadow=false;
    stems.name='Candidate Mud Dogs waterline stems';
    stems.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',
      sourceEnvironment:['mud channels','cypress-like wetlands'],
      stems:count,rootStationsPreserved:true,navigable:false,routeIds:[],principalCharacters:[],
      ambientClock:'ORDINARY_ENVIRONMENT',illustrativeMaxTipDisplacement:.091,drawBudgetDelta:1};
    return stems;
  }

  // One shared set of the pre-existing foliage-disc centers and independent phases.
  const floatingFoliageSites=Array.from({length:12},(_,i)=>({
    x:Math.sin(i*5)*7,z:Math.cos(i*9)*5,r:.18+(i%3)*.08,phase:i*2.399
  }));
  let floatingContactSites=null;
  function syncFloatingContactSites(time){
    if(!floatingContactSites)return;
    for(let i=0;i<floatingFoliageSites.length;i++){
      const site=floatingFoliageSites[i];
      const drift=.075*Math.sin(time*.35+site.phase)+.025*Math.sin(time*.79+site.phase*1.71);
      // Existing pool plane is X-rotated -PI/2: world +Z maps to texture -V.
      floatingContactSites[i].set(.5+(site.x+drift)/21,.5-(site.z+drift*.57)/16.4);
    }
  }
  function wetlandFloatingFoliage(g){
    // Rework ONLY the twelve existing leaf-colored water discs, at their original
    // candidate centers and radii. No additional pads, wetland habitat or canon.
    const positions=[],phases=[],edges=[],tints=[],indices=[];
    const palette=['#5a774f','#6e8257','#536f50','#637e55'].map(v=>new THREE.Color(v));
    const count=floatingFoliageSites.length,sides=9;
    for(let i=0;i<count;i++){
      const {x:cx,z:cz,r,phase}=floatingFoliageSites[i];
      const start=positions.length/3,tint=palette[i%palette.length];
      // Each former flat circle becomes an irregular but never larger fan.
      const add=(x,z,edge)=>{
        positions.push(x,.16,z);phases.push(phase);edges.push(edge);
        tints.push(tint.r,tint.g,tint.b);
      };
      add(cx,cz,0);
      for(let k=0;k<sides;k++){
        const angle=k*2*Math.PI/sides;
        const radius=r*(.91+.07*Math.sin(angle*3+i*1.37));
        add(cx+Math.cos(angle)*radius,cz+Math.sin(angle)*radius,1);
      }
      for(let k=0;k<sides;k++)indices.push(start,start+1+(k+1)%sides,start+1+k);
    }
    const geo=new THREE.BufferGeometry();
    geo.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));
    geo.setAttribute('aPhase',new THREE.Float32BufferAttribute(phases,1));
    geo.setAttribute('aEdge',new THREE.Float32BufferAttribute(edges,1));
    geo.setAttribute('aTint',new THREE.Float32BufferAttribute(tints,3));
    geo.setIndex(indices);geo.computeVertexNormals();geo.computeBoundingSphere();
    // Max horizontal drift <= .1, vertical relief <= .019 in local units.
    geo.boundingSphere.radius+=.12;
    const m=new THREE.ShaderMaterial({
      uniforms:{uTime:{value:0}},side:THREE.DoubleSide,transparent:false,depthWrite:true,
      vertexShader:`uniform float uTime;attribute float aPhase;attribute float aEdge;attribute vec3 aTint;
        varying vec3 vTint;varying float vEdge;
        void main(){
          vTint=aTint;vEdge=aEdge;
          float drift=.075*sin(uTime*.35+aPhase)+.025*sin(uTime*.79+aPhase*1.71);
          vec3 p=position;
          p.x+=drift;p.z+=drift*.57;
          p.y+=.010*sin(uTime*.90+aPhase)+.009*aEdge*sin(uTime*.52+aPhase*1.30);
          gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.);
        }`,
      fragmentShader:`varying vec3 vTint;varying float vEdge;
        void main(){gl_FragColor=vec4(vTint*(.94-.08*vEdge),1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }`
    });
    materials.set('candidate-wetland-floating-foliage',m);ambientMotion.push(m);
    const o=mesh(g,geo,m,0,0,0);o.name='Candidate Mud Dogs floating foliage';
    o.castShadow=false;o.receiveShadow=false;
    o.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',
      sourceEnvironment:['mud channels','cypress-like wetlands'],
      discs:count,localCenterPreserved:true,navigable:false,routeIds:[],principalCharacters:[],
      ambientClock:'ORDINARY_ENVIRONMENT',illustrativeMaxHorizontalDrift:.1,drawBudgetDelta:1};
    return o;
  }
  function wetlandButtressRoot(g,a,b,r,standIndex,rootIndex){
    // The 56 EXISTING root arms keep identical endpoints, radial limits and material.
    // Inward-only bark recesses replace seven-sided struts without inventing roots.
    const av=new THREE.Vector3(...a),bv=new THREE.Vector3(...b);
    const direction=bv.clone().sub(av),length=direction.length();
    const geometry=new THREE.CylinderGeometry(r*.62,r,length,18,6);
    geometry.name='Candidate Mud Dogs contoured buttress root';
    const p=geometry.getAttribute('position');
    for(let j=0;j<p.count;j++){
      const xx=p.getX(j),yy=p.getY(j),zz=p.getZ(j);
      if(Math.hypot(xx,zz)<.000001)continue; // Cap centers remain fixed.
      const vertical=yy/length+.5;
      const endHold=Math.pow(Math.sin(vertical*Math.PI),2);
      const angle=Math.atan2(zz,xx);
      const groove=Math.pow(.5+.5*Math.cos(angle*7+standIndex*.29+rootIndex*.43),3);
      const inset=.105*groove*endHold;
      p.setXYZ(j,xx*(1-inset),yy,zz*(1-inset));
    }
    p.needsUpdate=true;geometry.computeVertexNormals();geometry.computeBoundingSphere();
    const o=mesh(g,geometry,trunk,...av.clone().add(bv).multiplyScalar(.5).toArray());
    o.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),direction.normalize());
    o.name='Candidate Mud Dogs contoured buttress root';
    o.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',sourceEnvironment:['cypress-like wetlands'],
      originalEndpointsPreserved:true,originalRadiusEnvelopePreserved:true,
      navigable:false,routeIds:[],principalCharacters:[]};
    return o;
  }
  function cypressTrunk(g,x,y,z,h,standIndex){
    // Sculpt ONLY the existing 14 candidate Mud Dogs tree cylinders.
    // Keep the same height and .20 top/.45 base radius envelope, with no new mesh
    // or material: deep vertical bark flutes are illustrative, not botanical canon.
    const geo=new THREE.CylinderGeometry(.20,.45,h,16,6);
    geo.name='Candidate Mud Dogs fluted cypress-like trunk';
    const p=geo.getAttribute('position');
    for(let k=0;k<p.count;k++){
      const xx=p.getX(k),yy=p.getY(k),zz=p.getZ(k),radius=Math.hypot(xx,zz);
      if(radius<.000001)continue; // Existing cap centers remain centered.
      const angle=Math.atan2(zz,xx),lower=(h*.5-yy)/h;
      const flutes=Math.sin(angle*7+standIndex*.37+yy*.15)*(.50+.50*lower);
      const crossGrain=Math.sin(angle*13-standIndex*.23+yy*.47);
      const factor=.93+.055*flutes+.014*crossGrain; // <= .999, never beyond old rim.
      p.setXYZ(k,xx*factor,yy,zz*factor);
    }
    p.needsUpdate=true;
    geo.computeVertexNormals();geo.computeBoundingSphere();
    const o=mesh(g,geo,trunk,x,y+h/2,z);
    o.userData={...o.userData,visualAuthority:'CANDIDATE_NOT_APPROVED',
      sourceEnvironment:['cypress-like wetlands'],originalRadiusEnvelopePreserved:true};
    return o;
  }
  function sculptMudDogsCanopyLobe(lobe,standIndex,lobeIndex){
    // Inward-only physical relief on the 56 EXISTING candidate crown meshes.
    // Their transforms, enclosing radii, materials and triangle counts stay fixed.
    const geo=lobe.geometry,p=geo.getAttribute('position');
    for(let k=0;k<p.count;k++){
      const x=p.getX(k),y=p.getY(k),z=p.getZ(k),radius=Math.hypot(x,y,z);
      if(radius<.000001)continue;
      const azimuth=Math.atan2(z,x);
      const belt=Math.sqrt(Math.max(0,1-y*y/(radius*radius)));
      const grain=Math.sin(azimuth*7+standIndex*.41+lobeIndex*.67+y*4.2);
      const fold=Math.pow(.5+.5*grain,2);
      const inset=.086*(.28+.72*belt)*fold;
      p.setXYZ(k,x*(1-inset),y*(1-inset),z*(1-inset));
    }
    p.needsUpdate=true;geo.name='Candidate Mud Dogs inward-scalloped canopy lobe';
    geo.computeVertexNormals();geo.computeBoundingSphere();
    lobe.userData={...lobe.userData,visualAuthority:'CANDIDATE_NOT_APPROVED',
      sourceEnvironment:['cypress-like wetlands'],originalLobeEnvelopePreserved:true,
      navigable:false,routeIds:[],principalCharacters:[]};
    return lobe;
  }
  function swamp(g){
    // Raised ground and channels; no principal character or invented settlement.
    pool(g,'swamp',0,.12,0,10.5,8.2,'#375e50');pool(g,'channel',-6,.14,7,4.2,4.5,'#467767');
    const landformMaterial=new THREE.MeshStandardMaterial({vertexColors:true,roughness:.985,metalness:0,
      side:THREE.DoubleSide,transparent:false,depthWrite:true});
    materials.set('candidate-wetland-landform',landformMaterial);
    wetlandShoreline(g,landformMaterial);wetlandEmergentVegetation(g);
    const islands=[[1,.1,1,4,1.2,3],[-6,.1,-3,3,.9,2.7],[6,.2,-4,3.5,1,2.8],[-4,.1,5,2.7,.8,2]];
    wetlandRaisedGround(g,islands,landformMaterial);
    const illustratedTreeStands=[],illustratedTreeCrowns=[];
    for(let i=0;i<14;i++){
      // Two candidate cypress-like crown profiles break the old flat, repeated tree-disc silhouette.
      // All meshes remain direct children so the existing opaque batching path still applies.
      const a=i*2.4,r=3.8+(i%4)*1.5,x=Math.cos(a)*r,z=Math.sin(a)*r,y=.12,h=3.3+(i%3)*.9;
      illustratedTreeStands.push([x,z]);illustratedTreeCrowns.push({i,x,y,z,h});
      const mark=(o,part)=>{o.userData.wetlandStand=i;o.userData.wetlandPart=part;return o;};
      mark(cypressTrunk(g,x,y,z,h,i),'trunk');
      for(let k=0;k<4;k++){
        const b=k*Math.PI/2+i*.31,reach=.85+(i%3)*.15;
        mark(wetlandButtressRoot(g,[x,y+.67,z],[x+Math.cos(b)*reach,y+.045,z+Math.sin(b)*reach],.11,i,k),'buttress-root');
      }
      for(let j=0;j<4;j++){
        const width=(1.42-j*.24)*(i%3===1?.87:i%3===2?1.09:1);
        const rise=(.92-j*.09)*(i%3===1?1.17:.95);
        const drift=Math.sin(i*1.7+j*1.3)*.24;
        const lobe=rock(g,x+drift,y+h+.24+j*.44,z+Math.cos(i+j*2.1)*.23,width,rise,width*.82,j%3===0?leafDark:j%2?leafLight:leaf);
        mark(sculptMudDogsCanopyLobe(lobe,i,j),'canopy-lobe');
      }
      for(let k=0;k<2;k++){
        const b=k*Math.PI+i*.29;
        mark(branch(g,[x,y+h-.6,z],[x+Math.cos(b)*.72,y+h+.28,z+Math.sin(b)*.72],.11),'upper-branch');
        const t=mesh(g,new THREE.ConeGeometry(.085,.65+(i%3)*.12,5),moss,x+Math.cos(b)*.74,y+h-.18,z+Math.sin(b)*.74);
        t.rotation.z=(k?-.12:.12);mark(t,'hanging-vegetation');
      }
    }
    // A small, bounded shader field is anchored to the EXISTING illustrated stands,
    // not to an invented location, route or new moving water geometry.
    // The -PI/2 water plane rotation reverses world Z along texture V. Keep
    // wake and canopy-shadow sites on their original tree stands, not mirrored.
    const rootWakeSites=illustratedTreeStands.filter((_,i)=>i%3===0)
      .map(([x,z])=>new THREE.Vector2(.5+x/21,.5-z/16.4));
    const swampSurface=water.find(w=>w.kind==='swamp');
    swampSurface.material.uniforms.uRootSiteCount.value=rootWakeSites.length;
    swampSurface.material.uniforms.uRootSites.value=rootWakeSites;
    // Same four relief ellipses, projected through the existing rotated water disk.
    // Only this source-defined Mud Dogs candidate has island-contact wave sites.
    swampSurface.material.uniforms.uIslandSiteCount.value=islands.length;
    swampSurface.material.uniforms.uIslandSites.value=islands.map(([x,,z,sx,,sz])=>
      new THREE.Vector4(.5+x/21,.5-z/16.4,sx*.955/21,sz*.955/16.4));
    swampSurface.material.uniforms.uPadSiteCount.value=floatingFoliageSites.length;
    floatingContactSites=swampSurface.material.uniforms.uPadSites.value;
    syncFloatingContactSites(0);
    swampSurface.mesh.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',
      sourceStands:illustratedTreeStands.length,illustrativeWakeSites:rootWakeSites.length};
    wetlandWaterlineRoots(g,illustratedTreeStands);
    wetlandCanopyFringe(g,illustratedTreeCrowns);
    wetlandWaterlineStems(g);
    wetlandFloatingFoliage(g);
    branch(g,[-5,.5,1],[0,.8,4],.32,trunk);
  }
  function estateSculptedCourseGrass(index){
    // The THREE existing Jackson course discs retain their elliptical outlines
    // and positions. Only their interior gains bounded candidate turf relief.
    // The Week 3 contamination/cleanup state is NOT resolved by this sculpt.
    const segments=30,rings=7,pos=[0,0,0],uv=[.5,.5],indices=[];
    for(let ring=1;ring<=rings;ring++){
      const radius=ring/rings;
      for(let k=0;k<segments;k++){
        const angle=k*Math.PI*2/segments,x=radius*Math.cos(angle),y=radius*Math.sin(angle);
        const hold=(1-radius*radius)*(1-radius*radius);
        const z=(.028*Math.sin(x*2.9+index*.41)+.015*Math.cos(y*3.7-index*.59))*hold;
        pos.push(x,y,z);
        uv.push(.5+.5*x,.5+.5*y);
      }
    }
    for(let k=0;k<segments;k++)indices.push(0,1+k,1+(k+1)%segments);
    for(let ring=1;ring<rings;ring++)for(let k=0;k<segments;k++){
      const next=(k+1)%segments;
      const a=1+(ring-1)*segments+k,b=1+(ring-1)*segments+next;
      const c=1+ring*segments+k,d=1+ring*segments+next;
      indices.push(a,c,d,a,d,b);
    }
    const geometry=new THREE.BufferGeometry();
    geometry.name='Candidate Jackson bounded golf-ground relief';
    geometry.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));
    geometry.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));
    geometry.setIndex(indices);
    geometry.computeVertexNormals();
    geometry.computeBoundingSphere();
    return geometry;
  }
  function sculptJacksonAutumnGroveCrown(crown,treeIndex,lobeIndex){
    // Recess only the EXISTING folio-referenced crowns; never enlarge their original silhouette.
    // Illustrative leaf-cluster relief is not a permanent-season or botanical canon assertion.
    const geometry=crown.geometry,p=geometry.getAttribute('position');
    for(let k=0;k<p.count;k++){
      const x=p.getX(k),y=p.getY(k),z=p.getZ(k),radius=Math.hypot(x,y,z);
      if(radius<1e-8)continue;
      const azimuth=Math.atan2(z,x);
      const wave=.72*Math.sin(azimuth*8.5+treeIndex*.61+lobeIndex*.37)
        +.28*Math.cos(y*9.2+treeIndex*.27-lobeIndex*.44);
      const scallop=Math.pow(.5+.5*wave,2);
      const midCrown=1-Math.pow(Math.abs(y)/radius,4);
      const inset=.082*(.26+.74*midCrown)*scallop;
      p.setXYZ(k,x*(1-inset),y*(1-inset),z*(1-inset));
    }
    p.needsUpdate=true;
    geometry.name='Candidate Jackson inward-scalloped autumn crown';
    geometry.computeVertexNormals();geometry.computeBoundingSphere();
    crown.name='Candidate Jackson inward-scalloped autumn crown';
    crown.userData={...crown.userData,visualAuthority:'CANDIDATE_NOT_APPROVED',
      historicalReference:'W09-COUNTRY-CLUB-FOLIOS-05-08',
      originalCrownEnvelopePreserved:true,navigable:false,routeIds:[],principalCharacters:[]};
    return crown;
  }
  function estate(g){
    const cream=mat('#e4d8b3'),brick=mat('#997856'),roof=mat('#45605b'),glass=mat('#385953',.30),grass=mat('#648c43'),sand=mat('#c7ad76');
    const ground=cyl(g,0,-1.6,2,11.8,12.6,1.6,moss,48);ground.scale.z=1.15;ground.name='Candidate raised estate ground';
    box(g,0,-.15,0,12,.3,9,stone);box(g,0,.15,0,8,2.8,4.2,cream);box(g,-5,.15,.1,2.2,2.2,3.6,brick);box(g,5,.15,.1,2.2,2.2,3.6,brick);
    const hip=(x,y,z,w,h,d)=>{const geo=new THREE.CylinderGeometry(0,1,h,4);geo.rotateY(Math.PI/4);const o=mesh(g,geo,roof,x,y+h/2,z);o.scale.set(w/Math.SQRT2,1,d/Math.SQRT2);};
    hip(0,2.95,0,8.8,1.6,5.2);hip(-5,2.35,.1,2.7,1.1,4.2);hip(5,2.35,.1,2.7,1.1,4.2);
    box(g,0,.12,3,9,.25,2.4,edge);for(let x=-4;x<=4;x+=1.34)cyl(g,x,.37,3.6,.13,.16,2.3,cream,8);box(g,0,2.65,3.1,9.4,.25,2.5,cream);hip(0,2.9,3.1,9.6,.75,2.7);
    for(let x=-3;x<=3;x+=1.5){box(g,x,.85,2.12,.55,1.05,.04,glass);box(g,x-.38,.78,2.16,.12,1.23,.06,roof);box(g,x+.38,.78,2.16,.12,1.23,.06,roof);}
    box(g,0,.4,2.14,.9,1.9,.05,roof);for(let i=0;i<3;i++)box(g,0,-.05+i*.1,4.8-i*.34,3,.1,.4,edge);
    // Candidate course massing does not certify a pristine post-contamination state.
    for(let i=0;i<3;i++){
      const o=mesh(g,estateSculptedCourseGrass(i),grass,-4+i*4,.02,7.5+(i%2));
      o.name='Candidate Jackson sculpted course grass';
      o.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',sourceLandmark:'golf grounds',
        originalDiscRadius:1,originalSegments:30,originalGreenIndex:i,
        navigable:false,routeIds:[],principalCharacters:[]};
      o.rotation.x=-Math.PI/2;o.scale.set(2.7,1.8,1);o.castShadow=false;
    }
    for(const[x,z]of[[-6,6],[3,9]]){const o=mesh(g,new THREE.CircleGeometry(1,20),sand,x,.03,z);o.rotation.x=-Math.PI/2;o.scale.set(1.3,.6,1);o.castShadow=false;}
    pool(g,'pond',7,.06,6,3.8,2.3,'#458f83');
    // Historical visual reference: Week 9 Country Club folios 05–08 show warm
    // autumn vegetation, waterfront masonry and a distant clubhouse. The forms
    // below are LOCAL illustrated candidate texture, not a new Atlas road,
    // navigable crossing, confirmed course layout or resolved cleanup state.
    const bridge=new THREE.Group();bridge.name='Candidate Week 9 pond-side stone arch';
    bridge.position.set(7,.10,6);
    bridge.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',historicalReference:'W09-COUNTRY-CLUB-FOLIOS-05-08',routeIds:[],navigable:false,period:'HISTORICAL_REFERENCE_CANDIDATE'};
    g.add(bridge);
    const shape=new THREE.Shape();
    shape.moveTo(-2.65,0);shape.lineTo(-1.73,0);
    shape.bezierCurveTo(-1.58,1.30,1.58,1.30,1.73,0);
    shape.lineTo(2.65,0);shape.lineTo(2.65,1.48);
    shape.lineTo(-2.65,1.48);shape.closePath();
    for(const side of [-.88,.71]){
      const archGeo=new THREE.ExtrudeGeometry(shape,{depth:.17,steps:1,bevelEnabled:false,curveSegments:16});
      archGeo.rotateY(Math.PI/2);
      const face=mesh(bridge,archGeo,stone,side,0,0);
      face.userData={bridgePart:'stone-arch'};
      box(bridge,side+.07,1.48,0,.26,.15,5.42,edge);
      for(const z of [-2.26,-1.13,0,1.13,2.26])cyl(bridge,side+.07,1.64,z,.105,.13,.50,stone,7);
      box(bridge,side+.07,2.14,0,.22,.14,5.30,edge);
    }
    box(bridge,0,1.47,0,1.80,.19,5.48,mat('#997856'));
    // Irregular tree crowns echo the historical folio's autumn grove, without
    // asserting permanent season, tree species, or exact tree coordinates.
    const amber=[mat('#b77d39'),mat('#d1a052'),mat('#ad5937'),mat('#934d35'),mat('#a6a04b')];
    const grove=[[-9,-3,1.1],[-9,3,1.0],[-9,9,.9],[-5,11,1.08],[1,11,1.17],[10,1,1.05],[9,-4,1.25],[3,-8,.95],[-4,-8,1.12]];
    grove.forEach(([x,z,scale],i)=>{
      const y=0,h=(2.5+.24*(i%3))*scale;
      const stem=cyl(g,x,y,z,.15*scale,.32*scale,h,trunk,8);
      stem.userData={estateTreePart:'trunk',estateTree:i};
      const lobes=4+(i%2);
      for(let k=0;k<lobes;k++){
        const a=(k/lobes)*Math.PI*2+i*.34;
        const dx=Math.cos(a)*.66*scale,dz=Math.sin(a)*.63*scale;
        const crown=sculptJacksonAutumnGroveCrown(
          rock(g,x+dx,y+h+(.46+(k%2)*.30)*scale,z+dz,
            (1.08+(k%3)*.12)*scale,(.85+(k%2)*.17)*scale,(.94+(k%2)*.14)*scale,amber[(i+k)%amber.length]),
          i,k);
        crown.userData={...crown.userData,estateTreePart:'crown',estateTree:i};
      }
      const high=sculptJacksonAutumnGroveCrown(
        rock(g,x,y+h+1.05*scale,z,1.10*scale,.85*scale,1.0*scale,amber[(i+2)%amber.length]),
        i,lobes);
      high.userData={...high.userData,estateTreePart:'crown',estateTree:i};
    });
    for(let i=0;i<3;i++){cyl(g,-4+i*4,.08,7.5+(i%2),.024,.024,1,cream,5);const f=mesh(g,new THREE.PlaneGeometry(.45,.25),mat('#b86f43'),-3.78+i*4,.95,7.5+(i%2));f.material.side=THREE.DoubleSide;}
    box(g,0,0,6,1.4,.025,.5,mat('#806f4c'));
  }
  const builders={'LOC-TDS-WATERFALL-TEMPLE':temple,'LOC-MUD-DOGS-SWAMP':swamp,'LOC-COUNTRY-CLUB-JACKSON':estate};
  for(const p of bindings){if(!builders[p.id])continue;const g=new THREE.Group();g.name=p.id;g.userData={locationId:p.id,visualAuthority:'CANDIDATE_NOT_APPROVED',stateResolution:'UNRESOLVED_NOT_CURRENT_STATE',principalCharacters:[]};g.position.set(p.anchor[0],Math.max(.65,height(p.anchor[0],p.anchor[2])),p.anchor[2]);builders[p.id](g);root.add(g);locations.push({id:p.id,group:g,sourceStatus:p.canonStatus});}
  return {root,locations,water,worldMutationAllowed:false,principalCharacters:[],
    tick(time,{paused=false}={}){if(disposed||paused)return;if(!Number.isFinite(time))throw Error('INVALID_ANIMATION_TIME');syncFloatingContactSites(time);for(const w of water)w.material.uniforms.uTime.value=time;for(const m of ambientMotion)m.uniforms.uTime.value=time;},
    dispose(){if(disposed)return;disposed=true;for(const g of geometries)g.dispose();for(const m of materials.values())m.dispose();for(const t of textures)t.dispose();root.clear();}
  };
}
