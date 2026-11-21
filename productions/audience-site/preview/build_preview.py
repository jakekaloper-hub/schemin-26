#!/usr/bin/env python3
"""Offline observer build. Exact private art bytes are optional and never reconstructed.
Pinned renderer is embedded with its MIT license; no CDN/network request at run time.
"""
from pathlib import Path
import argparse,base64,json,re,hashlib
BASE=Path(__file__).resolve().parent
DEPENDENCY_SHA256={
 'three.core.js':'613e370f76638fdef83926642bf256dc9615684922de1ce1f63a8583e5d78578',
 'three.module.js':'104f56145899722094556490d787aae0617cc2fc3382f31df02d724ea1aee341',
 'THREE-LICENSE.txt':'8b378ebe60e2fe500158cb0ac71cb5e8b7d92953c2abcc63a0eb90499653b5bc',
}

def validate_catalog(data):
 if not re.fullmatch(r'[a-f0-9]{40}',str(data.get('sourceRevision',''))):raise ValueError('EXACT_SOURCE_REVISION_REQUIRED')
 if not isinstance(data.get('stateAsOf'),str) or not data['stateAsOf'].strip():raise ValueError('SOURCE_STATE_AS_OF_REQUIRED')
 if data.get('publicationAuthorized') is not False:raise ValueError('PUBLICATION_AUTHORITY_MUST_REMAIN_FALSE')
 if data.get('authority')!='DERIVED_PRESENTATION_ONLY':raise ValueError('DERIVED_PRESENTATION_AUTHORITY_REQUIRED')
 locations=data.get('locations')
 if not isinstance(locations,list) or not locations:raise ValueError('SOURCE_LOCATIONS_REQUIRED')
 ids=[x.get('id') for x in locations if isinstance(x,dict)]
 if len(ids)!=len(locations) or any(not isinstance(x,str) or not x.startswith('LOC-') for x in ids) or len(set(ids))!=len(ids):raise ValueError('UNIQUE_SOURCE_LOCATION_IDS_REQUIRED')

def dependency_bytes(vendor):
 result={}
 for name,expected in DEPENDENCY_SHA256.items():
  data=(vendor/name).read_bytes()
  if hashlib.sha256(data).hexdigest()!=expected:raise ValueError('DEPENDENCY_HASH_MISMATCH:'+name)
  result[name]=data
 return result

def wrap(path,name):
 text=path.read_text();names=re.findall(r'export function (\w+)\(',text)
 return f'const {name}=(()=>{{\n'+text.replace('export function ','function ')+f'\nreturn {{{",".join(names)}}};\n}})();\n'
