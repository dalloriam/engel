import ast
from .generator import generate
from .transformer.transformer import TreeTransformer


def to_javascript(code):
  raw_tree = ast.parse(code)
  print(ast.dump(raw_tree))
  tree = TreeTransformer().visit(raw_tree)
  # print("")
  # print("")
  # print(ast.dump(tree))

  out = generate(tree)

  print("PYTHON\n======\n")
  print(code)
  print("\nJAVSCRIPT\n==========\n")
  print(out)

  return out
