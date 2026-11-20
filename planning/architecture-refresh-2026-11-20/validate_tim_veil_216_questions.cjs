// Structural validation only: this is not evidence of real consultation, engineering quality or independent QA.
'use strict';
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const docket=JSON.parse(fs.readFileSync(path.join(__dirname,'TIM_VEIL_18_DIRECTOR_216_QUESTIONS_V1.json'),'utf8'));
const groupNames=docket.directors.map(d=>d.director);
assert.equal(groupNames.length,18);
assert.equal(new Set(groupNames).size,18);
const ids=new Set(),texts=new Set();
let total=0;
for(const group of docket.directors){
  assert.equal(group.questions.length,12,group.director+' question count');
  assert.equal(group.count,12);
  for(const q of group.questions){
    assert.equal(q.status,'QUESTION_AUTHORED_NOT_HUMAN_ASKED');
    assert.equal(typeof q.id,'string');
    assert.match(q.id,/^[A-Z-]+-Q(0[1-9]|1[0-2])$/);
    assert.ok(!ids.has(q.id),'duplicate ID: '+q.id);
    ids.add(q.id);
    assert.ok(typeof q.text==='string'&&q.text.split(/\s+/).length>=8,'low-value or missing question');
    assert.ok(!texts.has(q.text),'duplicate question content');
    texts.add(q.text);
    total++;
  }
}
assert.equal(total,216);
assert.equal(docket.counts.total,216);
assert.equal(docket.advisory_mode.includes('no human consultation'),true);
console.log('PASS 18 Director scopes x 12 original, unique questions = 216; no human consultation claimed');
