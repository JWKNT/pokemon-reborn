# Static, read-only Void map/event extraction. No save read, navigation write,
# game driver import, UI, input, or game data modification.
require_relative 'read_rgss'
root = '/Applications/Reborn.app/Contents/Game/Data'
ids = (754..759).to_a
out = ids.map do |id|
  map = load_rgss(File.join(root, 'Map%03d.rxdata' % id))
  events = map.instance_variable_get(:@events).map do |eid, event|
    {
      id: eid,
      name: event.instance_variable_get(:@name),
      x: event.instance_variable_get(:@x),
      y: event.instance_variable_get(:@y),
      pages: event.instance_variable_get(:@pages).map.with_index do |page, index|
        {
          index: index,
          condition: plain(page.instance_variable_get(:@condition)),
          trigger: page.instance_variable_get(:@trigger),
          through: page.instance_variable_get(:@through),
          graphic: plain(page.instance_variable_get(:@graphic)),
          move_type: page.instance_variable_get(:@move_type),
          list: plain(page.instance_variable_get(:@list))
        }
      end
    }
  end
  {map: id, width: map.instance_variable_get(:@width), height: map.instance_variable_get(:@height), events: events}
end
puts JSON.pretty_generate(out)
