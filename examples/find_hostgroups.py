#!/usr/bin/env python

""" 
Quick and dirty program to find objects matching a proper regular expression

EXAMPLES:

# Find all 'hosts' in 'prod' icinga2_api profile with host.name matching 'web-'
$proganame prod hosts 'web-' 

# Find all 'hostgroups' in 'prod' icinga2_api profile matching 'web-'
$proganame prod hostgroups 'web-' 
"""

import os
import re
import sys
import json
from icinga2_api import api

USAGE = 'USAGE: %s host_profile object_type regex' % os.path.basename(__file__)

class FindHostgroupsException(Exception):
  """ Exception class for this program """
  pass

def main(args):
  """ find hostgroups matching regex """

  if len(args) != 3:
    raise FindHostgroupsException({'message': 'Invalid number of args'})

  icinga2_host_profile = args[0]

  icinga2_obj_type = args[1]
  obj = api.Api(profile=icinga2_host_profile)

  regex = args[2]
  regex = regex.strip()
  if regex == '':
    raise FindHostgroupsException({'message': 'Invalid regex - %s' % regex})
  compiled_regex = re.compile(regex)

  uri = '/v1/objects/%s' % icinga2_obj_type
  data = {"attrs": ["name"]}
  output = obj.read(uri, data)

  if output['status'] != 'success': 
    raise FindHostgroupsException({'message': 'API call failed',
                                   'output_ds': output}) 

  results = output['response']['data']['results']
  if not results:
    return []

  return [x for x in results if re.search(compiled_regex, x['name'])]

if __name__ == '__main__':
  try:
    print json.dumps(main(sys.argv[1:]), indent=2)
  except FindHostgroupsException as hostgroup_exception:
    details = hostgroup_exception.args[0]
    print 'ERROR: ' + details['message']
    if 'output_ds' in details:
      print "------------------"
      print json.dumps(details['output_ds'], indent=2)
      print "------------------"
    print USAGE
    sys.exit(1)
