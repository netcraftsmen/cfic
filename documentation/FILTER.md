# Filters

Rather than sending all of the information gathered from the target network devices, it is desirable to create filters that can be used by the distributed clients to only publish Kafka messages that match the filter.

Ideally these filters can also be published as Kafka messages and the distributed publishers would subscribe to the filter topic, and update their local cache values.

## Filter format

The filters should be in JSON format and contain an identifier indicating the target network device.

As an example, assume the network operator would like to locate a specify MAC address or OS type on the network.

```json
{
    "publisher": "meraki",
    "type": "getNetworkClients",
    "start_date": "2023-05-12T18:32:50Z",
    "end_date": "2023-05-13T18:32:50Z",
    "match": "any",
    "conditions": [
      {"key": "mac", "value": "26:f5:a2:3c:e4:70"},
      {"key": "os", "value": "PlayStation 4"}
    ]
}
```

```python
import meraki
conditions = [{"key": "mac", "value": "26:f5:a2:3c:e4:70"}, {"key": "os", "value": "PlayStation 4"}]
dashboard = meraki.DashboardAPI(output_log=False, print_console=True)
orgs = dashboard.organizations.getOrganizations()
networks = dashboard.organizations.getOrganizationNetworks('719170')
clients = dashboard.networks.getNetworkClients(networks[0]['id'])
for client in clients:
    match = 0
    for condition in conditions:
        if client.get(condition['key']):
            if client[condition['key']] == condition['value']:
                match += 1

    if condition['match'] == 'any' & match > 0:
        return 'select'
    if condition['match'] == 'all' & match == len(condition):
        return 'select'
```

### Using fuzzy wuzzy

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

description = 'AXIS Camera M1014'
c_desc = 'AXIS Camera M1016'
fuzz.ratio(description, c_desc)
mac = 'dc:4a:3e:a0:d1:1e'
c_mac = 'dc:4a:3e:'
fuzz.partial_ratio(c_mac, mac)