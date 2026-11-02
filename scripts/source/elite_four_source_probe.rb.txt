# Installed declarations/maps only. No save, battle log, game runtime, or input access.
require_relative 'read_rgss'
game = '/Applications/Reborn.app/Contents/Game'
tokens = %w[MAWILITE SWAMPERTITE MEGARING AMPLIFIELDROCK CLEFABLE GRAVITY]
result = {source: 'Installed Reborn 19.5.43; static source only', events: [], arc_maps: {}, encounters: [], species: {}, teams: []}
Dir.glob(File.join(game, 'Data/Map[0-9][0-9][0-9].rxdata')).sort.each do |path|
  mid = File.basename(path)[3, 3].to_i
  # Raw token scan avoids unmarshalling unrelated item maps; requested Arc maps are complete.
  raw = File.binread(path)
  next unless [304, 305, 310, 311].include?(mid) || tokens.any? {|t| raw.include?(t)}
  map = load_rgss(path)
  events = map.instance_variable_get(:@events)
  if [304, 305, 310, 311].include?(mid)
    result[:arc_maps][mid] = {width: map.instance_variable_get(:@width), height: map.instance_variable_get(:@height), events: events.transform_values {|event| plain(event)}}
  end
  events.each do |eid, event|
    text = event.instance_variable_get(:@pages).map {|page| page.instance_variable_get(:@list).map {|cmd| cmd.instance_variable_get(:@parameters).to_s}.join("\n")}.join("\n")
    selected = tokens.select {|t| text.include?(t)}
    result[:events] << {map: mid, id: eid, tokens: selected, event: plain(event)} if selected.any?
  end
end
load File.join(game, 'Scripts/Reborn/enctext.rb')
ENCHASH.each do |mid, entries|
  selected = entries.select {|key, value| JSON.generate(value).match?(/MAWILE|CLEFAIRY|CLEFABLE|AGGRON/)}
  result[:encounters] << {map: mid, entries: selected} if selected.any?
end
load File.join(game, 'Scripts/Reborn/montext.rb')
result[:species] = MONHASH.select {|name, _| [:CLEFABLE, :MAWILE, :AGGRON, :SWAMPERT, :CRYOGONAL, :COFAGRIGUS, :KLINKLANG, :MIENSHAO, :ARCEUS, :EXCADRILL].include?(name)}
load File.join(game, 'Scripts/Reborn/trainertext.rb')
result[:teams] = TEAMARRAY.select {|team| [['Fern', :Hotshot, 7], ['Sirius', :Sirius, 2], ['Blake', :BLAKE, 2]].include?(team[:teamid])}
puts JSON.pretty_generate(result)
