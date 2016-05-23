from ui.widgets.base import BaseContainer, BaseElement


class ViewLink(BaseContainer):

  def __init__(self, id, view_name, params=None, classname=None):
    super(ViewLink, self).__init__(id, classname)
    self.html_tag = "a"

    url = view_name
    if params:
      query_string = "&".join([str(x) + "=" + str(params[x]) for x in params.keys()])
      if query_string:
        url += "?" + query_string

    self.attributes["href"] = url


class HeadLink(BaseElement):

  def __init__(self, id, link_type, path, classname=None):
    super(HeadLink, self).__init__(id, classname)
    self.attributes["href"] = path
    self.attributes["rel"] = link_type
    self.autoclosing = True

    self.html_tag = "link"


class PageTitle(BaseElement):

  def __init__(self, id, text, classname=None):
    super(PageTitle, self).__init__(id, classname)
    self.html_tag = "title"

    self.content = text


class Script(BaseElement):

  def __init__(self, id, js, classname=None):
    super(Script, self).__init__(id, classname)
    self.html_tag = "script"

    self.content = js
