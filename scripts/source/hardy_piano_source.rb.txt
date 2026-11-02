# Installed map/tileset assets only. No save, planner or runtime reads/writes.
require_relative 'read_rgss'
require 'digest'
def iv(o,k);o.instance_variable_get('@'+k.to_s);end
base='/Applications/Reborn.app/Contents/Game/Data/'
path=base+'Map739.rxdata'
map=load_rgss(path)
tilesets=load_rgss(base+'Tilesets.rxdata')
tileset=tilesets[iv(map,:tileset_id)]
raw=iv(iv(map,:data),:raw).pack('C*')
data=raw[20..].unpack('S<*')
width,height=iv(map,:width),iv(map,:height)
puts JSON.generate({map:739,width:iv(map,:width),height:iv(map,:height),
                    tileset_id:iv(map,:tileset_id),tileset_name:iv(tileset,:tileset_name),
                    door_base_tiles:(0..2).map{|z|data[11+width*4+width*height*z]},
                    map_sha256:Digest::SHA256.file(path).hexdigest,
                    tilesets_sha256:Digest::SHA256.file(base+'Tilesets.rxdata').hexdigest})
