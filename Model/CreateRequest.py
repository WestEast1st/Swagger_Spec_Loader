#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Output
from burp import IBurpExtender
from burp import IBurpExtenderCallbacks
import CreateTab
import urllib
import urlparse
from collections    import OrderedDict


class CreateRequest():
    def __init__ (self, pars, initData):
        self.params     = []
        self.initData   = initData
        print initData
        self.pars       = pars
        self.types      = ['path','body','query','formData']

    def fetch_list(self,num):
        ret_list = []
        if num:
            count = num+1
        else:
            count = 1
        for uri in self.pars.keys():
            for method in self.pars[uri].keys():
                if 'parameters' in self.pars[uri][method].keys():
                    self.create_param(uri,method)
                paramData   = OrderedDict()
                for param in self.params:
                    for type in self.types:
                        paramData[type] = self.paramDistribution(type,param)
                if 'head' in param.keys():
                    head = param['head']
                else :
                    head = ''
                header = self.createHeader(head)
                if paramData['body']:
                    body = '{'
                    for i in range(len(paramData['body'])):
                        if i < len(paramData['body'])-1:
                            body += paramData['body'][i]+","
                        else:
                            body += paramData['body'][i]
                    body += '}'
                elif paramData['formData'] :
                    body = '&'.join(paramData['formData'])
                else:
                    body = ''
                tmp_dict = OrderedDict()

                tmp_dict['#'] ='{0:03d}'.format(count)
                tmp_dict['Host'] = self.initData['header']["Host"]
                tmp_dict['Method'] = method.upper()
                tmp_dict['Base Path'] = self.initData['basePath']
                tmp_dict['End Point'] = paramData['path']
                tmp_dict['Query'] = paramData['query']
                tmp_dict['Header'] = header
                tmp_dict['Body'] = body
                ret_list.append(tmp_dict)
                count += 1
        return ret_list

    def create_param(self,uri,method):
        parameters              = self.fetchParameters(self.pars[uri][method]["parameters"])
        parameters['method']    = method
        parameters['uri']       = uri
        if 'consumes' in self.pars[uri][method].keys():
            parameters['head']  = self.pars[uri][method]['consumes'][0]
        self.params.append(parameters)

    def create (self) :
        for uri in self.pars.keys():
            #method別のパラメタの取り出し
            for method in self.pars[uri].keys():
                if 'parameters' in self.pars[uri][method].keys():
                    self.create_param(uri,method)
        self.requestCreater()

    def fetchParameters (self,parameters={}):
        data = {}
        for type in self.types:
            data[type] = []
        for parameter in parameters:
            for type in self.types:
                if parameter['in'] == type:
                    parametersData = self.ifTypeProcessing(type,parameter)
                    if parametersData:
                        for param in parametersData.keys():
                            for changeParam in self.initData['param'].keys():
                                if param == changeParam:
                                    parametersData[param] = self.initData['param'][changeParam]
                        data[type].append(parametersData)
        return data

    def fecheSchemaProperties(self,data):
        body = {}
        for param in data.keys():
            if 'description' in data[param].keys():
                if data[param]['type'] == 'integer':
                    body[param] = 0
                elif data[param]['type'] == 'string':
                    body[param] = data[param]['description']
            elif 'type' in data[param].keys():
                if data[param]['type'] == 'integer':
                    body[param] = 0
                elif data[param]['type'] == 'string':
                    body[param] = 'string'
        return body
    def ifTypeProcessing (self,type,parameter):
        keys = parameter.keys()
        if type not in ['body','formData']:
            return {parameter['name']:parameter['type']}

        if 'schema' not in keys:
            if type in ['formData']:
                return {parameter['name']:parameter['description']}
        else:
            schemaKeys = parameter['schema'].keys()

        if 'items' in schemaKeys:
            bodyParams = parameter['schema']['items']['properties']
            return self.fecheSchemaProperties(bodyParams)

        elif 'properties' in schemaKeys:
            bodyParams = parameter['schema']['properties']
            return self.fecheSchemaProperties(bodyParams)
        else:
            pass

    def replaceParamUri(self,data):
        for path in data['path']:
            for changeParam in self.initData['param'].keys():
                if path.keys()[0] == changeParam:
                    data['uri'] = data['uri'].replace('{'+changeParam+'}',str(self.initData['param'][changeParam]))
            for rep in path.keys():
                if path[rep] == 'integer': repdata = '9999'
                elif path[rep] == 'string': repdata = 'string'
                else : repdata = 'test'
                data['uri'] = data['uri'].replace('{'+rep+'}',repdata)
        return data['uri']

    def createQuery(self,data):
        uri = []
        for query in data['query']:
            for key in query.keys():
                if query[key] == 'integer': query[key] = '9999'
                elif query[key] == 'string': query[key] = 'string'
                else : query[key] = 'test'
            for changeParam in self.initData['param'].keys():
                for key in query.keys():
                    if changeParam == key:
                        query[key] = self.initData['param'][key]
            for key in query.keys():
                uri.append(key+'='+str(query[key]))
        query = '?'+'&'.join(uri)
        return query

    def operatJsonBody(self,data):
        bodyList = []
        for bodys in data['body']:
            for body in bodys.keys():
                if isinstance(bodys[body],int):
                    param = str(bodys[body])
                else :
                    param = "\""+bodys[body]+"\""
                bodyList.append(str((body+":"+param).encode('utf-8')))
        return bodyList

    def operatFormDataBody(self,data):
        bodyList = []
        for bodys in data['formData']:
            for body in bodys.keys():
                bodyList.append(str((body+"="+urllib.quote(bodys[body]).replace("%20",'+')).encode('utf-8')))
        return bodyList

    def paramDistribution(self,paramType,param):
        if paramType not in self.types: return -1
        length = len(param[paramType])
        if not length :
            if paramType == 'path':
                return param['uri']
            return ''
        if paramType == 'path':
            return self.replaceParamUri(param)
        elif paramType == 'query':
            return self.createQuery(param)
        elif paramType == 'body':
            return self.operatJsonBody(param)
        elif paramType == 'formData':
            return self.operatFormDataBody(param)

    def createHeader(self,consumes = ''):
        header = {}
        for head in self.initData['header'].keys():
            if isinstance(self.initData['header'][head],list):
                for token in self.initData['header'][head]:
                    header[head] = token['type']+" "+token['token']
            else:
                header[head] = self.initData['header'][head]
        if consumes :
            header['Content-Type'] = consumes
        data = ""
        for headType in header.keys():
            data += headType+": "+header[headType]+"\n"
        return data

    def requestCreater(self):
        c = 1
        for param in self.params:
            paramData   = {}
            method      = param['method'].upper()
            uri         = param['uri']
            httpv       = "HTTP/1.1"
            for type in self.types:
                paramData[type] = self.paramDistribution(type,param)
            uriInQuery = "".join([self.initData['basePath'],paramData['path'],paramData['query']])
            top = " ".join([method,uriInQuery,httpv])
            #header展開
            if 'head' in param.keys():
                head = param['head']
            else :
                head = ''
            header = self.createHeader(head)
            if paramData['body']:
                body = '{'
                for i in range(len(paramData['body'])):
                    if i < len(paramData['body'])-1:
                        body += paramData['body'][i]+","
                    else:
                        body += paramData['body'][i]
                body += '}'
            elif paramData['formData'] :
                body = '&'.join(paramData['formData'])
            else:
                body = ''
            if self.callbacks:
                request = "\n".join([top,header,body,"\n"])
                name = "".join([method,"  ",self.initData['basePath'],uri])
                print request
                #CreateTab.sendToIntruder(self.callbacks,self.initData['header']["Host"],request,name)
                #CreateTab.sendToRepeater(self.callbacks,self.initData['header']["Host"],request,name)
            else :
                Output.writeMd(param['method'].upper()+"  "+self.initData['basePath']+param['uri'],top+"\n"+header+"\n"+body+"\n\n","aaaaa")
            c += 1
