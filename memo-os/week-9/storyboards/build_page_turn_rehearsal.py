"""Reflow the existing GOTW drawing into a standalone page-turn rehearsal.
No scene is redrawn, no identity is promoted, and no result is selected.
Run this file from any working directory; uses only the Python standard library.
"""
from pathlib import Path
import copy
import hashlib
import html
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'W09_GOTW_ROUGH_BLOCKING_BOARD_V1.svg'
OUTPUT = HERE / 'W09_GOTW_PAGE_TURN_REHEARSAL_V1.html'
NS = '{http://www.w3.org/2000/svg}'
ET.register_namespace('', 'http://www.w3.org/2000/svg')


def build():
    original = SOURCE.read_bytes()
    root = ET.fromstring(original)
    defs = root.find(NS + 'defs')
    frames = {g.get('id'): g for g in root.findall(NS + 'g') if g.get('id', '').startswith('frame-')}
    if len(frames) != 9 or defs is None:
        raise ValueError('Expected the original nine-frame drawing and its definitions')
    def picture(number):
        key = f'frame-{number}'
        frame = frames[key]
        scene = next((g for g in frame.findall(NS + 'g') if g.get('clip-path')), None)
        if scene is None:
            raise ValueError(f'No scene group found in {key}')
        svg = ET.Element(NS + 'svg', {'viewBox': '0 0 720 340', 'role': 'img', 'aria-label': f'Existing rough drawing, source {key}', 'data-source-frame': key})
        svg.append(copy.deepcopy(defs))
        g = copy.deepcopy(scene)
        g.attrib.pop('transform', None)
        svg.append(g)
        # Each page owns its SVG IDs, avoiding cross-SVG URL collisions.
        text = ET.tostring(svg, encoding='unicode')
        return text.replace('id="sceneClip"', f'id="{key}-clip"').replace('url(#sceneClip)', f'url(#{key}-clip)').replace('id="arrow"', f'id="{key}-arrow"').replace('url(#arrow)', f'url(#{key}-arrow)')
    pages = [
        ('P04', 'The Invitation', 'Courtesy, before competition.', [(1, '01 / WIDE', 'The calm course introduces the clubhouse and water before either matters.'), (2, '02 / TWO-SHOT', 'A scorecard changes hands. Hospitality becomes a personal challenge.')], 'The next page answers this invitation with action.'),
        ('P05', 'A Round of Answers', 'Different shots. A changing relationship.', [(3, '03 / FOLLOW-THROUGH', 'Duckhook makes the opening statement; ObiWan watches outside the swing arc.'), (4, '04 / RECOVERY', 'ObiWan answers a different physical problem. Club, sand and ball stay distinct.'), (5, '05 / REACTION', 'Their smiles fade. This reaction changes the meaning of the round.')], 'The next page slows the rhythm and makes the risk visible.'),
        ('P06', 'The Quiet Before the Putt', 'Show the danger. Then hold the breath.', [(6, '06 / GEOGRAPHY', 'Ball, flag, sloped apron and pond are readable together before the stroke.'), (7, '07 / PAUSE', 'The grip steadies; the opponent waits. No result has been shown.')], 'The next page is unresolved. Preview either ending; neither is the actual result.'),
        ('P07A', 'The Last Putt', 'IF OBIWAN WINS — hypothetical preview only', [(8, '08A / CONDITIONAL', 'Duckhook’s overhit follows the established slope toward the pond.')], 'Alternative A only. This is not a reported score, winner, or final memo page.'),
        ('P07B', 'The Last Putt', 'IF DUCKHOOK WINS — hypothetical preview only', [(9, '08B / CONDITIONAL', 'ObiWan’s failed execution contrasts with Duckhook’s steady finish.')], 'Alternative B only. This is mutually exclusive with A, not a second consecutive event.'),
    ]
    sheets = []
    for pid, title, deck, moments, transition in pages:
        panels = ''.join('<figure>' + picture(n) + '<figcaption><b>' + html.escape(label) + '</b><span>' + html.escape(note) + '</span></figcaption></figure>' for n, label, note in moments)
        sheets.append(f'<section class="sheet count-{len(moments)}" data-page="{pid}" hidden><div class="eyebrow">SCHEMIN ’26 / WEEK 9 / GOTW <span>{pid}</span></div><header><h1>{html.escape(title)}</h1><p>{html.escape(deck)}</p></header><div class="panels">{panels}</div><div class="transition copy">{html.escape(transition)}</div><footer>ROUGH PAGE-TURN REHEARSAL <span>No final art · No verified winner</span></footer></section>')
    body = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Week 9 — GOTW page-turn rehearsal</title>
