#!/usr/bin/env python3
"""
ATTOM API
https://api.developer.attomdata.com
"""
import requests
from urllib.parse import quote
from api import api
from api import addresses

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
  for a in addresses.ADDRESSES:
    all_details.append(get_property_by_address(a))
  return all_details
