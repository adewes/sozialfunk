import sozialfunk.settings as settings          #your project settings file
from django.core.management  import setup_environ     #environment setup function
import sys
setup_environ(settings)

import workers.tasks as tasks

if __name__ == '__main__':
    tasks.update_friends()