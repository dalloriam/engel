import sys
sys.path.append('../popeui')

from popeui.client.compiler.compiler import to_javascript
from popeui.application.base import client


def test_compile_strings():
  assert to_javascript('""') == '"";'
  assert to_javascript('"hello"') == '"hello";'


def test_compile_integers():
  assert to_javascript("12") == "12;"


def test_compile_bools():
  assert to_javascript("True") == "true;"
  assert to_javascript("False") == "false;"


def test_compile_null():
  assert to_javascript("None") == "null;"


def test_compile_variable_definition():
  assert to_javascript("x = 2") == "var x = 2;"


def test_compile_basic_math_operations():
  assert to_javascript("1 + 1") == "1 + 1;"
  assert to_javascript("1 - 1") == "1 - 1;"
  assert to_javascript("1 * 2") == "1 * 2;"
  assert to_javascript("1/2") == "1 / 2;"
  assert to_javascript("7 * (3 + 5)") == "7 * (3 + 5);"


def test_compile_lists():
  assert to_javascript("mylist = [1, 2, 3]\nmyvar = mylist[0]") == "var mylist = [1,2,3];var myvar = mylist[0];"


def test_compile_comparisons():
  assert to_javascript("1 == 2") == "1 == 2;"
  assert to_javascript("1 != 2") == "1 != 2;"
  assert to_javascript("1 > 2") == "1 > 2;"
  assert to_javascript("1 < 2") == "1 < 2;"
  assert to_javascript("1 >= 2") == "1 >= 2;"
  assert to_javascript("1 <= 2") == "1 <= 2;"

  assert to_javascript("1 is 2") == "1 === 2;"
  assert to_javascript("1 is not 2") == "1 !== 2;"


def test_compile_conditional_statements():
  assert to_javascript("if 1 == 2:\n  1+1") == "if(1 == 2) { 1 + 1; }"
  assert to_javascript("if 1 == 2:\n  1+1\nelse:\n  1+2") == "if(1 == 2) { 1 + 1; }else { 1 + 2; }"
  assert to_javascript("if 1 == 2:\n  1+1\nelif 2 == 2:\n  1 + 3\nelse:\n  1 + 2") == "if(1 == 2) { 1 + 1; }else { if(2 == 2) { 1 + 3; }else { 1 + 2; } }"


def test_compile_function_call():
  assert to_javascript("MyFunction()") == "MyFunction();"


def test_compile_unary_operator():
  assert to_javascript("x = -1") == "var x = -(1);"


def test_compile_redefine_variable():
  assert to_javascript("x = 1\nx=3") == "var x = 1;var x = 3;"


@client
def MyFunction1():
  y = 1 + 1
  x = 2 + 1


@client
def MyFunction2(a):
  y = a * 2


@client
def MyFunction3(a, b):
  y = a * b


@client
def MyFunction4(a, b):
  return a + b


def test_compile_function_define():
  assert to_javascript(MyFunction1()) == "function MyFunction1(){ var y = 1 + 1;var x = 2 + 1; }"
  assert to_javascript(MyFunction2()) == "function MyFunction2(a){ var y = a * 2; }"
  assert to_javascript(MyFunction3()) == "function MyFunction3(a,b){ var y = a * b; }"
  assert to_javascript(MyFunction4()) == "function MyFunction4(a,b){ return a + b; }"


def test_compile_value_in_array():
  assert to_javascript("1 in [1, 2, 3]") == "[1,2,3].indexOf(1) != -(1);"
