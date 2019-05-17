from .settings_base import *
from .site_settings import *
from .ejudge_settings import *

DEBUG = True

if DEBUG:
    from .settings_local import *
else:
    from .settings_production import *


