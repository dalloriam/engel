class BaseElement(object):

  def __init__(self, id, classname=None):
    self.styles = {}
    self.attributes = {}
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

  def __init__(self, id, classname=None):
    super(BaseContainer, self).__init__(id, classname)
    self.children = []

  def add_child(self, child):
    # TODO: ADD "PARENT" parameter in widget constructors
    self.children.append(child)

  def remove_child(self, child):
    self.children.remove(child)

  def get_element_by_id(self, id):
    if self.attributes["id"] == id:
      return self
    else:
      results = map(self.get_element_by_id(id), filter(lambda x: hasattr("get_element_by_id", x), self.children))
      for result in results:
        if result:
          return result

  def get_children_by_classname(self, classname):
    return filter(lambda child: classname in child.attributes["class"], self.children)

  def compile(self):
    self.content = "".join(map(lambda x: x.compile(), self.children))
    return self._generate_html()
