import ast


class TreeTransformer(ast.NodeTransformer):

  def visit_Compare(self, node):
    """
    This changes conditions of the form if [val] not in [iterable] => not([val] in [iterable])
    as javascript does not support the form x not in y
    """

    # Broken atm. Gotta move "x in y" to "y.indexOf(x) != -1" and "x not in y" to "y.indexOf(x) == -1"
    for op in node.ops:
      if isinstance(op, ast.In):
        return ast.copy_location(ast.Compare(
            left=ast.Num(n=-1),
            ops=[ast.Eq()],
            comparators=[]
        ), node)
    return node
