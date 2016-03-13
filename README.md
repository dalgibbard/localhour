# localhour
Flask API which accepts a UTC Hour, and returns the Hour for the Requesting IP's Timezone

# Example API call:
```
# Request your physical timezone equivilent for 8pm (20:00):
curl http://<server>/localhour/20
```

# NOTE:
This app will not work for local IP addresses.
Please be sure to test it with an external IP :)

# Running in Docker
To run in docker:
* Clone the project:
```git clone https://github.com/dalgibbard/localhour```
* Create a docker folder to build in:
```cd dockerbuild```
* Copy the Dockerfile in:
```cp ../localhour/Dockerfile .```
* Build the docker container
```docker build -t localhour .```
* Run it, allowing access to the app, on the host machine, on port 8000:
```docker run -d -p 8000:80 --name localhour localhour```
