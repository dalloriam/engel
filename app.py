from ui.structure import Application, Division
from ui.text import Title, Span
from ui.widgets import Button

import os
import webbrowser


class HelloWorldView(object):

  def __init__(self, title1, title2, btnText):

    self.app = Application()

    main_div = Division()
    self.app.add_child(main_div)

    title = Title(classname="MainTitle")
    title.content = title1

    second_title = Title(size=2)
    second_title.content = title2

    my_span = Span()
    my_span.content = "test-span"

    btn = Button()
    btn.content = btnText

    main_div.add_child(title)
    main_div.add_child(second_title)
    main_div.add_child(my_span)
    main_div.add_child(btn)

  def compile(self):
    return self.app.compile()


app = HelloWorldView("Title 1", "Title 2", "My Button")

if os.path.isfile("index.html"):
  os.remove("index.html")

with open("index.html", "a") as outfile:
  chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
  outfile.write(app.compile())
  webbrowser.get(chrome_path).open("index.html")
