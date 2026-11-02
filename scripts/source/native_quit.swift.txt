import Foundation
import CoreGraphics
import AppKit
// Normal macOS Command-Q, with capture and native save checked by the caller.
let health=URL(fileURLWithPath:"/Users/jw/Documents/ChatGPT/Reborn/recordings/capture-health.json")
guard let data=try? Data(contentsOf:health),let v=(try? JSONSerialization.jsonObject(with:data)) as? [String:Any],v["active"]as?Bool==true,let epoch=v["epoch"]as?Double,Date().timeIntervalSince1970-epoch<8 else {fatalError("Recording is not fresh")}
guard let app=NSRunningApplication.runningApplications(withBundleIdentifier:"org.struma.mkxp-z").first else {fatalError("No Reborn process")}
app.activate(options:[.activateIgnoringOtherApps]);Thread.sleep(forTimeInterval:0.3)
let start=Date().timeIntervalSince1970
let down=CGEvent(keyboardEventSource:nil,virtualKey:12,keyDown:true)!
let up=CGEvent(keyboardEventSource:nil,virtualKey:12,keyDown:false)!
down.flags = .maskCommand;up.flags = []
down.post(tap:.cghidEventTap);Thread.sleep(forTimeInterval:0.12);up.post(tap:.cghidEventTap)
let row:[String:Any] = ["start":start,"end":Date().timeIntervalSince1970,"keys":"native-command-q"]
let path=URL(fileURLWithPath:"/Users/jw/Documents/ChatGPT/Reborn/recordings/actions.jsonl")
let h=try FileHandle(forWritingTo:path);try h.seekToEnd();try h.write(contentsOf:JSONSerialization.data(withJSONObject:row));try h.write(contentsOf:Data("\n".utf8));try h.close()
print("NORMAL COMMAND-Q SENT")
