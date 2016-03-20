#!/usr/bin/env python

""" Quick and dirty example to set flags on host/service checks for icinga2 """

""" 
Quick and dirty program to enable/disable host/service checks for icinga2 for
hostgroups matching a pattern

EXAMPLES:

# Set 'enable_active_checks' to 'true' for all hosts in the hostgroups matching 'webs' for 'prod'
# icinga2 profile
$proganame prod enable_active_checks:true hosts webs 

# Set 'enable_notifications' to 'false' for all services in the hostgroups matching 'webs' for 'prod'
# icinga2 profile
$proganame prod enable_notifications:false services webs 
"""

import os
import sys
import json
import find_hostgroups
from icinga2_api import api

USAGE = 'USAGE: %s host_profile enable|disable hosts|services hostgroup_pattern' %\
        os.path.basename(__file__)

class HostgroupChecksException(Exception):
  """ Exception class for this program """
  pass

def main(args):
  """ enable|disable checks for hosts|services for matching hostgroups """

  if len(args) != 4:
    raise HostgroupChecksException({'message': 'Invalid number of args'})

  icinga2_host_profile = args[0]
  obj = api.Api(profile=icinga2_host_profile)

  action_state = args[1]
  action, state = action_state.split(':')

  if state == 'true':
    state = True
  else:
    state = False
  # no validation for action as of now

  target = args[2]
  if target != 'hosts' and target != 'services':
    raise HostgroupChecksException({'message': 'Invalid action target - %s' % target})

  # find the hostgroups
  hostgroup_pattern = args[3]

  uri = '/v1/objects/%s' % target
  status = {}
  if action not in status:
    status[action] = {'success': [], 'failure': []}

  if hostgroup_pattern == '.+':
    data = {"attrs": {action: state}}
    output = obj.update(uri, data)
    if output['status'] != 'success':
      status[action]['failure'].append(output)
    else:
      status[action]['success'].append(output)
    return status

  target_hostgroups_ds = find_hostgroups.main([icinga2_host_profile,
                                               'hostgroups', hostgroup_pattern])
  hostgroup_names = [x['name'] for x in target_hostgroups_ds]

  # do the deed

  for hostgroup_name in hostgroup_names:
    print "STATUS: %s: %s" % (hostgroup_name, action)
    data = {"attrs": {action: state},
            "filter": "\"%s\" in host.groups" % hostgroup_name}
    output = obj.update(uri, data)

    print "STATUS: %s: %s: %s" % (hostgroup_name, action, output['status'].upper())
    if output['status'] != 'success':
      status[action]['failure'].append(output)
    else:
      status[action]['success'].append(output)

  return status

if __name__ == '__main__':
  try:
    print json.dumps(main(sys.argv[1:]), indent=2)
  except HostgroupChecksException as hostgroup_exception:
    details = hostgroup_exception.args[0]
    print 'ERROR: ' + details['message']
    if 'output_ds' in details:
      print "------------------"
      print json.dumps(details['output_ds'], indent=2)
      print "------------------"
    print USAGE
    sys.exit(1)
