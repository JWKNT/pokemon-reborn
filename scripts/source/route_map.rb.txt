require_relative 'read_rgss'
def iv(o,k);o.instance_variable_get('@'+k.to_s);end
def table(o);b=iv(o,:raw).pack('C*');h=b[0,20].unpack('l<*');{dims:h[1,3],data:b[20..].unpack('S<*')};end
id=ARGV[0].to_i;root='/Applications/Reborn.app/Contents/Game/Data/'
v=load_rgss(ENV.fetch('REBORN_FROZEN_SAVE','/Users/jw/Library/Application Support/Pokemon Reborn/Game_3.rxdata'));m=load_rgss(root+'Map%03d.rxdata'%id);ts=load_rgss(root+'Tilesets.rxdata')[iv(m,:tileset_id)]
sw=iv(v[:switches],:data);va=iv(v[:variable],:data);ss=iv(v[:self_switches],:data)
state_path=File.expand_path('../notes/navigation-state.json',__dir__)
nav_state={}
if File.exist?(state_path)
 nav_state=JSON.parse(File.read(state_path))
 (nav_state['variables']||{}).each{|k,value| va[k.to_i]=value}
 (nav_state['switches']||{}).each{|k,value| sw[k.to_i]=value}
 # Observed event progress is copied into this in-memory planning snapshot only.
 (nav_state['self_switches']||{}).each{|k,value| map,event,ch=k.split(',');ss[[map.to_i,event.to_i,ch]]=value}
end
# Optional read-only planning overrides, never written to the game or navigation state.
if ARGV[3]
 extra=JSON.parse(ARGV[3]);(extra['variables']||{}).each{|k,value|va[k.to_i]=value};(extra['switches']||{}).each{|k,value|sw[k.to_i]=value}
end
events=iv(m,:events).filter_map do |k,e|
 p=iv(e,:pages).reverse.find do |pg|
  c=iv(pg,:condition)
  (!iv(c,:switch1_valid)||sw[iv(c,:switch1_id)]) && (!iv(c,:switch2_valid)||sw[iv(c,:switch2_id)]) && (!iv(c,:variable_valid)||(va[iv(c,:variable_id)]||0)>=iv(c,:variable_value)) && (!iv(c,:self_switch_valid)||ss[[id,k,iv(c,:self_switch_ch)]])
 end
 next unless p
 g=iv(p,:graphic)
 [k,{x:iv(e,:x),y:iv(e,:y),name:iv(e,:name),through:iv(p,:through),character:iv(g,:character_name),tile_id:iv(g,:tile_id),trigger:iv(p,:trigger),move_type:iv(p,:move_type),direction:iv(g,:direction),list:plain(iv(p,:list))}]
end.to_h
((ARGV[3] && JSON.parse(ARGV[3])['reset_positions']) ? {} : ((nav_state['positions']||{})[id.to_s]||{})).each{|k,xy| if events[k.to_i];events[k.to_i][:x],events[k.to_i][:y]=xy;end}
override_path=File.expand_path('../notes/navigation-overrides.json',__dir__)
if File.exist?(override_path)
 (JSON.parse(File.read(override_path))[id.to_s]||[]).each{|k| events.delete(k.to_i)}
end
puts JSON.generate({map:id,position:ARGV[1,2].map(&:to_i),width:iv(m,:width),height:iv(m,:height),data:table(iv(m,:data)),passages:table(iv(ts,:passages)),priorities:table(iv(ts,:priorities)),terrain:table(iv(ts,:terrain_tags)),events:events})
