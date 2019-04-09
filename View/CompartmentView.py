from javax              import swing
from java.awt           import Color
from CreateSwing        import CreatePanle
from collections        import OrderedDict
from java.awt           import Font
from java.awt           import FlowLayout
from java.awt           import Dimension
from java.lang          import Short
from javax.swing        import BoxLayout
from javax.swing.border import EtchedBorder
from java.awt           import GridLayout
from ContentView        import ContentView
import ViewConfig

class CompartmentView(object):

    def __init__(self,comporment, info, contents):
        self._comporment = comporment
        self._contents = contents
        self._info = info
        self.compartment = None
        self._burpColor = Color(239,111,67)

    def fetch_compartment(self):
        if not self.compartment:
            self.create_compartment()
        return self.compartment

    def create_compartment(self):
        if self._comporment == 'TOP':
            self.top_panel()
        elif self._comporment == 'CENTER':
            layout = BoxLayout.X_AXIS
            self.create_cont_panel(layout)
        elif self._comporment == 'BOTTOM':
            layout = BoxLayout.Y_AXIS
            self.create_cont_panel(layout)

    def top_panel(self):
        title  = swing.JLabel(self._info['title'][0],swing.JLabel.LEFT)
        title.setFont(Font("Arial", Font.BOLD, 24))
        title.setForeground(self._burpColor)
        self.compartment = swing.JPanel()
        self.compartment.add(title)
        self.compartment.setLayout(FlowLayout(FlowLayout.LEFT))
        self.compartment.setMaximumSize(Dimension(Short.MAX_VALUE, 40))

    def create_cont_panel (self,layout):
        titles = self._info['title']
        self.compartment = swing.JPanel()
        self.compartment.setBorder(EtchedBorder(EtchedBorder.RAISED))
        self.compartment.setLayout(BoxLayout(self.compartment, layout))
        self.compartment.setLayout(GridLayout())
        for title in titles:
            content = ContentView(title,self._contents[title])
            self.compartment.add(content.fetch_content())
