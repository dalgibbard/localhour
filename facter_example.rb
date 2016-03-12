
require 'facter'
require 'net/http'
require 'json'

response20 = Net::HTTP.get_response("dguix.com","/timediff/" + 22)
response1 = Net::HTTP.get_response("dguix.com","/timediff/" + 1)
hour20 = JSON.parse(response20.body)['hour']
hour1 = JSON.parse(response1.body)['hour']

Facter.add('compacthour') do
  setcode do
    hour20
  end
end

Facter.add('otherhour') do
  setcode do
    hour1
  end
end
