import ast
from generator import generate


def to_javascript(code):
  tree = ast.parse(code)
  out = generate(tree)
  print out
  return out
