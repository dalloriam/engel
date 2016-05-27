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

  if isinstance(node, ast.FunctionDef):
    return "function {0}({2}){{ {1} }}".format(node.name, "\n".join(map(statement, node.body)), arguments(node.args))

  # If all fails, check expression tree
  elif isinstance(node, ast.Expr):
    return expression(node.value) + ";"


def arguments(node):

  return ",".join([x.arg for x in node.args])
