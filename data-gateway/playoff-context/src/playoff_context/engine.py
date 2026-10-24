from __future__ import annotations
from dataclasses import dataclass
from math import exp, sqrt
from random import Random
from statistics import mean, pstdev
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

@dataclass(frozen=True)
class TeamState:
    team_id: str
    name: str
    wins: int
    losses: int
    ties: int = 0
    points_for: float = 0.0
    scores: Tuple[float, ...] = ()

@dataclass(frozen=True)
class Game:
    week: int
    home_id: str
    away_id: str
    home_projection: Optional[float] = None
    away_projection: Optional[float] = None

@dataclass(frozen=True)
class LeagueRules:
    playoff_teams: int
    regular_season_weeks: int
    tiebreaker: str = "UNKNOWN"
    divisions: Optional[Mapping[str, str]] = None

@dataclass(frozen=True)
class Strength:
    mu: float
    sigma: float

def _blend_mean(scores: Sequence[float], projection: Optional[float], league_mean: float) -> float:
    if scores:
        season = mean(scores)
        recent = mean(scores[-3:])
        n = len(scores)
        w_data = min(0.80, 0.35 + 0.10 * n)
        observed = 0.60 * season + 0.40 * recent
        prior = projection if projection and projection > 0 else league_mean
        return w_data * observed + (1.0 - w_data) * prior
    return projection if projection and projection > 0 else league_mean

def estimate_strengths(teams: Mapping[str, TeamState], next_projection: Optional[Mapping[str, float]] = None, min_sigma: float = 12.0) -> Dict[str, Strength]:
    all_scores = [s for t in teams.values() for s in t.scores]
    league_mean = mean(all_scores) if all_scores else 130.0
    league_sigma = pstdev(all_scores) if len(all_scores) > 1 else 22.0
    out: Dict[str, Strength] = {}
    for team_id, t in teams.items():
        proj = (next_projection or {}).get(team_id)
        mu = _blend_mean(t.scores, proj, league_mean)
        sigma = max(min_sigma, pstdev(t.scores) if len(t.scores) > 1 else league_sigma)
        if len(t.scores) < 5:
            sigma = 0.5 * sigma + 0.5 * max(min_sigma, league_sigma)
        out[team_id] = Strength(mu=mu, sigma=sigma)
    return out

def win_probability(a: Strength, b: Strength) -> float:
    scale = max(1.0, sqrt(a.sigma * a.sigma + b.sigma * b.sigma) * 0.5513)
    x = (a.mu - b.mu) / scale
    return 1.0 / (1.0 + exp(-x))

def rank_teams(records: Mapping[str, Tuple[int, int, int]], points_for: Mapping[str, float]) -> List[str]:
    return sorted(records, key=lambda tid:(records[tid][0] + 0.5*records[tid][2], points_for.get(tid,0.0), tid), reverse=True)

