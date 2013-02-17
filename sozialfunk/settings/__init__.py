import os

if 'DJANGO_ENVIRONMENT' in os.environ:
    if os.environ['DJANGO_ENVIRONMENT'] == 'development':
        from settings_development import *
    elif os.environ['DJANGO_ENVIRONMENT'] == 'production':
        from settings_production import *
    elif os.environ['DJANGO_ENVIRONMNET'] == 'test':
        pass
else:
    from settings_development import *