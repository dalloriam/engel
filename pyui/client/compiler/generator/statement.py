import ast

from .expression import expression


def statement(node):
  if isinstance(node, ast.If):
    test = expression(node.test)
    body = ""
    for stt in node.body:
      body += statement(stt)

    # TODO: Fix this so that if cond: body elif cond: body compiles to if(cond){body}else if(cond){body} instead of if(cond){body}else{if(cond){body}}
    out = "if({0}) {{ {1} }}".format(test, body)

    if len(node.orelse) > 0:
      out += "else {{ {0} }}".format("".join(map(statement, node.orelse)))
    return out

  if isinstance(node, ast.Assign):
    return '\n'.join(map(lambda target: "{0} = {1};".format(expression(target), expression(node.value)), node.targets))

  # If all fails, check expression tree
  elif isinstance(node, ast.Expr):
    return expression(node.value) + ";"
