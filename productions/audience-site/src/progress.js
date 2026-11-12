const PREFIX='schemin-reader-v1:';
const progressKey=(id,sourceVersion)=>PREFIX+encodeURIComponent(id)+':'+encodeURIComponent(sourceVersion||'unversioned');
export function loadProgress(id,sourceVersion){try{const value=Number(localStorage.getItem(progressKey(id,sourceVersion)));return Number.isFinite(value)?Math.min(1,Math.max(0,value)):0;}catch{return 0;}}
export function saveProgress(id,value,sourceVersion){if(typeof value!=='number'||!Number.isFinite(value))return;try{localStorage.setItem(progressKey(id,sourceVersion),String(Math.min(1,Math.max(0,value))));}catch{/* Reading remains available when browser storage is disabled. */}}
