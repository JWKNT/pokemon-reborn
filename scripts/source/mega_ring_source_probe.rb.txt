# Static installed-data research only. No saves, runtime, input or battle logs.
require_relative 'read_rgss'
root = '/Applications/Reborn.app/Contents/Game/Data'
tokens = %w[MEGARING MEGA-Z MEGA\ Z ARCAUTOGRAPH MCKREZZYAUTOGRAPH HEADPHONES]
result = {origin: 'Installed map declarations only; not current event state.', events: []}
Dir.glob(File.join(root, 'Map[0-9][0-9][0-9].rxdata')).sort.each do |path|
  map = load_rgss(path)
  map.instance_variable_get(:@events).each do |eid, event|
    text = event.instance_variable_get(:@pages).map {|p| p.instance_variable_get(:@list).map {|c| c.instance_variable_get(:@parameters).to_s}.join("\n")}.join("\n")
    found = tokens.select {|t| text.upcase.include?(t)}
    conditions = event.instance_variable_get(:@pages).map {|p| plain(p.instance_variable_get(:@condition))}
    quest_variable = conditions.any? {|c| c['variable_valid'] && c['variable_id'] == 160}
    map_id = File.basename(path)[3,3].to_i
    shop_or_owner = [23,58,324,534,826].include?(map_id) && text.match?(/LOUDRED|JIGGLYPUFF|MAKUHITA|ROGGENROLA|VANILLITE|Santiago|Eustace|Lillin|McKrezzy|Felicia|pbAddPokemon/)
    chain = text.match?(/Eustace|Santiago|Colin|Matthew|MASTERMIND/) && map_id < 830
    nightclub_boundary = map_id == 826 && eid == 9
    next if found.empty? && !quest_variable && !shop_or_owner && !chain && !nightclub_boundary
    result[:events] << {map: File.basename(path)[3,3].to_i, id: eid, tokens: found, event: plain(event)}
  end
end
puts JSON.pretty_generate(result)
