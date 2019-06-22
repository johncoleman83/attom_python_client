#!/usr/bin/env python3
"""
testing out package
"""
import api
from file_io import io
from file_storage import (
  avm_results_western_springs,
  avm_results_clarendon_hills,
  avm_results_hinsdale,
  avm_results_la_grange
)
import json
import statistics
import time

# HOMES_TO_QUERY = api.addresses.CLARENDON_HILLS_HOMES
HOMES_TO_QUERY = api.addresses.WESTERN_SPRINGS_HOMES
# HOMES_TO_QUERY = api.addresses.LA_GRANGE_HOMES
# HOMES_TO_QUERY = api.addresses.HINSDALE_HOMES

# avm_results = avm_results_la_grange.avm_results
avm_results = avm_results_western_springs.avm_results
# avm_results = avm_results_hinsdale.avm_results
# avm_results = avm_results_clarendon_hills.avm_results

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

all_building_sizes, all_beds, all_baths, all_market_diffs, all_avm_diffs, all_sale_values = [], [], [], [], [], []

def init_file():
  io.append_to_file_storage("#!/usr/bin/env python3\n\navm_results = [\n")

def terminate_file():
  io.append_to_file_storage("]\n")


def show_and_write(p, write_to_file = False):
  print(p)
  if write_to_file:
    to_write = "\t{},\n".format(json.dumps(p))
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
  to_print = []
  mean_values_lists = [
    all_building_sizes, all_beds, all_baths, all_sale_values
  ]
  mean_names = [
    "Building Sizes", "Beds", "Baths", "Sale Values"
  ]
  for i, totals in enumerate(mean_values_lists):
    if len(totals) > 0:
      temp_mean = statistics.mean(totals)
      to_print.append("Mean {}: {}".format(mean_names[i], temp_mean))
  to_print.append("Mean Market Value - Sale Value: {}".format(statistics.mean(all_market_diffs)))
  to_print.append("Mean AVM - Sale Value: {}".format(statistics.mean(all_avm_diffs)))

  print('\n'.join(to_print))

def execute():
  """
  Should set write_to_file for:
  get_avm_for_properties_list &
  parse_and_filter_results
  """
  # init_file()
  # get_avm_for_properties_list(True)
  # terminate_file()
  properties = parse_and_filter_results(False)
  properties.append(PREDICTED_SALE)
  compare_properties(properties)
  show_differences()
  

if __name__ == "__main__":
    """
    MAIN APP
    """
    execute()