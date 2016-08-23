import sys
sys.path.append('../popeui')

from popeui.widgets import *


# ABSTRACT WIDGETS
def test_widget_headlink():
  hlink1 = HeadLink(id="h", link_type="stylesheet", path="application.css")
  o = hlink1.compile()

  assert "<link" in o
  assert 'rel="stylesheet"' in o
  assert 'href="application.css"' in o
  assert 'id="h"' in o
  assert '">' in o


def test_widget_pagetitle():
  title = PageTitle(id="h", text="title", classname="classy")
  assert title.id == "h"
  assert title._classes == ["classy"]
  assert title.content == "title"
  o = title.compile()
  assert ">title<" in o


def test_widget_script():
  scr = Script(id="scr", js_path="/Users/wduss/test.js")
  assert scr.source == "/Users/wduss/test.js"


# FORMS WIDGETS
def test_widget_button():
  btn = Button(id="btnTest", text="test")
  assert btn.content == "test"


def test_widget_textbox():
  txt1 = TextBox(id="txtTest")
  assert "name" not in txt1._attributes

  txt2 = TextBox(id="txtTest", name="name")
  assert "name" in txt2._attributes
  assert txt2.name == 'name'


# MEDIA WIDGETS
def test_widget_image():
  img = Image(id="img", img_url="http://www.google.ca")
  assert img.html_tag == "img"
  assert img.source == "http://www.google.ca"


def test_widget_video():
  vid = Video(id="myvid", vid_url="hello")
  assert vid.source == "hello"
  assert vid.loop == "true"


def test_widget_imagelink():
  imgl = ImageLink(id="yao", link="http://www.google.ca", img_url="http://wikipedia.org")
  assert imgl.html_tag == "a"

  assert imgl.target == "http://www.google.ca"

  assert len(imgl.children) == 1
  assert isinstance(imgl.children[0], Image)


def test_widget_audio():
  aud = Audio(id="aud", audio_path="test.mp3")
  assert aud.source == "test.mp3"


# STRUCTURE WIDGETS
def test_widget_document():
  doc = Document(id="doc", view=None)
  assert doc.html_tag == "html"


def test_widget_head():
  hd = Head(id="hd")
  assert hd.html_tag == "head"


def test_widget_body():
  bd = Body(id="bd")
  assert bd.html_tag == "body"


def test_widget_panel():
  pnl = Panel(id="pnl")
  assert pnl.html_tag == "div"


def test_widget_list():
  ls = List(id="ls")
  assert ls.html_tag == "ul"
  assert ls._count == 0

  itm = Image(id="yao", img_url="k")
  ls.append(itm)
  assert ls._count == 1
  assert len(ls.children) == 1
  assert len(ls.children[0].children) == 1
  assert isinstance(ls.children[0].children[0], Image)


def test_widget_list_item_remove():
  ls = List(id="ls")
  itm = Image(id="yao", img_url="k")
  ls.append(itm)
  assert len(ls._items) == 1
  ls.remove(itm)
  assert len(ls.children) == 0
  assert len(ls._items) == 0


def test_widget_list_item_indexer():
  ls = List(id="ls")
  itm = Image(id="yao", img_url="k")
  ls.append(itm)
  assert ls[0] is itm


def test_widget_list_item_setter():
  ls = List(id="ls")
  itm = Image(id="yao", img_url="k")
  itm2 = Panel(id="panel")
  ls.append(itm)
  assert ls[0] is itm
  ls[0] = itm2
  assert ls[0] is itm2


def test_widget_list_item_length():
  ls = List(id="ls")
  assert len(ls) == 0
  itm = Image(id="yao", img_url="k")
  ls.append(itm)
  assert len(ls) == 1
  ls.remove(itm)
  assert len(ls) == 0


def test_widget_inheritance():
  pnl = Panel(id="panel")
  assert len(pnl.children) == 0
  Image(id="yao", img_url="k", parent=pnl)
  assert len(pnl.children) == 1
  assert isinstance(pnl.children[0], Image)


# TEXT WIDGETS
def test_widget_title():
  t = Title(id="titl", text="Text")
  assert t.size == 1
  assert t._get_html_tag() == "h1"
  assert t.content == "Text"

  t2 = Title(id="titl", text="Text", size=3)
  assert t2.size == 3
  assert t2._get_html_tag() == "h3"


def test_widget_paragraph():
  p = Paragraph(id="p", text="yao")
  assert p.html_tag == "p"
  assert p.content == "yao"


def test_widget_span():
  s = Span(id="s", text="spans")
  assert s.html_tag == "span"
  assert s.content == "spans"


def test_widget_textlink():
  t = TextLink(id="id", text="abcd", url="http://www.google.ca")
  assert t.html_tag == "a"
  assert t.content == "abcd"
  assert "href" in t._attributes
  assert t.target == "http://www.google.ca"
