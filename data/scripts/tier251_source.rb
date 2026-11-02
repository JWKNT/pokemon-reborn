# Read-only installed quest event index.
require_relative 'read_rgss'
root='/Applications/Reborn.app/Contents/Game/Data/'
out=[]
Dir.glob(root+'Map*.rxdata').each do |path|
 next unless File.basename(path)=~/Map(\d+)\.rxdata/
 id=$1.to_i
 m=load_rgss(path)
 m.instance_variable_get(:@events).each do |eid,e|
  pages=e.instance_variable_get(:@pages)
  text=JSON.generate(plain(pages))
  next unless text.match?(/Cobalion|Tornadus|Thundurus|Landorus/) || pages.any?{|p| c=p.instance_variable_get(:@condition); c.instance_variable_get(:@variable_valid)&&[586,589].include?(c.instance_variable_get(:@variable_id))}
  out << {map:id,event:eid,data:plain(e)}
 end
end
File.write('work/251-quest-source.json',JSON.pretty_generate(out))
puts out.map{|e|[e[:map],e[:event],e[:data]['name'],e[:data]['x'],e[:data]['y']].inspect}
