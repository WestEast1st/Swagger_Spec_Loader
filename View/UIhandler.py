# -*- coding: utf-8 -*-
from collections import OrderedDict
from CreateSwing import CreatePanle
from java.awt       import BorderLayout
from javax  import swing
from java.awt           import Font
from java.awt           import Dimension

from java.awt       import Color
class UIhandler():
    """docstring for UIhandler."""
    def __init__(self,name,option):
        self.name = name
        self.option = option
        self.content_ui = None
        self._burpColor = Color(239,111,67)

    def fetch_ui(self):
        if not self.content_ui:
            self.create_ui()
        return self.content_ui

    def create_ui(self):
        cpanel = CreatePanle(self._burpColor)
        self.content_ui = swing.JPanel()

        content_panel = swing.JPanel()
        content_panel.setLayout(BorderLayout())
        text = swing.JLabel(self.option['text'])
        if self.option['type'] == 'file_chooser':
            #fileSelecter
            button = cpanel.create_button(self.option['funcopt']['FNfilter'],self.option,content_panel)
            button.setPreferredSize(Dimension(40, 40))
        elif self.option['type'] == 'param_list':
            ui = cpanel.create_table_panel(self.option)
            content_panel.add(ui)
        elif self.option['type'] == 'file_loader':
            button = cpanel.create_button(self.option['funcopt']['FNfilter'],self.option,content_panel)
            button.setPreferredSize(Dimension(40, 40))

        text.setFont(Font("Arial", Font.PLAIN, 12))
        content_panel.add(text,BorderLayout.PAGE_START)
        self.content_ui.setLayout(BorderLayout())
        self.content_ui.add(content_panel)
        if self.option['type'] == 'file_chooser' or self.option['type'] == 'file_loader':
            self.content_ui.add(button,BorderLayout.SOUTH)
