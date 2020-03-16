from __future__ import print_function
from twython import Twython
from twython.exceptions import TwythonError
import json
import csv
import random
import requests
from StringIO import StringIO

with open('credentials.json') as f:
    credentials = json.loads(f.read())

client = Twython(credentials["consumer_key"],
                 credentials["consumer_secret"],
                 credentials["access_token"],
                 credentials["access_token_secret"])

with open("hills.txt") as f:
    r = csv.DictReader(f, delimiter="|")
    hill = random.choice(list(r))

def locale(hill):
   c = hill["COUNTY_NAME"]
   s = hill["STATE_ALPHA"]
   if c.endswith(" (city)") or c.endswith(" (CA)"):
     # "Richmond (city)" => "Richmond"
     c = c.rsplit(" (", 1)[0]
     return c + ", " + s
   if s == "LA":
      return c + " Parish, LA"
   if s in ["GU", "DC"]:
     # "Guam", "District of Columbia"
      return c
   if s in ["VI", "PW", "AS", "AK"]:
      return c + ", " + s
   return c + " County, " + s

lat = hill["PRIM_LAT_DEC"]
lng = hill["PRIM_LONG_DEC"]

maps_link = "http://maps.google.com/?ll={},{}&t=p&z=15".format(lat, lng)

message = "{} ({}) {}".format(
   hill["FEATURE_NAME"],
   locale(hill),
   maps_link)

map_url = "https://maps.googleapis.com/maps/api/staticmap?size=504x252&maptype=terrain&markers=color:green%7C{},{}&scale=2&key={}".format(
   lat,
   lng,
   credentials["maps_api_key"])

def handler(event, context):
   response = client.upload_media(media=StringIO(requests.get(map_url).content))
   client.update_status(
        status=message,
        lat=lat,
        long=lng,
        media_ids=[response["media_id"]])

