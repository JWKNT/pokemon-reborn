require_relative 'read_rgss'
def iv(o,k);o.instance_variable_get('@'+k.to_s);end
def table(o)
 b=iv(o,:raw).pack('C*');h=b[0,20].unpack('l<*');{dims:h[1,3],data:b[20..].unpack('S<*')}
end
v=load_rgss('/Users/jw/Library/Application Support/Pokemon Reborn/Game_3.rxdata');m=v[:Map];rmap=iv(m,:map)
events=iv(m,:events).transform_values do |e|
 {x:iv(e,:x),y:iv(e,:y),name:iv(iv(e,:event),:name),through:iv(e,:through),character:iv(e,:character_name),tile_id:iv(e,:tile_id),trigger:iv(e,:trigger),list:plain(iv(e,:list),0)}
end
party=iv(v[:Trainer],:party).map{|p| p.instance_variables.select{|a| [:@species,:@name,:@level,:@hp,:@totalhp,:@exp,:@ability,:@moves,:@status,:@happiness,:@item,:@nature,:@attack,:@defense,:@spatk,:@spdef,:@speed].include?(a)}.to_h{|k|[k,plain(p.instance_variable_get(k),9)]}}
puts JSON.generate({map:v[:map_id],position:v[:position],direction:iv(v[:game_player],:direction),width:iv(rmap,:width),height:iv(rmap,:height),data:table(iv(rmap,:data)),passages:table(iv(m,:passages)),priorities:table(iv(m,:priorities)),events:events,party:party,bag:iv(v[:PokemonBag],:contents).select{|k,n|n>0},money:iv(v[:Trainer],:money)})
