import os
import sys


class R(object):

    # Every app should define a "public/" directory for static resources. If public/ is not found in the cwd,
    # it is most likely because the application has been compiled & called from somewhere else. In that case we fallback
    # on sys.executable + '/public' and assume it is the correct directory.
    if os.path.isdir('public'):
        resource_folder = os.path.abspath('public')
    else:
        resource_folder = os.path.join(os.path.dirname(sys.executable), 'public')
        if not os.path.isdir(resource_folder):
            os.mkdir(resource_folder)

    def __init__(self, filename):
        self._filename = filename
        self.path = os.path.join(R.resource_folder, filename)

    def open(self, *args, **kwargs):
        return open(self.path, *args, **kwargs)
