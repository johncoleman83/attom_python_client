#!/usr/bin/env python3
"""
ATTOM API
https://api.developer.attomdata.com
"""
import requests
from urllib.parse import quote, urlencode
from api import api

PATH = "attomavm/detail"

def get_avm_by_address(number_street, city_state):
  """
  API request to get attomavm/detail
  """
  params = urlencode(
    {
      "address1": number_street,
      "address2": city_state,
    }
  )

  url = "{}/{}?{}".format(api.ATTOM_URL, PATH, params)

  r = requests.get(url, headers=api.headers)
  return r.json()

