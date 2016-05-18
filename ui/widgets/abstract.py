from base import BaseContainer, BaseElement


class ViewLink(BaseContainer):

  def __init__(self, view_name, params=None, id=None, classname=None):
    super(ViewLink, self).__init__(id, classname)
    self.html_tag = "a"

    url = view_name

    query_string = "&".join([str(x) + "=" + str(params[x]) for x in params.keys()])
    if query_string:
      url += "?" + query_string

    self.attributes["href"] = url


class HeadLink(BaseElement):

  def __init__(self, link_type, path, id=None, classname=None):
    super(HeadLink, self).__init__(id, classname)
    self.attributes["href"] = path
    self.attributes["rel"] = link_type
    self.autoclosing = True

    self.html_tag = "link"


class PageTitle(BaseElement):

  def __init__(self, text, id=None, classname=None):
    super(PageTitle, self).__init__(id, classname)
    self.html_tag = "title"

    self.content = text


class Script(BaseElement):

    def __init__(self, script, id=None, classname=None):
        super(Script, self).__init__(id, classname)
        self.html_tag = "script"

        self.content = script
