
const fs=require('fs'),puppeteer=require('/Users/jakekaloper/.npm/_npx/4b4c857f6efdfb61/node_modules/puppeteer');
(async()=>{let b;try{b=await puppeteer.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--no-first-run','--disable-extensions','--disable-gpu']});
let p=await b.newPage();await p.setViewport({width:1080,height:1920,deviceScaleFactor:1});
for(let i=1;i<=7;i++){let n='RT7-P'+String(i).padStart(2,'0');await p.goto('file://'+process.argv[2]+'/'+n+'.html',{waitUntil:'load'});await p.screenshot({path:process.argv[2]+'/'+n+'-SOURCE-PROOF.png',type:'png',captureBeyondViewport:false});console.log(n,fs.statSync(process.argv[2]+'/'+n+'-SOURCE-PROOF.png').size)}}finally{if(b)await b.close()}})().catch(e=>{console.error(e.stack);process.exitCode=1});
