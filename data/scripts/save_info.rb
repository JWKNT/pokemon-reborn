require_relative 'read_rgss'
v=load_rgss('/Users/jw/Library/Application Support/Pokemon Reborn/Game_3.rxdata')
def vars(v)
 v.instance_variables.to_h{|k| a=v.instance_variable_get(k);[k, a.is_a?(Numeric)||a.is_a?(String)||a.is_a?(Symbol)||a==false||a==true ? a : a.class.name]}
end
puts JSON.pretty_generate({map_id:v[:map_id],position:v[:position],keys:v.keys,map:vars(v[:Map]),player:vars(v[:game_player]),trainer:vars(v[:Trainer])})
