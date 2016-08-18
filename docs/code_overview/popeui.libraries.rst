PopeUI-Supported Libraries
==========================

To use PopeUI supported libraries, simply import them and use them in your views.

.. code-block:: python

  from popeui.libraries import bootstrap4

  class MainView(View):
    title = "MyView"

    libraries = [bootstrap4]

    def build(self):
      main_panel = bootstrap4.Container(id="containerMain", parent=self.root)

      cols = bootstrap4.CardColumns(id="mycols", parent=main_panel)

      for i in range(30):
        bootstrap4.ImageCard(id="mycard" + str(i), title="This is a Title", text="This is a description", img_url="http://mysite.com", parent=cols)


Bootstrap 4 (Alpha)
-------------------

Widgets
~~~~~~~

.. automodule:: popeui.libraries.bootstrap4.widgets.structure
    :members:
    :undoc-members:
    :show-inheritance:
    :special-members: __init__
