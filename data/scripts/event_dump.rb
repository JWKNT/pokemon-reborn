require_relative 'read_rgss'
id,eid=ARGV.map(&:to_i)
m=load_rgss('/Applications/Reborn.app/Contents/Game/Data/Map%03d.rxdata'%id)
e=m.instance_variable_get(:@events)[eid]
puts JSON.pretty_generate(plain(e))
