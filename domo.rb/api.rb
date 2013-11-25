require 'redis'
require 'grape'
require 'i2c'

$io = I2C.create("/dev/i2c-1")
$redis ||= Redis.new

class DomoApi < Grape::API
  version 'v1', using: :header, vendor: 'fuckingawesome'
  format :json

  desc 'write room temperature'
  params do
    requires :room, type: String, desc: 'Room name'
    requires :temp, type: Float, desc: 'Room temperature'
  end
  post '/temperature/:room/' do
    $redis.rpush("room_#{params[:room].downcase}", params[:temp])
    $io.write(0x20, 0x00, params[:temp].to_s)
  end

  desc 'get room temperature'
  params do
    requires :room, type: String, desc: 'Room name'
  end
  get '/temperature/:room/' do
    $redis.lrange("room_#{params[:room].downcase}", -1, -1).first
    $io.write(0x20, 0x00, params[:temp].to_s)
  end
end
