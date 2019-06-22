#!/usr/bin/env python3
"""
testing out package
"""
import addresses
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

TEST_HOMES = addresses.test_list.HOMES
CH_HOMES = addresses.clarendon_hills.HOMES
WS_HOMES = addresses.western_springs.HOMES
LAG_HOMES = addresses.la_grange.HOMES
H_HOMES = addresses.hinsdale.HOMES

HOMES_TO_QUERY = TEST_HOMES

LAG_AVM = avm_results_la_grange.avm_results
WS_AVM = avm_results_western_springs.avm_results
H_AVM = avm_results_hinsdale.avm_results
CH_AVM = avm_results_clarendon_hills.avm_results

avm_results =  H_AVM

CH_DESIRED = addresses.clarendon_hills.TUTTLE_CLARENDON_HILLS
LAG_DESIRED = addresses.la_grange.MADISON_LA_GRANGE

DESIRED_PROPERTY = CH_DESIRED

WAIT_TIMEOUT = 2
SPECS_OF_INTEREST = [
  'address',
  'assessment',
  'avm',
  'building',
  'lot',
  'sale'
]

all_building_sizes, all_beds, all_baths, all_market_diffs, all_avm_diffs, all_sale_values = [], [], [], [], [], []

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

def parse_and_filter_results(avm_api_results, write_to_file = False):
  filtered_properties = []
  if avm_api_results:
    properties_to_loop = avm_api_results
  else:
    properties_to_loop = avm_results

  for avm in properties_to_loop:
    property_list = avm.get('property', None)
    if type(property_list).__name__ != 'list':
      continue
    if len(property_list) < 1:
      continue
    property = property_list[0] 
    property_reduced = { spec: property.get(spec) for spec in SPECS_OF_INTEREST }
    filtered_p = {
      'address': api.attomized_avm.get_address_from(property_reduced),
      'mktttlvalue': api.attomized_avm.get_market_value_from(property_reduced),
      'avm': api.attomized_avm.get_avm_from(property_reduced),
      'building': api.attomized_avm.get_building_from(property_reduced, all_beds, all_baths,  all_building_sizes),
      'lot': api.attomized_avm.get_lot_from(property_reduced),
      'sale': api.attomized_avm.get_sale_from(property_reduced, all_sale_values)
    }
    filtered_properties.append(filtered_p)
    show_and_write(filtered_p, write_to_file)
  return filtered_properties

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
  write_to_file = True
  if write_to_file:
    io.init_file()
    avm_api_results = get_avm_for_properties_list(write_to_file)
    io.terminate_file()
  else:
    avm_api_results = None
  properties = parse_and_filter_results(avm_api_results, False)
  compare_properties(properties)
  show_differences()
  

if __name__ == "__main__":
    """
    MAIN APP
    """
    execute()