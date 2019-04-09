# -*- coding: utf-8 -*-
#from java.lang import String
from java.lang import Short
from java.io   import File

from java.awt       import Insets
from java.awt       import Dimension
from java.awt       import Color
from java.awt       import BorderLayout
from java.awt       import FlowLayout
from java.awt       import Component
from java.awt       import Font

from javax                      import swing
from javax.swing                import BoxLayout
from javax.swing.filechooser    import FileNameExtensionFilter
from javax.swing.border         import TitledBorder
from javax.swing.border         import LineBorder
from javax.swing.border         import EtchedBorder
from javax.swing.border         import BevelBorder
from javax.swing.table          import DefaultTableModel
from collections                import OrderedDict
from AddAction                  import AddAction
import ContentData

class CreatePanle():
    def __init__(self,color):
        self._burpColor = color
        self._content_table = {}

    def create_table (self,opt,panel) :
        self._select_table = {"row":-1,"col":-1}
        table_name = opt['funcopt']['tableName']
        coloNames = opt['funcopt']['coloName']
        ContentData.content_data[table_name] = DefaultTableModel(coloNames, 0)
        self._content_table = swing.JTable(ContentData.content_data[table_name])
        self._content_table.setAutoCreateRowSorter(True)
        self._content_table.addMouseListener(AddAction(self,opt['type'],opt['funcopt']))
        column_model = self._content_table.getColumnModel()
        for i in xrange(column_model.getColumnCount()):
            column = column_model.getColumn(i)
            if '#' == self._content_table.getColumnName(i):
                column.setPreferredWidth(3)
            else:
                column.setPreferredWidth(200)
        self._content_table.fillsViewportHeight = True
        dtcr = self._content_table.getTableHeader().getDefaultRenderer()
        dtcr.setHorizontalAlignment(swing.SwingConstants.CENTER)
        return swing.JScrollPane(self._content_table)

    def create_panle_on_title (self,title):
        title = self.burp_label_color(title)
        panel = self.create_panle()
        panel.setBorder(title)
        return panel

    def create_x_axis_layout_panel(self, title = None):
        if title:
            panel = self.create_panle_on_title(title)
        else :
            panel = self.create_panle()
        panel.setLayout(BoxLayout(panel, BoxLayout.X_AXIS))
        return panel

    def create_y_axis_layout_panel(self, title = None):
        if title:
            panel = self.create_panle_on_title(title)
        else :
            panel = self.create_panle()
        panel.setLayout(BoxLayout(panel, BoxLayout.Y_AXIS))
        return panel

    def create_bottom_panel(self,title):
        BottomPanel = self.create_y_axis_layout_panel(title)
        return BottomPanel

    def create_center_panel(self,title):
        centerPanel = self.create_y_axis_layout_panel(title)
        return centerPanel

    def create_button(self,table_name,opt,panel,mode=''):
        ContentData.file_path = '/'
        button =  swing.JButton(table_name)
        button.setMargin(Insets(0, 0, 0, 0))
        button.addActionListener(AddAction(self,opt['type'],opt['funcopt'],mode))
        return button

    def create_buttons_y(self,opt):
        panel = self.create_y_axis_layout_panel()
        button = OrderedDict()
        max =[0,'']
        for i in opt['funcopt']['buttonType']:
            button[i] = self.create_button(i,opt,panel,i)
            if len(i) > max[0]:
                max[0] = len(i)
                max[1] = i
        for i in opt['funcopt']['buttonType']:
            size = button[max[1]].getMaximumSize()
            button[i].setMaximumSize(Dimension(size))
            panel.add(button[i])
        return panel

    def create_table_panel(self,opt):
        #テーブル系
        panel   = swing.JPanel()
        panel.setPreferredSize(Dimension(Short.MAX_VALUE, 70))
        panel.setLayout(BorderLayout())
        panel.setLayout(BoxLayout(panel, BoxLayout.X_AXIS))
        #table
        list = self.create_table(opt,panel)
        #button
        buttons = self.create_buttons_y(opt)
        border = BevelBorder(BevelBorder.RAISED)
        panel.add(buttons)
        panel.add(list)
        return panel

    def create_text_area(self):
        tA          = swing.JTextArea()
        tA.margin   = Insets(4,5,4,5)
        tA.editable = False
        return tA

    def create_log_pane (self,logTA) :
        lp = swing.JScrollPane(logTA)
        lp.setBorder(EtchedBorder(EtchedBorder.RAISED))
        lp.setVerticalScrollBarPolicy(swing.ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS)
        lp.setPreferredSize(Dimension(Short.MAX_VALUE, 60))
        return lp

    def burp_label_color(self,text,isBorder = 1):
        if isBorder:
            title = TitledBorder(LineBorder(Color.black, 1 ,True),'<html><h3><b>'+text+'</b></h3></html>',TitledBorder.LEFT,TitledBorder.TOP)
        else :
            title = TitledBorder(LineBorder(Color.white, 1 ,True),'<html><h3><b>'+text+'</b></h3></html>',TitledBorder.LEFT,TitledBorder.TOP)
        title.setTitleColor(self._burpColor)
        return title

    def create_content_panel(self):
        panel = self.create_panle()
        panel.setLayout(BorderLayout())
        return panel

    def create_label(self,text):
        return swing.JLabel(text)

    def create_panle (self):
        panel = swing.JPanel()
        return panel

    def create_file_selecter(self,file,filter_f_n,panel):
        selectFile  = swing.JFileChooser()
        filter      = FileNameExtensionFilter(filter_f_n,file);
        selectFile.addChoosableFileFilter(filter)
        return selectFile.showDialog(panel,filter_f_n),selectFile

    def create_option_panel(self,mode,table_name,colomn_names):
        option_panel = swing.JOptionPane()
        main = self.create_y_axis_layout_panel()
        panel = self.create_y_axis_layout_panel()
        title = swing.JLabel(table_name)
        panel.add(title)
        texts = []
        for i in range(len(colomn_names)):
            title = swing.JLabel(colomn_names[i]+" : \n")
            if mode == 'Add':
                texts.append(swing.JTextField())
            elif mode == 'Edit':
                texts.append(swing.JTextField(ContentData.content_data[table_name].getValueAt(self._select_table["row"], i)))
            minipanel = self.create_y_axis_layout_panel()
            minipanel.add(title)
            minipanel.add(texts[i])
            panel.add(minipanel)
        main.add(panel)
        option_panel.showMessageDialog(option_panel,main,table_name,swing.JOptionPane.PLAIN_MESSAGE)
        return texts
