#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
from collections import OrderedDict

class YamlReader():
    """docstring for YamlReader."""
    def __init__(self, path):
        yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,lambda loader, node: OrderedDict(loader.construct_pairs(node)))
        f   = open(path,'r+')
        self.file= yaml.load(f)

    def fechFile(self):
        return self.file

class YamlProcessor(YamlReader):
    """docstring for YamlProcessor."""
    def __init__(self, data):
        self.data = data
        self.keys = self.fetchYamlKeys(data)
        self.yamlData = {}
        for key in self.keys:
            if key in ["paths","definitions","securityDefinitions"]:
                self.yamlData[key] = self.data[key]

    def YamlProcessorMain (self):
        if not self.keys: return 0
        return self.yamlParser(self.keys,self.data)

    def fetchYamlKeys(self,data):
        yamlKeys = data.keys()
        return yamlKeys;

    def getdata (self,keys,data,path):
        path.append(keys[0])
        if len(keys) < 2:
            d = data[keys[0]]
            path.pop()
            return d
        d = self.getdata(keys[1:],data[keys[0]],path)
        path.pop()
        return d

    def processingYamlData(self,data,path):
        self.yamlParser(data.keys(),data,path)

    def appendData(self,data,adddata,path):
        if len(path) > 1 :
            data[path[0]] = self.appendData(data[path[0]],adddata,path[1:])
        elif len(path) == 1:
            data[path[0]] = self.appendData(data[path[0]],adddata,[])
        else:
            return adddata
        return data
    def yamlParser(self,keys,data,path=[]):
        for key in keys:
            if isinstance(data[key],dict):
                path.append(key)
                self.processingYamlData(data[key],path)
                path.pop()
        return self.yamlData
