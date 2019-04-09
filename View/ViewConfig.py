import sys
sys.path.append("./Model")
from YamlReader import YamlReader
sys.path.append("../")
from collections import OrderedDict

config = YamlReader("./.config.yml").fechFile()
tabs   = config['info'].keys()
