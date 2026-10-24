import AppKit
import Foundation
import ImageIO

let root = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : FileManager.default.currentDirectoryPath
let srcPath = (root as NSString).appendingPathComponent("canon/characters/assets/lineups/SCHEMIN_26_COMMISSIONER_APPROVED_LINEUP_2026_10_18.png")
let destination = (root as NSString).appendingPathComponent("canon/characters/assets/lineups/2026-10-18-crops")
try FileManager.default.createDirectory(atPath: destination, withIntermediateDirectories: true)
let url=URL(fileURLWithPath: srcPath)
guard let src=CGImageSourceCreateWithURL(url as CFURL,nil),
      let image=CGImageSourceCreateImageAtIndex(src,0,nil) else { fatalError("unreadable") }
guard image.width==1448 && image.height==1086 else { fatalError("bad dimensions") }
let names=[
 "CHAR-JAKE-KALOPER","CHAR-WILSON-LOOK","CHAR-PHILLIP-PITTS","CHAR-AUSTIN-BYARS",
 "CHAR-BRANDON-PRYOR","CHAR-JORDAN-HOLLINGSHEAD","CHAR-ZACH-WILSON","CHAR-KEVIN-ZEEK",
 "CHAR-BOBBY-MITCHELL","CHAR-BEN-WHIPPLE","CHAR-DAVID-BABB","CHAR-MANNING-WELTY"
]
let xStops=[0,362,724,1086,1448]
let yStops=[0,405,695,1086]
for (i,character) in names.enumerated() {
 let col=i%4, row=i/4
 let x=xStops[col],y=yStops[row],w=xStops[col+1]-x,h=yStops[row+1]-y
 let area=CGRect(x:x,y:y,width:w,height:h)
 guard let crop=image.cropping(to:area) else {fatalError("crop failed "+character)}
 let rep=NSBitmapImageRep(cgImage:crop)
 guard let encoded=rep.representation(using:.png,properties:[:]) else {fatalError("png encode")}
 let file=(destination as NSString).appendingPathComponent(character+".png")
 try encoded.write(to:URL(fileURLWithPath:file),options:.atomic)
 print(character,"x",x,"y",y,"w",w,"h",h,"size",encoded.count)
}
