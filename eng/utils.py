import os

from eng.logging import error, success, info

def create_folder(folder_path):
  if os.path.isdir(folder_path):
    error("Directory {dirName} already exists.".format(dirName=os.path.abspath(folder_path)))
  os.mkdir(folder_path)
  success(os.path.abspath(folder_path) + "/")

def write_file(file_path, content):
  if os.path.isdir(file_path):
    error("File {filePath} already exists.").format(filePath=os.path.abspath(file_path))

  with open(file_path, "a") as outfile:
    outfile.write(content)
  success(os.path.abspath(file_path))

def read_template(template):
  template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
  filename = template + ".template"

  template_file = os.path.join(template_dir, filename)

  if not os.path.isfile(template_file):
    error("Unknown template file ({tmpl}).".format(tmpl=filename))

  data = None
  with open(template_file, "rU") as infile:
    data = infile.read()
  return data

def render_app(app_name):
  src = read_template("app")
  ccName = app_name.replace('_', ' ').title().replace(' ', '')
  return src.format(appCamelCase=ccName)

def render_view(view_name):
  src = read_template("view")
  view_title = view_name.replace('_', ' ').title().replace(' ', '')
  view_camel = view_title + 'View'
  return src.format(viewCamelCase=view_camel, viewTitle=view_title)

def render_service(service_name):
  src = read_template("service")
  svc_camel = service_name.replace('_', ' ').title().replace(' ', '') + 'Service'
  return src.format(serviceCamelCase=svc_camel)
