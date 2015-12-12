import os

CONFIGFILE        = os.path.join(os.environ['HOME'], '.icinga2', 'api.yml') 
PROFILE           = 'default'
READ_ACTION_URI   = '/v1/status'
READ_ACTION_DATA  = '{}'
