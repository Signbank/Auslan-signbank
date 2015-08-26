#!/usr/bin/env python
import os, sys

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

    # Determine if there are live settings (not commited to source control) and load that if it exists instead of the default settings
    code_path = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'signbank'))
    host_specific_settings = os.path.join(code_path, 'settings', 'live.py')
    if os.path.isfile(host_specific_settings):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "signbank.settings.live")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "signbank.settings.development")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
