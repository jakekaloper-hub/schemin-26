import Foundation
import AppKit
let base = URL(fileURLWithPath: CommandLine.arguments[1])
let data = try Data(contentsOf: base.appendingPathComponent("fixtures/p3i_page_copy.json"))
let pages = try JSONSerialization.jsonObject(with:data) as! [[String:Any]]
let out = base.appendingPathComponent("previews")
try FileManager.default.createDirectory(at:out,withIntermediateDirectories:true)
var results:[[String:Any]]=[]
for p in pages {
 let n=p["page"] as! Int
 let headline=p["headline"] as! String
 let copy=p["copy"] as! String
 let fact=p["fact"] as! String
 let image=NSImage(size:NSSize(width:1080,height:1920))
 image.lockFocus()
 NSColor(calibratedRed:0.065,green:0.075,blue:0.09,alpha:1).setFill()
 NSRect(x:0,y:0,width:1080,height:1920).fill()
 func draw(_ s:String,_ rect:NSRect,_ font:NSFont,_ color:NSColor)->CGFloat{
   let style=NSMutableParagraphStyle();style.lineSpacing=7;style.lineBreakMode = .byWordWrapping
   let attrs:[NSAttributedString.Key:Any]=[.font:font,.foregroundColor:color,.paragraphStyle:style]
   let measured=(s as NSString).boundingRect(with:NSSize(width:rect.width,height:10000),options:[.usesLineFragmentOrigin,.usesFontLeading],attributes:attrs)
   (s as NSString).draw(in:rect,withAttributes:attrs)
   return measured.height
 }
 let cream=NSColor(calibratedRed:0.94,green:0.88,blue:0.76,alpha:1)
 let grey=NSColor(calibratedRed:0.69,green:0.73,blue:0.77,alpha:1)
 _=draw("SCHEMIN’ AFTER DARK  /  SPOTLIGHT 001",NSRect(x:75,y:1775,width:930,height:60),NSFont.boldSystemFont(ofSize:30),grey)
 _=draw(headline,NSRect(x:75,y:1610,width:930,height:150),NSFont.boldSystemFont(ofSize:57),cream)
 NSColor(calibratedRed:0.15,green:0.18,blue:0.21,alpha:1).setFill()
 NSRect(x:75,y:1120,width:930,height:460).fill()
 _=draw("ARTWORK HELD  •  CHARACTER / ATLAS CANDIDATE",NSRect(x:110,y:1320,width:850,height:100),NSFont.monospacedSystemFont(ofSize:25,weight:.medium),grey)
 let bodyRect=NSRect(x:75,y:310,width:930,height:770)
 let needed=draw(copy,bodyRect,NSFont.systemFont(ofSize:34),cream)
 let factNeeded=draw(fact,NSRect(x:75,y:145,width:930,height:140),NSFont.systemFont(ofSize:22),grey)
 _=draw("NONCANON TYPOGRAPHY PROOF  /  \(String(format:"%02d",n))  /  1080 × 1920",NSRect(x:75,y:48,width:930,height:45),NSFont.monospacedSystemFont(ofSize:20,weight:.regular),grey)
 image.unlockFocus()
 let tiff=image.tiffRepresentation!
 let rep=NSBitmapImageRep(data:tiff)!
 let png=rep.representation(using:.png,properties:[:])!
 let file=out.appendingPathComponent(String(format:"page-%02d.png",n))
 try png.write(to:file)
 let resize=Process();resize.executableURL=URL(fileURLWithPath:"/usr/bin/sips")
 resize.arguments=["-z","1920","1080",file.path]
 resize.standardOutput=FileHandle.nullDevice
 try resize.run();resize.waitUntilExit()
 guard resize.terminationStatus == 0 else {fatalError("PNG resize failed")}

 results.append(["page":n,"copy_height":needed,"copy_capacity":770,"fits":needed<=770,"fact_height":factNeeded,"dimensions":"1080x1920"])
}
let report=try JSONSerialization.data(withJSONObject:results,options:[.prettyPrinted,.sortedKeys])
try report.write(to:base.appendingPathComponent("fixtures/p3i_layout_metrics.json"))
print(String(data:report,encoding:.utf8)!)
