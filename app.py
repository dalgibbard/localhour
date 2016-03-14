#!/usr/bin/env python
from flask import Flask, abort, request
from geoip import geolite2
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import logging
from logging.handlers import RotatingFileHandler
from werkzeug.contrib.fixers import ProxyFix

utc = pytz.utc

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# API Endpoint to return a specific UTC Hour as the Requesting IP's Timezone
# eg. '20' = 20:00 UTC, which returns '15' (for 15:00 Eastern Time)
@app.route('/localhour/<int:utchour>', methods=['GET'])
def return_local_time(utchour):
    app.logger.info(str(request.remote_addr) + '[' + str(datetime.utcnow()) + '] Request: GET /timediff/' + str(utchour))
    if utchour == 24:
        utchour = 0
    if not 0 <= utchour <= 23:
        app.logger.warning(str(request.remote_addr) + '[' + str(datetime.utcnow()) +  '] Invalid utchour ' + str(utchour))
        return str('{ "error": "invalid utchour ' + str(utchour) + '" }')
    # Do GeoIP based on remote IP to determine TZ
    try:
        match = geolite2.lookup(request.remote_addr)
    except Exception as e:
        app.logger.error(str(request.remote_addr) + '[' + str(datetime.utcnow()) + '] Error: ' + str(e) + ' - whilst matching GeoIP data for IP')
        return str('{ "error": "error looking up match for IP ' + str(request.remote_addr) + '" }')
    # Check we got a match
    if match is None:
        app.logger.error(str(request.remote_addr) + '[' + str(datetime.utcnow()) + "] Failed to match IP to GeoIP data")
        return str('{ "error": "no geoip match for IP ' + str(request.remote_addr) + '" }')
    app.logger.info(str(request.remote_addr) + '[' + str(datetime.utcnow()) + '] Matched IP to timezone: ' + str(match.timezone))
    # Get Hour for 8pm in given TZ
    ## Create unix epoch from given time:
    utc_epoch = utchour * 60 * 60 - 100
    ## Generate a datetime type variable from that epoch
    utc_dt = utc.localize(datetime.utcfromtimestamp(utc_epoch))
    ## Generate TZ Type element
    tz = timezone(match.timezone)
    ## Convert and normalize
    local = tz.normalize(utc_dt.astimezone(tz))
    # Return the Hour for local 8pm
    return str('{ "hour": ' + str(local.hour) + ' }')

@app.route('/', methods=['GET'])
def index():
    app.logger.info(str(request.remote_addr) + '[' + str(datetime.utcnow()) + '] Request: GET /')
    return('<html>You probably want /localhour/(utc_hour)<br /><br />'
           '-- This is an API endpoint that converts a given UTC Hour<br />'
           '-- to the timezone of the requesting IP based on GeoIP lookup</html>')

if __name__ == '__main__':
    handler = RotatingFileHandler('flask.log', maxBytes=10240, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', debug=False)
