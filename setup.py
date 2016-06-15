from distutils.core import setup

import os

def is_package(path):
  return (
    os.path.isdir(path) and
    os.path.isfile(os.path.join(path, '__init__.py'))
    )

def find_packages(path, base="" ):
  """ Find all packages in path """
  packages = {}
  for item in os.listdir(path):
    dir = os.path.join(path, item)
    if is_package( dir ):
      if base:
        module_name = "%(base)s.%(item)s" % vars()
      else:
        module_name = item
      packages[module_name] = dir
      packages.update(find_packages(dir, module_name))
  return packages


pkgs = find_packages("pyui/", "pyui")
setup(name='PyUI',
      version='0.1',
      description='Create Miraculous WebUIs in pure Python.',
      author='William Dussault',
      author_email='dalloriam@gmail.com',
      url='theuniverse.servebeer.com',
      package_dir=pkgs,
      packages=pkgs.keys()
)
