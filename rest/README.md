# Some notes about the REST API server

TODO: change node list structure to something more tree-ish.


## A directory tree like this

    .
    ├── A
    │   ├── B
    │   └── C
    ├── H
    │   ├── I
    │   │   ├── 1
    │   │   └── 2
    │   ├── J
    │   └── K
    ├── X
    ├── Y
    └── Z


## would become:

    {
        'A': {
            'B': {},
            'C': {}
        },
        'H': {
            'I': {
                '1': {},
                '2': {}
            },
            'J': {},
            'K': {}
        }
        'X': {},    <= carpeta vacia
        'Y': null,  <= nodo
        'Z': null
    }


see: http://stackoverflow.com/questions/25226208/represent-directory-tree-as-json


## or like this


{'children': [{'children': [{'name': 'FC1413C35FDF76F7CFF5362BA0BA40D3',
                             'type': 'file'},
                            {'name': 'ECE8F89BCCD4BBB7310662D259519053',
                             'type': 'file'}],
               'name': 'DF05F55D8D16AE431394E37E95D0EF00',
               'type': 'directory'},
              {'children': [{'name': '4B1F3F08CEF4ABA16A3FA98D95F0C2A8',
                             'type': 'file'},
                            {'name': '7E580AAB8D48D6EF88888B72FFD41B82',
                             'type': 'file'}],
               'name': '8D09C3CF58C45456B04A4F44F182EBD4',
               'type': 'directory'},
              {'name': '587E18CEEAC240540CA1E4AED488C716', 'type': 'file'},
              {'children': [{'name': 'mappings.json', 'type': 'file'},
                            {'name': 'recipients', 'type': 'file'}],
               'name': '.auth',
               'type': 'directory'},
              {'name': 'C0E64C2D3E7E920EF9E9C3B804914358', 'type': 'file'}],
 'name': '.',
 'type': 'directory'}

