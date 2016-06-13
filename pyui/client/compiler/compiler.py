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

# TODO: Switch this to pure python if possible

def generate_event_handler(event_name, elem_id, func_name):
  return 'document.getElementById("{0}").addEventListener("{1}", {2});'.format(elem_id, event_name, func_name)

def generate_websocket_handler(event_name, elem_id, outFn=None):
  if outFn:
    return generate_event_handler(event_name, elem_id, 'function(){{ws.send(JSON.stringify({{event: "{EVT}", element_id: "{ID}", data: {FN}()}}))}}'.format(EVT=event_name, ID=elem_id, FN=outFn))
  else:
    return generate_event_handler(event_name, elem_id, 'function(){{ws.send(JSON.stringify({{event: "{EVT}", element_id: "{ID}" }}))}}'.format(EVT=event_name, ID=elem_id))
