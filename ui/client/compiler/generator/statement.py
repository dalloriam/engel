import ast

from expression import expression


def statement(node):
  if isinstance(node, ast.If):
    return "if({0}) {{ {1} }}".format(expression(node.test), ''.join(map(statement, node.body)))
    # TODO: Handle elif / else:

  if isinstance(node, ast.Assign):
    return '\n'.join(map(lambda target: "{0} = {1};".format(expression(target), expression(node.value)), node.targets))

  # If all fails, check expression tree
  elif isinstance(node, ast.expr):
    return expression(node)
