from base import BaseContainer


class Application(BaseContainer):

  def __init__(self, id=None, classname=None):
    super(Application, self).__init__(id, classname)
    self.html_tag = "body"

  def _get_html_tag(self):
    return self.html_tag

  def compile(self):
    return "<html>\n{0}\n</html>".format(super(Application, self).compile())


class Division(BaseContainer):

  def __init__(self, id=None, classname=None):
    super(Division, self).__init__(id, classname)
    self.html_tag = "div"

  def _get_html_tag(self):
    return self.html_tag
