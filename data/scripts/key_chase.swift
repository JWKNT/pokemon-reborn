import Foundation
import CoreGraphics
import AppKit
let app=NSRunningApplication.runningApplications(withBundleIdentifier:"org.struma.mkxp-z").first!
app.activate(options:[.activateIgnoringOtherApps])
Thread.sleep(forTimeInterval:0.01)
let keys: [String: CGKeyCode] = ["q":12,"w":13,"up":126,"down":125,"left":123,"right":124,"c":8,"x":7,"z":6,"d":2,"s":1,"a":0,"return":36,"space":49,"esc":53,"tab":48,"m":46,"f12":111]
func captureHealthy() -> Bool {
 let url=URL(fileURLWithPath:"/Users/jw/Documents/ChatGPT/Reborn/recordings/capture-health.json")
 guard let data=try? Data(contentsOf:url),let v=(try? JSONSerialization.jsonObject(with:data)) as? [String:Any],let epoch=v["epoch"] as? Double,let active=v["active"] as? Bool else {return false}
 return active && Date().timeIntervalSince1970-epoch < 8
}
let args = Array(CommandLine.arguments.dropFirst())
func logInterrupted(_ start: Double) {
 let value: [String:Any] = ["start":start,"end":Date().timeIntervalSince1970,"keys":args.joined(separator:" "),"interrupted":true]
 let url=URL(fileURLWithPath:"/Users/jw/Documents/ChatGPT/Reborn/recordings/actions.jsonl")
 if let data=try? JSONSerialization.data(withJSONObject:value),let h=try? FileHandle(forWritingTo:url) {
  try? h.seekToEnd();try? h.write(contentsOf:data);try? h.write(contentsOf:Data("\n".utf8));try? h.close()
 }
}
let start=Date().timeIntervalSince1970
for arg in args {
 let recoveryDeadline = Date().timeIntervalSince1970 + 5
 while !captureHealthy() && Date().timeIntervalSince1970 < recoveryDeadline {Thread.sleep(forTimeInterval:0.1)}
 if !captureHealthy() {logInterrupted(start);fputs("INPUT BLOCKED: capture is not producing fresh frames\n",stderr);exit(2)}
 let p=arg.split(separator:":").map(String.init)
 if p[0]=="wait" { Thread.sleep(forTimeInterval:Double(p[1])!); continue }
 if p[0]=="release" {
  for code in Array(Set(keys.values))+[54,55,56,58,59,60,61,62,63] { let e=CGEvent(keyboardEventSource:nil,virtualKey:code,keyDown:false)!; e.flags=[]; e.post(tap:.cghidEventTap); Thread.sleep(forTimeInterval:0.02) }; continue
 }
 guard let k=keys[p[0]] else {continue}
 let duration=p.count>1 ? Double(p[1])! : 0.12
 let press=CGEvent(keyboardEventSource:nil,virtualKey:k,keyDown:true)!; press.flags=[]; press.post(tap:.cghidEventTap)
 let deadline=Date().timeIntervalSince1970+duration
 var healthy=true
 while Date().timeIntervalSince1970 < deadline {
  Thread.sleep(forTimeInterval:min(0.08,max(0,deadline-Date().timeIntervalSince1970)))
  if !captureHealthy() {healthy=false;break}
 }
 let release=CGEvent(keyboardEventSource:nil,virtualKey:k,keyDown:false)!; release.flags=[]; release.post(tap:.cghidEventTap)
 if !healthy {logInterrupted(start);fputs("INPUT STOPPED: capture failed during key hold\n",stderr);exit(2)}
 Thread.sleep(forTimeInterval:0.002)
}
let end=Date().timeIntervalSince1970
let line="{\"start\":\(start),\"end\":\(end),\"keys\":\"\(args.joined(separator:" "))\"}\n"
let url=URL(fileURLWithPath:"/Users/jw/Documents/ChatGPT/Reborn/recordings/actions.jsonl")
if !FileManager.default.fileExists(atPath:url.path) {FileManager.default.createFile(atPath:url.path,contents:nil)}
if let h=try? FileHandle(forWritingTo:url){try? h.seekToEnd();try? h.write(contentsOf:Data(line.utf8));try? h.close()}
