'''
Config File
'''

from os import environ

SETTINGS = {
    'api':{
        'port': environ.get('API_PORT'),
        'host': environ.get('API_HOST'),
        'debug': True if environ.get('ENVIRONMENT') != 'production' else False
    },
    'sql': {
        'connections': {
            'host': environ.get('AWS_RDS_HOST'),
            'port': int(environ.get('AWS_RDS_PORT')),
            'user': environ.get('AWS_RDS_USER'),
            'password': environ.get('AWS_RDS_PASSWORD'),
            'database': environ.get('AWS_RDS_DATABASE_NAME')
        },
        'tables': {
            'users': 'users',
            'documents': 'documents',
            'annotations': 'annotations',
            'named_entities': 'named_entities',
        },
    },
    'location_lookup_url':environ.get('LOCATION_LOOKUP_URL'),
    'log_level':environ.get('LOG_LEVEL'),
    'enable_console_logging':environ.get('LOG_ENABLE_CONSOLE'),
}
