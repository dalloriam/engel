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

    self.view = None
    """
    Instance of :class:`~.application.View` in which this widget was declared.
    """

    self._classes = []

    if classname:
      self.add_class(classname)

    self.autoclosing = False
    self.content = ""

    self.build()

    if parent is not None:
      parent.add_child(self)

  def add_class(self, classname):
    self._classes.append(classname)

    if self.view and self.view.is_loaded:
      self.view.dispatch({'name': 'addclass', 'selector': '#' + self.attributes['id'], 'cl': classname})

  def remove_class(self, classname):
    self._classes.remove(classname)

    if self.view and self.view.is_loaded:
      self.view.dispatch({'name': 'removeclass', 'selector': '#' + self.attributes['id'], 'cl': classname})

  def build(self):
    """
    This method is called between the initialization of the widget and its binding to a view.
    Add here any procedure required to take place before binding to a view (Ex: add child widgets).
    """
    pass

  def _get_html_tag(self):
    return self.html_tag

  def __setattr__(self, name, value):
    super(BaseElement, self).__setattr__(name, value)
    if name == 'parent' and value is not None:
      self.view = self.parent.view
    elif name == 'parent' and value is None:
      self.view = None

    elif name == 'view' and value is not None:
      self.on_view_attached()

  def _format_attributes(self):
    return "".join([' {0}="{1}"'.format(x, self.attributes[x])for x in self.attributes.keys()])

  def _generate_html(self):
    self.attributes['class'] = ' '.join(self._classes)
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

  def on_view_attached(self):
    """
    Gets triggered when the widget gets attached to a view.
    """
    pass


class BaseContainer(BaseElement):
  """
  Base class common to all widgets that can contain other widgets.
  """

  def __init__(self, id, classname=None, parent=None):
    """
    Constructor of the Base Container
    """
    self.children = []
    super(BaseContainer, self).__init__(id, classname, parent)
    """
    List of objects inheriting :class:`BaseElement`.
    """

  def __setattr__(self, name, value):
    super(BaseContainer, self).__setattr__(name, value)
    if name == 'parent' and value is not None:
      for child in self.children:
        child.view = self.view


  def add_child(self, child):
    """
    Add a new child element to this widget.

    :param child: Object inheriting :class:`BaseElement`.
    """
    self.children.append(child)
    child.parent = self

    if self.view and self.view.is_loaded:
      self.view.dispatch({
        'name': 'append',
        'html': child.compile(),
        'selector': '#' + str(self.attributes['id'])
      })

  def remove_child(self, child):
    """
    Remove a child widget from this widget.

    :param child: Object inheriting :class:`BaseElement`
    """
    self.children.remove(child)
    child.parent = None

    if self.view and self.view.is_loaded:
      self.view.dispatch({
        'name': 'remove',
        'selector': '#' + child.attributes['id']
      })

  def replace_child(self, old_child, new_child):

    for i, child in enumerate(self.children):
      if child is old_child:
        old_child.parent = None
        new_child.parent = self
        self.children[i] = new_child

        if self.view and self.view.is_loaded:
          self.view.dispatch({
            'name': 'replace',
            'selector': '#' + old_child.attributes['id'],
            'html': new_child.compile()
          })
        return


  def compile(self):
    """
    Recursively compile this widget as well as all of its children to HTML.

    :returns: HTML string representation of this widget.
    """
    self.content = "".join(map(lambda x: x.compile(), self.children))
    return self._generate_html()
