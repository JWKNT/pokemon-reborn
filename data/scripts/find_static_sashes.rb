# Installed item events only; never load game state or modify game data.
require_relative 'read_rgss'
r=[]
Dir.glob('/Applications/Reborn.app/Contents/Game/Data/Map[0-9][0-9][0-9].rxdata').each do |path|
 next unless File.binread(path).include?('FOCUSSASH')
 m=load_rgss(path);m.instance_variable_get(:@events).each do |id,e|
  p=plain(e);next unless JSON.generate(p).include?('FOCUSSASH')
  r << {map:File.basename(path)[3,3].to_i,event:id,data:p}
 end
end
puts JSON.pretty_generate(r)
