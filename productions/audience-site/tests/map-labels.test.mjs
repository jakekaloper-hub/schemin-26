import test from 'node:test';
import assert from 'node:assert/strict';
import {mapLabelHeight,placeMapLabels} from '../src/map-labels.js';
test('crowded source anchors receive distinct readable 44px-plus callouts without moving dots',()=>{
 for(const width of [280,330,760,1000]){
  const points=Array.from({length:23},(_,i)=>({id:String(i),x:width/2,y:200+i%3})),original=structuredClone(points),height=mapLabelHeight(points.length,width),labels=placeMapLabels(points,width,height);
  assert.deepEqual(points,original);assert.equal(labels.length,23);
  for(const a of labels){assert(a.width>=44&&a.height>=44);assert(a.x>=0&&a.y>=0&&a.x+a.width<=width&&a.y+a.height<=height);for(const b of labels){if(a===b)continue;assert(a.x+a.width<=b.x||b.x+b.width<=a.x||a.y+a.height<=b.y||b.y+b.height<=a.y)}}
 }
});
