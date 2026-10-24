// Screen-space callouts only. Dot positions and source topology never change.
export function mapLabelHeight(count,width){const columns=Math.max(1,Math.floor((width-24)/150));return Math.max(420,Math.ceil(count/columns)*68+80);}
export function placeMapLabels(points,width,height){
 const columns=Math.max(1,Math.floor((width-24)/150)),cellWidth=(width-24)/columns;
 const cells=[];for(let row=0;row<Math.floor((height-80)/68);row++)for(let col=0;col<columns;col++)cells.push({x:12+col*cellWidth,y:40+row*68,width:cellWidth-8,height:60});
 return points.map(point=>{if(!cells.length)throw new Error('Map callouts need more vertical space');let best=0,distance=Infinity;cells.forEach((cell,i)=>{const d=(cell.x+cell.width/2-point.x)**2+(cell.y+cell.height/2-point.y)**2;if(d<distance){distance=d;best=i}});return {id:point.id,...cells.splice(best,1)[0]};});
}
