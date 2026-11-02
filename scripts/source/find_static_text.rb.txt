# Installed event text only. Explicit string, never active runtime state.
require_relative 'read_rgss'
needle=ARGV.fetch(0);raise 'Empty search' if needle.empty?
r=[]
Dir.glob('/Applications/Reborn.app/Contents/Game/Data/Map[0-9][0-9][0-9].rxdata').each do |path|
 next unless File.binread(path).include?(needle)
 m=load_rgss(path);m.instance_variable_get(:@events).each do |id,e|
  p=plain(e);next unless JSON.generate(p).include?(needle)
  r << {map:File.basename(path)[3,3].to_i,event:id,data:p}
 end
end
puts JSON.pretty_generate(r)
