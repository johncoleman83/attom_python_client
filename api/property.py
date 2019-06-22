#!/usr/bin/env python3
"""
ATTOM API
https://api.developer.attomdata.com
"""
import requests
from urllib.parse import quote
from api import api

ADDRESSES = [
  "266 ANN ST, CLARENDON HILLS, IL 60514",
  "546 PAMELA CIR, HINSDALE, IL 60521",
  "923 LAWN CIR, WESTERN SPRINGS, IL 60558",
  "6474 BIG BEAR DR, INDIAN HEAD PARK, IL 60525",
  "5405 FRANKLIN AVE, WESTERN SPRINGS, IL 60558",
  "4036 HOWARD AVE, WESTERN SPRINGS, IL 60558",
  "908 S THURLOW ST, HINSDALE, IL 60521"
]

PATH = "property/detail"

def get_property_by_address(address):
  """
  API request to get property/detail?address=
  """
  params = "address={}".format(quote(address))

  url = "{}/{}?{}".format(api.URL, PATH, params)

  r = requests.get(url, headers=api.headers)
  return r.json()

def get_properties():
  """
  loop through all addresses
  """
  all_details = []
  for a in ADDRESSES:
    all_details.append(get_property_by_address(a))
  return all_details
