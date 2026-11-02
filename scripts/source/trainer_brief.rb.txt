# Read-only trainer metadata, selected by trainer class/name/version.
require_relative 'read_rgss'
v=load_rgss('/Applications/Reborn.app/Contents/Game/Data/trainers.dat')
t=v.fetch(ARGV[0].to_sym).fetch(ARGV[1]);t=t.select{|a|a[0]==ARGV[2].to_i} if ARGV[2]
puts JSON.pretty_generate(plain(t))
