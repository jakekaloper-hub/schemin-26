"""Deterministic wireframe terrain view plates: proof of geometry reuse, not cinematic QA."""
import hashlib,html,math
from world.atlas.spatial.cinematic_scene_proof import build
from world.atlas.spatial.landscape_experiment import build_landscape

def plate(camera_index=0):
    pack=build();cam=pack['cameras'][camera_index];a=cam['xyz'];b=cam['look_at']
    vx=[b[i]-a[i] for i in range(3)];n=math.sqrt(sum(i*i for i in vx));f=[v/n for v in vx]
    right=[f[1],-f[0],0];nr=math.hypot(*right);right=[v/nr for v in right]
    up=[right[1]*f[2]-right[2]*f[1],right[2]*f[0]-right[0]*f[2],right[0]*f[1]-right[1]*f[0]]
    z=build_landscape()['heightfield'];n=len(z)
    def project(i,j,h):
        p=[i*50-a[0],j*50-a[1],h-a[2]]
        depth=sum(p[k]*f[k] for k in range(3))
        if depth<=1:return None
        x=sum(p[k]*right[k] for k in range(3))/depth
        y=sum(p[k]*up[k] for k in range(3))/depth
        return (600+x*480,340-y*480,depth)
    faces=[]
    for j in range(n-1):
        for i in range(n-1):
            pts=[project(i,j,z[j][i]),project(i+1,j,z[j][i+1]),project(i+1,j+1,z[j+1][i+1]),project(i,j+1,z[j+1][i])]
            if None in pts:continue
            coords=' '.join(f'{p[0]:.1f},{p[1]:.1f}' for p in pts)
            faces.append((sum(p[2] for p in pts)/4, f'<polygon points="{coords}" fill="#83978c" fill-opacity=".28" stroke="#426c66" stroke-width=".65"/>'))
    polygons=''.join(s for _,s in sorted(faces,reverse=True))
    title=html.escape(cam['id'])
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="700" viewBox="0 0 1200 700">'
            '<rect width="1200" height="700" fill="#dce7e6"/>'
            f'{polygons}<rect y="0" width="1200" height="88" fill="#183e3c"/>'
            f'<text x="28" y="38" font-size="24" fill="white" font-family="sans-serif">{title}</text>'
            '<text x="28" y="65" font-size="14" fill="#b7d6d1" font-family="sans-serif">SYNTHETIC GEOGRAPHY — NOT CANON / NOT VISUAL QA APPROVAL</text>'
            f'<text x="25" y="674" font-size="13" fill="#24423f" font-family="sans-serif">Mesh SHA256 {pack["mesh_sha256"][:24]} · Camera {camera_index+1}/3 · Shared 5 landmark IDs</text>'
            '</svg>')
