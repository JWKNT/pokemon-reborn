# Find literal installed-map transfers; never reads saves or runtime state.
require_relative 'read_rgss'
targets=ARGV.map { |n| Integer(n) }
raise 'Specify destination map IDs' if targets.empty?
rows=[]
Dir.glob('/Applications/Reborn.app/Contents/Game/Data/Map[0-9][0-9][0-9].rxdata').each do |path|
  map=load_rgss(path)
  map.instance_variable_get(:@events).each do |id,event|
    event.instance_variable_get(:@pages).each_with_index do |page,pi|
      page.instance_variable_get(:@list).each do |command|
        args=command.instance_variable_get(:@parameters)
        next unless command.instance_variable_get(:@code)==201 && args[0]==0 && targets.include?(args[1])
        rows << {map:File.basename(path)[3,3].to_i,event:id,page:pi,
                 position:[event.instance_variable_get(:@x),event.instance_variable_get(:@y)],transfer:args}
      end
    end
  end
end
puts JSON.pretty_generate(rows)
