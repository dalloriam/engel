import ast


def code_generator(node):

  # Top level module, contains expressions / statements
  if isinstance(node, ast.Module):
    return "".join(map(code_generator, ast.iter_child_nodes(node)))

  # Condition generation
  if isinstance(node, ast.If):
    return "if({0}) {{ {1} }}".format(code_generator(node.test), ''.join(map(code_generator, node.body)))

  if isinstance(node, ast.Compare):
    # for k, v in ast.iter_fields(node):
    #   print(k + ": " + str(v))
    ops = ''.join(map(code_generator, node.ops))
    comparators = ''.join(map(code_generator, node.comparators))
    return "{0} {1} {2}".format(code_generator(node.left), ops, comparators)

  # Expression condition generation
  if isinstance(node, ast.Expr):
    return code_generator(node.value)

  if isinstance(node, ast.Eq):
    return "=="

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


def to_javascript(code):
  tree = ast.parse(code)
  out = code_generator(tree)
  print out
  return out
