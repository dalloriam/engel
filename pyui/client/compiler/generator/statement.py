import ast

from .expression import expression


def statement(node):
  if isinstance(node, ast.If):
    test = expression(node.test)
    body = ""
    for stt in node.body:
      body += statement(stt)

    return "if({0}) {{ {1} }}".format(test, body)
    # TODO: Handle elif / else:

  if isinstance(node, ast.Assign):
    return '\n'.join(map(lambda target: "{0} = {1};".format(expression(target), expression(node.value)), node.targets))

  # If all fails, check expression tree
  elif isinstance(node, ast.Expr):
    return expression(node.value) + ";"
