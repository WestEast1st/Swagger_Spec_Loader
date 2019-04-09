# -*- coding: utf-8 -*-
#from java.lang import String
from java.io        import File
from java.awt.event import MouseAdapter
from java.awt.event import MouseEvent
from java.awt.event import ActionEvent
from java.awt.event import ActionListener
from javax          import swing
from collections    import OrderedDict
import os
import sys
from ContextMenu import ContextMenu
sys.path.append("./Model")
from EndPointListUp import EndPointListUp
sys.path.append("./View")
import ContentData

class AddAction(ActionListener,MouseAdapter):
    def __init__(self, instans, type, funcopt, mode=''):
        self.s          = instans
        self.type       = type
        self.funcopt    = funcopt
        self.panel      = swing.JPanel()
        self.mode       = mode
        if 'tableName' in self.funcopt.keys():
            self.table_name = self.funcopt['tableName']
            self.colomn_names = self.funcopt['coloName']
    #Event listener
    ## Mouse Action
    def mouseClicked(self, e):
        self.s._select_table["row"] = self.s._content_table.getSelectedRow()
        self.s._select_table["col"] = self.s._content_table.columnCount

    def mouseReleased(self,e):
        if 'is_show' in self.funcopt.keys():
            if self.funcopt['is_show']:
                selectedRow = self.s._content_table.rowAtPoint(e.getPoint());

                if selectedRow >= 0 and selectedRow < self.s._content_table.getRowCount():
                    if not self.s._content_table.getSelectionModel().isSelectedIndex(selectedRow):
                        self.s._content_table.setRowSelectionInterval(selectedRow, selectedRow)
                if e.isPopupTrigger() and isinstance(e.getComponent(), swing.JTable):
                    self.show(e)
                    e.consume()

    def mousePressed(self,e):
        if 'is_show' in self.funcopt.keys():
            if self.funcopt['is_show']:
                if e.isPopupTrigger() and isinstance(e.getComponent(), swing.JTable) and self.s._content_table.getRowCount():
                    self.show(e)
                    e.consume()

    ##Button Push
    def actionPerformed (self,e) :
        if self.type == 'file_chooser':
            self.file_selecter()
        elif self.type == 'param_list':
            self.list_button()
        elif self.type == 'file_loader':
            self.file_loader()

    def fetch_input_data (self,texts):
        raw = []
        for i in range(len(self.funcopt['coloName'])):
            if texts[i].getText():
                raw.append(texts[i].getText())
        return raw

    def record_insert (self,raw):
        ContentData.content_data[self.table_name].addRow(raw)

    def input_data_insert (self,texts):
        raw = self.fetch_input_data(texts)
        if raw:
            self.record_insert(raw)
            return True,raw
        return False,raw

    def add_text_data(self,texts):
        flag,raw = self.input_data_insert(texts)
        if flag:
            self.s._select_table = {"row":self.s._content_table.rowCount-1,"col":self.s._content_table.columnCount}

    def list_button(self):
        if self.mode == 'Add':
            self.list_button_add_action()
        elif self.mode == 'Edit':
            self.list_button_edit_action()
        elif self.mode == 'Remove':
            self.list_button_remove_action()

    def list_button_add_action(self):
        texts = self.s.create_option_panel('Add',self.table_name,self.colomn_names)
        self.add_text_data(texts)

    def list_button_edit_action(self):
        row = self.s._select_table["row"]
        col = self.s._select_table["col"]
        if row > -1:
            texts = self.s.create_option_panel('Edit',self.table_name,self.colomn_names)
            for i in range(col):
                if texts[i].getText():
                    ContentData.content_data[self.table_name].setValueAt(texts[i].getText(), row, i)
                    self.setting_select_pix()

    def list_button_remove_action(self):
        row = self.s._select_table['row']
        if row > -1:
            ContentData.content_data[self.table_name].removeRow(row)
            self.setting_select_pix()

    def setting_select_pix(self):
        self.s._select_table['row'] = self.s._content_table.rowCount -1
        self.s._select_table['col'] = self.s._content_table.columnCount

    def file_selecter (self) :
        returnedFile,selectFile = self.s.create_file_selecter(self.funcopt['file'],self.funcopt['FNfilter'],self.panel)
        if returnedFile == swing.JFileChooser.APPROVE_OPTION:
            self.file = selectFile.getSelectedFile()
            path = self.file.getPath()
            root, ext = os.path.splitext(path)
            isFileExt = 0
            for i in self.funcopt['file']:
                if not isFileExt and i == ext[1:] :
                    isFileExt =1
            if not len(ext) < 1 and isFileExt:
                ContentData.file_path = path
            else :
                ContentData.file_path = '/'

    def file_loader(self):
        tmplate_column_names = OrderedDict()
        for i in self.funcopt['coloName']:
            tmplate_column_names[i] = None
        if not ContentData.file_path == '/':
            eplu = EndPointListUp(tmplate_column_names,ContentData.file_path)
            end_point_data = eplu.list_up()
            for i in range(len(end_point_data)):
                tmp_list = []
                for j in ['#','Host','Method','Base Path','End Point','Query','Header','Body']:
                    tmp_list.append(end_point_data[i][j])
                ContentData.content_data['end_point'].addRow(tmp_list)

    def show(self,e):
        contextMenu = ContextMenu(e,self.s)
        contextMenu.show(e.getComponent(), e.getX(), e.getY())
