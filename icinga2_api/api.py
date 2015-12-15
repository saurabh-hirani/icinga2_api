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

    mandatory_attrs = [
      'host',
      'port',
      'user',
      'password'
    ]
    optional_attrs = {
      'timeout': defaults.TIMEOUT,
      'verify': defaults.VERIFY,
      'cert_path': defaults.CERT_PATH,
      'verbose': defaults.VERBOSE
    }

    # load the defaults from the configfile
    if not os.path.exists(configfile):
      err = 'configfile %s does not exist. See '
      raise ApiException('ERROR: configfile does not exist %s' % configfile)

    configfile_ds = yaml.load(open(configfile).read())

    if profile not in configfile_ds:
      raise ApiException('ERROR: Invalid profile [%s] not present in %s' % 
                         (profile, configfile))
    cfg_defaults = configfile_ds[profile]

    # update cfg_defaults with optional values
    for attr in optional_attrs.keys():
      if attr not in cfg_defaults:
        cfg_defaults[attr] = optional_attrs[attr]

    # initialize attributes to default values
    self.__dict__.update(cfg_defaults)

    # remove the None values from kwargs before updating
    kwargs = {k: kwargs[k] for k in kwargs if kwargs[k] is not None}

    # overrides the environment defaults by user passed values
    self.__dict__.update(kwargs)

    # find out the mandatory attrs not specified
    empty_attrs = [m for m in mandatory_attrs if m not in self.__dict__ or self.__dict__[m] is None]
    if empty_attrs:
      raise ApiException('ERROR: No values provided for %s' % empty_attrs)

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

  def read(self, uri=defaults.READ_ACTION_URI, data=None):
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

  def delete(self, uri, data=None):
    headers = {
      'Accept': 'application/json',
      'X-HTTP-Method-Override': 'DELETE'
    }
    return self._make_request(uri, headers, data)
