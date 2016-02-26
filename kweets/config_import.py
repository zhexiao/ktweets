import os

try:
    # kt_environment = os.environ['KT_ENV']
    kt_environment = 'development'
    if str(kt_environment) in 'development testing':
        from .config_dev import *
    elif str(kt_environment) in 'staging production':
        from .config_production import *
except KeyError:
    raise KeyError('Enviroment Variable `KT_ENV` not set')
