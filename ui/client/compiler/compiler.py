import ast
from ui.client.compiler.generator import generate
from ui.client.compiler.transformer.transformer import TreeTransformer


def to_javascript(code):
  print(code)
  print("")
  tree = TreeTransformer().visit(ast.parse(code))
  # print ast.dump(tree)
  out = generate(tree)
  print(out)
  return out