<style>
:root{color-scheme:light}*{box-sizing:border-box}body{margin:0;background:#1d2421;color:#f4f0e6;font:16px/1.45 system-ui,sans-serif}button{font:inherit;cursor:pointer;min-height:44px;border:1px solid #727d73;background:#354139;color:#fff;border-radius:6px;padding:8px 14px}button:hover{background:#4b5a50}button:focus-visible{outline:3px solid #e7c984;outline-offset:3px}button:disabled{opacity:.4;cursor:default}nav{position:sticky;top:0;z-index:20;background:#1d2421f5;border-bottom:1px solid #576056;padding:10px 16px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}.brand{font-weight:700;margin-right:auto}.status{padding:10px 18px;text-align:center;font-size:13px;color:#d8ded6}.stage{position:relative;margin:0 auto 28px;overflow:hidden}.sheet{width:1080px;height:1920px;padding:55px 60px;background:#f4f0e5;color:#30352e;position:absolute;top:0;left:0;transform-origin:top left;display:flex;flex-direction:column;box-shadow:0 12px 50px #0005}.sheet[hidden]{display:none}.eyebrow{font-size:23px;font-weight:700;letter-spacing:1.5px;border-bottom:2px solid #6a7265;padding-bottom:18px;display:flex;justify-content:space-between}header{padding:30px 0 24px}h1{font-size:61px;line-height:1.04;margin:0 0 18px;letter-spacing:-2px}header p{font-size:26px;margin:0;color:#56604f}.panels{display:flex;flex-direction:column;gap:28px}.count-3 figure svg{height:370px}.count-3 .panels{gap:20px}.count-2 .panels{gap:56px;margin-top:70px}.count-1 .panels{margin-top:180px}figure{margin:0;border:1px solid #b6b6a7;background:#faf8ef}figure svg{display:block;width:100%;height:auto}figcaption{padding:12px 16px 15px;font-size:23px;line-height:1.3;border-top:1px solid #cbc7b8;display:flex;gap:18px}figcaption b{font-size:19px;min-width:150px;letter-spacing:.6px}.transition{margin-top:auto;padding:28px 0;font-size:27px;line-height:1.35;max-width:880px}footer{border-top:1px solid #b3b6a8;padding-top:20px;font-size:20px;display:flex;justify-content:space-between;color:#68705f}.hide-captions figcaption,.hide-captions .copy,.hide-captions header p{visibility:hidden}.hide-captions svg text{visibility:hidden}.selector{padding:32px;text-align:center;max-width:760px;margin:40px auto;background:#2e3a32;border:1px solid #77816e;border-radius:12px}.selector h2{font-size:28px}.selector button{margin:10px}.selector[hidden]{display:none}.review-note{overflow-wrap:anywhere;max-width:820px;margin:20px auto 40px;padding:0 20px;color:#c8d0c5;font-size:14px}.review-note h2{font-size:18px}#ending-controls{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin:10px 0 18px}#ending-controls[hidden]{display:none}@media(max-width:520px){nav{gap:7px;padding:8px}.brand{font-size:14px;width:100%}button{font-size:13px;padding:7px 10px}.status{font-size:12px}}@media print{nav,.status,.selector,.review-note,#ending-controls{display:none}.stage{width:1080px!important;height:auto!important;overflow:visible}.sheet{position:relative;transform:none!important;break-after:page}.sheet[hidden]{display:flex}}
</style></head><body>
<nav aria-label="Storyboard controls"><div class="brand">THE CHARITY CLASSIC / ROUGH REHEARSAL</div><button id="back">Previous</button><span id="page-label" aria-live="polite"></span><button id="next">Next</button><button id="captions" aria-pressed="false">Hide captions</button></nav>
<div class="status">Existing drawn panels reflowed for page turns. Not new illustration, approved publication, or a reported Week 9 outcome.</div>
<div id="ending-controls" hidden><button data-branch="A">Preview: ObiWan wins</button><button data-branch="B">Preview: Duckhook wins</button><button id="clear-branch">Clear preview</button></div>
<div class="selector" id="choose-ending" hidden><h2>The final result is not selected.</h2><p>Review one alternative at a time. This choice previews a fictional ending; it does not record a real winner.</p><button data-branch="A">IF OBIWAN WINS</button><button data-branch="B">IF DUCKHOOK WINS</button></div>
<main class="stage" id="stage">__SHEETS__</main>
<div class="review-note"><h2>Page-turn review</h2><p>Hide the captions. Can you follow the invitation, competing actions, change in mood, visible hazard, pause and one alternative finish? The pond stays on the same side; the opponent stays outside the swing. A review interface is not independent audience approval.</p><p>Source: PR287 rough SVG / SHA-256 __SOURCE_SHA__. The two finale previews are mutually exclusive. No player statistics or final scores have been supplied.</p></div>
<script>
const actualResult = null;
let branch = null;
let position = 0;
const ids = ['P04','P05','P06','P07'];
const stage=document.getElementById('stage'), chooser=document.getElementById('choose-ending');
function resize(){const viewport=document.documentElement.clientWidth;const scale=Math.min((viewport-24)/1080,0.56);stage.style.width=(1080*scale)+'px';stage.style.height=(1920*scale)+'px';document.querySelectorAll('.sheet').forEach(p=>p.style.transform='scale('+scale+')');}
function show(){const id=position===3?(branch?'P07'+branch:null):ids[position];document.querySelectorAll('.sheet').forEach(p=>p.hidden=p.dataset.page!==id);stage.hidden=!id;chooser.hidden=position!==3||branch!==null;document.getElementById('ending-controls').hidden=position!==3;document.getElementById('page-label').textContent=(id||'P07 — choose a preview')+' / 4-page sequence';document.getElementById('back').disabled=position===0;document.getElementById('next').disabled=position===3;resize();}
document.getElementById('next').onclick=()=>{position=Math.min(3,position+1);show();window.scrollTo(0,0)};
document.getElementById('back').onclick=()=>{position=Math.max(0,position-1);show();window.scrollTo(0,0)};
document.getElementById('captions').onclick=()=>{document.body.classList.toggle("hide-captions");const hidden=document.body.classList.contains('hide-captions');document.getElementById('captions').setAttribute('aria-pressed',String(hidden));document.getElementById('captions').textContent=hidden?'Show captions':'Hide captions'};
document.querySelectorAll('[data-branch]').forEach(b=>b.onclick=()=>{branch=b.dataset.branch;position=3;show()});
document.getElementById('clear-branch').onclick=()=>{branch=null;show()};
document.addEventListener('keydown',e=>{if(e.target.tagName==='BUTTON')return;if(e.key==='ArrowRight'){position=Math.min(3,position+1);show()}if(e.key==='ArrowLeft'){position=Math.max(0,position-1);show()}});
const requested=location.hash.slice(1);if(['P04','P05','P06'].includes(requested))position=ids.indexOf(requested);if(['P07A','P07B'].includes(requested)){position=3;branch=requested.slice(-1)}if(requested==='P07')position=3;
if(new URLSearchParams(location.search).get('captions')==='off')document.getElementById('captions').click();
window.addEventListener('resize',resize);show();
</script></body></html>'''
    document=body.replace('__SHEETS__','\n'.join(sheets)).replace('__SOURCE_SHA__',hashlib.sha256(original).hexdigest())
    OUTPUT.write_text(document)
    print(f'Built {OUTPUT.name}: five preview states from nine existing frames, no actual result selected')
    return OUTPUT

if __name__=='__main__':
    build()
