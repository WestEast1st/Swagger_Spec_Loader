#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
def writeMd(title,data,dt_now):
    f = open('../payload'+dt_now+'.txt','a')
    f.write('# '+title+'\n')
    f.write('```\n')
    f.write(data)
    f.write('```\n\n')
    f.close()

def param(param,dt_now):
    #f = open('output'+dt_now+'.csv', 'a')
    #writer = csv.writer(f, lineterminator='\n')
    print ""
    print param['method']," ",param['uri']
    print "path"+"   ",param['path']
    print "query"+"  ",param['query']
    print "body"+"   ",param['body']
    column = ['method','uri','MU','type','paraname','paratype']
    #writer.writerow(column)
    paraLen = len(param['path'])+len(param['query'])+len(param['body'])
    print paraLen
