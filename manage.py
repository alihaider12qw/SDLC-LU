#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "django_toosimple_q.tests.settings")

#    # region debugging
#    from django.conf import settings
#    print('Not Attached!')
#    if settings.DEBUG:
#        if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
#            import debugpy
#            debugpy.listen(("0.0.0.0", 3000))
#            debugpy.wait_for_client()
#            print('Attached!')
#    # endregion debugging

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
