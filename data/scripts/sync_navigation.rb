# Refresh only planning notes from a just-written save. Never modify game data.
require_relative 'read_rgss'
root=File.expand_path('..',__dir__)
save='/Users/jw/Library/Application Support/Pokemon Reborn/Game_3.rxdata'
raise 'Navigation sync requires a fresh checkpoint' if Time.now-File.mtime(save)>120
v=load_rgss(save);path=root+'/notes/navigation-state.json';s=JSON.parse(File.read(path))
s['variables']||={};v[:variable].instance_variable_get(:@data).each_with_index{|value,i|s['variables'][i.to_s]=(value.is_a?(Numeric) ? value : 0) if value.nil? || value.is_a?(Numeric)}
s['switches']||={};v[:switches].instance_variable_get(:@data).each_with_index{|value,i|s['switches'][i.to_s]=value==true}
s['self_switches']=v[:self_switches].instance_variable_get(:@data).to_h{|key,value|[key.join(','),value]}
s['positions']||={};s['positions'][v[:map_id].to_s]=v[:Map].instance_variable_get(:@events).to_h{|id,event|[id.to_s,[event.instance_variable_get(:@x),event.instance_variable_get(:@y)]]}
# Grand Hall clears its transient weekday switches before serialization, while
# its saved event pages still identify the trainers actually visible in-game.
# Preserve that observed page condition in planning notes only.
if v[:map_id]==38
 v[:Map].instance_variable_get(:@events).each do |id,event|
  next unless (41..52).include?(id) && !event.instance_variable_get(:@character_name).to_s.empty?
  page=event.instance_variable_get(:@page);next unless page
  condition=page.instance_variable_get(:@condition)
  weekday=condition.instance_variable_get(:@switch2_id)
  next unless condition.instance_variable_get(:@switch2_valid) && (108..115).include?(weekday)
  s['switches'][weekday.to_s]=true
  s['observed_weekday_evidence']={'map'=>38,'event'=>id,'switch'=>weekday,'save_mtime'=>File.mtime(save).to_i,'evidence'=>'Active visible trainer page in freshly saved map; planning only.'}
 end
end
File.write(path,JSON.generate(s))
puts "NAVIGATION NOTES SYNCED from current save: map #{v[:map_id]}, position #{v[:position].inspect}"
