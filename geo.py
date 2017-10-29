import requests
import json
def lookup(ip=""):
    "Returns a dict containing an IP geolocation lookup from the freegeoip.net api. Optionally takes an IP address or hostname to lookup as argument, otherwise looks up the client's IP."
    r=requests.get("http://freegeoip.net/json/" + ip)
    if r.status_code != 200: return {"http_status_code":r.status_code}
    return json.loads(r.text)

def as_string(r):
    "Parses an object in the form returned by lookup to a human-readable string."
    if 'http_status_code' in r:
        if r['http_status_code'] == 404: return "unknown"
        if r['http_status_code'] == 403: return "geolocation API rate limit exceeded."
    res=""
    if 'city' in r and r['city'] != "": res+=r['city']+", "
    if 'region_name' in r and r['region_name'] != "": res+=r['region_name']+", "
    if 'country_name' in r and r['country_name'] != "": res+=r['country_name']+" "
    if 'ip' in r and r['ip'] != "": res+="("+r['ip']+" )"
    if res == "": return "Invalid response from the freegeoip.net API. The response was: " + str(r)
    else: return res
