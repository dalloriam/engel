import ast


def expression(node):

  if isinstance(node, ast.Attribute):
    return expression(node.value) + "." + node.attr

  elif isinstance(node, ast.Subscript):
    fields = []
    for k, v in ast.iter_fields(node):
      fields.append(k)

    return_val = expression(node.value)

    if "slice" in fields:
      return_val += slice(node.slice)
    return return_val

  elif isinstance(node, ast.Compare):
    ops = ''.join(map(comparison_operator, node.ops))
    comparators = ''.join(map(expression, node.comparators))
    return "{0} {1} {2}".format(expression(node.left), ops, comparators)

  elif isinstance(node, ast.Call):
    # TODO: Handle keywords (maybe)
    return "{0}({1})".format(expression(node.func), ','.join(map(expression, node.args)))

  else:
    return base_types(node)


def slice(node):

  if isinstance(node, ast.Index):
    return "[{0}]".format(expression(node.value))


def base_types(node):

  if isinstance(node, ast.Str):
    return '"{0}"'.format(node.s)

  elif isinstance(node, ast.Num):
    return str(node.n)

  elif isinstance(node, ast.Name):
    # TODO: Add tree transformer to remove logic from code generator
    if context(node.ctx) == "store":
      return "var {0}".format(node.id)
    else:
      return node.id


def comparison_operator(node):

  if isinstance(node, ast.Eq):
    return "=="

  elif isinstance(node, ast.NotEq):
    return "!="

  elif isinstance(node, ast.Lt):
    return "<"

  elif isinstance(node, ast.LtE):
    return "<="

  elif isinstance(node, ast.Gt):
    return ">"

  elif isinstance(node, ast.GtE):
    return ">="

  elif isinstance(node, ast.Is):
    return "==="

  elif isinstance(node, ast.IsNot):
    return "!=="

  elif isinstance(node, ast.In):
    return "in"

  elif isinstance(node, ast.NotIn):
    # TODO: Tree Transformation: [val] not in [iterable] => !([val] in [iterable])
    return None


def context(node):

  if isinstance(node, ast.Load):
    return "load"

  elif isinstance(node, ast.Store):
    return "store"

  elif isinstance(node, ast.Del):
    return "del"
