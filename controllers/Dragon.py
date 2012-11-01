#!usr/bin/env python
# coding: utf-8
from config.settings import  globalpath
import subprocess
from controllers.PathInit import ParseInitPath
import shutil
import re
import time
import os
from  controllers.XmlCreate import write_xml
#调用不同的分子计算符软件进行分子描述符计算参数分别为DRAGON,GAUSSIAN,MOPAC
class Dragon(object):
    def __init__(self,filePath):
        self.parse=ParseInitPath(globalpath+'config/InitPath.xml')
        #dragon的filepath是xmlCreate生成的xml路径，默认在此文件夹中
        self.OrderPath=self.parse.get_xml_data(globalpath+'config/InitPath.xml','DRAGON')
        #self.InputFile=filePath #public variable       
        #to gain input file name such as i.mop
        self.Inputfilename=filePath
        #to gain input file name without extension such as i
        self.InputfilenameWithoutExt=self.Inputfilename.split('.')[0]
        #to gain input file extension
        self.InputfileExt=self.Inputfilename.split('.')[-1]
        #####################################################################################################
        #build new dictionary 
        try:   
            os.mkdir(globalpath+'fordragon/'+self.InputfilenameWithoutExt)
        except:
            None
        self.InputFilepath=globalpath+'fordragon/'+self.InputfilenameWithoutExt+'/'  
        try:
            shutil.move(filePath, self.InputFilepath+ self.Inputfilename)
        except:
            None
            ####################################################################################################
    def DealWithMolFile(self):
        wx=write_xml()
        wx.set_tag(self.InputFilepath+self.Inputfilename, self.InputFilepath+self.InputfilenameWithoutExt+'.drs')
        #dragon6shell -s .drs to get the result 
        Cmd=self.OrderPath+self.InputFilepath+self.InputfilenameWithoutExt+'.drs'
        print Cmd
        subprocess.Popen(Cmd,shell=True)

    