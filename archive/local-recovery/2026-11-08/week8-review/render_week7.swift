import Foundation
import PDFKit
import AppKit
let p="/Users/jakekaloper/Desktop/Desktop - Jake’s MacBook Pro/Fantasy Football/Pro Schemin'/2026 Memos/Weeks/official/Schemin_26_Official_Week_7_Memo.pdf"
let dir=NSHomeDirectory()+"/Developer/ai/schemin-visual-local/week8-review/week7-pages"
if let doc=PDFDocument(url:URL(fileURLWithPath:p)) {
 for i in 0..<doc.pageCount {
  if let page=doc.page(at:i) {
   let thumb=page.thumbnail(of:NSSize(width:288,height:432),for:.mediaBox)
   if let t=thumb.tiffRepresentation,let b=NSBitmapImageRep(data:t),let data=b.representation(using:.jpeg,properties:[.compressionFactor:0.7]) {try? data.write(to:URL(fileURLWithPath:dir+String(format:"/page-%02d.jpg",i+1)))}
  }
 }
 print("Rendered",doc.pageCount)
}
