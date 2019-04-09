from javax       import swing
from collections import OrderedDict
from CreateSwing import CreatePanle
from java.awt    import Color
from UIhandler   import UIhandler

class CreateContent(object):
    """docstring for CreateContent."""
    def __init__(self, name, option):
        self.name = name
        self.option = option
        self.content = None
        self._burpColor = Color(239,111,67)


    def fetch_content(self):
        if not self.content:
            self.create()
        return self.content

    def create(self):
        c_panel = CreatePanle(self._burpColor)
        ui = UIhandler(self.name,self.option)
        self.content = c_panel.create_x_axis_layout_panel(self.name)
        content_ui = ui.fetch_ui()
        self.content.add(content_ui)
