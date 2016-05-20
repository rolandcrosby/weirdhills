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

def county(hill):
   c = hill["COUNTY_NAME"]
   if hill["STATE_ALPHA"] == "LA":
      return c + " Parish"
   return c + " County"

message = "{} ({}, {})".format(
   hill["FEATURE_NAME"],
   county(hill),
   hill["STATE_ALPHA"])

map_url = "https://maps.googleapis.com/maps/api/staticmap?size=504x252&maptype=terrain&markers=color:green%7C{},{}&key={}".format(
   hill["PRIM_LAT_DEC"],
   hill["PRIM_LONG_DEC"],
   credentials["maps_api_key"])

def handler(event, context):
   response = client.upload_media(media=StringIO(requests.get(map_url).content))
   client.update_status(status=message, media_ids=[response["media_id"]])

