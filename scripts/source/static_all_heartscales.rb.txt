require_relative 'read_rgss'
r=[]
Dir.glob('/Applications/Reborn.app/Contents/Game/Data/Map[0-9][0-9][0-9].rxdata').each do |file|
 mid=File.basename(file)[3,3].to_i
 next unless File.binread(file).include?('HEARTSCALE')
 m=load_rgss('/Applications/Reborn.app/Contents/Game/Data/Map%03d.rxdata'%mid)
 m.instance_variable_get(:@events).each do |id,e|
  p=plain(e);p['pages'].each_with_index do |pg,i|
   pg['list'].each do |c|
    next unless c['code']==111 && c['parameters'][0]==12 && c['parameters'][1].match?(/pbItemBall\(:HEARTSCALE/)
    r << {map:mid,event:id,x:p['x'],y:p['y'],page:i,script:c['parameters'][1]}
   end
  end
 end
end
v=load_rgss(ARGV[0] || ENV.fetch('REBORN_FROZEN_SAVE','/Users/jw/Documents/ChatGPT/Reborn/backups/Aster-League218-LightClay.rxdata'));ss=v[:self_switches].instance_variable_get(:@data)
r.each{|e|e[:collected]=!!ss[[e[:map],e[:event],'A']]}
puts JSON.pretty_generate(r)
