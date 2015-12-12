#!/usr/bin/env python

import os
import yaml
import json

import requests
requests.packages.urllib3.disable_warnings()

from icinga2_api import defaults

class ApiException(Exception): pass

class Api(object):
  def __init__(self, configfile=defaults.CONFIGFILE, 
               profile=defaults.PROFILE, **kwargs):
    # set the attributes passed by the user
    self.configfile = configfile
    self.profile = profile

    # env vars corresponding to each attr
    attrs_env_vars = {
      'host': 'ICINGA2_API_HOST',
      'port': 'ICINGA2_API_PORT',
      'user': 'ICINGA2_API_USER',
      'password': 'ICINGA2_API_PASSWORD',
      'timeout': 'ICINGA2_API_TIMEOUT',
      'verify': 'ICINGA2_API_VERIFY',
      'cert_path': 'ICINGA2_API_CERT_PATH',
      'verbose': 'ICINGA2_API_VERBOSE'
    }

    # load the defaults from the configfile
    if not os.path.exists(configfile):
      raise ApiException('ERROR: Invalid configfile %s' % configfile)

    configfile_ds = yaml.load(open(configfile).read())

    if profile not in configfile_ds:
      raise ApiException('ERROR: Invalid profile [%s] not present in %s' % 
                         (profile, configfile))
    cfg_defaults = configfile_ds[profile]

    # overrides the configfile defaults by the environment
    defaults = cfg_defaults
    for attr, attr_env_var in attrs_env_vars.iteritems():
      if attr not in defaults:
        defaults[attr] = None
      if attr_env_var in os.environ:
        defaults[attr] = os.environ[attr_env_var]

    # initialize attributes to default values
    self.__dict__.update(defaults)

    # overrides the environment defaults by user passed values
    self.__dict__.update(kwargs)

  def _make_request(self, uri, headers, data, method='post'):
    # validate input
    if not uri.startswith('/'):
      raise ApiException('ERROR: Invalid uri [%s] must begin with single /' % 
                         uri)
    url = 'https://%s:%s%s' % (self.host, self.port, uri)

    # build the request body
    kwargs = {
      'headers': headers,
      'auth': (self.user, self.password),
      'verify': False,
    }
    if data is not None:
      kwargs['data'] = json.dumps(data)
    if self.verify is not False:
      kwargs['verify'] = self.verify

    if self.verbose:
      print 'url: %s' % url
      print 'attrs: %s' % kwargs

    # make the request
    method_ref = getattr(requests, method)
    r = method_ref(url, **kwargs)

    if r.status_code == 200:
      # convert unicode to str 
      return yaml.safe_load(json.dumps(r.json()))
    
    raise ApiException('Apierror status:%d error:%s' % (r.status_code, r.text))

  def create(self, uri, data):
    headers = {
      'Accept': 'application/json',
    }
    return self._make_request(uri, headers, data, 'put')

  def read(self, uri=defaults.READ_ACTION_URI, data=defaults.READ_ACTION_DATA):
    headers = {
      'Accept': 'application/json',
      'X-HTTP-Method-Override': 'GET'
    }
    return self._make_request(uri, headers, data)

  def update(self, uri, data):
    headers = {
      'Accept': 'application/json',
    }
    return self._make_request(uri, headers, data)

  def delete(self, uri, data):
    headers = {
      'Accept': 'application/json',
      'X-HTTP-Method-Override': 'DELETE'
    }
    return self._make_request(uri, headers, data)
