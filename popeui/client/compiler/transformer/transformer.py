import ast


class TreeTransformer(ast.NodeTransformer):

  def visit_NameConstant(self, node):
    """
    This changes the singleton value of NameConstant to a string value of a javascript constant (Ex: None => "null")
    """
    new_val = None
    if node.value is None:
      new_val = "null"
    elif node.value is True:
      new_val = "true"
    elif node.value is False:
      new_val = "false"

    return ast.copy_location(ast.NameConstant(
        value=new_val
    ), node)

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
            left=ast.Call(func=ast.Attribute(value=node.comparators[0], attr="indexOf"), ctx=ast.Load(), args=[node.left], keywords=[]),
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
