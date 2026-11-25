// Run from this folder: node validate.mjs
import fs from 'node:fs';
import assert from 'node:assert/strict';
function derive(snapshot,chronology){
 const req=(b,m)=>{if(!b)throw Error(m)};
 const cents=n=>{req(typeof n==="number"&&Number.isFinite(n)&&n>=0&&Math.abs(n*100-Math.round(n*100))<1e-6,"invalid points");return Math.round(n*100)};
 const pair=m=>[m.home,m.away].sort((a,b)=>a-b).join("-");
 const ids=Array.from({length:12},(_,i)=>i+1);
 req(snapshot.season===2026&&snapshot.leagueId==="1417621"&&snapshot.weeks.length===12,"wrong scope");
 const owners=Object.fromEntries(ids.map(id=>[id,{id,name:"",ribbon:"",wins:0,losses:0}]));
 req(chronology.weeks.length===11&&chronology.owners.length===12,"archive scope");
 for(let i=0;i<12;i++){
  const w=snapshot.weeks[i];req(w.week===i+1&&w.success&&w.matchups.length===6,"week "+(i+1));const seen=new Set();
  const archive=chronology.weeks[i];
  for(const m of w.matchups){
   for(const [id,name] of [[m.home,m.home_name],[m.away,m.away_name]]){req(ids.includes(id)&&!seen.has(id)&&typeof name==="string"&&name.length>0,"team integrity W"+w.week);seen.add(id);if(owners[id].name)req(owners[id].name===name,"name drift "+id);owners[id].name=name}
   if(i===11){req(m.winner==="UNDECIDED","week 12 already decided; pregame lock stale");continue}
   const h=cents(m.home_points),a=cents(m.away_points);req(h!==a&&m.winner===(h>a?"HOME":"AWAY"),"winner mismatch W"+w.week);
   const v=archive?.matchups.find(x=>x.home===m.home&&x.away===m.away);req(archive?.week===w.week&&v&&cents(v.home_points)===h&&cents(v.away_points)===a&&v.winner===m.winner,"archive mismatch W"+w.week+" "+pair(m));
   for(const [id,result] of [[m.home,h>a?"W":"L"],[m.away,a>h?"W":"L"]]){owners[id].ribbon+=result;owners[id][result==="W"?"wins":"losses"]++}
  }req(seen.size===12,"incomplete week");
 }
 const order=[1,5,10,6,2,12,3,7,8,4,9,11];const groups=["Burgers","Wings","Pizza"];
 const teams=order.map((id,i)=>{const o=owners[id],a=chronology.owners.find(x=>x.id===id);req(a&&a.name.trim()===o.name&&a.record===`${o.wins}-${o.losses}`&&a.chronology.map(x=>x.result).join("")===o.ribbon,"owner chronology mismatch "+id);return {...o,record:`${o.wins}-${o.losses}`,division:groups[Math.floor(i/4)]}});
 const prior=snapshot.weeks[3].matchups;const rematches=snapshot.weeks[11].matchups.map(m=>{const p=prior.find(x=>pair(x)===pair(m));req(p,"not a rematch "+pair(m));const home=p.winner==="HOME";const winner=home?p.home:p.away,loser=home?p.away:p.home,win=cents(home?p.home_points:p.away_points),loss=cents(home?p.away_points:p.home_points);return {winner,loser,winner_name:owners[winner].name,loser_name:owners[loser].name,week4_score:`${(win/100).toFixed(2)} – ${(loss/100).toFixed(2)}`,margin:((win-loss)/100).toFixed(2),week12_state:m.winner}});
 req(new Set(rematches.map(m=>m.winner+"-"+m.loser)).size===6,"duplicate rematches");
 req(teams.reduce((n,t)=>n+t.wins,0)===66&&teams.reduce((n,t)=>n+t.losses,0)===66,"totals");
 return {season:2026,as_of:"2026-11-25",completed_weeks:11,completed_matchups:66,owner_weeks:132,teams,rematches};
}
const read=p=>JSON.parse(fs.readFileSync(new URL(p,import.meta.url),'utf8'));
const snapshot=read('./provider-snapshot.json'), chronology=read('../W12_TWELVE_OWNER_W1_W11_SPORTS_CHRONOLOGY_2026-11-25.json');
const actual=derive(snapshot,chronology);assert.deepEqual(actual,read('./sports-lock.json').data);
for(const mutate of [s=>s.weeks[3].matchups[0].home_points+=1,s=>s.weeks[11].matchups[0].winner='HOME',s=>s.weeks[0].matchups.pop()]){const bad=structuredClone(snapshot);mutate(bad);assert.throws(()=>derive(bad,chronology));}
console.log('PASS: 66 final matchups, 132 team-weeks, 12 records and six undecided rematches; mutation tests passed');
