import sys
from burp import IBurpExtender
from burp import IBurpExtenderCallbacks
from burp import ITab
from burp import IContextMenuInvocation
from burp import IContextMenuFactory
from collections import OrderedDict
from java.util import LinkedList
from javax import swing

sys.path.append("./View")
from ViewMain import ViewMain
#from ContextMenuFactory import ContextMenuFactory
import ContentData

sys.path.append("../")

class BurpExtender(IBurpExtender,IContextMenuFactory,ITab,IBurpExtenderCallbacks):
    view = None
    def registerExtenderCallbacks(self, callbacks):
        self._helpers = callbacks.getHelpers()
        self._jPanelMain = None
        ContentData.callbacks = callbacks
        BurpExtender.ViewMain  = ViewMain()
        self._jPanelMain= BurpExtender.ViewMain.feche_extension()
        ContentData.callbacks.setExtensionName("Swagger_Spec_Loader")
        ContentData.callbacks.customizeUiComponent(self._jPanelMain)
        ContentData.callbacks.addSuiteTab(self)
        ContentData.callbacks.registerContextMenuFactory(self)
        return

    def getTabCaption(self):
        return 'Swagger_Spec_Loader'

    def getUiComponent(self):
        return self._jPanelMain

    def createMenuItems(self,invocation):
        httpRequestResponseArray = invocation.getSelectedMessages()
        ctx = invocation.getInvocationContext()
        print ctx
        self.menu_list = LinkedList()
        self.menu_item_1 = swing.JMenuItem('test1 button')
        self.menu_item_1.addMouseListener(ResponseContextMenu(self.callbacks, httpRequestResponseArray))
        self.menu_list.add(self.menu_item_1)
        self.menu_item_2 = swing.JMenuItem('test2 button')
        self.menu_item_2.addMouseListener(ResponseContextMenu(self.callbacks, httpRequestResponseArray))
        self.menu_list.add(self.menu_item_2)
        return self.menu_list
