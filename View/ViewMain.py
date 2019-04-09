# -*- coding: utf-8 -*-
from javax import swing

from collections import OrderedDict
from java.awt       import Color

from TabView import TabView
import ViewConfig

class ViewMain():
    """docstring for ViewMain.
    タブ要素に振り分けることが担当

    """
    def __init__(self):
        self.extension = None
        self._burpColor = Color(239,111,67)

    def feche_extension(self):
        if not self.extension:
            self.create()
        return self.extension

    def create(self):
        if len(ViewConfig.tabs) == 1:
            panel = TabView(tab)
            self.extension = panel.fetch_panel()
        else:
            self.extension = swing.JTabbedPane()
            #各パネルをタブの下に
            for tab_name in ViewConfig.tabs:
                tab = TabView(tab_name)
                self.extension.addTab(tab_name,tab.fetch_panel())
