class BaseElement(object):

  def __init__(self, id=None, classname=None):
    self.styles = {}
    self.attributes = {}
    if id:
      self.attributes["id"] = id
    if classname:
      self.attributes["class"] = classname
    self.autoclosing = False
    self.content = ""

    self.html_tag = None

  def get_content(self):
    return self.content

  def _get_html_tag(self):
    return self.html_tag

  def _format_attributes(self):
    return "".join([' {0}="{1}"'.format(x, self.attributes[x])for x in self.attributes.keys()])

  def _generate_html(self):
    if self.autoclosing:
      return "<{0}{1}>".format(self._get_html_tag(), self._format_attributes())
    else:
      return "<{0}{1}>{2}</{0}>".format(self._get_html_tag(), self._format_attributes(), self.content)

  def compile(self):
    return self._generate_html()


class BaseContainer(BaseElement):

  def __init__(self, id=None, classname=None):
    super(BaseContainer, self).__init__(id, classname)
    self.children = []

  def add_child(self, child):
    self.children.append(child)

  def remove_child(self, child):
    self.children.remove(child)

  def get_child_by_id(self, id):
    res = filter(lambda child: child.attributes["id"] == id, self.children)
    if res:
      return res[0]
    else:
      return None

  def get_children_by_classname(self, classname):
    return filter(lambda child: classname in child.attributes["class"], self.children)

  def compile(self):
    self.content = "".join(map(lambda x: x.compile(), self.children))
    return self._generate_html()
