import ast


class TreeTransformer(ast.NodeTransformer):

  def visit_Compare(self, node):
    """
    This changes conditions of the form if [val] in [iterable] => [iterable].indexOf(val) != 1
    as javascript does not support the form "[x] in [y]"
    """

    # BROKEN AGAIN, FIX PLEASE
    # TODO: fix this HACK: doesn't work if more thant one op or more than one comparator
    for op in node.ops:
      # TODO: Optimize this node transform
      if isinstance(op, ast.In):
        # Current structure: If(test=Compare(left=Str(s='3'), ops=[In()], comparators=[Name(id='my_arr', ctx=Load())]), body=[...])

        # Target structure: If(test=Compare(left=Call(func=Attribute(value=Name(id='my_arr', ctx=Load()), attr='indexOf', ctx=Load()), args=[Str(s='3')], keywords=[]),
        # ops=[NotEq()], comparators=[UnaryOp(op=USub(), operand=Num(n=1))]), body=[...])
        return ast.copy_location(ast.Compare(
            left=ast.Call(func=ast.Attribute(value=ast.Name(id=node.comparators[0].id, ctx=ast.Load()), attr="indexOf"), ctx=ast.Load(), args=[node.left], keywords=[]),
            ops=[ast.NotEq()],
            comparators=[ast.UnaryOp(op=ast.USub(), operand=ast.Num(n=1))]
        ), node)
      elif isinstance(op, ast.NotIn):
        return ast.copy_location(ast.Compare(
            left=ast.Call(func=ast.Attribute(value=ast.Name(id=node.comparators[0].id, ctx=ast.Load()), attr="indexOf"), ctx=ast.Load(), args=[node.left], keywords=[]),
            ops=[ast.Eq()],
            comparators=[ast.UnaryOp(op=ast.USub(), operand=ast.Num(n=1))]
        ), node)
    return node
