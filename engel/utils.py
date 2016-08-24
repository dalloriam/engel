def html_property(prop_name):

  def getter(self):
    return self._attributes[prop_name]
  
  def setter(self, value):
    self._set_attribute(prop_name, value)

  def deleter(self):
    self._set_attribute(prop_name, None)

  return property(getter, setter, deleter)
