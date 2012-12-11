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

t1=threading.Thread(target=DealWithMopac,args=('toluene.mop',))
t1.start()
