require 'redis'
require 'grape'

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
  end

  desc 'get room temperature'
  params do
    requires :room, type: String, desc: 'Room name'
  end
  get '/temperature/:room/' do
    $redis.lrange("room_#{params[:room].downcase}", -1, -1).first
  end
end
