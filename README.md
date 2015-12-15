### icinga2_api

Python library and command line utility to support [icinga2 api](http://docs.icinga.org/icinga2/snapshot/doc/module/icinga2/chapter/icinga2-api)

### Installation

* stable release: ``` pip install icinga2_api``` 
* ongoing development package:
  ```bash
  git clone https://github.com/saurabh-hirani/icinga2_api
  cd icinga2_api
  sudo ./install.sh
  ```

### Pre-requisites

* A working icinga2 API setup through:
  - [icinga2 docker image](https://github.com/icinga/docker-icinga2)
  - [icinga2 vagrant boxes](https://github.com/Icinga/icinga-vagrant)
  - your own setup

### Description

* The python library and the command line utility's aim is to abstract out repetitive data like host, port, credentials, headers, etc. 
* Strip out that layer and you have a 1:1 mapping to how the icinga2 API is written. 
* See **Examples** mapping from command line curl calls => the command line utlity => the python library.
* To see more curl calls check out [icinga2 api examples](https://github.com/saurabh-hirani/icinga2-api-examples)

### Examples

* Check API status

  - Without icinga2_api, through the command line

    ```bash
    curl -u $ICINGA2_API_USER:$ICINGA2_API_PASSWORD \
         -k "https://$ICINGA2_HOST:$ICINGA2_API_PORT/v1/status" | python -m json.tool
    ```

  - With the icinga2_api command line utility

    ```bash
    icinga2_api -p docker
    ```

    No connection parameters are required as the user can specify connection parameters for a profile in a profile file. 

    ```bash
    Default location: ~/.icinga2/api.yml 
    Default profile: default
    ```
    
    Check ```sample_api.yml``` in this repo to view a sample configuration.

    ```bash
    icinga2_api --help
    ```

    to view all options

  - With the icinga2_api library

    ```python
    from icinga2_api import api
    obj = api.Api(profile='docker')
    obj.read()
    ```

* Create a host:

  - Without icinga2_api, through the command line

    ```bash
    curl -u $ICINGA2_API_USER:$ICINGA2_API_PASSWORD  \
         -H 'Accept: application/json' -X PUT \
         -k "https://$ICINGA2_HOST:$ICINGA2_API_PORT/v1/objects/hosts/api_dummy_host_1" \
         -d '{ "templates": [ "generic-host" ], "attrs": { "address": "8.8.8.8", "vars.os" : "Linux", "groups": ["api_dummy_hostgroup"] } }' | python -m json.tool
    ```

  - With the icinga2_api command line utility

    ```bash
    icinga2_api -p docker \
                -a create \
                -u '/v1/objects/hosts/api_dummy_host_1' \
                -d '{ "templates": [ "generic-host" ], "attrs": { "address": "8.8.8.8", "vars.os" : "Linux" } }'
    ```

  - With the icinga2_api library

    ```python
    from icinga2_api import api
    obj = api.Api(profile='docker')
    uri = '/v1/objects/hosts/api_dummy_host_1'
    data = { "templates": [ "generic-host" ], "attrs": { "address": "8.8.8.8", "vars.os" : "Linux" } }
    obj.create(uri, data)
    ```

* Read host name, address attributes for this host

  - Without icinga2_api, through the command line

    ```bash
    curl -u $ICINGA2_API_USER:$ICINGA2_API_PASSWORD \
         -H 'Accept: application/json' -H 'X-HTTP-Method-Override: GET' \
         -X POST \
         -k "https://$ICINGA2_HOST:$ICINGA2_API_PORT/v1/objects/hosts/api_dummy_host_1" \
         -d '{ "attrs": ["name", "address"] }' | python -m json.tool
    ```

  - With the icinga2_api command line utility

    ```bash
    icinga2_api -p docker \
                -a read \
                -u '/v1/objects/hosts/api_dummy_host_1' \
                -d '{ "attrs": ["name", "address"] }'
    ```

  - With the icinga2_api library

    ```python
    from icinga2_api import api
    obj = api.Api(profile='docker')
    uri = '/v1/objects/hosts/api_dummy_host_1'
    data = { "attrs": ["name", "address"] }
    obj.read(uri, data)
    ```

* Update attributes for this host - add a custom var

  - Without icinga2_api, through the command line

    ```bash
    curl -u $ICINGA2_API_USER:$ICINGA2_API_PASSWORD \
         -H 'Accept: application/json' -H 'X-HTTP-Method-Override: GET' \
         -X POST \
         -k "https://$ICINGA2_HOST:$ICINGA2_API_PORT/v1/objects/hosts/api_dummy_host_1" \
         -d '{ "attrs": { "address": "8.8.8.8", "vars.os": "Linux", "vars.environment" : "stage" } }'
    ```

  - With the icinga2_api command line utility

    ```bash
    icinga2_api -p docker \
                -a update \
                -u '/v1/objects/hosts/api_dummy_host_1' \
                -d '{ "attrs": { "address": "8.8.8.8", "vars.os": "Linux", "vars.environment" : "stage" } }'
    ```

  - With the icinga2_api library

    ```python
    from icinga2_api import api
    obj = api.Api(profile='docker')
    uri = '/v1/objects/hosts/api_dummy_host_1'
    data = { "attrs": { "address": "8.8.8.8", "vars.os": "Linux", "vars.environment" : "stage" } }
    obj.update(uri, data)
    ```

* Delete this host

  - Without icinga2_api, through the command line

    ```bash
    curl -u $ICINGA2_API_USER:$ICINGA2_API_PASSWORD  \
         -H 'Accept: application/json' -H 'X-HTTP-Method-Override: DELETE' -X POST \
         -k "https://$ICINGA2_HOST:$ICINGA2_API_PORT/v1/objects/hosts/api_dummy_host_1" \
         -d '{ "cascade": 1 }'
    ```

  - With the icinga2_api command line utility

    ```bash
    icinga2_api -p docker \
                -a delete \
                -u '/v1/objects/hosts/api_dummy_host_1' \
                -d '{ "cascade": 1 }'
    ```

  - With the icinga2_api library

    ```python
    from icinga2_api import api
    obj = api.Api(profile='docker')
    uri = '/v1/objects/hosts/api_dummy_host_1'
    data = {'cascade': 1}
    obj.delete(uri, data)
    ```
