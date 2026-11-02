require_relative 'read_rgss'
def iv(o,k);o.instance_variable_get('@'+k.to_s);end
root='/Applications/Reborn.app/Contents/Game/Data/'
v=load_rgss(ENV.fetch('REBORN_FROZEN_SAVE','/Users/jw/Library/Application Support/Pokemon Reborn/Game_3.rxdata'))
sw=iv(v[:switches],:data);va=iv(v[:variable],:data);ss=iv(v[:self_switches],:data)
n=JSON.parse(File.read(File.expand_path('../notes/navigation-state.json',__dir__)))
(n['variables']||{}).each{|k,x|va[k.to_i]=x};(n['switches']||{}).each{|k,x|sw[k.to_i]=x};(n['self_switches']||{}).each{|k,x|a,b,c=k.split(',');ss[[a.to_i,b.to_i,c]]=x}
info=load_rgss(root+'MapInfos.rxdata');hits=[]
(ARGV.empty? ? (350..456).to_a : ARGV.map(&:to_i)).each do |id|
 next unless File.exist?(root+'Map%03d.rxdata'%id)
 m=load_rgss(root+'Map%03d.rxdata'%id)
 iv(m,:events).each do |eid,e|
  pg=iv(e,:pages).reverse.find do |p|
   c=iv(p,:condition)
   (!iv(c,:switch1_valid)||sw[iv(c,:switch1_id)])&&(!iv(c,:switch2_valid)||sw[iv(c,:switch2_id)])&&(!iv(c,:variable_valid)||(va[iv(c,:variable_id)]||0)>=iv(c,:variable_value))&&(!iv(c,:self_switch_valid)||ss[[id,eid,iv(c,:self_switch_ch)]])
  end
  next unless pg
  cs=plain(iv(pg,:list));s=cs.select{|c|[111,126,355,655].include?(c[:code]||c['code'])}.to_s
  items=(ENV['REBORN_FIND_ITEMS'] ? ENV['REBORN_FIND_ITEMS'].split(',') : ['HEARTSCALE','SYNTHETICSEED']).select{|x|s.include?(x)&&s.match?(/pbReceiveItem|Kernel.pbReceiveItem|HiddenItem|pbItemBall/)}
  next if items.empty?
  hits<<{map:id,name:iv(info[id],:name),event:eid,x:iv(e,:x),y:iv(e,:y),items:items}
 end
end
puts JSON.pretty_generate(hits)
