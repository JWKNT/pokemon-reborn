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
  next unless text.match?(/Volcanion|Diancie|Meloetta|Genesect|Zeraora|Hoopa|Victini/) || pages.any?{|p| c=p.instance_variable_get(:@condition); c.instance_variable_get(:@variable_valid)&&[611,613,616,618,619,627].include?(c.instance_variable_get(:@variable_id))}
  out << {map:id,event:eid,data:plain(e)}
 end
end
File.write('work/260-tier4-quest-source.json',JSON.pretty_generate(out))
puts out.map{|e|[e[:map],e[:event],e[:data]['name'],e[:data]['x'],e[:data]['y']].inspect}
