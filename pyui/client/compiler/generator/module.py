import ast
from .expression import expression
from .statement import statement


def module(node):
  body = ""
  for child in node.body:
    if isinstance(child, ast.expr):
      body += expression(child)

    elif isinstance(child, ast.stmt):
      body += statement(child)
    body += "\n"
  return body
