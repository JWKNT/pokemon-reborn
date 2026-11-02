# Read-only installed event transfer lookup; pages remain proposals, not active route proof.
require_relative 'read_rgss'
targets=ARGV.map(&:to_i);raise 'Target map IDs required' if targets.empty?
r=[]
Dir.glob('/Applications/Reborn.app/Contents/Game/Data/Map[0-9][0-9][0-9].rxdata').each do |f|
 mid=File.basename(f)[3,3].to_i;m=load_rgss(f)
 m.instance_variable_get(:@events).each do |id,e|
  p=plain(e);p['pages'].each_with_index do |pg,i|
   pg['list'].each do |c|
    next unless c['code']==201 && c['parameters'][0]==0 && targets.include?(c['parameters'][1])
    r << {map:mid,event:id,x:p['x'],y:p['y'],page:i,destination:c['parameters'][1,3],condition:pg['condition']}
   end
  end
 end
end
puts JSON.pretty_generate(r)
