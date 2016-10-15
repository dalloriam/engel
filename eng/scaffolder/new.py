from eng.logging import error, info, success
from eng.utils import create_folder, render_app, render_view, write_file

import os

def new(options):
  if len(options) != 1:
    error("Invalid Syntax.")

  app_name = options[0]

  info("Generating {appName}...".format(appName=app_name))

  create_folder(app_name)

  app_abspath = os.path.abspath(app_name)
  write_file(os.path.join(app_abspath, 'app.py'), render_app(app_name))

  create_folder(os.path.join(app_abspath, 'views'))
  write_file(os.path.join(app_abspath, 'views', '__init__.py'), '')
  write_file(os.path.join(app_abspath, 'views', 'home.py'), render_view('home'))

  create_folder(os.path.join(app_abspath, 'services'))
  write_file(os.path.join(app_abspath, 'services', '__init__.py'), '')

  create_folder(os.path.join(app_abspath, 'public'))

