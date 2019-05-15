from .settings_base import *

DEBUG = False

if DEBUG:
    from .settings_local import *
else:
    from .settings_production import *


