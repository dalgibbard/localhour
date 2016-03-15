#!/usr/bin/env python
## Same as app.py, but uses a locally sourced DB for example's sake.
## Has an additional require of 'geoip2' module: pip install geoip2
## DB file can be obtained from MaxMind

from flask import Flask, abort, request
#from geoip import geolite2
import geoip2.database
from datetime import datetime, timedelta
from pytz import timezone, country_timezones, UnknownTimeZoneError
import pytz
import logging
from logging.handlers import RotatingFileHandler
from werkzeug.contrib.fixers import ProxyFix
reader = geoip2.database.Reader('./GeoLite2-City.mmdb')
utc = pytz.utc


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
handler = RotatingFileHandler('/var/log/flask.log', maxBytes=10240, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# API Endpoint to return a specific UTC Hour as the Requesting IP's Timezone
# eg. '20 LocalDC Time = 15:00 UTC, which returns '15'
@app.route('/localhour/<int:utchour>', methods=['GET'])
def return_local_time(utchour):
    app.logger.info(str(request.remote_addr) + ' [' + str(datetime.utcnow()) + '] Request: GET /localhour/' + str(utchour))
    if utchour == 24:
        utchour = 0
    if not 0 <= utchour <= 23:
        app.logger.warning(str(request.remote_addr) + ' [' + str(datetime.utcnow()) +  '] Invalid utchour ' + str(utchour))
        return str('{ "error": "invalid utchour ' + str(utchour) + '" }')
    # Do GeoIP based on remote IP to determine TZ
    try:
        match = reader.city(request.remote_addr)
    except Exception as e:
        app.logger.error(str(request.remote_addr) + ' [' + str(datetime.utcnow()) + '] Error: ' + str(e) + ' - whilst matching GeoIP data for IP')
        return str('{ "error": "error looking up match for IP ' + str(request.remote_addr) + '" }')
    # Check we got a match
    if match is None:
        app.logger.error(str(request.remote_addr) + ' [' + str(datetime.utcnow()) + "] Failed to match IP to GeoIP data")
        return str('{ "error": "no geoip match for IP ' + str(request.remote_addr) + '" }')

### TEST
    try:
        print(match)
        local = timezone(match.time_zone)
    except UnknownTimeZoneError:
        local = timezone(country_timezones(match.subdivisions.most_specific.iso_code))
    except Exception as e:
        return str('{ "error": "Error: ' + str(e) + ' - whilst getting timezone" }')
    app.logger.info(str(request.remote_addr) + ' [' + str(datetime.utcnow()) + '] Matched IP to timezone: ' + str(local))
    local_dt = local.localize(datetime(datetime.today().year, datetime.today().month, datetime.today().day, utchour, 0, 0))
    utc_dt = utc.normalize(local_dt.astimezone(utc))
    app.logger.info(str(request.remote_addr) + ' [' + str(datetime.utcnow()) + '] Returning value: ' + str(utc_dt.hour) + ' for requested hour ' + str(utchour) + ' in Timezone ' + str(local))
    return str('{ "hour": ' + str(utc_dt.hour) + ' }')

@app.route('/localhour', methods=['GET'])
def index():
    app.logger.info(str(request.remote_addr) + '[' + str(datetime.utcnow()) + '] Request: GET /')
    return('<html>You probably want /localhour/(utc_hour)<br /><br />'
           '-- This is an API endpoint that converts a given UTC Hour<br />'
           '-- to the timezone of the requesting IP based on GeoIP lookup</html>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
