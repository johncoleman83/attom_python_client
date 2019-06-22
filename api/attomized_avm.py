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

def get_building_from(p, all_beds, all_baths, all_building_sizes):
  b = {
    'size': p.get('building', {}).get('size', {}).get('livingsize', None),
    'baths': p.get('building', {}).get('rooms', {}).get('bathstotal', None),
    'beds': p.get('building', {}).get('rooms', {}).get('beds', None),
    'bsmt': p.get('building', {}).get('interior', {}).get('bsmtsize', None),
  }
  if b.get('beds'):
    all_beds.append(b.get('beds'))
  if b.get('baths'):
    all_baths.append(b.get('baths'))
  if b.get('size'):
    all_building_sizes.append(b.get('size'))
  return b

def get_sale_from(p, all_sale_values):
  sale = {
    'saleamt': p.get('sale', {}).get('amount', {}).get('saleamt', None),
    'saledate': p.get('sale', {}).get('amount', {}).get('salerecdate', None),
  }
  all_sale_values.append(sale.get('saleamt'))
  return sale

def get_address_from(p):
  return p.get('address', {}).get('line1', "NULL")

def get_lot_from(p):
  return p.get('lot', {}).get('lotsize2', "NULL")

def get_market_value_from(p):
  return p.get('assessment', {}).get('market', {}).get('mktttlvalue', "NULL")

def get_avm_from(p):
  return p.get('avm', {}).get('amount', {}).get('value', "NULL")
