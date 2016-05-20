import ast
from generator import generate
from transformer.transformer import TreeTransformer


def to_javascript(code):
  tree = TreeTransformer().visit(ast.parse(code))
  print ast.dump(tree)
  out = generate(tree)
  print out
  return out
