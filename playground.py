#!/usr/bin/env python3
"""
testing out package
"""
import api
from file_io import io
from file_storage import avm_results_44579066315903093, avm_results_9118152176506649
import json
import statistics
import time

# HOMES_TO_QUERY = api.addresses.SOLD_ADDRESSES_FOR_AVM
HOMES_TO_QUERY = api.addresses.LA_GRANGE_HOMES

# avm_results = avm_results_44579066315903093.avm_results
avm_results = avm_results_9118152176506649.avm_results

# PREDICTED_SALE = api.addresses.TUTTLE_CLARENDON_HILLS
# PREDICTED_SALE = api.addresses.SPRING_LA_GRANGE
PREDICTED_SALE = api.addresses.MADISON_LA_GRANGE

WAIT_TIMEOUT = 2
DESIRED_KEYS = [
  'address',
  'assessment',
  'avm',
  'building',
  'lot',
  'sale'
]

all_building_sizes = []
all_beds = []
all_baths = []
all_market_diffs = []
all_avm_diffs = []
all_sale_values = []

def show_and_write(p, write_to_file = False):
  print(p)
  if write_to_file:
    to_write = "{},\n".format(json.dumps(p))
    io.append_to_file_storage(to_write)
  else:
    print("ONLY writing results to STDOUT, NOT to file_storage")

def get_avm_for_properties_list(write_to_file = False):
  """
  loop through all addresses to get avms
  """
  properties = []
  for number_street, city_state in HOMES_TO_QUERY.items():
    property_avm = api.attomized_avm.get_avm_by_address(number_street, city_state)
    properties.append(property_avm)
    show_and_write(property_avm, write_to_file)
    time.sleep(WAIT_TIMEOUT)
  return properties

def parse_and_filter_results(write_to_file = False):
  filtered_properties = []
  for avm in avm_results:
    property = avm['property'][0]
    p = { desired_key: property.get(desired_key) for desired_key in DESIRED_KEYS }
    filtered_p = {
      'address': get_address_from(p),
      'mktttlvalue': get_market_value_from(p),
      'avm': get_avm_from(p),
      'building': get_building_from(p),
      'lot': get_lot_from(p),
      'sale': get_sale_from(p)
    }
    filtered_properties.append(filtered_p)
    show_and_write(filtered_p, write_to_file)
  return filtered_properties

def get_building_from(p):
  try:
    b = {
      'size': p['building']['size']['livingsize'],
      'baths': p['building']['rooms']['bathstotal'],
      'beds': p['building']['rooms']['beds'],
      'bsmt': p['building']['interior']['bsmtsize']
    }
  except:
    return {}
  if b.get('beds'):
    all_beds.append(b.get('beds'))
  if b.get('baths'):
    all_baths.append(b.get('baths'))
  if b.get('size'):
    all_building_sizes.append(b.get('size'))
  return b

def get_sale_from(p):
  try:
    sale = {
      'saleamt': p['sale']['amount']['saleamt'],
      'saledate': p['sale']['amount']['salerecdate']
    }
  except:
    return "NULL"
  if sale.get('saleamt'):
    all_sale_values.append(sale.get('saleamt'))
  return sale

def get_address_from(p):
  try:
    lot = p['address']['line1']
  except:
    return "NULL"
  return lot

def get_lot_from(p):
  try:
    lot = p['lot']['lotsize2']
  except:
    return "NULL"
  return lot

def get_market_value_from(p):
  try:
    mv = p['assessment']['market']['mktttlvalue']
  except:
    return "NULL"
  return mv

def get_avm_from(p):
  try:
    avm = p['avm']['amount']['value']
  except:
    return "NULL"
  return avm

def compare_one_property(p):
  """
  pretty print one property and add it to the comparisons
  """
  mktval, date, saleamt, avm, mktdiff, avmdiff = None, None, None, None, None, None
  sale = p.get('sale')
  if type(sale).__name__ == 'dict':
    date = sale.get("saledate")
    saleamt = sale.get("saleamt", 0)
  mktval = p.get('mktttlvalue', 0)
  avm = p.get('avm', 0)
  if mktval and saleamt:
    mktdiff = mktval - saleamt
    all_market_diffs.append(mktdiff)
  if avm and saleamt:
    avmdiff = avm - saleamt
    all_avm_diffs.append(avmdiff)
  to_print = '\n'.join(
    [
      "Address: {}".format(p.get('address')),
      "SaleDate: {}".format(date),
      "Lot: {}".format(p.get('lot')),
      "Building: {}".format(p.get('building')),
      "AVM: {}".format(avm),
      "MarketValue: {}".format(mktval),
      "SaleValue: {}".format(saleamt),
      "MarketValue - SaleValue: {}".format(mktdiff),
      "AVM - SaleValue: {}".format(avmdiff),
      "-------------------",
    ]
  )
  print(to_print)

def compare_properties(properties):
  for p in properties:
    compare_one_property(p)

def show_differences():
  mean_sale_values = statistics.mean(all_sale_values)
  mean_market_diffs = statistics.mean(all_market_diffs)
  mean_avm_diffs = statistics.mean(all_avm_diffs)
  mean_beds = statistics.mean(all_beds)
  mean_baths = statistics.mean(all_baths)
  mean_building_sizes = statistics.mean(all_building_sizes)
  
  to_print = '\n'.join(
    [
      "Mean Beds: {}".format(mean_beds),
      "Mean Baths: {}".format(mean_baths),
      "Mean Building Sizes: {}".format(mean_building_sizes),
      "Mean Sale Values: {}".format(mean_sale_values),
      "Mean Market Value - Sale Value: {}".format(mean_market_diffs),
      "Mean AVM - Sale Value: {}".format(mean_avm_diffs),
    ]
  )
  print(to_print)

def execute():
  """
  Should set write_to_file for:
  get_avm_for_properties_list &
  parse_and_filter_results
  """
  # get_avm_for_properties_list(True)
  properties = parse_and_filter_results(False)
  #properties.append(PREDICTED_SALE)
  compare_properties(properties)
  show_differences()
  

if __name__ == "__main__":
    """
    MAIN APP
    """
    execute()