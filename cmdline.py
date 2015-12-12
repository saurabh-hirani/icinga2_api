#!/usr/bin/env python

import click
import json
import re

from icinga2_api.api import Api
from icinga2_api import defaults

VALID_ACTIONS = ['create', 'read', 'update', 'delete']

def validate_uri(ctx, param, value):
  if not value.startswith('/'):
    raise click.BadParameter('should begin with single /')
  return value

def validate_action(ctx, param, value):
  if value not in VALID_ACTIONS:
    raise click.BadParameter('should be in %s' % VALID_ACTIONS)
  return value

def validate_data(ctx, param, value):
  try:
    return json.loads(value)
  except ValueError as e:
    raise click.BadParameter('should be valid json')

@click.command()
@click.option('-c', '--configfile',
              help='icinga2 API config file. Default: %s' % defaults.CONFIGFILE,
              default=defaults.CONFIGFILE)
@click.option('-p', '--profile',
              help='icinga2 profile to load. Default: %s' % defaults.PROFILE,
              default=defaults.PROFILE)
@click.option('-v', '--verbose/--no-verbose', 
              help='verbose. Default: false',
              default=False)
@click.option('-a', '--action', help='|'.join(VALID_ACTIONS) + ' Default: read', 
              callback=validate_action,
              default='read')
@click.option('-u', '--uri', help='icinga2 api uri. Default: ' + defaults.READ_ACTION_URI,  
              callback=validate_uri,
              default=defaults.READ_ACTION_URI)
@click.option('-d', '--data', help='json data to pass', 
              callback=validate_data,
              default=defaults.READ_ACTION_DATA)
def icinga2_api(**kwargs):
  """
  create|read|update|delete on a uri
  http://docs.icinga.org/icinga2/snapshot/doc/module/icinga2/chapter/icinga2-api
  """
  if kwargs['verbose']:
    print 'args: %s' % kwargs
  obj = Api(configfile=kwargs['configfile'], profile=kwargs['profile'], 
            verbose=kwargs['verbose'])
  kwargs['uri'] = re.sub("/{2,}", "/", kwargs['uri'])
  method_ref = getattr(obj, kwargs['action'])
  output_ds = method_ref(kwargs['uri'], kwargs['data'])
  click.echo(json.dumps(output_ds, indent=2))

if __name__ == '__main__':
  icinga2_api()
