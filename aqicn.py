import sys
import os
import logging
import logging.config
import copy
import types

# import settings
import requests
from hashlib import sha1
import hmac
import binascii

import settings

# https://aqicn.org/data-platform/token-confirm/417dacf2-ea4e-49cc-b0cc-76b37d8d2644
# https://aqicn.org/json-api/demo/
__version__ = "1.0"

# Google APIKeyRequest@ptv.vic.gov.au as to how to request for a set
devId = settings.devId
apiKey = settings.apiKey

key = '228af9abea7b097628c8993711f0f7aac53095c1'
egURL = 'https://api.waqi.info/feed/beijing/?token=228af9abea7b097628c8993711f0f7aac53095c1'
url = 'https://aqicn.org/data-platform/token-confirm/417dacf2-ea4e-49cc-b0cc-76b37d8d2644'


def _getSignature(request):
    key = apiKey
    request = request + ('&' if ('?' in request) else '?')
    raw = request+'devid={0}'.format(devId)
    hashed = hmac.new(key, raw, sha1)
    signature = hashed.hexdigest()

    return signature


def _getUrl(request):
    key = apiKey
    request = request + ('&' if ('?' in request) else '?')
    raw = request+'devid={0}'.format(devId)
    hashed = hmac.new(key, raw, sha1)
    signature = hashed.hexdigest()

    return 'http://timetableapi.ptv.vic.gov.au'+raw+'&signature={1}'.format(devId, signature)


def fetchPTV(args):
    """ Usage: no args 
    /v2/mode/%@/line/%@/stop/%@/directionid/%@/departures/all/limit/%@?for_utc=%@ &devid=%@&signature=%@
    """
    import json
    import pprint


    url = "/v2/mode/0/line/%@/stop/%@/directionid/%@/departures/all/limit/%@?for_utc=%@ &devid=%@&signature=%@"
    url = "/v2/mode/0/line/8/stop/1104/directionid/8/departures/all/limit/5?for_utc=2019-09-06T11:01:08Z"
    url = "/v2/mode/0/line/8/stop/1104/directionid/8/departures/all/limit/5"
    url = '/v2/healthcheck'  # works
    url = '/v2/nearme/latitude/-37.817993/longitude/144.981916'
    url = '/v3/routes'
    url = "/v3/disruptions/route/{route_id}"
    url = "/v3/routes/{route_id}"
    # 1 = Alamein
    url = "/v3/route_types"
    url = "/v3/routes?route_types=0"

    u = _getUrl(url)

    print u
    r = requests.get(u)  # returns a list of dictionaries
    # print r.text
    # json.dumps(r.json(), indent=4, sort_keys=True)
    # pprint.pprint(r.json())
    # pprint.pprint(r.json()["routes"])

    routes = r.json().get("routes")  # is a list of dict
    for route in routes:
        print "======================="
        pprint.pprint(route)




def t1(args):
    u = _getUrl('/v2/healthcheck')
    print u
    r = requests.get(u)
    print r.text
    print r.json


def _showAll(args):
    all = copy.copy(args.items())
    print "Script version", __version__

    for name, f in all:
        if isinstance(f, types.FunctionType):
            if not name.startswith("_"):
                print "******************************"
                print "Function ** %s **" % name
                print "******************************"
                if f.__doc__ is not None:
                    print '\t', f.__doc__





if __name__ == '__main__':
    REVISION = "$LastChangedRevision: 10220 $"
    if os.path.exists("logging.conf"):
        logging.config.fileConfig("logging.conf")
        logging.info("Using logging.conf for logging settings.")
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info('Version =%s', REVISION)
    if len(sys.argv) < 2:
        _showAll(locals())
        os._exit(0)

    # Globals
    fnName = sys.argv[1]
    logging.info('Function *** %s ***', fnName)

    if fnName not in locals():
        logging.error("Unknown function '%s'", fnName)
        os._exit(0)

    n = locals()[fnName](args=sys.argv[2:])
    sys.stdout.flush()

    logging.info('** bye')
    os._exit(0)
"""
      "/v3/departures/route_type/{route_type}/stop/{stop_id}":{
      "/v3/departures/route_type/{route_type}/stop/{stop_id}/route/{route_id}":{
      "/v3/directions/route/{route_id}":{
      "/v3/directions/{direction_id}":{
      "/v3/directions/{direction_id}/route_type/{route_type}":{
      "/v3/disruptions":{
      "/v3/disruptions/route/{route_id}":{
      "/v3/disruptions/route/{route_id}/stop/{stop_id}":{
      "/v3/disruptions/stop/{stop_id}":{
      "/v3/disruptions/{disruption_id}":{
      "/v3/disruptions/modes":{
      "/v3/outlets":{
      "/v3/outlets/location/{latitude},{longitude}":{
      "/v3/pattern/run/{run_id}/route_type/{route_type}":{
      "/v3/routes":{
      "/v3/routes/{route_id}":{
      "/v3/route_types":{
      "/v3/runs/route/{route_id}":{
      "/v3/runs/route/{route_id}/route_type/{route_type}":{
      "/v3/runs/{run_id}":{
      "/v3/runs/{run_id}/route_type/{route_type}":{
      "/v3/search/{search_term}":{
      "/v3/stops/{stop_id}/route_type/{route_type}":{
      "/v3/stops/route/{route_id}/route_type/{route_type}":{
      "/v3/stops/location/{latitude},{longitude}":{
"""
