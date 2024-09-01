from metaflow.plugins.cards.card_modules.card import MetaflowCard

DEFAULT = "<html><body>no html specified</body></html>"

class HTMLCard(MetaflowCard):

    ALLOW_USER_COMPONENTS = True
    RUNTIME_UPDATABLE = True
    type = 'html'

    def __init__(self, options={"attribute":"html"}, **kwargs):
        self._attr_nm = options.get("attribute", "html")

    def render(self, task):
        rt_data = getattr(self, 'runtime_data', {}).get("user")
        if self._attr_nm in task:
            return str(task[self._attr_nm].data)
        elif rt_data:
            return rt_data['html']
        else:
            return DEFAULT

CARDS = [HTMLCard]
