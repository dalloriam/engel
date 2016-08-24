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

  popereddit                    - main app directory
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



Next, let's edit ``app.py`` to be a bit cleaner

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


Building the view
-----------------


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

