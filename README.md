# localhour
Flask API which accepts a UTC Hour, and returns the Hour for the Requesting IP's Timezone

# Example API call:
```
# Request your physical timezone equivilent for 8pm (20:00):
curl http://<server>/localhour/20
```

# Example Return Data:
If the request is for '20' (8pm UTC), and the request comes from a UTC+5 timezone, the return will be:
* Success:
```
{ "hour": 1 }
```
If the request is invalid (for example, from a local IP), an error will be displayed instead, eg:
* Error:
```
{ "error": "no geoip match for IP 127.0.0.1" }
```

# NOTE:
This app will not work for local IP addresses.
Please be sure to test it with an external IP :)

# Running in Docker (including Build)
To run in docker:
* Clone the project:
```git clone https://github.com/dalgibbard/localhour```
* Create a docker folder to build in:
```cd dockerbuild```
* Copy the Dockerfile in:
```cp ../localhour/Dockerfile .```
* Build the docker container
```docker build --no-cache=true -t localhour .```
* Run it, allowing access to the app, on the host machine, on port 8000:
```docker run -d -p 8000:80 --name localhour localhour```

# Running in Docker (from auto-builds)
* Run it, using the image from Docker Hub -- Available on port 80.
```docker run -d -p 80 --name localhour dalgibbard/localhour```
