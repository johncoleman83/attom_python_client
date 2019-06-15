# ATTOM Data SolutionsOM

https://api.developer.attomdata.com/docs#/

## Setup

create the file `attom_python_client/api/secrets.py` based off of this template,
but add your api key (the default api key from the docs is used here below):
  ```
  #!/usr/bin/env python3  
  API_KEY = "736f1130096aa92549d800921bca8e8c"
  ```

## Playground

use the `python3` repl. Note that the `ping` method uses the defautl API key,
and does not use your secret key
```
$ python3
Python 3.7.0 (default, Aug 22 2018, 15:22:33) 
[Clang 9.1.0 (clang-902.0.39.2)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pprint
>>> import api
>>> r = api.api.ping()
>>> r['status']
{'version': '1.0.0', 'code': 0, 'msg': 'SuccessWithResult', 'total': 1, 'page': 1, 'pagesize': 10}
>>> pprint.pprint(r)
{'property': [{'address': {'country': 'US',
                           'countrySubd': 'CO',
                           'line1': '4529 WINONA CT',
                           'line2': 'DENVER, CO 80212',
                           'locality': 'Denver',
                           'matchCode': 'ExaStr',
                           'oneLine': '4529 WINONA CT, DENVER, CO 80212',
                           'postal1': '80212',
                           'postal2': '2512',
                           'postal3': 'C037'},
               'area': {'blockNum': '36',
                        'countrysecsubd': 'Denver County',
                        'countyuse1': '113',
                        'muncode': 'DE',
                        'munname': 'DENVER',
                        'srvyRange': '68W',
                        'srvySection': '19',
                        'srvyTownship': '03S',
                        'subdname': 'BERKELEY',
                        'subdtractnum': '0',
                        'taxcodearea': '0'},
               'building': {'construction': {'condition': 'AVERAGE',
                                             'wallType': 'BRICK'},
                            'interior': {'bsmtsize': 480,
                                         'bsmttype': 'UNFINISHED',
                                         'fplccount': 1,
                                         'fplcind': 'Y',
                                         'fplctype': 'YES'},
                            'parking': {'garagetype': 'DETACHED GARAGE',
                                        'prkgSize': 240,
                                        'prkgSpaces': '0',
                                        'prkgType': 'GARAGE DETACHED'},
                            'rooms': {'bathfixtures': 0,
                                      'baths1qtr': 0,
                                      'baths3qtr': 0,
                                      'bathscalc': 1.0,
                                      'bathsfull': 1,
                                      'bathshalf': 0,
                                      'bathstotal': 1.0,
                                      'beds': 2,
                                      'roomsTotal': 5},
                            'size': {'bldgsize': 1414,
                                     'grosssize': 1414,
                                     'grosssizeadjusted': 934,
                                     'groundfloorsize': 934,
                                     'livingsize': 934,
                                     'sizeInd': 'LIVING SQFT ',
                                     'universalsize': 934},
                            'summary': {'bldgType': 'TYPE UNKNOWN',
                                        'bldgsNum': 0,
                                        'imprType': 'RESIDENTIAL',
                                        'levels': 1,
                                        'mobileHomeInd': ' ',
                                        'quality': 'EXCELLENT',
                                        'storyDesc': 'TYPE UNKNOWN',
                                        'unitsCount': '1',
                                        'yearbuilteffective': 0}},
               'identifier': {'apn': '0219204018000',
                              'apnOrig': '219204018000',
                              'attomId': 184713191,
                              'fips': '08031',
                              'obPropId': 18471319108031},
               'location': {'accuracy': 'Street',
                            'distance': 0.0,
                            'elevation': 0.0,
                            'geoid': 'CO08031, CS0891007, DB0803360, '
                                     'MT30001324, ND0000119198, ND0000539537, '
                                     'PL0820000, SB0000076114, SB0000076155, '
                                     'SB0000076161, SB0000135819, ZI80212',
                            'latitude': '39.778904',
                            'longitude': '-105.047624'},
               'lot': {'depth': 0,
                       'frontage': 0,
                       'lotnum': '31',
                       'lotsize1': 0.1077,
                       'lotsize2': 4690,
                       'pooltype': 'NONE'},
               'summary': {'absenteeInd': 'OWNER OCCUPIED',
                           'legal1': 'BERKELEY B36 L31 & S/2 OF L32 EXC REAR '
                                     '8FT TO CITY',
                           'propIndicator': '10',
                           'propLandUse': 'SFR',
                           'propclass': 'Single Family Residence / Townhouse',
                           'propsubtype': 'RESIDENTIAL',
                           'proptype': 'SFR',
                           'yearbuilt': 1900},
               'utilities': {'heatingtype': 'FORCED AIR'},
               'vintage': {'lastModified': '2019-5-22',
                           'pubDate': '2019-5-23'}}],
 'status': {'code': 0,
            'msg': 'SuccessWithResult',
            'page': 1,
            'pagesize': 10,
            'total': 1,
            'version': '1.0.0'}}
```
