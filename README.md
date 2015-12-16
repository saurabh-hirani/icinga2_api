### icinga2_api

Python library and command line utility to support [icinga2 api](http://docs.icinga.org/icinga2/snapshot/doc/module/icinga2/chapter/icinga2-api)

### Advantages over direct curl/wget calls

* Abstract out repetitive data like host, port, credentials, etc. in a configuration file
* Instead of specifying different HTTP headers - GET, PUT, POST - work with actions - create, read, update, delete.
* Better error handling.
* Python library and command line support.
* See **Examples** mapping from command line curl calls => the command line utlity => the python library.
* To see more curl calls check out [icinga2 api examples](https://github.com/saurabh-hirani/icinga2-api-examples)

### Installation

* stable release: ```pip install icinga2_api``` 
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

    gives the output

    ```bash
    OK: read action succeeded
    {
      "status": "success",
      "request": {
        "url": "https://192.168.1.103:4665/v1/status",
        "headers": {
          "X-HTTP-Method-Override": "GET",
          "Accept": "application/json"
        },
        "data": null
      },
      "response": {
        "status_code": 200,
        "data": {
          "results": [
            {
              "status": {
                "api": {
                  "zones": {
                    "docker-icinga2": {
                      .
                      .
                      .

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
    output = obj.read()
    print json.dumps(output['response']['data'], indent=2)
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

    gives the output

    ```bash
    OK: create action succeeded
    {
      "status": "success",
      "request": {
        "url": "https://192.168.1.103:4665/v1/objects/hosts/api_dummy_host_1",
        "headers": {
          "Accept": "application/json"
        },
        "data": {
          "templates": [
            "generic-host"
          ],
          "attrs": {
            "vars.os": "Linux",
            "address": "8.8.8.8"
          }
        }
      },
      "response": {
        "status_code": 200,
        "data": {
          "results": [
            {
              "status": "Object was created",
              "code": 200.0
            }
          ]
        }
      }
    }
    ```

  - With the icinga2_api library

    ```python
    from icinga2_api import api
    obj = api.Api(profile='docker')
    uri = '/v1/objects/hosts/api_dummy_host_1'
    data = { "templates": [ "generic-host" ], "attrs": { "address": "8.8.8.8", "vars.os" : "Linux" } }
    output = obj.create(uri, data)
    print json.dumps(output['response']['data'], indent=2)
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

    gives the output

    ```bash
    OK: read action succeeded
    {
      "status": "success",
      "request": {
        "url": "https://192.168.1.103:4665/v1/objects/hosts/api_dummy_host_1",
        "headers": {
          "X-HTTP-Method-Override": "GET",
          "Accept": "application/json"
        },
        "data": {
          "attrs": [
            "name",
            "address"
          ]
        }
      },
      "response": {
        "status_code": 200,
        "data": {
          "results": [
            {
              "meta": {},
              "type": "Host",
              "attrs": {
                "name": "api_dummy_host_1",
                "address": "8.8.8.8"
              },
              "joins": {},
              "name": "api_dummy_host_1"
            }
          ]
        }
      }
    }
    ```

  - With the icinga2_api library

    ```python
    from icinga2_api import api
    obj = api.Api(profile='docker')
    uri = '/v1/objects/hosts/api_dummy_host_1'
    data = { "attrs": ["name", "address"] }
    output = obj.read(uri, data)
    print json.dumps(output['response']['data'], indent=2)
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

    gives the output

    ```bash
    OK: update action succeeded
    {
      "status": "success",
      "request": {
        "url": "https://192.168.1.103:4665/v1/objects/hosts/api_dummy_host_1",
        "headers": {
          "Accept": "application/json"
        },
        "data": {
          "attrs": {
            "vars.os": "Linux",
            "vars.environment": "stage",
            "address": "8.8.8.8"
          }
        }
      },
      "response": {
        "status_code": 200,
        "data": {
          "results": [
            {
              "status": "Attributes updated.",
              "code": 200.0,
              "type": "Host",
              "name": "api_dummy_host_1"
            }
          ]
        }
      }
    }
    ```

  - With the icinga2_api library

    ```python
    from icinga2_api import api
    obj = api.Api(profile='docker')
    uri = '/v1/objects/hosts/api_dummy_host_1'
    data = { "attrs": { "address": "8.8.8.8", "vars.os": "Linux", "vars.environment" : "stage" } }
    output = obj.update(uri, data)
    print json.dumps(output['response']['data'], indent=2)
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

    gives the output

    ```bash
    OK: delete action succeeded
    {
      "status": "success",
      "request": {
        "url": "https://192.168.1.103:4665/v1/objects/hosts/api_dummy_host_1",
        "headers": {
          "X-HTTP-Method-Override": "DELETE",
          "Accept": "application/json"
        },
        "data": {
          "cascade": 1
        }
      },
      "response": {
        "status_code": 200,
        "data": {
          "results": [
            {
              "status": "Object was deleted.",
              "code": 200.0,
              "type": "Host",
              "name": "api_dummy_host_1"
            }
          ]
        }
      }
    }
    ```

  - With the icinga2_api library

    ```python
    from icinga2_api import api
    obj = api.Api(profile='docker')
    uri = '/v1/objects/hosts/api_dummy_host_1'
    data = {'cascade': 1}
    obj.delete(uri, data)
    ```

* Disable notifications for all hosts in hostgroup:

  - Without icinga2_api, through the command line

  ```bash
  curl -u $ICINGA2_API_USER:$ICINGA2_API_PASSWORD  \
       -H 'Accept: application/json' \
       -X POST \
       -k "https://$ICINGA2_HOST:$ICINGA2_API_PORT/v1/objects/hosts/" \
       -d '{ "filter": "match(\"*,api_dummy_hostgroup,*\",host.groups)",  \
             "attrs": { "enable_notifications": false } }' | python -m json.tool
  ```

  - With the icinga2_api command line utility

    ```bash
    icinga2_api -p docker \
                -a update \
                -u '/v1/objects/hosts/' \
                -d '{ "filter": "match(\"*,api_dummy_hostgroup,*\",host.groups)", \
                      "attrs": { "enable_notifications": false } }' | python -m json.tool
    ```

  - With the icinga2_api library:

    ```python
    from icinga2_api import api
    obj = api.Api(profile='docker')
    uri = '/v1/objects/hosts/'
    data = { 'filter': 'match("*,api_dummy_hostgroup,*",host.groups)', 
             'attrs': {'enable_notifications': false } }
    obj.update(uri, data)
    ```

  This functionality can be abstracted out in a ```manage_hostgroup_hosts_notifications``` function

### Error handling examples

* Deleting a non-existent host

    ```bash
    icinga2_api -p docker \
                -a delete \
                -u '/v1/objects/hosts/api_dummy_host_non_existent' \
                -d '{ "cascade": 1 }'
    ```

    gives the output

    ```bash
    CRITICAL: delete action failed
    {
      "status": "failure",
      "request": {
        "url": "https://192.168.1.103:4665/v1/objects/hosts/api_dummy_host_non_existent",
        "headers": {
          "X-HTTP-Method-Override": "DELETE",
          "Accept": "application/json"
        },
        "data": {
          "cascade": 1
        }
      },
      "response": {
        "status_code": 503,
        "data": "Error: Object does not exist.\n\n\t(0) libremote.so: void boost::throw_exception<boost::exception_detail::error_info_injector<std::invalid_argument> >(boost::exception_detail::error_info_injector<std::invalid_argument> const&) (+0xf8) [0x7f645d126428]\n\t(1) libremote.so: void boost::exception_detail::throw_exception_<std::invalid_argument>(std::invalid_argument const&, char const*, char const*, int) (+0x69) [0x7f645d1264e9]\n\t(2) libremote.so: icinga::ConfigObjectTargetProvider::GetTargetByName(icinga::String const&, icinga::String const&) const (+0xd2) [0x7f645d0cd772]\n\t(3) libremote.so: icinga::FilterUtility::GetFilterTargets(icinga::QueryDescription const&, boost::intrusive_ptr<icinga::Dictionary> const&, boost::intrusive_ptr<icinga::ApiUser> const&) (+0x1d1) [0x7f645d0cf011]\n\t(4) libremote.so: icinga::DeleteObjectHandler::HandleRequest(boost::intrusive_ptr<icinga::ApiUser> const&, icinga::HttpRequest&, icinga::HttpResponse&) (+0x341) [0x7f645d0d76c1]\n\t(5) libremote.so: icinga::HttpHandler::ProcessRequest(boost::intrusive_ptr<icinga::ApiUser> const&, icinga::HttpRequest&, icinga::HttpResponse&) (+0x52b) [0x7f645d0d58eb]\n\t(6) libremote.so: icinga::HttpServerConnection::ProcessMessageAsync(icinga::HttpRequest&) (+0x47d) [0x7f645d10c34d]\n\t(7) libbase.so: icinga::WorkQueue::WorkerThreadProc() (+0x4a2) [0x7f645da4c5d2]\n\t(8) libboost_thread-mt.so.1.53.0: <unknown function> (+0xd24a) [0x7f645e4a624a]\n\t(9) libpthread.so.0: <unknown function> (+0x7df5) [0x7f645ab37df5]\n\t(10) libc.so.6: clone (+0x6d) [0x7f645b04a1ad]\n\n"
      }
    }
    ```

    The status code is non-200 and the data non-json.

