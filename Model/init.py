#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

def init (yamlData,init_data):
    ret = {}
    if 'host' in yamlData.keys():
        host = yamlData['host']
    else :
        host = 'test'
    if 'basePath' in yamlData.keys():
        ret['basePath'] = yamlData['basePath']
    else:
        ret['basePath'] = "/"
    ret['time'] = str(datetime.datetime.now())
    if 'set_head' in init_data.keys():
        ret['header'] = {'Host':host,'Content-Type':'application/json'}
        for i in init_data['set_head']:
            ret['header'][i[0]] = i[1]
    else :
        ret['header'] = {'Host':host,'Content-Type':'application/json'}
    if 'auth_token' in init_data.keys():
        ret['header']['Authorization'] = []
        for ds in init_data['auth_token']:
            ret['header']['Authorization'].append({'type':ds[0],'token':ds[1]})
    if 'set_param' in init_data.keys():
        ret['param'] = {}
        for i in init_data['set_param']:
            ret['param'][i[0]] = i[1]
    else :
        ret['param'] = {}
    return ret
