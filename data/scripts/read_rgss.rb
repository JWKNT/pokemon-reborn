require 'json'
class RGSSStub
 def self._load(data)
  o=new;o.instance_variable_set(:@raw,data.unpack('C*'));o
 end
end
def load_rgss(path)
 data=File.binread(path)
 100.times do
  begin
   return Marshal.load(data)
  rescue ArgumentError => e
   warn e.message
   name=e.message[/undefined class\/module ([A-Za-z0-9_:]+)/,1]
   raise unless name
   parent=Object
   name.split('::').reject(&:empty?).each do |part|
    parent.const_set(part,Class.new(RGSSStub)) unless parent.const_defined?(part,false)
    parent=parent.const_get(part,false)
   end
  end
 end
end
def plain(o,depth=0)
 return '...' if depth>12
 case o
 when Hash then o.transform_values{|v| plain(v,depth+1)}
 when Array then o.map{|v|plain(v,depth+1)}
 when Numeric,String,Symbol,NilClass,TrueClass,FalseClass then o
 else
  {'type'=>o.class.name}.merge(o.instance_variables.to_h{|v|[v.to_s.delete_prefix('@'),plain(o.instance_variable_get(v),depth+1)]})
 end
end
if __FILE__==$0
 v=load_rgss(ARGV[0]);puts JSON.generate(v.is_a?(Hash) ? v.transform_values{|a|a.class.name} : v.class.name)
end
