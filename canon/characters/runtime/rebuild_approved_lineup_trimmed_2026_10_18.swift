import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

// Pixel-only, non-generative and non-destructive source extraction.
// Strips the lower panel region containing nameplates; this DOES NOT
// eliminate the background/title or pass a visual subject-isolation gate.
let root = CommandLine.arguments.count > 1 ? URL(fileURLWithPath:CommandLine.arguments[1], isDirectory: true) : URL(fileURLWithPath:FileManager.default.currentDirectoryPath, isDirectory:true)
let out = CommandLine.arguments.count > 2 ? URL(fileURLWithPath:CommandLine.arguments[2], isDirectory: true) : root.appendingPathComponent("canon/characters/assets/lineups/2026-10-18-nameplate-trimmed", isDirectory:true)
let manifestURL = root.appendingPathComponent("canon/characters/APPROVED_LINEUP_2026_10_18.json")
let doc = try JSONSerialization.jsonObject(with:Data(contentsOf:manifestURL)) as! [String:Any]
let original = root.appendingPathComponent(doc["stored_repository_path"] as! String)
let source = CGImageSourceCreateWithURL(original as CFURL, nil)!
let image = CGImageSourceCreateImageAtIndex(source, 0, nil)!
guard image.width == 1448 && image.height == 1086 else { fatalError("Unexpected approved master image geometry") }
try FileManager.default.createDirectory(at:out,withIntermediateDirectories:true)
let entries = doc["individuals"] as! [[String:Any]]
for e in entries {
    let id = e["character_id"] as! String
    let coords = e["crop_rectangle_top_left"] as! [String:Int]
    let y = coords["y"]!
    let h = coords["height"]!
    // Deliberate conservative trim: do not generate pixels, inpaint or recompose.
    let strip = y == 0 ? 72 : (y == 405 ? 55 : 115)
    let rect = CGRect(x:coords["x"]!,y:y,width:coords["width"]!,height:h-strip)
    guard let cropped = image.cropping(to:rect) else { fatalError("Crop failed for "+id) }
    let dest=out.appendingPathComponent(id+".png")
    guard let writer=CGImageDestinationCreateWithURL(dest as CFURL,UTType.png.identifier as CFString,1,nil) else { fatalError("Writer failed") }
    CGImageDestinationAddImage(writer,cropped,nil)
    guard CGImageDestinationFinalize(writer) else { fatalError("PNG write failed") }
    print("\(id)\t\(Int(rect.minX))\t\(Int(rect.minY))\t\(Int(rect.width))\t\(Int(rect.height))\t\(dest.path)")
}
