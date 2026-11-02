require_relative 'read_rgss'
r=[]
[355,519,520,521,523,524,530,531,168,324,325,178,179,412].each do |mid|
 m=load_rgss('/Applications/Reborn.app/Contents/Game/Data/Map%03d.rxdata'%mid)
 m.instance_variable_get(:@events).each do |id,e|
  p=plain(e);p['pages'].each_with_index do |pg,i|
   pg['list'].each do |c|
    next unless c['code']==111 && c['parameters'][0]==12 && c['parameters'][1].match?(/pbItemBall\(:(?:RED|BLUE|GREEN|PURPLE)SHARD/)
    r << {map:mid,event:id,x:p['x'],y:p['y'],page:i,script:c['parameters'][1]}
   end
  end
 end
end
v=load_rgss('/Users/jw/Documents/ChatGPT/Reborn/backups/Aster-League217-Reflect.rxdata');ss=v[:self_switches].instance_variable_get(:@data)
r.each{|e|e[:collected]=!!ss[[e[:map],e[:event],'A']]}
puts JSON.pretty_generate(r)
