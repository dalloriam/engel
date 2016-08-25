class BaseElement(object):
  """
  Base class common to all Engel widgets.
  """

  html_tag = None
  """
  HTML tag of this widget.
  """

  @property
  def view(self):
    return self._view

  @view.setter
  def view(self, value):
    self._view = value

    if value is not None:
      self.on_view_attached()

  @property
  def parent(self):
    return self._parent

  @parent.setter
  def parent(self, value):
    self._set_parent(value)

  def _set_parent(self, value):
    self._parent = value

    if value is not None:
      self.view = value.view
    else:
      self.view = None

  @property
  def id(self):
    return self._attributes['id']

  @id.setter
  def id(self, value):
    return self._set_attribute('id', value)

  @property
  def classname(self):
    return ' '.join(self._attributes['class'])

  @classname.setter
  def classname(self, value):
    if value:
      self._attributes['class'] = value
    elif 'class' in self._attributes:
      del self._attributes['class']

  def __init__(self, id, classname=None, parent=None, **kwargs):
    """
    Constructor of the base widget.

    :param id: ID of the widget
    :param classname: Class name of the widget Analogous to HTML classes, mostly used for styling. (``string``)
    :param parent: Parent widget (Subclass of :class:`BaseElement`)
    """
    self._attributes = {}

    self._view = None
    """
    Instance of :class:`~.application.View` in which this widget was declared.
    """

    self.id = id

    self._classes = []

    if classname:
      self.add_class(classname)

    self.autoclosing = False
    self.content = ""

    self.build(**kwargs)

    if parent is not None:
      parent.add_child(self)

  def _set_attribute(self, name, value):

    if value is not None:
      self._attributes[name] = value
      if self.view and self.view.is_loaded:
        self.view.dispatch({'name': 'attr', 'selector': '#' + self.id, 'attr': name, 'value': value})

  def add_class(self, classname):
    self._classes.append(classname)
    self.classname = ' '.join(self._classes)

    if self.view and self.view.is_loaded:
      self.view.dispatch({'name': 'addclass', 'selector': '#' + self.id, 'cl': classname})

  def remove_class(self, classname):
    self._classes.remove(classname)
    self.classname = ' '.join(self._classes)

    if self.view and self.view.is_loaded:
      self.view.dispatch({'name': 'removeclass', 'selector': '#' + self.id, 'cl': classname})

  def _get_html_tag(self):
    return self.html_tag

  def _format_attributes(self):
    return "".join([' {0}="{1}"'.format(x, self._attributes[x])for x in self._attributes.keys()])

  def _generate_html(self):
    if self.autoclosing:
      return "<{0}{1}>".format(self._get_html_tag(), self._format_attributes())
    else:
      return "<{0}{1}>{2}</{0}>".format(self._get_html_tag(), self._format_attributes(), self.content)

  def build(self, **kwargs):
    """
    Gets called before the widget gets attached to a view. Override this
    to define your widget's specific traits.
    """
    pass

  def compile(self):
    """
    Generate the HTML representing this widget.

    :returns: HTML string representing this widget.
    """
    return self._generate_html()

  def on_view_attached(self):
    """
    Gets called when the widget gets attached to a view.
    """
    pass


class BaseContainer(BaseElement):
  """
  Base class common to all widgets that can contain other widgets.
  """

  @BaseElement.parent.setter
  def parent(self, value):
    self._set_parent(value)
    if value is not None:
      for child in self.children:
        child.view = self.view

  def __init__(self, id, classname=None, parent=None, **kwargs):
    """
    Constructor of the Base Container
    """
    self.children = []
    super(BaseContainer, self).__init__(id, classname, parent, **kwargs)
    """
    List of objects inheriting :class:`BaseElement`.
    """


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
        'selector': '#' + str(self.id)
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
        'selector': '#' + child.id
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
            'selector': '#' + old_child.id,
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
