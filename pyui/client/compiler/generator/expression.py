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

  elif isinstance(node, ast.UnaryOp):
    return "{0}({1})".format(unary_operation(node.op), expression(node.operand))

  elif isinstance(node, ast.List):
    return "[{0}]".format(",".join(map(expression, node.elts)))

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
    # Handle Booleans TODO: Maybe check to add new node type in transform? Or Maybe True = 1 && False = 0?
    out = node.id
    if node.id == "True":
      out = "true"
    elif node.id == "False":
      out = "false"
    return "{1}{0}".format(out, context(node.ctx))


def unary_operation(node):

  if isinstance(node, ast.Not):
    return "!"
  elif isinstance(node, ast.USub):
    return "-"


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


def context(node):

  if isinstance(node, ast.Load):
    return ""

  elif isinstance(node, ast.Store):
    return "var "
