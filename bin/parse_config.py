#!/usr/bin/env python

from __future__ import print_function
import json
import sys
import ast


def return_error(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def is_num(val):
    if val is True or val is False:
        return False
    try:
        float(val)
        return True
    except ValueError:
        return False


def convert_dict(d):
    if not isinstance(d, dict):
        error_out("{} not a map".format(d))
    for k, v in d.iteritems():
        if isinstance(v, dict):
            v = convert_dict(v)
        elif v.startswith('[') and v.endswith(']'):
            # treat as literal list
            d[k] = ast.literal_eval(v)
        elif v == '{}':
            # treat as empty dict
            d[k] = ast.literal_eval(v)
        elif is_num(v):
            # treat as numeric
            d[k] = ast.literal_eval(v)
        elif v in ['true', 'True']:
            d[k] = True
        elif v in ['false', 'False']:
            d[k] = False
    return d


if len(sys.argv) > 3:
    return_error("wrong number of arguments; 1 or 2 expected but {} given"
                 .format(len(sys.argv)))

data = json.loads(sys.argv[-1])
config = {'inputs': {}, 'outputs': {}}

if 'global_tags' in data:
    # expects global_tags/<config_map>
    config['global_tags'] = convert_dict(data['global_tags'])
if 'agent' in data:
    # expects agent/<config_map>
    config['agent'] = convert_dict(data['agent'])

if 'inputs' in data:
    # expects inputs/<in_type>/<in_name>/<config_map> where in_name is arbitrary
    for in_type, in_map in data['inputs'].iteritems():
        for in_name, in_config in in_map.iteritems():
            if not isinstance(in_config, dict):
                return_error("inputs[{}][{}] not a map".format(in_type, in_name))
            config['inputs'].setdefault(in_type, []).append(convert_dict(in_config))
if 'outputs' in data:
    # expects outputs/<out_type>/<out_name>/<config_map> where out_name is arbitrary
    for out_type, out_map in data['outputs'].iteritems():
        for out_name, out_config in out_map.iteritems():
            if not isinstance(out_config, dict):
                return_error("outputs[{}][{}] not a map".format(out_type, out_name))
            config['outputs'].setdefault(out_type, []).append(convert_dict(out_config))

if len(sys.argv) == 2:
    print(json.dumps(config))
elif sys.argv[1] == 'pretty':
    print(json.dumps(config, sort_keys=True, indent=2))
# elif sys.argv[1] == 'toml':
#     import toml
#     print(toml.dumps(config))
