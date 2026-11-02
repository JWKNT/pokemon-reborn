# Read only installed transfer declarations for quest route planning.
require_relative 'read_rgss'
rows=[]
Dir['/Applications/Reborn.app/Contents/Game/Data/Map[0-9]*.rxdata'].each do |path|
 mid=File.basename(path)[/\d+/].to_i
 h=plain(load_rgss(path))
 h['events'].each do |eid,ev|
  ev['pages'].each_with_index do |p,pi|
   p['list'].each do |c|
    if c['code']==201 && c['parameters'][0]==0
     rows << {map:mid,event:eid.to_i,x:ev['x'],y:ev['y'],page:pi,condition:p['condition'],destination:c['parameters'][1,3]}
    end
   end
  end
 end
end
File.write('work/179-installed-transfers.json',JSON.generate(rows))
puts JSON.generate(rows.select{|r| [533,536,613,693,324].include?(r[:destination][0])}.uniq{|r| [r[:map],r[:event],r[:destination]]})
