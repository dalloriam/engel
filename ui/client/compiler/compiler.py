import ast


def code_generator(node):
  # Top level module, contains expressions / statements
  if isinstance(node, ast.Module):
    return "\n".join(map(code_generator, ast.iter_child_nodes(node)))

  # Assignment operator
  elif isinstance(node, ast.Assign):
    return '\n'.join(map(lambda target: "{0} = {1};".format(code_generator(target), code_generator(node.value)), node.targets))

  # Subscript
  elif isinstance(node, ast.Subscript):
    fields = []
    for k, v in ast.iter_fields(node):
      fields.append(k)

    return_val = code_generator(node.value)
    if "slice" in fields:
      return_val += code_generator(node.slice)
    return return_val

  elif isinstance(node, ast.Index):
    return "[{0}]".format(code_generator(node.value))

  elif isinstance(node, ast.Num):
    return str(node.n)

  # Function Call
  elif isinstance(node, ast.Call):
    return "{0}({1})".format(code_generator(node.func), ','.join(map(code_generator, node.args)))

  # Attribute
  elif isinstance(node, ast.Attribute):
    return code_generator(node.value) + "." + node.attr

  # String
  elif isinstance(node, ast.Str):
    return '"{0}"'.format(node.s)

  # Variable name
  elif isinstance(node, ast.Name):
    if code_generator(node.ctx) == "store":
      return "var {0}".format(node.id)
    else:
      return node.id

  elif isinstance(node, ast.Store):
    return "store"

  elif isinstance(node, ast.Load):
    return "load"


def to_javascript(code):
  tree = ast.parse(code)

  print ""
  print code
  print ""
  print "Compiling..."
  print ""
  return code_generator(tree)
