# -*- coding: utf-8 -*-
from javax import swing

from collections import OrderedDict
from javax.swing                import BoxLayout
from javax.swing.border         import EtchedBorder

from CompartmentView import CompartmentView
import ViewConfig

class TabView():
    """docstring for TabView.
    タブ内での描画を担当
    """
    def __init__(self, tab):
        self._compartments = ViewConfig.config['info'][tab]
        self._contents =  ViewConfig.config['content'][tab]
        self._panel = None

    def fetch_panel(self):
        if not self._panel :
            self.create_panel()
        return self._panel

    def create_panel(self):
        self._panel = swing.JPanel()
        self._panel.setLayout(BoxLayout(self._panel, BoxLayout.Y_AXIS))
        self._panel.setBorder(EtchedBorder(EtchedBorder.RAISED))
        #各区画をadd
        for compartment in self._compartments.keys():
            if compartment in self._contents.keys():
                content = self._contents[compartment]
            else :
                content = None
            compartment_panel = CompartmentView(compartment,self._compartments[compartment],content)
            self._panel.add(compartment_panel.fetch_compartment())
        return self._panel
