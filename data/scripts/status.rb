require_relative 'read_rgss'
v=load_rgss('/Users/jw/Library/Application Support/Pokemon Reborn/Game_3.rxdata')
t=v[:Trainer]
puts JSON.pretty_generate({map:v[:map_id],position:v[:position],trainer:plain(t).slice('name','money','badges'),party:t.instance_variable_get(:@party).map{|p|plain(p).slice('species','name','level','hp','totalhp','status','item','moves')},bag:plain(v[:PokemonBag])})
