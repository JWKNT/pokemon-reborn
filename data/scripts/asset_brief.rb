require_relative 'read_rgss'
ARGV.each do |id|
 m=load_rgss("/Applications/Reborn.app/Contents/Game/Data/Map%03d.rxdata" % id.to_i)
 puts "MAP #{id}"
 m.instance_variable_get(:@events).each do |k,e|
  pages=e.instance_variable_get(:@pages)
  text=pages.flat_map{|p| p.instance_variable_get(:@list).filter_map{|c| a=c.instance_variable_get(:@parameters); code=c.instance_variable_get(:@code); a.inspect if [101,201,355,655].include?(code) || (code==111 && a.to_s.match?(/pbTrainerBattle|pbDoubleTrainerBattle|pbItemBall/))}}.uniq
  next if text.empty?
  puts "#{k} [#{e.instance_variable_get(:@x)},#{e.instance_variable_get(:@y)}] #{e.instance_variable_get(:@name)}: #{text.join(' | ')}"
 end
end
