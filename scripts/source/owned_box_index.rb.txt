# Read an explicit owned frozen save; compact inventory only, never battle/runtime data.
require_relative 'read_rgss'
raise 'Explicit frozen save required' unless ARGV[0] && File.file?(ARGV[0])
v=load_rgss(ARGV[0]);s=plain(v[:PokemonStorage]);out=[]
s['boxes'].each_with_index do |box,b|
 box['pokemon'].each_with_index do |p,i|
  next unless p
  out << {box:b,slot:i,name:p['name'],species:p['species'],level:p['level'],trainerID:p['trainerID'],ot:p['ot'],item:p['item'],ability:p['ability'],moves:p['moves'].map{|m|m['move']}}
 end
end
puts JSON.pretty_generate(out)
