import sys
import os
import init
from YamlReader import YamlReader
from YamlReader import YamlProcessor
from SwaggerSpecAnalys import SwaggerSpecAnalys
from CreateRequest import CreateRequest
from collections    import OrderedDict
sys.path.append("./View")
import ContentData
sys.path.append("./Model")

class EndPointListUp():
    """docstring for EndPointListUp."""
    def __init__(self,tmplate_column_names,file_path):
        self.file_path = file_path
        tmp = self.file_path.split('/')
        self.path = "./"+tmp[-1]
        self.dir = "/".join(tmp[0:len(tmp)-1])
        os.chdir(self.dir)
        self.yaml = YamlReader(self.path).fechFile()
        self.init_data = init.init(self.yaml,self.fetch_init_data())
        self.swaggerPaths = YamlProcessor(self.yaml).YamlProcessorMain()
        self.pars = SwaggerSpecAnalys(self.swaggerPaths).SwaggerSpecAnalysMain()

    def fetch_init_data(self):
        init_data = OrderedDict()
        for table_name in ContentData.content_data.keys():
            if 0 < ContentData.content_data[table_name].rowCount :
                init_data[table_name] = []
            for rc in range(ContentData.content_data[table_name].rowCount):
                init_data[table_name].append([])
                for cc in range(ContentData.content_data[table_name].columnCount):
                    init_data[table_name][rc].append(ContentData.content_data[table_name].getValueAt(rc, cc))
        return init_data


    def list_up(self):
        self.cr = CreateRequest(self.pars,self.init_data)
        a = self.cr.fetch_list(ContentData.content_data['end_point'].rowCount)
        return a
