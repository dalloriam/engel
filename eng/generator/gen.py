from eng.logging import error
from eng.utils import render_view, write_file, render_service

import os


def make_view(view_name):
    if not os.path.isdir('views'):
        error("eng generate must be called from the root directory of an engel application.")

    write_file(os.path.join(os.path.abspath('views'), view_name + '.py'), render_view(view_name))


def make_service(svc):
    if not os.path.isdir('services'):
        error("eng generate must be called from the root directory of an engel application.")

    write_file(os.path.join(os.path.abspath('services'), svc + '.py'), render_service(svc))


valid_options = {'view': make_view, 'service': make_service}


def generate(options):

    if len(options) != 2:
        error("Invalid Syntax.")

    target = options[0]
    name = options[1]

    for key in valid_options:
        if key == target or target == key[0]:
            valid_options[key](name)
            return

    error("Invalid Operation.")
