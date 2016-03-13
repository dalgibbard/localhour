require 'facter'
require 'net/https'
require "uri"
require 'json'

# Get 8pm in localDC time
uri20 = URI.parse("https://dgunix.com/localhour/20")
http20 = Net:HTTP.new(uri20.host, uri20.port)
http20.use_ssl = true
http20.verify_mode = OpenSSL::SSL::VERIFY_NONE
request20 = Net::HTTP::Get.new(uri20.request_uri)
response20 = http.request(request20)
hour20 = JSON.parse(response20.body)['hour']

# Get 1am in localDC time
uri1 = URI.parse("https://dgunix.com/localhour/1")
http1 = Net:HTTP.new(uri1.host, uri1.port)
http1.use_ssl = true
http1.verify_mode = OpenSSL::SSL::VERIFY_NONE
request1 = Net::HTTP::Get.new(uri1.request_uri)
response1 = http.request(request1)
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
