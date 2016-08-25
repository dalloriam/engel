import os
import sys


def read_file(filename):
  data = None
  with open(filename, 'rU') as infile:
    data = infile.read()
  return data


def generate_view(name, templates):
  base_view = read_file(templates + '/view.template')

  if not os.path.isfile('views/__init__.py'):
    open('views/__init__.py', 'a').close()

  with open('views/{0}.py'.format(name).lower(), 'a') as outfile:
    outfile.write(base_view.format(name + 'View'))
  return 'ok'


def generate_service(name, templates):
  base_service = read_file(templates + '/service.template')

  if not os.path.isfile('services/__init__.py'):
    open('services/__init__.py', 'a').close()

  with open('services/{0}.py'.format(name).lower(), 'a') as outfile:
    outfile.write(base_service.format(name + 'Service'))
  return 'ok'


def generate_app(name, templates):
  if os.path.isdir(name):
    return "Directory {0} exists. Aborting...".format(os.path.abspath(name))

  base_app = read_file(templates + '/app.template')

  os.mkdir(name)
  os.mkdir(name + '/views')
  os.mkdir(name + '/services')

  with open(name + '/app.py', 'a') as outfile:
    outfile.write(base_app.format(name))

  os.chdir(name)
  print(generate_view('Home', templates))
  print(generate_service('Home', templates))
  os.chdir('..')


def main():
  templates = os.path.abspath(os.path.dirname(__file__)) + '/templates'
  if not os.path.isdir(templates):
    return "ERROR: Template directory does not exist..."

  args = sys.argv
  if len(args) >= 3:
    action = args[1]
    target = args[2]

    if 'new'.startswith(action):
      return generate_app(target, templates)
    elif 'generate'.startswith(action) and len(args) == 4:
      name = args[3]
      if 'view'.startswith(name):
        return generate_view(name, templates)
      elif 'service'.startswith(name):
        return generate_service(name, templates)

  return "Invalid Syntax"
