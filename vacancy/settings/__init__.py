from .base import *

from .production import *

try:
    from .local import *
except:
    print('Some problem with local.py')
    pass
