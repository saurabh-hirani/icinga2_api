icinga2_api

python library to support [icinga2 api](http://docs.icinga.org/icinga2/snapshot/doc/module/icinga2/chapter/icinga2-api)

Work in progress.

### Examples

* Check API status

```python
from icinga2_api import api
# load this profile from ~/.icinga2/api.yaml - sample in sample_api.yaml
obj = api.Api(profile='stage') 
obj.read('/v1/status')
```
