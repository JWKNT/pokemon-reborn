require 'minitest/autorun'
require_relative 'checkpoint_weather'
require_relative 'read_rgss'

class CheckpointWeatherTest < Minitest::Test
  def object(fields)
    value = Object.new
    fields.each { |name, v| value.instance_variable_set("@#{name}", v) }
    value
  end

  def test_saved_symbol_weather_and_numeric_intensity
    screen = object(weather_type: :Rain, weather_max: 20.0,
                    weather_type_target: :Rain, weather_max_target: 20.0,
                    weatherVector: ['must not export forecast'])
    metadata = object(MapPosition: [0, 13, 6])
    result = CheckpointWeather.export(screen, metadata, false)
    assert_equal({weather_type: :Rain, weather_type_id: 1, weather_max: 20.0,
                  weather_type_target: :Rain, weather_max_target: 20.0,
                  region: 4}, result)
    refute_includes JSON.generate(result), 'forecast'
    assert_equal 'Rain', JSON.parse(JSON.generate(result))['weather_type']
  end

  def test_transition_preserves_actual_and_target_instead_of_inventing_power
    screen = object(weather_type: :Storm, weather_max: 7.5,
                    weather_type_target: 0, weather_max_target: 0.0)
    result = CheckpointWeather.export(screen, object(MapPosition: [0, 8, 10]), false)
    assert_equal :Storm, result[:weather_type]
    assert_equal 2, result[:weather_type_id]
    assert_equal 7.5, result[:weather_max]
    assert_equal 0, result[:weather_type_target]
    assert_equal 0.0, result[:weather_max_target]
    refute result.key?(:power)
  end

  def test_source_region_boundaries_and_city_restore
    cases = [[[0, 8, 7], false, 2], [[0, 7, 6], false, 3],
             [[0, 8, 6], false, 4], [[0, 5, 15], false, 0],
             [[0, 6, 15], false, 5], [[0, 9, 15], false, 1],
             [[0, 9, 15], true, 2], [[0, 0, 14], false, 0],
             [[0, 10, 10], false, 5]]
    cases.each { |position, restored, expected| assert_equal expected, CheckpointWeather.region(position, restored) }
  end

  def test_unknown_type_or_missing_screen_is_not_reported_clear
    result = CheckpointWeather.export(object(weather_type: :CustomFog), nil, false)
    assert_equal :CustomFog, result[:weather_type]
    assert_nil result[:weather_type_id]
    assert_nil result[:weather_max]
    assert_nil result[:region]
    assert_nil CheckpointWeather.export(nil, nil, false)[:weather_type]
    assert_equal 3, CheckpointWeather.export(nil, object(MapPosition: nil), false)[:region]
  end

  def test_installed_static_source_and_agate_metadata
    game = '/Applications/Reborn.app/Contents/Game'
    source = File.read(game + '/Scripts/Game_Screen.rb')
    assert_includes source, '@weather_max_target = (power + 1) * 4.0'
    assert_includes source, 'def determineWeatherRegion'
    assert_includes File.read(game + '/Scripts/Save.rb'), 'savehash[:game_screen]'
    assert_match(/Reborn_City_Restore:\s*479/, File.read(game + '/Scripts/Reborn/SystemConstants.rb'))
    maps = load_rgss(game + '/Data/maps.dat')
    assert_equal [0, 13, 6], maps[763].instance_variable_get(:@MapPosition)
    assert_equal 4, CheckpointWeather.export(nil, maps[763], false)[:region]
  end
end
