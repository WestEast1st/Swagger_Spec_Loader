#!/usr/bin/env python
# -*- coding: utf-8 -*-
from YamlReader import YamlReader

class SwaggerSpecAnalys():
    """docstring for SwaggerSpecAnalys."""
    def __init__(self, data):
        self.data = data

    def SwaggerSpecAnalysMain (self) :
        data = self.data['paths']
        specData = {}
        for uri in data.keys():
            if "$ref" in data[uri].keys():
                data[uri] = self.linkAnalys(data[uri]["$ref"])
            specData[uri] = {}
            for method in data[uri].keys():
                specData[uri][method] = self.reFecheData(data[uri][method],method)
        return specData

    def fecheRefData(self,keys,data):
        if len(keys) < 2:
            return data[keys[0]]
        return self.fecheRefData(keys[1:],data[keys[0]])

    def reFecheData(self,data,indexKey):
        if isinstance(data, dict):
            return self.reFecheDataDict(data,indexKey)
        elif isinstance(data, list):
            return self.reFecheDataList(data)
        return data

    def linkAnalys (self,path):
        ref = path.split('/')
        if '#' == ref[0]:
            data = self.fecheRefData(ref[1:],self.data)
        else:
            data = YamlReader(path).fechFile()
        return data

    def reFecheDataDict(self,data,indexKey):
        if "$ref" in data.keys():
            retdata = self.linkAnalys(data["$ref"])
            del data["$ref"]
            data = retdata
        for index in data.keys():
            data[index] = self.reFecheData(data[index],index)
        return data

    def reFecheDataList(self,list):
        for index in range(len(list)):
            list[index] = self.reFecheData(list[index],index)
        return list
