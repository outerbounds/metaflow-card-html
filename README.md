 [![](https://img.shields.io/github/license/outerbounds/metaflow-card-notebook)](./LICENSE)  [![Test Flow](https://github.com/outerbounds/metaflow-card-html/actions/workflows/test.yaml/badge.svg)](https://github.com/outerbounds/metaflow-card-html/actions/workflows/test.yaml) [![](https://img.shields.io/pypi/v/metaflow-card-html)](https://pypi.org/project/metaflow-card-html/)  [![](https://img.shields.io/badge/slack-@outerbounds-purple.svg?logo=slack )](http://slack.outerbounds.co/)  

# HTML Metaflow Card

Render raw HTML as a [Metaflow card][1].

## Installation

```bash
pip install metaflow-card-html
```

## Usage

To use the HTML card, you need to supply the `type=html` argument to the `@card` decorator.  You can then set the `html` attribute of your Flow to an html string you want to render:

```python
@card(type='html')
@step
def train(self):
    ...
    ...
    self.html = some_html() # set some html to the self attribute
```

In these examples, we assume `some_html` is returning a HTML string, like this:

```py
def some_html():
    return "<html><body><h1 style='color: blue'>Hello World</h1></body></html>"
```

However, you may want to use a different attribute name than `html`.  To accomplish this, you can use the `options` parameter of the `@card` decorator.  For example, if we wanted to store our HTML in an attribute named `myhtml` we would do the following:

```python
@card(type='html',options={"attribute":"myhtml"}) # set the attribute name to myhtml
@step
def train(self):
    ...
    ...
    self.myhtml = some_html() # set the html like before
```

## Error Handling

Some things to keep in mind about this card:

- This card is meant to render HTML passed as a string.  If you pass a non-string value, this card will attempt to render it as a string instead.  
- Failure to render a card will not result in an error in the flow.

# Making Your Own Card Modules

You may want to implement your own card modules to customize your own workflows.  This HTML card also serves as a great example of how to implement your own card modules.  You can follow the steps below to accomplish this:

## Step 1: Create a directory structure

To get started create the following directory structure:

```
some_random_dir/ # the name of this dir doesn't matter
├ setup.py
├ metaflow_extensions/ # namespace package name 
│  └ card_html/ # NO __init__.py file, rename this folder to card_yourcardname
│      └ plugins/ # NO __init__.py file
│        └ cards/ # NO __init__.py file 
│           └ my_card_module/  # Name of card_module
│               └ __init__.py. # This is the __init__.py is required to recoginize `my_card_module` as a package
│               └ somerandomfile.py. # [Optional] some file as a part of the package. 
.
```

If you are using GitHub, you can easily create this directory structure by using [this template][2].  Otherwise, you can copy the directory structure in [the template](https://github.com/outerbounds/metaflow-card-template) and modify it as indicated below.

_Note: Metaflow cards are distributed via [namespace packages](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/), under the namespace `metaflow_extensions`.  You need not worry about the mechanics of namespace packages to distribute or publish your own card module!  We recommend just following the directory structure indicated above._

## Step 2: Modify Files & Directory Structure

After creating the necessary directory structure, you will need to modify the following files/directories:

1. `setup.py`: review and change the parameters passed to `setup` as appropriate.  Do not forget to add dependencies to other packages if they are required.
2. Change the name of folder `metaflow_extensions/card_*` to `metaflow_extensions/card_<yourcardname>`.  This is a suggestion to help keep the directory structure consistent with other cards
3. Change the name of the folder `metaflow_extensions/..../cards/html` to `metaflow_extensions/.../cards/<yourcardname>`

## Step 3: Create a Card Module

In `__init__.py` located in `metaflow_extensions/.../cards/<yourcardname>`, you must import or define your custom card module. Here is a minimal example:

```python
from metaflow.cards import MetaflowCard

class BasicCard(MetaflowCard):
    type = "basic_card"

    def render(self, task): # this function returns the HTML to be rendered
        return task.data.html # assumes you are saving an attribute named `html` in the task

CARDS = [BasicCard]
```

Note that `__init__.py` requires a `CARDS` attribute which needs to be a `list` of objects inheriting `MetaflowCard` class.  

What is shown above is only a minimal example.  Recall that in the `HTML` card, you can specify the name of the attribute via the `options` parameter.  We can implement this functionality as follows:

```python
from metaflow.cards import MetaflowCard

class HTMLCard(MetaflowCard):

    type = 'html'
    
    def __init__(self, options={"attribute":"html"}, **kwargs):
        self._attr_nm = options.get("attribute", "html")
 
    def render(self, task):
        if self._attr_nm in task:
            return str(task[self._attr_nm].data) # retrieves the html from the task by accessing `task[self._attr_nm]`

CARDS = [HTMLCard]
```

## Step 4: Test Your Card

Now that you have finished creating your custom card, you can install it so that it is  present in the python path.   You can then test your card by passing the correct argument for `type` to `@card` as follows (no need to import anything):

```python
@card(type='helloworld')
@step
def train(self):
    ...
    ...
    self.html = some_html() # set some html to the self attribute
```

We recommend setting up automated tests in CI if possible.  Take a look at [tests/](tests/) and [.github/workflows/](.github/workflows/) for an example.  This is optional.

## Step 5: Publish Your Card

You are now ready to publish your card to pyipi.  If you have are not familiar with how to do this, you can follow the steps in [this tutorial](https://realpython.com/pypi-publish-python-package/).  For a more in-depth discussion on python packaging, you can read [this article](https://packaging.python.org/tutorials/packaging-projects/).

## Step 6: Tell Everyone About Your Card :rocket:

Now its time to let people know about your card!  You can make a [PR to this README][3] as well as letting us know on Twitter, tagging [@MetaflowOSS](https://twitter.com/MetaflowOSS).


[1]: https://docs.metaflow.org/
[2]: https://github.com/outerbounds/metaflow-card-template/generate
[3]: https://github.com/outerbounds/awesome-metaflow/edit/main/README.md
