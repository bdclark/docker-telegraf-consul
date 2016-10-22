# telegraf-consul Docker image

Docker image that runs [Telegraf][1] with its configuration driven via
[Consul-Template][2].

## NOTE
This image currently uses a patched build of consul-template (included with this
repo) due to https://github.com/hashicorp/consul-template/pull/749. This fix has
been merged but not yet released. The included binary is `0.16.0` plus the fix.

## Environment Variables
Use `TELEGRAF_CONF_KEY` to set the key prefix where the telegraf configuration
will be found in Consul. If not set, `telegraf` will be used.

Also, you must set `CONSUL_HTTP_ADDR` in order for consul-template to render
any templates when the container runs. Any supported consul-template environment
variables can be used, such as:

- CONSUL_HTTP_ADDR
- CONSUL_HTTP_TOKEN
- CONSUL_HTTP_AUTH
- CONSUL_HTTP_SSL
- CONSUL_HTTP_SSL_VERIFY

## Supported Consul keys
- `<conf_key>/global_tags/*` - global tag key/value pairs
- `<conf_key>/agent/*` - any valid agent key/value pairs
- `<conf_key>/inputs/<input_type>/<input_name>/*` - telegraf input(s)*
- `<conf_key>/inputs/<output_type>/<output_name>/*` - telegraf outputs(s)*

The keys/values will be converted to a TOML telegraf config.

### Inputs/Output Configurations
Since telegraf inputs/outputs are actually arrays (can have multiple of each
type) and Consul K/Vs are a map, an (arbitrary) name is required for each
input/output for uniqueness and to "array-ify" them.

### Value Types
Since Consul basically stores everything as strings and values in the telegraf
TOML config may require strings, values, or arrays, Consul KV values are converted
as follows:

- any value matching `True`, `true`, `False`, `false` will be treated as Boolean
- any value that can be converted to float will be treated as numeric
- any value beginning with `[` and ending with `]` will be treated as an array
- any value matching `{}` will be treated as an empty map
- anything else will be string

## Example
The following example Consul keys/values:
```
KEY                                                  VALUE
telegraf/agent/omit_hostname                         true
telegraf/outputs/influxdb/1/urls                     ["http://1.1.1.1:8086"]
telegraf/inputs/mongodb/cluster1/servers             ["mongo1.example.com:27017"]
telegraf/inputs/mongodb/cluster1/gather_perdb_stats  true
telegraf/inputs/mongodb/cluster2/servers             ["1.2.3.4:27017"]
telegraf/inputs/mem/foo                              {}
```

Will generate the following effective telegraf.conf:
```
[agent]
omit_hostname = true

[[outputs.influxdb]]
urls = ["http://1.1.1.1:8086"]

[[inputs.mongodb]]
servers = ["mongo1.example.com:27017"]
gather_perdb_stats = true

[[inputs.mongodb]]
servers = ["1.2.3.4:27017"]

[[inputs.mem]] # empty - no config necessary
```

[1]: https://github.com/influxdata/telegraf
[2]: https://github.com/hashicorp/consul-template