def simulate(teams: Mapping[str, TeamState], future_games: Sequence[Game], rules: LeagueRules, simulations: int = 50000, seed: int = 2604, forced_results: Optional[Mapping[Tuple[int,str,str],str]] = None) -> Dict[str, dict]:
    if simulations <= 0:
        raise ValueError("simulations must be positive")
    rng = Random(seed)
    forced_results = forced_results or {}
    proj: Dict[str,List[float]] = {tid:[] for tid in teams}
    for g in future_games:
        if g.home_projection: proj[g.home_id].append(g.home_projection)
        if g.away_projection: proj[g.away_id].append(g.away_projection)
    next_proj={tid:mean(v) for tid,v in proj.items() if v}
    strength=estimate_strengths(teams,next_proj)
    playoff_count={tid:0 for tid in teams}
    seed_count={tid:[0]*(len(teams)+1) for tid in teams}
    final_wins={tid:[] for tid in teams}
    for _ in range(simulations):
        rec={tid:[t.wins,t.losses,t.ties] for tid,t in teams.items()}
        pf={tid:t.points_for for tid,t in teams.items()}
        for g in future_games:
            key=(g.week,g.home_id,g.away_id)
            forced=forced_results.get(key)
            if forced==g.home_id: hw=True
            elif forced==g.away_id: hw=False
            else: hw=rng.random()<win_probability(strength[g.home_id],strength[g.away_id])
            hs=max(0.0,rng.gauss(strength[g.home_id].mu,strength[g.home_id].sigma))
            as_=max(0.0,rng.gauss(strength[g.away_id].mu,strength[g.away_id].sigma))
            pf[g.home_id]+=hs; pf[g.away_id]+=as_
            if hw:
                rec[g.home_id][0]+=1; rec[g.away_id][1]+=1
            else:
                rec[g.away_id][0]+=1; rec[g.home_id][1]+=1
        ranking=rank_teams({k:tuple(v) for k,v in rec.items()},pf)
        for idx,tid in enumerate(ranking,start=1):
            seed_count[tid][idx]+=1
            if idx<=rules.playoff_teams: playoff_count[tid]+=1
            final_wins[tid].append(rec[tid][0])
    result={}
    for tid in teams:
        wins=sorted(final_wins[tid])
        lo=wins[int(0.10*(len(wins)-1))]; hi=wins[int(0.90*(len(wins)-1))]
        result[tid]={
            "playoff_probability":playoff_count[tid]/simulations,
            "seed_probability":{str(i):seed_count[tid][i]/simulations for i in range(1,len(teams)+1) if seed_count[tid][i]},
            "expected_final_wins":mean(final_wins[tid]),
            "final_wins_p10_p90":[lo,hi],
        }
    return result

def remaining_games_by_team(future_games: Sequence[Game]) -> Dict[str,int]:
    rem={}
    for g in future_games:
        rem[g.home_id]=rem.get(g.home_id,0)+1
        rem[g.away_id]=rem.get(g.away_id,0)+1
    return rem

def exact_bounds_status(teams: Mapping[str, TeamState], future_games: Sequence[Game], rules: LeagueRules) -> Dict[str,dict]:
    rem=remaining_games_by_team(future_games)
    ids=list(teams); k=rules.playoff_teams; out={}
    for tid in ids:
        t=teams[tid]; min_w=t.wins; max_w=t.wins+rem.get(tid,0)
        guaranteed_above=sum(1 for oid in ids if oid!=tid and teams[oid].wins>max_w)
        if guaranteed_above>=k:
            out[tid]={"status":"ELIMINATED","class":"EXACT","proof":"win_bounds"}; continue
        possible_at_or_above=sum(1 for oid in ids if oid!=tid and teams[oid].wins+rem.get(oid,0)>=min_w)
        if possible_at_or_above<=k-1:
            out[tid]={"status":"CLINCHED","class":"EXACT","proof":"win_bounds"}; continue
        out[tid]={"status":"ALIVE","class":"EXACT","proof":"not_eliminated_by_bounds","note":"Clinching/elimination beyond safe W/L bounds may remain UNKNOWN until tiebreak-complete solving is available."}
    return out

def conditional_leverage(teams: Mapping[str, TeamState], future_games: Sequence[Game], rules: LeagueRules, current_game: Game, simulations: int = 20000, seed: int = 2604) -> Dict[str,dict]:
    key=(current_game.week,current_game.home_id,current_game.away_id)
    win_home=simulate(teams,future_games,rules,simulations,seed,{key:current_game.home_id})
    win_away=simulate(teams,future_games,rules,simulations,seed+1,{key:current_game.away_id})
    out={}
    for tid,win_result,loss_result in ((current_game.home_id,win_home,win_away),(current_game.away_id,win_away,win_home)):
        pw=win_result[tid]["playoff_probability"]; pl=loss_result[tid]["playoff_probability"]
        out[tid]={"conditional_win_probability":pw,"conditional_loss_probability":pl,"leverage_delta_pp":abs(pw-pl)*100.0}
    return out
