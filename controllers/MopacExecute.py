#! /usr/bin/env python
#coding=utf-8
'''
Created on 2012-7-24

@author: sytmac
'''
import threading
from controllers.Mopac import Mopac
def DealWithMopac(MopacFile):
    m=Mopac(MopacFile)
    m.Gasphase_MopToOut()
    #m.Fluentphase_MopToOut()
'''
t1=threading.Thread(target=DealWithMopac,args=('/home/est863/workspace/863program/src/formopac/toluene.mop',))
t1.start()
'''