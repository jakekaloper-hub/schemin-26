#!/usr/bin/env node
/**
 * Atlas-adjacent challenge affordance / physical feasibility rule engine.
 * Explicitly NOT a Newtonian engine, structural survey, real-meter geography or
 * active World OS data. This is an unpromoted rule contract for candidate venues.
 */
export const VENUES=Object.freeze({
'CAND-POST-IRON-QUARRY':{round:'QF',terrain:'rock_cut_quarry',surface:'stone',weather:'sheltered',capacities:['barrier','melee_ring','stone_floor','target_range','marked_course','arena_field','engineering_grid','board_stage','card_table','obstacle_rig','water_basin','rope_rig','vertical_climb','siege_yard'],effects:'controlled_quarry_berm',provenance:'ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json'},
'CAND-POST-SALTWIND':{round:'QF',terrain:'windward_terraces',surface:'rock_and_prepared_field',weather:'wind_exposed',capacities:['barrier','melee_ring','stone_floor','target_range','wind_lane','marked_course','vehicle_track','arena_field','engineering_grid','board_stage','card_table','obstacle_rig','water_basin','rope_rig','vertical_climb','siege_yard','stair_lanes'],effects:'protected_sacrificial_rig',provenance:'ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json'},
'CAND-POST-BREAKWATER':{round:'QF',terrain:'sea_wall_court',surface:'stone_and_tideproof',weather:'tide_sensitive',capacities:['barrier','melee_ring','stone_floor','target_range','marked_course','vehicle_track','arena_field','engineering_grid','board_stage','card_table','obstacle_rig','water_basin','water_course','rope_rig','siege_yard'],effects:'protected_water_baffles',provenance:'ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json'},
'CAND-POST-CROWN-STAIR':{round:'SF',terrain:'monumental_grand_stair',surface:'stone',weather:'sheltered',capacities:['barrier','melee_ring','stone_floor','target_range','marked_course','arena_field','engineering_grid','board_stage','card_table','obstacle_rig','rope_rig','vertical_climb','siege_yard','stair_lanes'],effects:'temporary_gate_rig',provenance:'ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json'},
'CAND-POST-GROVE':{round:'SF',terrain:'protected_old_growth_grove',surface:'prepared_natural_ground',weather:'tree_canopy',capacities:['barrier','melee_ring','stone_floor','target_range','marked_course','arena_field','engineering_grid','board_stage','card_table','obstacle_rig','rope_rig','vertical_climb','siege_yard','forest_lane'],effects:'non_destructive_obstacle_rig',provenance:'ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json'},
'CAND-POST-LAST-FIELD':{round:'FINAL',terrain:'ancient_fixed_championship_oval',surface:'stone_and_maintained_turf',weather:'controlled_open_air',capacities:['barrier','melee_ring','stone_floor','target_range','marked_course','vehicle_track','arena_field','engineering_grid','board_stage','card_table','obstacle_rig','water_basin','rope_rig','vertical_climb','siege_yard'],effects:'temporary_stadium_infill_no_damage_to_final_stone',provenance:'ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json'}
});
export const RISK_CONTROLS=Object.freeze({
CONTACT:['padded_training_equipment','qualified_arbiter','medical_team','clear_throw_zone'],
PROJECTILE:['protected_backstop','firing_line_restrictions','spectator_exclusion_zone','official_range_clear'],
VEHICLE:['inspected_course','speed_limits','mechanical_inspection','segregated_marshal_lane'],
SPORT:['marked_playing_area','scorekeeping','participant_protection'],
TACTICAL:['nonlethal_replicas','boundary_marshals','fog_or_smoke_ventilation_if_used'],
PSYCHOLOGICAL:['impartial_dealer','sealed_materials','rule_display','no_fraud_or_forced_loss'],
STRUCTURAL:['safe_load_limit','rig_inspection','catch_net_or_barrier','repair_crew'],
FALL:['rated_anchors','harness_and_catch_net','rescue_access','no_unprotected_cliff_exposure'],
WATER:['qualified_rescue','floatation_gear','tidal_window','controlled_water_depth'],
EXERTION:['medical_screening','rest_protocol','voluntary_stop'],
COGNITIVE:['equal_puzzle_information','safe_exit','verified_solution'],
MIXED:['combined_objective_rules','stage_transition_protocol','appropriate_component_safety']
});
export function evaluatePhysicalFit({obstacle,venue_id,round,year,conditions={}}){
 const reasons=[],v=VENUES[venue_id];
 if(!v)reasons.push('UNREGISTERED_VENUE');
 else {
  if(v.round!==round)reasons.push('WRONG_ROUND_FOR_PERMANENT_ARENA');
  for(const c of obstacle?.needs||[])if(!v.capacities.includes(c))reasons.push('MISSING_CAPABILITY:'+c);
  if(v.weather==='wind_exposed' && ['STORM','SEVERE_WIND'].includes(conditions.weather))reasons.push('CLOSED_SEVERE_CLIFF_WEATHER');
  if(v.weather==='tide_sensitive' && ['STORM_SURGE','UNSAFE_TIDE'].includes(conditions.tide))reasons.push('CLOSED_UNSAFE_HARBOR_WATER');
  if(v.weather==='tree_canopy' && conditions.fire_hazard==='HIGH' && (obstacle?.risk_class==='TACTICAL'||obstacle?.risk_class==='PROJECTILE'))reasons.push('CLOSED_GROVE_FIRE_RISK');
 }
 if(!obstacle || !obstacle.id)reasons.push('OBSTACLE_MISSING');
 else {
  if(!Number.isInteger(year)||year<obstacle.earliest_year)reasons.push('TECH_NOT_AVAILABLE_IN_HISTORICAL_ERA');
  if(!Array.isArray(obstacle.three_phase)||obstacle.three_phase.length!==3)reasons.push('THREE_PHASES_REQUIRED');
  if(!RISK_CONTROLS[obstacle.risk_class])reasons.push('UNKNOWN_RISK_CONTROL_CLASS');
 }
 return {
  eligible:reasons.length===0,
  reasons,
  required_controls:RISK_CONTROLS[obstacle?.risk_class]||[],
  venue_id,round,year,terrain:v?.terrain||null,
  physical_evidence:'CANDIDATE_AFFORDANCE_CONTRACT_NOT_MEASURED_GIS_OR_REAL_PHYSICS',
  outcome_authority:'ESPN_VERIFIED_MATCHUP_ONLY',
  world_mutation:'NONE',
  scenic_scars:'CANDIDATE_ONLY_UNLESS_WORLD_EVENT_PROMOTED'
 };
}
export function candidateCompatibility(lexicon,year=2026){
 const counts={};
 for(const [site,v] of Object.entries(VENUES)){
  counts[site]=lexicon.obstacles.filter(o=>evaluatePhysicalFit({obstacle:o,venue_id:site,round:v.round,year}).eligible).length;
 }
 return {year,eligible_scenarios_by_site:counts,total_valid_site_scenario_pairs:Object.values(counts).reduce((a,b)=>a+b,0)};
}
