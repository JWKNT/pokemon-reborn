import Foundation
import CoreGraphics
import AppKit
let keys:[String:CGKeyCode] = ["up":126,"down":125,"left":123,"right":124,"c":8,"x":7]
var held:[String:Double]=[:]
func health()->Bool {
 guard let d=try? Data(contentsOf:URL(fileURLWithPath:"/Users/jw/Documents/ChatGPT/Reborn/recordings/capture-health.json")),let h=(try? JSONSerialization.jsonObject(with:d))as?[String:Any],let t=h["epoch"]as?Double,let a=h["active"]as?Bool else{return false}
 return a && Date().timeIntervalSince1970-t<2
}
func edge(_ name:String,_ down:Bool){
 guard let code=keys[name]else{return}
 let e=CGEvent(keyboardEventSource:nil,virtualKey:code,keyDown:down)!;e.flags=[];e.post(tap:.cghidEventTap)
 if down{held[name]=Date().timeIntervalSince1970}else if let st=held.removeValue(forKey:name){
  let value:[String:Any] = ["start":st,"end":Date().timeIntervalSince1970,"keys":name,"source":"recorded-pixel movement controller"]
  if let d=try? JSONSerialization.data(withJSONObject:value),let f=try? FileHandle(forWritingTo:URL(fileURLWithPath:"/Users/jw/Documents/ChatGPT/Reborn/recordings/actions.jsonl")){try? f.seekToEnd();try? f.write(contentsOf:d);try? f.write(contentsOf:Data("\n".utf8));try? f.close()}
 }
}
defer{for k in Array(held.keys){edge(k,false)}}
while let line=readLine(){
 let p=line.split(separator:" ").map(String.init);guard p.count==2 else{continue}
 let down=p[0]=="down"
 if down && !health(){for k in Array(held.keys){edge(k,false)};print("BLOCKED");fflush(stdout);break}
 edge(p[1],down);print("OK");fflush(stdout)
}
