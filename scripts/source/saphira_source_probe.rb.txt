# Read-only installed-data lookup for future Saphira preparation.
# No save/runtime/log access, input, game mutation, or control-helper import.
require_relative 'read_rgss'
root = '/Applications/Reborn.app/Contents/Game/Data'
result = {sylveon_events: [], marill_encounters: [], preparation_events: []}
Dir.glob(File.join(root, 'Map[0-9][0-9][0-9].rxdata')).sort.each do |path|
  map = load_rgss(path)
  map.instance_variable_get(:@events).each do |eid, event|
    pages = event.instance_variable_get(:@pages)
    text = pages.map {|p| p.instance_variable_get(:@list).map {|c| c.instance_variable_get(:@parameters).to_s}.join("\n")}.join("\n")
    item = {map: File.basename(path)[3,3].to_i, id: eid, event: plain(event)}
    result[:sylveon_events] << item if text.include?('SYLVEON')
    tokens = ['CALMMINT', 'CAREFULMINT', 'AMPLIFIELDROCK', 'ICEPUNCH', 'WISEGLASSES', 'POWERBAND', 'POWERANKLET'].select {|t| text.include?(t)}
    result[:preparation_events] << item.merge(tokens: tokens) if tokens.any?
  end
end
load '/Applications/Reborn.app/Contents/Game/Scripts/Reborn/enctext.rb'
result[:marill_lookup_origin] = 'Installed enctext.rb static declarations; not a current encounter/runtime query.'
ENCHASH.each do |mapid, entries|
  next unless JSON.generate(entries).match?(/MARILL|AZUMARILL/)
  selected = entries.select {|_, v| JSON.generate(v).match?(/MARILL|AZUMARILL/)}
  result[:marill_encounters] << {map: mapid, entries: selected}
end
load '/Applications/Reborn.app/Contents/Game/Scripts/Reborn/montext.rb'
result[:species] = MONHASH.select {|name,_| [:SWAMPERT, :SYLVEON, :NOIVERN, :SALAMENCE, :GARCHOMP, :HAXORUS, :CHARIZARD, :DRAGONITE, :STEELIX, :CLEFABLE, :AZUMARILL, :COFAGRIGUS].include?(name)}
puts JSON.pretty_generate(result)
