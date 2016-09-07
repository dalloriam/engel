import os
import sys
import shutil
import platform
import subprocess

IS_WINDOWS = platform.system() == "Windows"


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


def build(target, templates):
  app_name = input("Application name: ")
  author = input("Author: ")
  subprocess.call(['pyinstaller', '--onefile', target])

  build_path = os.path.join('build', app_name) if not os.path.isdir(os.path.join('build', app_name)) else os.path.join('build', app_name + '_2')
  distpath = os.path.abspath(os.path.join(os.getcwd(), 'dist'))

  os.mkdir(build_path)
  if IS_WINDOWS:
    shutil.move(os.path.join(distpath, target.replace('.py', '.exe')), os.path.join(build_path, 'engelapp.exe'))
  else:
    shutil.move(os.path.join(distpath, target.replace('.py', '')), os.path.join(build_path, 'engelapp'))

  shutil.copytree('public', os.path.join(build_path, 'public'))

  os.chdir(build_path)

  package = read_file(os.path.join(templates, 'package.template')).format(app_name, author)

  path = os.path.dirname(os.path.realpath(__file__))
  path = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), 'engel')

  index_js = os.path.join(templates, 'index.template')
  shutil.copy(index_js, 'index.js')

  html_file = os.path.join(path, 'index.html')
  shutil.copy(html_file, 'index.html')

  js_file = os.path.join(path, 'engeljs.js')
  shutil.copy(js_file, 'engeljs.js')

  with open('package.json', 'a') as outfile:
    outfile.write(package)

  subprocess.call(['npm', 'install'], shell=IS_WINDOWS)
  subprocess.call(['npm', 'install', 'electron-packager'], shell=IS_WINDOWS)
  subprocess.call(['node', os.path.join('node_modules', 'electron-packager', 'cli.js'), '.', app_name], env={'PATH': os.getenv('PATH')})

  for file in os.listdir('.'):
    if os.path.isdir(file) and file.startswith(app_name + '-'):
      shutil.move(file, os.path.join(distpath, file))


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
    elif 'build'.startswith(action):
      return build(target, templates)

  return "Invalid Syntax"
