# Installed declarations only. No game/save/runtime writes.
require_relative 'read_rgss'
rows=[]
Dir['/Applications/Reborn.app/Contents/Game/Data/Map[0-9]*.rxdata'].each do |path|
 mid=File.basename(path)[/\d+/].to_i
 map=load_rgss(path)
 (map.instance_variable_get(:@events)||{}).each do |eid,ev|
  h=plain(ev); pages=h['pages']||[]
  hits=pages.each_with_index.filter_map do |p,i|
   text=p['list'].map{|c|c['parameters'].to_s}.join(' ')
   {'page'=>i,'condition'=>p['condition'],'list'=>p['list']} if text.match?(/Magikarp|MAGIKARP|Corin-Rouge|renowned by Dragon/i) || (p['condition']['variable_valid'] && p['condition']['variable_id']==155) || p['list'].any?{|c| [111,122].include?(c['code']) && c['parameters'].include?(155)}
  end
  rows << {'map'=>mid,'event'=>eid,'x'=>h['x'],'y'=>h['y'],'pages'=>hits} unless hits.empty?
 end
end
File.write('work/magikarp-installed-events.json',JSON.pretty_generate(rows))
puts JSON.generate(rows.map{|e|e.reject{|k,v|k=='pages'}.merge('pages'=>e['pages'].map{|p|p['page']})})
