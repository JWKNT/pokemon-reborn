require_relative 'read_rgss'
v=load_rgss('/Users/jw/Library/Application Support/Pokemon Reborn/Game_3.rxdata')
s=v[:PokemonStorage]
if !s
 puts v.keys.inspect
else
 puts JSON.pretty_generate(plain(s))
end
