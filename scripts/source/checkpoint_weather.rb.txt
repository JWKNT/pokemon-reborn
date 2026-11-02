# Pure weather projection from explicitly supplied frozen objects.
# Does not load a save, instantiate Game_Screen, update weather or inspect forecasts.
module CheckpointWeather
  TYPE_IDS = {0 => 0, :Rain => 1, :Storm => 2, :Snow => 3,
              :Sandstorm => 4, :Sunny => 5, :Winds => 6,
              :HeavyRain => 7, :Blizzard => 8}.freeze

  def self.region(position, restored)
    return nil unless position.is_a?(Array) && position.length >= 3 &&
                      position[1].is_a?(Numeric) && position[2].is_a?(Numeric)
    x, y = position[1], position[2]
    if y == 7 && x == 8
      2
    elsif y < 7
      x < 8 ? 3 : 4
    elsif (y > 14 && x != 9) || (y == 14 && x == 0)
      x < 6 ? 0 : 5
    elsif x < 10
      restored ? 2 : 1
    else
      5
    end
  end

  def self.numeric(value)
    return nil unless value.is_a?(Numeric)
    return nil if value.respond_to?(:finite?) && !value.finite?
    value
  end

  def self.export(screen, metadata, restored)
    type = screen&.instance_variable_get(:@weather_type)
    position = metadata&.instance_variable_get(:@MapPosition)
    # A present metadata record with no position follows the game's fallback.
    position = [0, 0, 0] if metadata && position.nil?
    {
      weather_type: type,
      weather_type_id: TYPE_IDS[type],
      weather_max: numeric(screen&.instance_variable_get(:@weather_max)),
      weather_type_target: screen&.instance_variable_get(:@weather_type_target),
      weather_max_target: numeric(screen&.instance_variable_get(:@weather_max_target)),
      region: region(position, restored)
    }
  end
end
