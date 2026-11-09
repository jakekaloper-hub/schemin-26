import Foundation
import PDFKit
import AppKit
let dir=CommandLine.arguments[1]
let source=try String(contentsOfFile:dir+"/week8_path.txt",encoding:.utf8)
guard let doc=PDFDocument(url:URL(fileURLWithPath:source)) else {fatalError("PDF unreadable")}
let output=dir+"/week8-review"
try FileManager.default.createDirectory(atPath:output,withIntermediateDirectories:true)
var rows=[[String:Any]]()
func save(_ image:NSImage,_ path:String){guard let t=image.tiffRepresentation, let rep=NSBitmapImageRep(data:t),let png=rep.representation(using:.png,properties:[:]) else {fatalError("PNG encode")};try! png.write(to:URL(fileURLWithPath:path))}
for i in 0..<doc.pageCount {let page=doc.page(at:i)!,rect=page.bounds(for:.mediaBox);let img=page.thumbnail(of:NSSize(width:540,height:1000),for:.mediaBox);save(img,output+String(format:"/page-%02d.png",i+1));rows.append(["page":i+1,"width_pt":rect.width,"height_pt":rect.height,"text_characters":page.string?.count ?? 0])}
let cols=4,cellW=280,cellH=530
for start in stride(from:0,to:doc.pageCount,by:12){let count=min(12,doc.pageCount-start),r=(count+cols-1)/cols;let sheet=NSImage(size:NSSize(width:cols*cellW,height:r*cellH));sheet.lockFocus();NSColor.white.setFill();NSRect(x:0,y:0,width:cols*cellW,height:r*cellH).fill();for j in 0..<count {let n=start+j+1;let im=NSImage(contentsOfFile:output+String(format:"/page-%02d.png",n))!;let x=(j%cols)*cellW+8;let y=(r-1-j/cols)*cellH+24;im.draw(in:NSRect(x:x,y:y,width:264,height:495));("W8 / "+String(n) as NSString).draw(at:NSPoint(x:x,y:y-20),withAttributes:[.font:NSFont.systemFont(ofSize:14),.foregroundColor:NSColor.black])};sheet.unlockFocus();save(sheet,output+"/contact-"+String(start/12+1)+".png")}
let data=try JSONSerialization.data(withJSONObject:["pages":doc.pageCount,"source":source,"page_geometry":rows],options:[.prettyPrinted,.sortedKeys]);try data.write(to:URL(fileURLWithPath:output+"/source.json"));print("PDF_PAGES",doc.pageCount,"CONTACTS",(doc.pageCount+11)/12,"OUTPUT",output)
