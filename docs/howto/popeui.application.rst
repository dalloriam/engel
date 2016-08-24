Building a PopeUI Application
=============================

This section will cover the creation of a basic PopeUI application that will display the headlines from Reddit using
PRAW_.

.. _PRAW: https://github.com/praw-dev/praw/

Let's begin by installing PRAW.

.. code-block:: shell

  $ pip install praw


Generating the project files
----------------------------

Once PRAW is installed, let's use PopeUI's build-in code generator to generate the basic skeleton of our application.

.. code-block:: shell

  $ pope new popereddit

This will generate the following structure:

.. code-block:: text

  popereddit/                   - main app directory
  ├── app.py                    - application entry point
  ├── views/                    - views package
  │   ├── home.py               - Default home view
  ├── services/                 - services package
  │   ├── home.py               - default home service


Building the service
--------------------

Let's rename ``services/home.py`` to ``services/reddit.py`` and edit it so that the contents
look like:

.. code-block:: python

  import praw


  class RedditService(object):

    def __init__(self):
      self.agent = praw.Reddit(user_agent='popereddit')

    def get_sub(self, subreddit):
      return [str(x) for x in self.agent.get_subreddit(subreddit).get_hot(limit=50)]


The service provides only one method, which fetches the top 50 submissions from a given subreddit.
This is the only logic needed in our application.


Next, let's edit ``app.py`` so it is up-to-date with our service.

.. code-block:: python

  from popeui import Application

  from views.home import HomeView
  from services.reddit import RedditService


  class popereddit(Application):

    base_title = "{0} | popereddit"

    def __init__(self, debug=False):
      super(popereddit, self).__init__(debug)

      self.views['default'] = HomeView

      self.services['reddit'] = RedditService

  if __name__ == '__main__':
    app = popereddit(debug=True)
    app.start()

When the app starts, the framework instantiates all services defined in ``Application.services`` and first builds the view corresponding
to the ``default`` route. Now we only need a view for our application to work.

Building the view
-----------------

The bulk of the view definition process is done in the ``build()`` method, which must be overidden in all of your views.
This method is called by the framework when loading a view, and is tasked with building the layout for the view as well as registering
most of the events that are to be handled at runtime.

With that in mind, let's define our layout in ``/views/home.py``.

.. note::
  When using an external library (such as :py:mod:`~.libraries.bootstrap4`), you `must` add the module to ``YourView.libraries``, so that the view loader
  is able to load the CSS and Javascript files required by your library.

.. code-block:: python

  from popeui import View

  from popeui.libraries import bootstrap4
  from popeui.widgets import TextBox, Button

  from copy import copy


  class HomeView(View):

    title = "HomeView"

    libraries = [bootstrap4]

    def build(self):
      self.main_panel = bootstrap4.Container(id="main-panel", parent=self.root)

      self.results = bootstrap4.CardColumns(id="results", parent=self.main_panel)

      self.txt_subreddit = TextBox(id="txt-subreddit", name="subreddit", parent=self.main_panel)
      btnSearch = Button(id="btn-get-sub", text="Get Subreddit", parent=self.main_panel)

      self.on(event='click', callback=self.load_subreddit, selector='#' + btnSearch.id)

    def clear_results(self):
      for rs in copy(self.results.children):
        self.results.remove_child(rs)

    def load_subreddit(self, event, interface):
      self.clear_results()
      subreddit = self.txt_subreddit.text

      if subreddit:
        for i, hit in enumerate(self.context.services['reddit'].get_sub(subreddit)):
          print(hit)
          bootstrap4.ImageCard(
            id="result-" + str(i),
            title=hit,
            text=str(i),
            img_url="http://i.imgur.com/CduSn7x.png",
            parent=self.results
          )

You now have a fully functional PopeUI application!
If you want more information on the framework's API, head over to the :doc:`../code_overview/popeui`. Otherwise, take a look at :doc:`popeui.widget`.
