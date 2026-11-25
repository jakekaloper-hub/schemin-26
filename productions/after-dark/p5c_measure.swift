import AppKit
import Foundation
let base=URL(fileURLWithPath:CommandLine.arguments[1])
let data=try Data(contentsOf:base.appendingPathComponent("P5B_PAGE_00_OPENING_PRODUCTION_KIT.json"))
let d=try JSONSerialization.jsonObject(with:data) as! [String:Any]
let c=d["copy"] as! [String:String]
func size(_ text:String,_ fontSize:CGFloat,_ width:CGFloat)->CGFloat {
 let font=NSFont.systemFont(ofSize:fontSize)
 let attrs:[NSAttributedString.Key:Any]=[.font:font]
 return (text as NSString).boundingRect(with:NSSize(width:width,height:3000),options:[.usesFontLeading,.usesLineFragmentOrigin],attributes:attrs).height
}
let slots:[(String,CGFloat,CGFloat)]=[("eyebrow",26,50),("masthead",78,220),("tagline",40,120),("joke",32,130),("announcer",31,180),("reveal",35,100),("bill",25,60),("guest",27,75)]
var rows=[[String:Any]]()
for (key,font,limit) in slots {
 let height=size(c[key]!,font,900)
 rows.append(["field":key,"font_size":font,"measured_height":height,"allocated_height":limit,"fits":height<=limit])
}
let ok=rows.allSatisfy{$0["fits"] as! Bool}
let report:[String:Any]=["status":ok ? "PREFLIGHT_TEXT_FIT_PASS":"TEXT_FIT_FAIL","canvas":[1080,1920],"rows":rows,"note":"Native AppKit type metrics only; not a rendered-image or subjective visual QA."]
let bytes=try JSONSerialization.data(withJSONObject:report,options:[.prettyPrinted,.sortedKeys])
try bytes.write(to:base.appendingPathComponent("fixtures/p5c_opening_text_fit.json"))
print(String(data:bytes,encoding:.utf8)!)
if !ok {exit(1)}
