require 'facter'
require 'net/http'
require "uri"
require 'json'

if Facter.value(:fqdn).match(/(^cdb-.*$|^.*-cdb-.*$)/)
  # Get 9pm in localDC time
  uri21 = URI.parse("http://localhour.dgunix.com/21")
  http21 = Net::HTTP.new(uri21.host, uri21.port)
  request21 = Net::HTTP::Get.new(uri21.request_uri)
  response21 = http21.request(request21)
  hour21 = JSON.parse(response21.body)['hour']
  
  # Get 5am in localDC time
  uri5 = URI.parse("http://localhour.dgunix.com/5")
  http5 = Net::HTTP.new(uri5.host, uri5.port)
  request5 = Net::HTTP::Get.new(uri5.request_uri)
  response5 = http5.request(request5)
  hour5 = JSON.parse(response5.body)['hour']
  
  ##To use as an external fact instead:
  # puts "compacthour: #{hour21}"
  # puts "viewcompact: #{hour5}" 
  
  Facter.add('compacthour') do
    setcode do
      hour21
    end
  end
  
  Facter.add('viewcompact') do
    setcode do
      hour5
    end
  end
end
