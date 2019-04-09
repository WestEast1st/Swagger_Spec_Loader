from  javax import swing
from  javax.swing import JPopupMenu
from  javax.swing import AbstractAction
from burp import IBurpExtenderCallbacks
import ContentData
from java.awt.event import ActionListener
from java.awt.event import MouseAdapter
from java.awt.event import MouseEvent
from collections import OrderedDict
from burp import IBurpExtenderCallbacks

import sys

class ContextMenu(JPopupMenu):
    """docstring for ContextMenu."""
    def __init__(self,e,instans):
        self.e = e
        self.tab_instans = instans
        send_to_repeater = swing.JMenuItem('Send To Repeater')
        send_to_repeater.addActionListener(ActionEvent('send_to_repeater',e,self.tab_instans))
        send_to_intruder = swing.JMenuItem('Send To Intruder')
        send_to_intruder.addActionListener(ActionEvent('send_to_intruder',e,self.tab_instans))
        clear = swing.JMenuItem('Clear')
        clear.addActionListener(ActionEvent('clear',e,self.tab_instans))
        clear_all = swing.JMenuItem('Clear All')
        clear_all.addActionListener(ActionEvent('clear_all',e,self.tab_instans))

        self.add(send_to_repeater)
        self.add(send_to_intruder)
        self.add(swing.JSeparator())
        self.add(clear)
        self.add(clear_all)


class ActionEvent(ActionListener,AbstractAction):
    def __init__(self,mode,e,instans):
        self.tab_instans = instans
        self.callbacks = ContentData.callbacks
        self.mode = mode
        self.e = e

    def actionPerformed(self,e):
        if self.mode == 'send_to_repeater':
            for row in self.tab_instans._content_table.getSelectedRows():
                list = []
                for col in range(8):
                    add = ContentData.content_data['end_point'].getValueAt(row,col)
                    if not add :
                        add = ''
                    list.append(add)
                list = list[1:]
                request_line = list[1]+' '+''.join(list[2:5])
                head = list[5]
                body = list[6]
                request = "".join([request_line,"\n",head,"\n",body])
                IBurpExtenderCallbacks.sendToRepeater(self.callbacks,list[0],443,True,request,request_line)
        elif self.mode == 'send_to_intruder':
            for row in self.tab_instans._content_table.getSelectedRows():
                list = []
                for col in range(8):
                    add = ContentData.content_data['end_point'].getValueAt(row,col)
                    if not add :
                        add = ''
                    list.append(add)
                list = list[1:]
                request_line = list[1]+' '+''.join(list[2:5])
                head = list[5]
                body = list[6]
                request = "".join([request_line,"\n",head,"\n",body])
                IBurpExtenderCallbacks.sendToIntruder(self.callbacks,list[0],443,True,request)
        elif self.mode == 'clear':
            for row in self.tab_instans._content_table.getSelectedRows():
                ContentData.content_data['end_point'].removeRow(row)
        elif self.mode == 'clear_all':
            ContentData.content_data['end_point'].setRowCount(0)
