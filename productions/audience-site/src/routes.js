const HOME={page:'home',id:null};
export function parseRoute(hash=''){
  const raw=String(hash||'').replace(/^#/,'');
  if(!raw||raw==='home') return {...HOME};
  const [page,...rest]=raw.split('/');
  let id=null;
  if(rest.length){
    try{id=decodeURIComponent(rest.join('/'));}catch{return {page:'missing',id:null};}
  }
  return {page,id};
}
export function routeHash(page,id=null){
  if(page==='home'&&!id) return '#home';
  return '#'+page+(id?'/'+encodeURIComponent(String(id)):'');
}
