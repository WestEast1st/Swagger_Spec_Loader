from CreateSwing   import CreatePanle
from CreateContent import CreateContent
from collections   import OrderedDict
from java.awt      import Color

class ContentView(object):

    def __init__(self,title,contents):
        self._title = title
        self._contents = contents
        self.content_names = self._contents.keys()
        self.contents = None
        self._burpColor = Color(239,111,67)

    def fetch_content(self):
        if not self.contents :
            self.creater()
        return self.contents

    def creater(self):
        c_swing = CreatePanle(self._burpColor)
        self.contents = c_swing.create_y_axis_layout_panel(self._title)
        for content_name in self.content_names:
            c_content = CreateContent(content_name,self._contents[content_name])
            self.contents.add(c_content.fetch_content())
