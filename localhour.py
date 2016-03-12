#!/usr/bin/env python
from flask import Flask, abort, request
from geoip import geolite2
from datetime import datetime, timedelta
from pytz import timezone
import pytz

app = Flask(__name__)

# API Endpoint to return a specific UTC Hour as the Requesting IP's Timezone
# eg. '20' = 20:00 UTC, which returns '15' (for 15:00 Eastern Time)
@app.route('/timediff/<int:utchour>', methods=['GET'])
def return_local_time(utchour):
    if utchour == 24:
        utchour = 0
    if not 0 <= utchour <= 23:
        print("Invalid UTC Hour: " + utchour)
        abort(500)
    # Do GeoIP based on remote IP to determine TZ
    try:
        match = geolite2.lookup(request.remote_addr)
    except Exception as e:
        print("Error: " + str(e) + " - whilst matching GeoIP data for IP " + str(request.remote_addr))
        abort(500);
    # Check we got a match
    if match is None:
        print("Failed to match IP " + str(request.remote_addr) + " to GeoIP data")
        abort(500)
    # Get Hour for 8pm in given TZ
    ## Create unix epoch from given time:
    utc_epoch = utchour * 60 * 60
    ## Generate a datetime type variable from that epoch
    utc_dt = utc.localize(datetime.utcfromtimestamp(utc_epoch))
    ## Generate TZ Type element
    tz = timezone(match.timezone)
    ## Convert and normalize
    local = tz.normalize(utc_dt.astimezone(tz))
    # Return the Hour for local 8pm
    return str(local.hour)

@app.route('/', methods=['GET'])
def index():
    abort(404)

if __name__ == '__main__':
    app.run(debug=True)
