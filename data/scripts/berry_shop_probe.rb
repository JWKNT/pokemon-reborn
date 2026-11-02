# Installed map declarations only; no saves, runtime or game mutations.
require_relative 'read_rgss'
hits=[]
Dir['/Applications/Reborn.app/Contents/Game/Data/Map[0-9]*.rxdata'].each do |f|
 m=load_rgss(f); events=m.instance_variable_get(:@events);next unless events
 events.each do |id,e|
  e.instance_variable_get(:@pages).each_with_index do |p,i|
   cs=plain(p.instance_variable_get(:@list)); s=cs.to_s
   if s.include?('LUMBERRY') || s.include?('PERSIMBERRY')
    hits << {map:File.basename(f)[/\d+/].to_i,event:id,x:e.instance_variable_get(:@x),y:e.instance_variable_get(:@y),page:i,commands:cs.select{|c|[101,401,111,355,655].include?(c['code'])}}
   end
  end
 end
end
puts JSON.pretty_generate(hits)
