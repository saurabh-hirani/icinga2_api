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
  if value is None:
    return value
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
@click.option('-a', '--action', help='|'.join(VALID_ACTIONS) + ' Default: read', 
              callback=validate_action,
              default='read')
@click.option('-H', '--host', help='icinga2 api host - not required if profile specified',
              default=None)
@click.option('--port', help='icinga2 api port - not required if profile specified',
              default=None)
@click.option('-u', '--uri', help='icinga2 api uri. Default: ' + defaults.READ_ACTION_URI,  
              callback=validate_uri,
              default=defaults.READ_ACTION_URI)
@click.option('-U', '--user', help='icinga2 api user - not required if profile specified',
              default=None)
@click.option('--password', help='icinga2 api password - not required if profile specified',
              default=None)
@click.option('-t', '--timeout', help='icinga2 api timeout - not required if profile specified',
              default=None)
@click.option('-V', '--verify', help='verify certificate. Default: false',
              default=False)
@click.option('-C', '--cert-path', help='verify certificate path - not required if profile specified',
              default=None)
@click.option('-v', '--verbose/--no-verbose', help='verbose. Default: false',
              default=False)
@click.option('-d', '--data', help='json data to pass', 
              callback=validate_data,
              default=None)
def icinga2_api(**kwargs):
  """
  https://github.com/saurabh-hirani/icinga2_api/blob/master/README.md
  """
  if kwargs['verbose']:
    print 'args: %s' % kwargs
  obj = Api(**kwargs)
  kwargs['uri'] = re.sub("/{2,}", "/", kwargs['uri'])
  method_ref = getattr(obj, kwargs['action'])
  output_ds = method_ref(kwargs['uri'], kwargs['data'])
  click.echo(json.dumps(output_ds, indent=2))

if __name__ == '__main__':
  icinga2_api()
