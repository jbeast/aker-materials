import os

ENVIRONMENT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'environment.py')
execfile(ENVIRONMENT_PATH)

material_type_schema = {
  'name': {
    'type': 'string',
    'required': True
  }
}

set_schema = {
  'definition': {
    'type': 'string'
  }
}

material_schema = {
  'material_type': {
    'type': 'objectid',
    'data_relation': {
      'resource': 'material_types',
      'field': '_id',
      'embeddable': True
    }
  },
  'supplier_name': {
    'type': 'string',
  },
  'donor_id': {
    'type': 'string',
  },
  'gender': {
    'type': 'string',
    'allowed': ['male', 'female', 'unknown'],
    'required': True
  },
  'common_name': {
    'type': 'string',
  },
  'phenotype': {
    'type': 'string',
  },
  'date_of_receipt': {
    'type': 'datetime',
  },
  'meta': {
    'type': 'dict',
    'allow_unknown': True,
  },
  'ancestors': {
    'type': 'list',
    'schema': {
      'type': 'objectid',
      'data_relation': {
        'resource': 'materials',
        'field': '_id',
        'embeddable': True
      }
    },
  },
  'parent': {
    'type': 'objectid'
  },
  'sets': {
    'type': 'list',
    'schema': {
      'type': 'objectid',
      'data_relation': {
        'resource': 'sets',
        'field': '_id',
        'embeddable': True
      }
    },
  },
}

material_types = {
  'schema': material_type_schema
}

materials = {
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'schema': material_schema
}

sets = {
  'schema': set_schema
}

set_materials = {
  "schema": material_schema,
  "url": "sets/<regex('[a-f0-9]{24}'):sets>/materials",
  "datasource": { "source": "materials" }
}

DOMAIN = {
  'materials': materials,
  'material_types': material_types,
  'sets': sets,
  'set_materials': set_materials
}