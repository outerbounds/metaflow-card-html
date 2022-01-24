from metaflow import FlowSpec, step, card

class HTMLFlow(FlowSpec):

    @step
    def start(self):
        self.next(self.end)

    @card(type='html')
    @step
    def end(self):
        self.html = "<html><body><h1 style='color: blue'>Hello World</h1></body></html>"

if __name__ == '__main__':
    HTMLFlow()