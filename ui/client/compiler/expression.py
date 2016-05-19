import ast


def parse_expression(node):

  if isinstance(node, ast.Attribute):
    return parse_expression(node.value) + "." + node.attr


def parse_base_types(node):

  if isinstance(node, ast.Str):
    return "{0}".format(node.s)

  elif isinstance(node, ast.Num):
    return str(node.n)

  elif isinstance(node, ast.Name):
    # TODO: Add tree transformer to remove logic from code generator
    if parse_context(node.ctx) == "store":
      return "var {0}".format(node.id)
    else:
      return node.id


def parse_context(node):

  if isinstance(node, ast.Load):
    return "load"

  elif isinstance(node, ast.Store):
    return "store"

  elif isinstance(node, ast.Del):
    return "del"
