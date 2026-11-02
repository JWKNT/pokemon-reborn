require_relative 'read_rgss'
r=[]
(510..635).each do |id|
 path='/Applications/Reborn.app/Contents/Game/Data/Map%03d.rxdata'%id
 next unless File.exist?(path)
 m=load_rgss(path)
 m.instance_variable_get(:@events).each do |eid,e|
  p=plain(e);p['pages'].each_with_index do |pg,i|
   pg['list'].each do |c|
    next unless c['code']==201 && c['parameters'][0]==0
    r << {map:id,event:eid,x:p['x'],y:p['y'],page:i,destination:c['parameters'][1..3],condition:pg['condition']}
   end
  end
 end
end
puts JSON.pretty_generate(r)
