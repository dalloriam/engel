import ast


class TreeTransformer(ast.NodeTransformer):

  def visit_Compare(self, node):
    """
    This changes conditions of the form if [val] not in [iterable] => not([val] in [iterable])
    as javascript does not support the form x not in y
    """

    # TODO: in javascript "in" only works for int arrays for some reason.
    # optimize this so it either converts all "in" calls to iterable.indexOf([val]) !=-1
    # OR (better) so it converts only non-int iterables to iterable.indexOf([val]) != -1
    for op in node.ops:
      if isinstance(op, ast.NotIn):
        return ast.copy_location(ast.UnaryOp(
            op=ast.Not(),
            operand=ast.Compare(
                left=node.left,
                ops=[ast.In()],
                comparators=node.comparators
            )
        ), node)
    return node
