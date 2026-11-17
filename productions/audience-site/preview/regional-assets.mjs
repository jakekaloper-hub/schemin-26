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
    const m=new THREE.ShaderMaterial({uniforms:{uTime:{value:0},uColor:{value:new THREE.Color(color)},uFall:{value:kind==='waterfall'?1:0},uWetland:{value:wetland?1:0},uFlow:{value:flow},uSheenGain:{value:kind==='swamp'?.42:kind==='channel'?.62:0}},transparent:true,depthWrite:false,side:THREE.DoubleSide,
      vertexShader:`varying vec2 vUv;varying vec3 vWorld;void main(){vUv=uv;vWorld=(modelMatrix*vec4(position,1.)).xyz;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
      fragmentShader:`uniform float uTime;uniform vec3 uColor;uniform float uFall;uniform float uWetland;uniform vec2 uFlow;uniform float uSheenGain;varying vec2 vUv;varying vec3 vWorld;void main(){float stripe;if(uFall>.5){stripe=pow(.5+.5*sin(vUv.x*21.+sin(vUv.y*9.-uTime*3.8)*1.9),3.);float foam=pow(.5+.5*sin(vUv.y*35.+uTime*9.+sin(vUv.x*13.)),4.);gl_FragColor=vec4(mix(uColor,vec3(.84,.96,.89),.27+stripe*.14+foam*.17),.88);}else if(uWetland>.5){
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
      gl_FragColor=vec4(waterTint+lowSheen+quietEddy,.92);
      }else{float a=sin(vWorld.x*3.+uTime*.6+sin(vWorld.z*2.2))*sin(vWorld.z*3.8-uTime*.34);float rim=pow(clamp(a,0.,1.),6.);gl_FragColor=vec4(uColor+vec3(.25,.34,.24)*rim,.88);}}`});
    materials.set('water-'+water.length,m);return m;
  }
  function pool(g,kind,x,y,z,rx,rz,color='#387e75'){
    const m=waterMaterial(kind,color),o=mesh(g,new THREE.CircleGeometry(1,40),m,x,y,z);o.rotation.x=-Math.PI/2;o.scale.set(rx,rz,1);o.castShadow=false;o.renderOrder=2;water.push({kind,material:m,mesh:o});return o;
  }
  function waterfall(g,x,y,z,width,drop){
    const m=waterMaterial('waterfall','#67aaa0'),o=mesh(g,new THREE.PlaneGeometry(width,drop,8,12),m,x,y-drop/2,z);o.castShadow=false;o.renderOrder=2;water.push({kind:'waterfall',material:m,mesh:o});
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
          p.x+=aDrift.x*age*.42+sin(uTime*.31+aPhase*35.)*.10;
          p.y+=age*(.55+.65*aDrift.y);
          p.z+=aDrift.z*age*.28;
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
  function temple(g){
    // Source-supported raised stone temple, vegetation and falling water; exact forms are candidates.
    rock(g,-6,3,-3,4,6,3,mat('#677163'));rock(g,-8,2,-4,3.6,4.8,3.2,mat('#777b6a'));rock(g,-5,1,-5,4,4,3.6,mat('#596955'));
    for(let j=0;j<4;j++)box(g,1,j*.58,-.8,9-j*1.1,.58,7-j*.75,j%2?edge:stone);
    for(let j=0;j<9;j++)box(g,1,j*.24,5.3-j*.43,2.8,.24,.55,j%2?stone:edge);
    box(g,1,2.3,-1,5.2,2.8,3.6,dark);
    for(let i=-2;i<=2;i++){cyl(g,1+i*1.05,2.3,1.1,.23,.29,3.1,stone,8);box(g,1+i*1.05,5.34,1.1,.7,.22,.65,edge);}
    box(g,1,5.5,-.1,6.7,.4,5,edge);box(g,1,5.9,-.1,6.1,.32,4.5,stone);box(g,1,6.22,-.1,5.2,.3,3.9,dark);
    box(g,1,2.32,1.02,1.25,2.3,.15,mat('#263c35'));
    for(let i=0;i<15;i++)box(g,-2.1+i*.44,5.52,2.43,.16,.25,.15,dark);
    for(let i=0;i<12;i++){const a=i*2.399;rock(g,Math.cos(a)*(5+i%3),.3,Math.sin(a)*(4+i%2),.7,.45,.6,i%3?stone:moss);}
    pool(g,'river',-5.8,7.2,-1.5,2.2,2.6,'#458c7d');waterfall(g,-5.8,7.2,1.8,2.15,6.9);pool(g,'pool',-5.8,.30,3,3.8,2.8,'#3b8c7e');waterfallMist(g,-5.8,7.2,1.8,6.9);
    for(const [x,z,s]of[[-10,-1,1.5],[-9,5,1.25],[-2,-6,1.4],[6,-4,1.5],[7,1,1.3],[6,6,1.1],[-2,7,.9]])canopy(g,x,0,z,s);
    box(g,2.7,2.31,1.9,.8,.05,.6,moss);box(g,-1.8,1.16,2.2,1.1,.04,.8,moss);
  }
  function wetlandShoreline(g){
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
    // Keep vertex colors intact: the current static batcher merges position/normal/UV only.
    const bankMat=new THREE.MeshStandardMaterial({vertexColors:true,roughness:.98,side:THREE.DoubleSide,transparent:true,opacity:1,depthWrite:true});
    materials.set('candidate-wetland-bank',bankMat);
    const bank=mesh(g,geo,bankMat,0,0,0);bank.name='Candidate wetland shoreline transition';
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
  function wetlandRaisedGround(g,islands){
    // Source: permanent Mud Dogs raised ground and Southern Wetlands mudflats.
    // Only the pre-existing FOUR local illustrative island footprints are sculpted;
    // this creates no canonical shoreline, path, travel route or new waterway.
    const sides=28,radii=[.27,.53,.77,.955],heights=[.88,.73,.36,-.12];
    const positions=[],colors=[],islandIds=[],faces=[];
    const strata=['#697456','#626952','#555844','#393e35'].map(v=>new THREE.Color(v));
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
        const tint=strata[r].clone().multiplyScalar(.90+.095*(.5+.5*Math.sin(theta*8+island+r)));
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
    // The inherited opaque batcher intentionally omits vertex colors. One
    // transparent=true/opacity=1 mesh preserves per-vertex sediment strata.
    const reliefMaterial=new THREE.MeshStandardMaterial({vertexColors:true,roughness:.99,metalness:0,
      side:THREE.DoubleSide,transparent:true,opacity:1,depthWrite:true});
    materials.set('candidate-wetland-raised-ground',reliefMaterial);
    const relief=mesh(g,geo,reliefMaterial,0,0,0);
    relief.name='Candidate wetland raised-ground relief';
    relief.userData={visualAuthority:'CANDIDATE_NOT_APPROVED',sourceEnvironment:['raised ground','mudflats'],
      islandCount:islands.length,routeIds:[],navigable:false};
    relief.renderOrder=1;
  }
  function swamp(g){
    // Raised ground and channels; no principal character or invented settlement.
    pool(g,'swamp',0,.12,0,10.5,8.2,'#375e50');pool(g,'channel',-6,.14,7,4.2,4.5,'#467767');
    wetlandShoreline(g);wetlandEmergentVegetation(g);
    const islands=[[1,.1,1,4,1.2,3],[-6,.1,-3,3,.9,2.7],[6,.2,-4,3.5,1,2.8],[-4,.1,5,2.7,.8,2]];
    wetlandRaisedGround(g,islands);
    for(let i=0;i<14;i++){
      // Two candidate cypress-like crown profiles break the old flat, repeated tree-disc silhouette.
      // All meshes remain direct children so the existing opaque batching path still applies.
      const a=i*2.4,r=3.8+(i%4)*1.5,x=Math.cos(a)*r,z=Math.sin(a)*r,y=.12,h=3.3+(i%3)*.9;
      const mark=(o,part)=>{o.userData.wetlandStand=i;o.userData.wetlandPart=part;return o;};
      mark(cyl(g,x,y,z,.20,.45,h,trunk,8),'trunk');
      for(let k=0;k<4;k++){
        const b=k*Math.PI/2+i*.31,reach=.85+(i%3)*.15;
        mark(branch(g,[x,y+.67,z],[x+Math.cos(b)*reach,y+.045,z+Math.sin(b)*reach],.11,trunk),'buttress-root');
      }
      for(let j=0;j<4;j++){
        const width=(1.42-j*.24)*(i%3===1?.87:i%3===2?1.09:1);
        const rise=(.92-j*.09)*(i%3===1?1.17:.95);
        const drift=Math.sin(i*1.7+j*1.3)*.24;
        mark(rock(g,x+drift,y+h+.24+j*.44,z+Math.cos(i+j*2.1)*.23,width,rise,width*.82,j%3===0?leafDark:j%2?leafLight:leaf),'canopy-lobe');
      }
      for(let k=0;k<2;k++){
        const b=k*Math.PI+i*.29;
        mark(branch(g,[x,y+h-.6,z],[x+Math.cos(b)*.72,y+h+.28,z+Math.sin(b)*.72],.11),'upper-branch');
        const t=mesh(g,new THREE.ConeGeometry(.085,.65+(i%3)*.12,5),moss,x+Math.cos(b)*.74,y+h-.18,z+Math.sin(b)*.74);
        t.rotation.z=(k?-.12:.12);mark(t,'hanging-vegetation');
      }
    }
    for(let i=0;i<26;i++){const a=i*2.399,r=6.8+Math.sin(i)*.8,x=Math.cos(a)*r,z=Math.sin(a)*r;cyl(g,x,.1,z,.04,.06,.55+(i%3)*.15,leafLight,4);}
    for(let i=0;i<12;i++){const o=mesh(g,new THREE.CircleGeometry(.18+(i%3)*.08,9),leafLight,Math.sin(i*5)*7,.16,Math.cos(i*9)*5);o.rotation.x=-Math.PI/2;o.castShadow=false;}
    branch(g,[-5,.5,1],[0,.8,4],.32,trunk);
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
    for(let i=0;i<3;i++){const o=mesh(g,new THREE.CircleGeometry(1,30),grass,-4+i*4,.02,7.5+(i%2));o.rotation.x=-Math.PI/2;o.scale.set(2.7,1.8,1);o.castShadow=false;}
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
        const crown=rock(g,x+dx,y+h+(.46+(k%2)*.30)*scale,z+dz,
          (1.08+(k%3)*.12)*scale,(.85+(k%2)*.17)*scale,(.94+(k%2)*.14)*scale,amber[(i+k)%amber.length]);
        crown.userData={estateTreePart:'crown',estateTree:i};
      }
      const high=rock(g,x,y+h+1.05*scale,z,1.10*scale,.85*scale,1.0*scale,amber[(i+2)%amber.length]);
      high.userData={estateTreePart:'crown',estateTree:i};
    });
    for(let i=0;i<3;i++){cyl(g,-4+i*4,.08,7.5+(i%2),.024,.024,1,cream,5);const f=mesh(g,new THREE.PlaneGeometry(.45,.25),mat('#b86f43'),-3.78+i*4,.95,7.5+(i%2));f.material.side=THREE.DoubleSide;}
    box(g,0,0,6,1.4,.025,.5,mat('#806f4c'));
  }
  const builders={'LOC-TDS-WATERFALL-TEMPLE':temple,'LOC-MUD-DOGS-SWAMP':swamp,'LOC-COUNTRY-CLUB-JACKSON':estate};
  for(const p of bindings){if(!builders[p.id])continue;const g=new THREE.Group();g.name=p.id;g.userData={locationId:p.id,visualAuthority:'CANDIDATE_NOT_APPROVED',stateResolution:'UNRESOLVED_NOT_CURRENT_STATE',principalCharacters:[]};g.position.set(p.anchor[0],Math.max(.65,height(p.anchor[0],p.anchor[2])),p.anchor[2]);builders[p.id](g);root.add(g);locations.push({id:p.id,group:g,sourceStatus:p.canonStatus});}
  return {root,locations,water,worldMutationAllowed:false,principalCharacters:[],
    tick(time,{paused=false}={}){if(disposed||paused)return;if(!Number.isFinite(time))throw Error('INVALID_ANIMATION_TIME');for(const w of water)w.material.uniforms.uTime.value=time;for(const m of ambientMotion)m.uniforms.uTime.value=time;},
    dispose(){if(disposed)return;disposed=true;for(const g of geometries)g.dispose();for(const m of materials.values())m.dispose();for(const t of textures)t.dispose();root.clear();}
  };
}