def safe_json(obj):return json.dumps(obj,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
def build(catalog_path,output,art_path=None,no_editions=True):
 data=json.loads(Path(catalog_path).read_text());validate_catalog(data)
 if not no_editions and art_path is None:raise ValueError('EXPLICIT_PRIVATE_ART_DIRECTORY_REQUIRED')
 art_path=Path(art_path) if art_path is not None else None
 manifest=None;assets={}
 if not no_editions:
  manifest=json.loads((art_path/'edition-memory.json').read_text())
  for memory in manifest['memories']:
   for p in memory['pages']:
    path=(art_path/p['path']).resolve()
    if art_path.resolve() not in path.parents:raise ValueError('ASSET_PATH_ESCAPE')
    b=path.read_bytes()
    if hashlib.sha256(b).hexdigest()!=p['sha256']:raise ValueError('ORIGINAL_ART_HASH_MISMATCH:'+p['id'])
    assets[p['id']]='data:image/jpeg;base64,'+base64.b64encode(b).decode('ascii')
 vendor=BASE/'vendor';deps=dependency_bytes(vendor);core=deps['three.core.js'];module=deps['three.module.js'];license=deps['THREE-LICENSE.txt'].decode('utf-8')
 if b"const REVISION = '187'" not in core:raise ValueError('PINNED_THREE_REVISION_REQUIRED')
 bootstrap="""const coreURL=URL.createObjectURL(new Blob([Uint8Array.from(atob(CORE64),c=>c.charCodeAt(0))],{type:'text/javascript'}));
const moduleSource=new TextDecoder().decode(Uint8Array.from(atob(MODULE64),c=>c.charCodeAt(0))).replaceAll('./three.core.js',coreURL);
const moduleURL=URL.createObjectURL(new Blob([moduleSource],{type:'text/javascript'}));
let THREE=null;try{THREE=await import(moduleURL);}catch(e){console.warn('Enhanced renderer unavailable; retaining source Atlas fallback.');}
window.addEventListener('pagehide',()=>{URL.revokeObjectURL(coreURL);URL.revokeObjectURL(moduleURL);});
""".replace('CORE64',json.dumps(base64.b64encode(core).decode())).replace('MODULE64',json.dumps(base64.b64encode(module).decode()))
 files=[(BASE.parent/'src/observer-world.mjs','ObserverWorld'),(BASE.parent/'src/observer-weather.mjs','ObserverWeather'),(BASE/'spatial.mjs','Spatial'),(BASE/'renderer.mjs','WorldRenderer'),(BASE/'regional-assets.mjs','RegionalAssets'),(BASE/'atlas-site-assets.mjs','AtlasSites'),(BASE/'three-world.mjs','ThreeWorldRenderer'),(BASE/'memory.mjs','EditionMemory'),(BASE/'place-history.mjs','PlaceHistory')]
 bundle=bootstrap+'\n'.join(wrap(path,name) for path,name in files)+(BASE/'app.mjs').read_text()+'\n'+(BASE/'memory-ui.mjs').read_text()+'\n'+(BASE/'place-history-ui.mjs').read_text()
 html=(BASE/'index.template.html').read_text().replace('__CATALOG__',safe_json(data)).replace('__MEMORY_INDEX__',safe_json(manifest)).replace('__MEMORY_ASSETS__',safe_json(assets)).replace('__BUNDLE__',bundle.replace('</script','<\\/script'))
 edition_note=(f"{len(manifest['memories'])} locations open historical artwork from the supplied private issue; those images do not approve present-day geometry." if manifest else "No private edition artwork is included in this repository preview. Original folios require a separate explicit private build.")
 html=html.replace('__EDITION_NOTE__',edition_note)
 html=html.replace('</body>', '<script type="text/plain" id="third-party-license">'+license.replace('</script','<\\/script')+'</script></body>')
 output=Path(output);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(html)
 return {'file':str(output),'bytes':len(html.encode()),'sha256':hashlib.sha256(html.encode()).hexdigest(),'sourceRevision':data['sourceRevision'],'sourceStateAsOf':data['stateAsOf'],'originalJPEGs':len(assets),'linkedLocations':len(manifest['memories']) if manifest else 0,'publicationAuthorized':False,'renderer':'PINNED_THREE_R187_WITH_EXISTING_FALLBACK','geometry':'REGIONAL_CANDIDATE_NOT_APPROVED','visualAcceptance':'NOT_REVIEWED','dependencies':{n:hashlib.sha256((vendor/n).read_bytes()).hexdigest() for n in ['three.core.js','three.module.js','THREE-LICENSE.txt']}}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--catalog',required=True);p.add_argument('--output',required=True)
 p.add_argument('--art',help='Explicit private edition asset directory; requires --private-editions')
 mode=p.add_mutually_exclusive_group()
 mode.add_argument('--private-editions',action='store_true',help='Opt in to private source artwork; never use in repository CI')
 mode.add_argument('--no-editions',action='store_true',help='Explicit safe default: world only')
 a=p.parse_args()
 if a.art and not a.private_editions:p.error('--art requires --private-editions')
 if a.private_editions and not a.art:p.error('--private-editions requires --art')
 print(json.dumps(build(a.catalog,a.output,a.art,no_editions=not a.private_editions),indent=2))
