#!/usr/bin/env python3
"""
ATTOM API
https://api.developer.attomdata.com
"""
import copy
import requests
from api import secrets
from api import defaults

URL = 'https://search.onboard-apis.com/propertyapi/v1.0.0'
ATTOM_URL = 'https://api.gateway.attomdata.com/propertyapi/v1.0.0'
HEADERS_DEFAULT = {
  'Accept': 'application/json',
}
headers = copy.deepcopy(HEADERS_DEFAULT)
headers['apikey'] = secrets.API_KEY

def ping():
  """
  ping api example property/detail by id
  """
  path = "property/detail"
  params = "id={}".format(defaults.ID)
  headers['apikey'] = defaults.API_KEY

  url = "{}/{}?{}".format(URL, path, params)

  r = requests.get(url, headers=headers)
  return r.json()
