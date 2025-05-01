#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
from sina.model import Record
import json

# This record could have come back from a data store as well.
record_1 = Record(
    'some_id', 'run',
    data={
        'energy': {
            'value': 123.456,
            'units': 'J',
            'tags': ['output', 'main'],
        },
        'temperature': {
            'value': 987.6,
            'units': 'K',
            'tags': ['output', 'main'],
        }
    },
)


print(json.dumps(record_1.data, indent=4))


energy_data = record_1.data['energy']
print('energy_data is just a Python dictionary:', type(energy_data))
print('Energy is ', energy_data['value'], energy_data['units'])
print('Energy is tagged with', energy_data['tags'])

energy_data['value'] = 15
print('The energy has been updated in the original record:', record_1.data['energy']['value'])


print('Energy is', record_1.data_values.energy)
print('Can also access with subscript operator:', record_1.data_values['energy'])


record_1.data_values.energy = 20
print('Energy has been updated, leaving tags and units alone ', record_1.data['energy'])


record_1.data_values.my_new_value = 100
print('Units and tags for new items are not set:', record_1.data['my_new_value'])


record_2 = Record(
    'some_id', 'run',
    curve_sets={
        'cs1': {
            'independent': {
                'time': {
                    'value': [0.1, 0.2, 0.3, 0.4, 0.5]
                }
            },
            'dependent': {
                'energy': {
                    'value': [12.34, 56.78, 90.12, 34.56],
                    'units': 'J'
                },
                'temperature': {
                    'value': [50, 60, 70, 65, 30],
                    'units': 'K'
                }
            }
        }
    },
)


print('The full curve set is a python dictionary:', record_2.curve_sets['cs1'])
print('Time values are', record_2.curve_sets['cs1']['independent']['time']['value'])


record_2.curve_set_values.cs1.time
record_2.curve_set_values.cs1.independent.time
record_2.curve_set_values['cs1']['time']
record_2.curve_set_values['cs1'].independent['time']

record_2.curve_set_values.cs1.energy


record_2.curve_set_values.cs1.dependent.new_entry = [-1, -2, -3, -4, -5]
print(record_2.curve_sets['cs1']['dependent']['new_entry'])


record_3 = Record(
    'some_id', 'run',
    library_data={
        'my_library': {
            'data': {
                'helium_volume': {
                    'value': 12.34
                },
                'hydrogen_volume': {
                    'value': 56.78
                }
            },
            'curve_sets': {
                'cs1': {
                    'independent': {
                        'time': {
                            'value': [0.1, 0.2, 0.3, 0.4, 0.5]
                        }
                    },
                    'dependent': {
                        'energy': {
                            'value': [12.34, 56.78, 90.12, 34.56],
                            'units': 'J'
                        },
                        'temperature': {
                            'value': [50, 60, 70, 65, 30],
                            'units': 'K'
                        }
                    }
                }
            },
            'library_data': {
                'my_nested_library': {
                    'data': {
                        'max_iterations': {
                            'value': 200
                        }
                    }
                }
            }
        }
    }
)


print('Helium occupies a volume of',
      record_3.library_data['my_library']['data']['helium_volume']['value'])
print('It is easier to access values through "library_data_values"',
      record_3.library_data_values.my_library.data.hydrogen_volume)


record_3.library_data_values.my_library.data.new_entry = 10


record_3.library_data_values.my_library.curve_sets.cs1.temperature


record_3.library_data_values.my_library.library_data.my_nested_library.data.max_iterations

