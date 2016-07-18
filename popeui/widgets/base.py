class BaseElement(object):
  """
  Base class common to all PopeUI widgets.
  """

  html_tag = None
  """
  HTML tag of this widget.
  """

  def __init__(self, id, classname=None, parent=None):
    """
    Constructor of the base widget.

    :param id: ID of the widget
    :param classname: Class name of the widget Analogous to HTML classes, mostly used for styling. (``string``)
    :param parent: Parent widget (Subclass of :class:`BaseElement`)
    """
    self.attributes = {}
    """
    Dictionary of HTML attributes for this widget. (Ex: ``{"class": "test1 test2"}``)
    """

    self.attributes["id"] = id

    self.server_events = []
    self.event_handlers = []
    self.socket_events = {}

    if classname:
      self.attributes["class"] = classname

    self.view = None
    """
    Instance of :class:`~.application.View` in which this widget was declared.
    """

    if parent is not None:
      parent.add_child(self)

    self.autoclosing = False
    self.content = ""

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
    """
    Generate the HTML representing this widget.

    :returns: HTML string representing this widget.
    """
    return self._generate_html()


class BaseContainer(BaseElement):
  """
  Base class common to all widgets that can contain other widgets.
  """

  def __init__(self, id, classname=None, parent=None):
    """
    Constructor of the Base Container
    """
    super(BaseContainer, self).__init__(id, classname, parent)
    self.children = []
    """
    List of objects inheriting :class:`BaseElement`.
    """

  def add_child(self, child):
    """
    Add a new child element to this widget.

    :param child: Object inheriting :class:`BaseElement`.
    """
    self.children.append(child)
    child.view = self.view

  def redraw(self):
    """
    Trigger a client-side redrawing of all the children of this widget
    """
    self.view.ctx.socket.try_send_message({"event": "redraw", "element_id": self.attributes["id"], "data": {"inner_html": "".join(map(lambda x: x.compile(), self.children))}})

  def remove_child(self, child):
    """
    Remove a child widget from this widget.

    :param child: Object inheriting :class:`BaseElement`
    """
    self.children.remove(child)

  def get_element_by_id(self, id):
    """
    Find a child widget by its ID.

    :param id: ID of the widget to find.
    :returns: Object inheriting :class:`BaseElement`
    """
    if self.attributes["id"] == id:
      return self
    else:
      results = map(self.get_element_by_id(id), filter(lambda x: hasattr("get_element_by_id", x), self.children))
      for result in results:
        if result:
          return result

  def get_children_by_classname(self, classname):
    """
    .. note::
      This method is not recursive (yet). It only searches in the immediate children of the widget.
    Find an immediate child widget by its HTML class.

    :param classname: HTML class of the widgets to find.
    :returns: List of objects inheriting :class:`BaseElement`
    """
    return list(filter(lambda child: classname in child.attributes["class"], self.children))

  def _update_events(self):
    for child in self.children:
      if hasattr(child, "_update_events"):
        child._update_events()
      self.server_events += child.server_events
      self.event_handlers += child.event_handlers

      for key in child.socket_events:
        if key in self.socket_events:
          self.socket_events[key].update(child.socket_events[key])
        else:
          self.socket_events[key] = child.socket_events[key]

  def compile(self):
    """
    Recursively compile this widget as well as all of its children to HTML.

    :returns: HTML string representation of this widget.
    """
    self.content = "".join(map(lambda x: x.compile(), self.children))
    return self._generate_html()
