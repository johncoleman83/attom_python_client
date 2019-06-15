#!/usr/bin/env python3
"""
ATTOM API
https://api.developer.attomdata.com
"""
import requests
from urllib.parse import quote, urlencode
from api import api

PATH = "assessment/snapshot"

def get_assessment_of_area_by(geoid, radius):
  """
  API request to get assessment/snapshot
  """
  params = urlencode(
    {
      "geoid": geoid,
      "radius": radius,
      "minassdttlvalue": "250000",
      "maxassdttlvalue": "751000",
      "startcalendardate": "2017-01-01",
      "endcalendardate": "2019-05-31",
    }
  )

  url = "{}/{}?{}".format(api.URL, PATH, params)

  r = requests.get(url, headers=api.headers)
  return r.json()

def get_assessment_history_by(id):
  """
  API request to get assessmenthistory/detail
  """
  path = "assessmenthistory/detail"
  params = urlencode(
    {
      "id": id
    }
  )

  url = "{}/{}?{}".format(api.URL, path, params)

  r = requests.get(url, headers=api.headers)
  return r.json()
