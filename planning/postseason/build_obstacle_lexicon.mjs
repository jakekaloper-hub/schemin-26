#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';

const dir=path.dirname(fileURLToPath(import.meta.url));
const defs=[
['combat','Controlled combat & honor','melee_ring','CONTACT',
'Stone Circle Sumo|Shield and Blade|Lance and Tilt|Twin Staff Balance|Spear Ring|Crown Wrestling Ladder|Hammerfall Grapple|Armored Flag Duel|Shield Gate Capture|Three Count Wrestle',
'Recognize distance, stance, lawful grappling and controlled impact','The opponent counters a change in balance, grip or defended space','A referee records the final lawful pin, strike or boundary capture'],
['marksmanship','Precision & archery','target_range','PROJECTILE',
'Longbow Convergence|Axe Wall|Crossbow Clock|Slingstone Spiral|Archers Split|Stormwind Marksmen|Siege Catapult Accuracy|Night Lantern Target|Bow and Obstacle|Moving Bullseye',
'Establish separated safe firing stations and visible target rules','Adjust range, elevation, wind or protected target motion while the rival responds','Officials lock the final target result behind a cleared backstop'],
['racing','Racing & riding','marked_course','VEHICLE',
'Dirt Bike Clifftop|Chariot Run|Stone Kart Derby|Mountain Cycle Pursuit|Mounted Relay|Sled Drag Dash|Lantern Cart Circuit|Stair Sprint Trial|Flag Line Sprint|Obstacle Drift Relay',
'Inspect equal equipment and declare a neutral start and route','One racer changes approach through a defended turn or checkpoint','The last protected crossing is recorded under the declared course rules'],
['sports','Ball & field sport','arena_field','SPORT',
'Last Basket Challenge|Floodline Soccer|Arena Dodgeball|Stonewall Lacrosse|Cliffside Putting|Court of Paddles|Ninepins Gauntlet|Bastion Volleyball|Croquet Siege|Banner Rugby',
'Introduce the sport, scoring objective and two opponent strategies','Counter-formation and field control shift across a new scoring period','A witnessed final goal, roll, possession or mark resolves the trial'],
['tactical','Tactical war game','arena_field','TACTICAL',
'Paintball Citadel|Banner Fort Siege|Three Bridges|Midnight Flag Heist|Shieldwall Formation|Signal Tower Contest|Bunker Circuit|Quarry Ambush|Siege Engine Demonstration|Ruined Bastion',
'Give equal maps, simulated units and nonlethal engagement rules','Opponents move to contest a changing marker, strongpoint or supply line','An arbiter certifies the final controlled objective without harming spectators'],
['board','Cards & boards','board_stage','PSYCHOLOGICAL',
'Last Hand Poker|Giant Chess Conquest|Go at the Gates|Bridge of Four|Domino Dominion|Blackjack Brink|Dice and Standards|Bluff Table|Nine Kings Checkers|Auction Vault',
'Announce sealed cards or board rules and reveal the first legal move','The second round exposes an opponent bluff, sacrifice or strategic trap','The final hand, piece, wager or lock becomes publicly intelligible'],
['engineering','Construction & siege craft','engineering_grid','STRUCTURAL',
'Trebuchet Target|Bridge Over Void|Tower of Counterweights|Floodgate Repair|Pulley Labyrinth|Stone Raft Craft|Siege Crank|Rolling Obstacle Rig|Clockwork Siege|Catapult Repair',
'Both sides receive equal tools, load limits and safe build space','A trial load or challenge changes the design problem and the counterstrategy','Inspect the final tested structure, device or repaired mechanism'],
['traverse','Height & traversal','obstacle_rig','FALL',
'Rope Bridge Duel|Cliff Ladder Traverse|Vertical Wall|Zipline Relay|Stone Maze Ascent|Logwalk Exchange|Cave Crawl Trial|Scaffold Ladder|Crown Stair Gauntlet|Quarry Net',
'Inspect anchors, harnesses and safe twin approach lines','Competing route choices change the climb, obstacle or line-of-sight balance','Verify the final protected marker and exit without spectator exposure'],
['aquatic','Water and harbor trials','water_basin','WATER',
'Harbor Rowing Sprint|Raft Across Quay|Water Polo Citadel|Dockside Relay|Canoe Slalom|Bridge and Boat Race|Paddleboard Pursuit|Tidal Marker Recovery|Watergate Escape|Towline Contest',
'Inspect controlled water depth, rescue facilities and neutral flotation gear','Two contenders adapt their course or craft at a defended water checkpoint','Certify the final buoy, dock, or raised marker after safety clearance'],
['endurance','Strength & endurance','marked_course','EXERTION',
'Stone Carry Circuit|Iron Bell Trial|Warship Tug|Gauntlet Run|Timber Haul|Sled Push|Sandbag Bastion|Balance of Twelve|Long Loop|Burden Gate',
'Define equal loads, time limits and voluntary health exits','Both sides manage fatigue and choose a strategic pacing adjustment','The final measured effort ends the trial without implying fatal consequences'],
['puzzles','Logic & escape','board_stage','COGNITIVE',
'Cipher Vault|Escape Tower|Signal Flag Logic|Twelve Keys|Labyrinth Letters|Mechanical Riddle|Hidden Standards|Knots and Numbers|Memory Wall|Forgery Tribunal',
'Open two identical evidence packets and announce the limits of knowledge','A new clue undermines an opponent theory while both attempt a revision','An official tests the final unlocked mechanism or verified solution'],
['hybrid','Combined championship trials','arena_field','MIXED',
'Arrow and Sprint|Chess and Capture|Joust and Longbow|Row and Riddle|Stone and Strategy|Three Trials of Crown|Bastion Pentathlon|Cards and Catapult|Paintball Puzzle|Last Standard',
'Commit to a composite objective whose sub-stages share one final outcome','Switch discipline while preserving the previously earned physical position','Finish with a decisive combined station and verified survivor']
];
const rareNeeds={
'Crossbow Clock':'target_range','Stormwind Marksmen':'wind_lane','Night Lantern Target':'target_range',
'Dirt Bike Clifftop':'vehicle_track','Chariot Run':'vehicle_track','Stone Kart Derby':'vehicle_track','Mountain Cycle Pursuit':'vehicle_track','Mounted Relay':'vehicle_track','Obstacle Drift Relay':'vehicle_track','Stair Sprint Trial':'stair_lanes',
'Joust and Longbow':'vehicle_track','Bridge and Boat Race':'water_course',
'Harbor Rowing Sprint':'water_course','Dockside Relay':'water_course','Canoe Slalom':'water_course','Paddleboard Pursuit':'water_course',
'Rope Bridge Duel':'rope_rig','Cliff Ladder Traverse':'vertical_climb','Vertical Wall':'vertical_climb','Scaffold Ladder':'vertical_climb','Crown Stair Gauntlet':'stair_lanes','Quarry Net':'rope_rig','Zipline Relay':'rope_rig',
'Trebuchet Target':'siege_yard','Siege Engine Demonstration':'siege_yard','Ruined Bastion':'siege_yard','Catapult Repair':'siege_yard',
'Floodgate Repair':'water_basin','Stone Raft Craft':'water_basin','Row and Riddle':'water_basin','Axe Wall':'target_range','Siege Catapult Accuracy':'siege_yard',
'The Last Standard':'arena_field'
};
const earliestByName={
'Dirt Bike Clifftop':2021,'Stone Kart Derby':2021,'Crossbow Clock':2021,'Night Lantern Target':2021,
'Moving Bullseye':2021,'Midnight Flag Heist':2021,'Zipline Relay':2021,
'Paddleboard Pursuit':2021,'Joust and Longbow':2021,'Row and Riddle':2021,
'Paintball Puzzle':2021,'Ruined Bastion':2021,'Clockwork Siege':2021,
'Bridge of Four':2021
};
const names=new Set();
const familyEntries=defs.map(([slug,label,base,risk,raw,a,b,c],familyIndex)=>{
 const list=raw.split('|');
 assert.equal(list.length,10,'expected ten per family '+slug);
 return {slug,label,base_capability:base,risk,phase_method:[a,b,c],entries:list.map((name,i)=>{
 assert.ok(!names.has(name),'duplicate scenario name '+name);names.add(name);
 const needs=[...new Set([base,rareNeeds[name]||base])];
 const special=name.toLowerCase();
 return {id:'OBST-'+String(familyIndex+1).padStart(2,'0')+'-'+String(i+1).padStart(2,'0'),name,family:slug,
  hook:'A public head-to-head contest organized around '+name.toLowerCase()+', using physical opponent counterplay rather than an isolated trick.',
  earliest_year:earliestByName[name]||2015,needs,risk_class:risk,
  three_phase:[
    {n:1,beat:'Opening trial',objective:a,unique_action:'Opening configuration for '+name.toLowerCase()+'; both contenders share a neutral starting condition.'},
    {n:2,beat:'Opponent counterpressure',objective:b,unique_action:'A rule-bound counter to the '+name.toLowerCase()+' objective changes the tactical problem for both sides.'},
    {n:3,beat:'Decisive confrontation',objective:c,unique_action:'Resolve '+name.toLowerCase()+' through witnessed, certified winner only; no source score changes.'}
  ],
  spectacle:'Two rival viewpoints, visible changing field state, impartial adjudication and a public bracket update.',
  material_footprint:'Temporary controlled rig; any historical scar or artifact requires a separately accepted annual world-state event.',
  canon_status:'CREATIVE_CANDIDATE_NOT_HISTORICAL_ESPN'
 };
 })};
});
const obstacles=familyEntries.flatMap(f=>f.entries);
assert.equal(obstacles.length,120);
const obj={
 schema:'schemin.postseason.obstacle_lexicon.v1',
 status:'UNPROMOTED_CREATIVE_REGISTRY',
 founder_source:'planning/postseason/FOUNDER_CHAMPIONSHIP_ISLAND_DECISIONS_2026-11-18.md',
 summit_source:'planning/postseason/SUMMIT_2026_11_19_18_DIRECTORS_12_ANGLES_V1.md',
 note:'Twelve families and 120 distinct named curated seed mechanisms; combinations beyond this are candidate design space, not 120 historical verified contests.',
 families:familyEntries.map(({slug,label,base_capability,risk,phase_method})=>({slug,label,base_capability,risk,phase_method})),
 obstacles,
 constraints:['Always two opposed competitors or teams','Always three causally linked stages','No deathmatch or lethal principal-character elimination','No unsupported advanced mechanism backdated to early league seasons','Never derive real result from an in-world task or device']
};
const out=path.join(dir,'OBSTACLE_LEXICON_120_V1.json');
const serialized=JSON.stringify(obj,null,2)+'\n';
if(process.argv.includes('--check')){
 assert.equal(fs.readFileSync(out,'utf8'),serialized,'Obstacle registry drift');
}else fs.writeFileSync(out,serialized);
console.log(JSON.stringify({status:'PASS',families:familyEntries.length,obstacles:obstacles.length,mode:process.argv.includes('--check')?'CHECK':'BUILD',source:'ORIGINAL_FICTION',file:path.basename(out)}));
