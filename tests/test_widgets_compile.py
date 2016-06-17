import sys
sys.path.append('../pyui')

from pyui.widgets.abstract import *
from pyui.widgets.forms import *
from pyui.widgets.media import *
from pyui.widgets.structure import *
from pyui.widgets.text import *

# ABSTRACT WIDGETS

def test_viewlink():
  view_link1 = ViewLink(id="hello", view_name="test")
  view_link2 = ViewLink(id="hello", view_name="test", params={"id": 3})

  v1 = view_link1.compile()
  v2 = view_link2.compile()

  assert v1 == '<a href="test" id="hello"></a>' or v1 == '<a id="hello" href="test"></a>'
  assert v2 == '<a href="test?id=3" id="hello"></a>' or v2 == '<a id="hello" href="test?id=3"></a>'

def test_headlink():
  hlink1 = HeadLink(id="h", link_type="stylesheet", path="application.css")
  o = hlink1.compile()

  assert "<link" in o
  assert 'rel="stylesheet"' in o
  assert 'href="application.css"' in o
  assert 'id="h"' in o
  assert '">' in o

def test_pagetitle():
  title = PageTitle(id="h", text="title", classname="classy")
  assert title.attributes["id"] == "h"
  assert title.attributes["class"] == "classy"
  assert title.content == "title"
  o = title.compile()
  assert ">title<" in o

def test_script():
  scr = Script(id="scr", js="console.log('test');")
  assert scr.content == "console.log('test');"


# FORMS WIDGETS
def test_button():
  btn = Button(id="btnTest", text="test")
  assert btn.content == "test"

def test_textbox():
  txt1 = TextBox(id="txtTest")
  assert not "name" in txt1.attributes

  txt2 = TextBox(id="txtTest", name="name")
  assert "name" in txt2.attributes

  assert "change" in txt2.socket_events
  assert "txtTest" in txt2.socket_events["change"]
  assert txt2.socket_events["change"]["txtTest"] == txt2._set_text
  assert txt2.server_events == ['document.getElementById("txtTest").addEventListener("change", function(){ws.send(JSON.stringify({event: "change", element_id: "txtTest", data: function(){return document.getElementById("txtTest").value;}()}))});']



# MEDIA WIDGETS
def test_image():
  img = Image(id="img", img_url="http://www.google.ca")
  assert img.html_tag == "img"
  assert img.attributes["src"] == "http://www.google.ca"

def test_video():
  vid = Video(id="myvid", vid_url="hello")
  assert vid.attributes["src"] == "hello"
  assert vid.attributes["loop"] == "true"

def test_imagelink():
  imgl = ImageLink(id="yao", link="http://www.google.ca", img_url="http://wikipedia.org")
  assert imgl.html_tag == "a"

  assert imgl.attributes["href"] == "http://www.google.ca"

  assert len(imgl.children) == 1
  assert isinstance(imgl.children[0], Image)

def test_audio():
  aud = Audio(id="aud", audio_path="test.mp3")
  assert aud.attributes["src"] == "test.mp3"

def test_viewimagelink():
  vil = ViewImageLink(id="vil", img_url="test.jpg", view_name="Alo")
  assert len(vil.children) == 1
  assert isinstance(vil.children[0], Image)

def test_viewvideolink():
  vil = ViewVideoLink(id="vil", vid_url="test.mp4", view_name="Alo")
  assert len(vil.children) == 1
  assert isinstance(vil.children[0], Video)


# STRUCTURE WIDGETS
def test_document():
  doc = Document(id="doc")
  assert doc.html_tag == "html"

def test_head():
  hd = Head(id="hd")
  assert hd.html_tag == "head"

def test_body():
  bd = Body(id="bd")
  assert bd.html_tag == "body"

def test_panel():
  pnl = Panel(id="pnl")
  assert pnl.html_tag == "div"

def test_list():
  ls = List(id="ls")
  assert ls.html_tag == "ul"
  assert ls._count == 0

  itm = Image(id="yao", img_url="k")
  ls.append(itm)
  assert ls._count == 1
  assert len(ls.children) == 1
  assert len(ls.children[0].children) == 1
  assert isinstance(ls.children[0].children[0], Image)

def test_inheritance():
  pnl = Panel(id="panel")
  assert len(pnl.children) == 0
  itm = Image(id="yao", img_url="k", parent=pnl)
  assert len(pnl.children) == 1
  assert isinstance(pnl.children[0], Image)


# TEXT WIDGETS
def test_title():
  t = Title(id="titl", text="Text")
  assert t.size == 1
  assert t._get_html_tag() == "h1"
  assert t.content == "Text"

  t2 = Title(id="titl", text="Text", size=3)
  assert t2.size == 3
  assert t2._get_html_tag() == "h3"

def test_paragraph():
  p = Paragraph(id="p", text="yao")
  assert p.html_tag == "p"
  assert p.content == "yao"

def test_span():
  s = Span(id="s", text="spans")
  assert s.html_tag == "span"
  assert s.content == "spans"

def test_textlink():
  t = TextLink(id="id", text="abcd", url="http://www.google.ca")
  assert t.html_tag == "a"
  assert t.content == "abcd"
  assert "href" in t.attributes
  assert t.attributes["href"] == "http://www.google.ca"

def test_viewtextlink():
  vtl = ViewTextLink(id="id", text="abcd", view_name="test")
  assert len(vtl.children) == 1
  assert isinstance(vtl.children[0], Span)
