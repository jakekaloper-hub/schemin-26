#!/usr/bin/env node
/** Internal, source-derived production coverage; never a new geography authority. */
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve,dirname} from 'node:path';
import {execFileSync} from 'node:child_process';
import {supportedAtlasSiteIds} from '../preview/atlas-site-assets.mjs';
const WETLANDS=new Set(['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON']);
export function reportSiteCoverage({locations,candidates,worldMemory,revision}){
 if(!/^[a-f0-9]{40}$/.test(revision||''))throw Error('EXACT_SOURCE_REVISION_REQUIRED');
 if(!Array.isArray(locations?.locations)||!Array.isArray(candidates?.candidates)||!Array.isArray(worldMemory?.events))throw Error('SOURCE_COVERAGE_INPUT_REQUIRED');
 const supported=new Set([...WETLANDS,...supportedAtlasSiteIds()]);
 const currentSites=locations.locations.map(l=>({id:l.id,name:l.name,zoneId:l.physical_zone_id,canonStatus:l.canon_status,sourceLandmarks:[...l.persistent_landmarks],sourcePath:'world/data/locations.json',model:supported.has(l.id)?'SITE_SPECIFIC_CANDIDATE':'MISSING',module:WETLANDS.has(l.id)?'preview/regional-assets.mjs':supported.has(l.id)?'preview/atlas-site-assets.mjs':null,historyIds:worldMemory.events.filter(e=>e.location===l.id).map(e=>e.event_id),visualAcceptance:'NOT_APPROVED',inhabitants:'NOT_IMPLEMENTED',liveInputs:'NOT_CONNECTED',publicationAuthorized:false}));
 const proposedSites=candidates.candidates.map(c=>({id:c.id,name:c.working_name,lifecycle:c.lifecycle_status,sourcePath:'world/data/atlas_location_candidates.json',trigger:c.activation_trigger??null,prerequisites:[...(c.prerequisites||[])],relatedLocationIds:[...(c.related_active_location_ids||[])],rendered:false,publicationAuthorized:false}));
 return {authority:'DERIVED_INTERNAL_PRODUCTION_COVERAGE',sourceRevision:revision,worldMutationAllowed:false,publicationAuthorized:false,currentSites,proposedSites,missingModelIds:currentSites.filter(x=>x.model==='MISSING').map(x=>x.id)};
}
export function coverageMarkdown(r){
 const esc=x=>String(x).replaceAll('|','/').replaceAll('\n',' ');
 const rows=r.currentSites.map(x=>`| ${esc(x.name)} | ${x.zoneId.replace('REG-','')} | ${x.model.replaceAll('_',' ')} | ${x.historyIds.length} |`);
 const counts={};for(const p of r.proposedSites)counts[p.lifecycle]=(counts[p.lifecycle]||0)+1;
 return `# Commonwealth — All Current Sites\n\nSource revision: \`${r.sourceRevision}\`. Internal coverage, not visual approval or public release.\n\n## Current Atlas\n\n${r.currentSites.length} current sites; ${r.currentSites.filter(x=>x.model==='SITE_SPECIFIC_CANDIDATE').length} distinct source-bound model candidates. All preserve source IDs, positions and statuses. No principal actors or live weather/result connections are claimed.\n\n| Site | Region | Model coverage | World Memory records |\n|---|---|---|---:|\n${rows.join('\n')}\n\n## Expansion proposals\n\n${r.proposedSites.length} proposals remain outside the rendered world. Unvisited is not the same as unauthored or unapproved.\n\n${Object.entries(counts).map(([k,v])=>`- ${k}: ${v}`).join('\n')}\n\n## Remaining gates for every site\n\nCandidate geometry/materials require source-reference visual review and Founder acceptance. Physical-phone/hardware performance, current state reconciliation, inhabitants and live data adapters remain separate work. Existing original folios remain separate edition assets. No source mutations, paid service, merge or deployment.\n`;
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const root=fileURLToPath(new URL('../../../',import.meta.url));
 const read=n=>JSON.parse(readFileSync(resolve(root,'world/data',n),'utf8'));
 const revision=execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim();
 const r=reportSiteCoverage({locations:read('locations.json'),candidates:read('atlas_location_candidates.json'),worldMemory:read('world_memory.json'),revision});
 const output=resolve(root,process.argv[2]||'productions/audience-site/dist/site-coverage.json');mkdirSync(dirname(output),{recursive:true});writeFileSync(output,JSON.stringify(r,null,2)+'\n');writeFileSync(output.replace(/\.json$/,'.md'),coverageMarkdown(r));
 console.log(JSON.stringify({currentSites:r.currentSites.length,proposedSites:r.proposedSites.length,missingModels:r.missingModelIds,publicationAuthorized:false,output}));
}
