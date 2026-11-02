import Foundation
import CoreGraphics
import Vision
import AppKit
let gamePID=NSRunningApplication.runningApplications(withBundleIdentifier:"org.struma.mkxp-z").first?.processIdentifier
let infos=CGWindowListCopyWindowInfo([.optionOnScreenOnly,.excludeDesktopElements],kCGNullWindowID) as! [[String:Any]]
if CommandLine.arguments.count < 2 {
 for i in infos where (i[kCGWindowOwnerPID as String] as? Int)==gamePID.map(Int.init) {print(i)}
 exit(0)
}
let url=URL(fileURLWithPath:CommandLine.arguments[1])
let request=VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = false
try VNImageRequestHandler(url:url).perform([request])
let result=(request.results ?? []).map { r -> [String:Any] in
 let box=r.boundingBox
 return ["text":r.topCandidates(1).first?.string ?? "", "x":box.minX,"y":1-box.maxY,"w":box.width,"h":box.height]
}
let data=try JSONSerialization.data(withJSONObject:result,options:[.sortedKeys])
print(String(data:data,encoding:.utf8)!)
