# Read-only checkpoint evidence for play planning and battle archive panels.
require_relative 'read_rgss'
require_relative 'checkpoint_weather'
require 'time'
path='/Users/jw/Library/Application Support/Pokemon Reborn/Game_3.rxdata'
v=load_rgss(path);t=v[:Trainer];sw=v[:switches].instance_variable_get(:@data);var=v[:variable].instance_variable_get(:@data)
keys=%w[species form name level hp totalhp status item ability abilityflag nature natureflag moves ev iv attack defense spatk spdef speed happiness]
maps=load_rgss('/Applications/Reborn.app/Contents/Game/Data/maps.dat')
weather=CheckpointWeather.export(v[:game_screen],maps[v[:map_id]],!!sw[479])
puts JSON.pretty_generate({save_mtime:File.mtime(path).iso8601,map:v[:map_id],position:v[:position],weather:weather,trainer:plain(t).slice('name','money','badges'),party:t.instance_variable_get(:@party).map{|p|plain(p).slice(*keys)},bag:plain(v[:PokemonBag]),switches:[183,393,410,464,470,471,472,486,488,490,548,577,579,1920,2041,2042,2045,2046].to_h{|i|[i,sw[i]]},main_quest:var[173],route_quests:[184,185,193].to_h{|i|[i,var[i]]},story_variables:([192,276]+(256..264).to_a).to_h{|i|[i,var[i]]}})
