#! /usr/bin/env python
#coding=utf-8
from config.settings import  globalpath
import subprocess
from controllers.PathInit import ParseInitPath
import shutil
import re
import time
import os
#调用不同的分子计算符软件进行分子描述符计算参数分别为DRAGON,GAUSSIAN,MOPAC
class Mopac():
    '''
    to deal with mop file and get molecular descriptor
    '''
    def __init__(self,filePath):
        self.parse=ParseInitPath(globalpath+'config/InitPath.xml')
        #dragon的filepath是xmlCreate生成的xml路径，默认在此文件夹中
        self.OrderPath=self.parse.get_xml_data(globalpath+'config/InitPath.xml','MOPAC')
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
            os.mkdir(globalpath+'formopac/'+self.InputfilenameWithoutExt)
        except:
            None
        self.InputFilepath=globalpath+'formopac/'+self.InputfilenameWithoutExt+'/'  
        try:
            shutil.move(filePath, self.InputFilepath+ self.Inputfilename)
        except:
            None
            ####################################################################################################
        if(cmp(self.InputfileExt,'mop')==0):
            print'InputFile is mop file'
        elif (cmp(self.InputfileExt,'mol')==0):
            self.OrientationFromMolToMop()
            print'InputFile is mol file'
        self.Mopfilename=self.InputfilenameWithoutExt+'.mop'
        self.GasMopfile=self.InputfilenameWithoutExt+'Gas.Mop'
        self.FluentMopfile=self.InputfilenameWithoutExt+'Flu.Mop'
    ##produce mop file with corresponding  mol file
    def OrientationFromMolToMop(self):
        pass
    def Gasphase_MopToOut(self):
        f=open(self.InputFilepath+self.Mopfilename,'r')
        lines=f.readlines()
        f.close()
        lines[0]='PM6 COSMO  CHARGE=0 EF ESP GNORM=0.100 MULLIK POLAR SHIFT=80\n'
        f=open(self.InputFilepath+self.GasMopfile,'w')
        f.writelines(lines)
        f.close()
        
        if(os.path.isfile(self.InputFilepath+self.InputfilenameWithoutExt+'Gas.out')==True):
            f=open(self.InputFilepath+self.InputfilenameWithoutExt+'Gas.out','r')
            lines=f.readlines();
            length=len(lines)
            f.close()
            regex=".*MOPAC DONE.*"
            if(re.match(regex,lines[length-1])!=None):
                self.ParameterExtractFromOut(self.InputFilepath+self.InputfilenameWithoutExt+'Gas.out')
            else:
                while(re.match(regex,lines[length-1])==None):
                    time.sleep(0.1)
                    lines=f.readlines()
                    length=len(lines)
                self.ParameterExtractFromOut(self.InputFilepath+self.InputfilenameWithoutExt+'Gas.out')               
        else:
            Cmd=self.OrderPath+self.InputFilepath+self.GasMopfile
            subprocess.Popen(Cmd,shell=True)
               
            #whether Gas.out does exist and out file has been produced completely
            while (os.path.isfile(self.InputFilepath+self.InputfilenameWithoutExt+'Gas.out')==False) :
                continue
            #time.sleep(0.5)
            
            #to measure the out file
            #####################################################################
            f=open(self.InputFilepath+self.InputfilenameWithoutExt+'Gas.out','r')
            lines=f.readlines();
            length=len(lines)
            #print lines
            regex=".*MOPAC DONE.*"
            while(length==0):
                lines=f.readlines();
                length=len(lines)
            while(re.match(regex,lines[length-1])==None):
                time.sleep(0.1)
                lines=f.readlines()
                length=len(lines)
                #print lines[length-1]
            f.close()
            ###################################################################
            self.ParameterExtractFromOut(self.InputFilepath+self.InputfilenameWithoutExt+'Gas.out')
    def Fluentphase_MopToOut(self):
        f=open(self.InputFilepath+self.Mopfilename,'r')
        lines=f.readlines()
        f.close()
        lines[0]='PM6 eps=78.6 CHARGE=0 EF ESP GNORM=0.100 MULLIK POLAR SHIFT=80\n'
        f=open(self.InputFilepath+self.FluentMopfile,'w')
        f.writelines(lines)
        f.close()
        
        Cmd=self.OrderPath+self.InputFilepath+self.FluentMopfile
        subprocess.Popen(Cmd,shell=True)
        
        #self.ParameterExtractFromOut(self.InputFilepath+self.InputfilenameWithoutExt+'Flu.out')
    def ParameterExtractFromOut(self,OutFile):
        self.NetAtomicCharges=[]
        self.ParameterList=[]
        j=1
        k=0
        f=open(OutFile,'r')
        lines=f.readlines()        
        f.close()
        for lineNum in range(len(lines)):
            if(re.match('.*ATOM NO\..*TYPE.*CHARGE.*No\.',lines[lineNum])!=None):
                while(re.match('.*DIPOLE.*',lines[lineNum+j])==None):
                    List=list(lines[lineNum+j].split(' '))
                    while(1):
                        try:
                            List.remove('')
                        except:
                            break
                    j=j+1
                    self.NetAtomicCharges.append(List)
                DIPOLE=lines[lineNum+j+3].split(' ')[-1]
            if(re.match('.*HEAT OF FORMATION.*',lines[lineNum])!=None):
                while(re.match('.*MOLECULAR.*DIMENSIONS.*',lines[lineNum+k])==None):

                    List=list(lines[lineNum+k].split(' '))
                    while(1):
                        try:
                            List.remove('')
                        except:
                            break
                    k=k+1
                    self.ParameterList.append(List)
                    #print list
                    #######remove '\n' in  ParameterList
        print self.ParameterList
        while(1):
            try:
                self.ParameterList.remove(['\n'])
            except:
                break
        #print self.ParameterList
        try:
            HOFKCAL= float(self.ParameterList[0][5])
            HOFKJ=float(self.ParameterList[0][8])
            #print self.ParameterList[1][3]
            TE=float(self.ParameterList[1][3])
            EE=float(self.ParameterList[2][3])
            CCR=float(self.ParameterList[3][3])
            CA=float(self.ParameterList[4][3])
            CV=float(self.ParameterList[5][3])
            IonizationPotential=float(self.ParameterList[7][3])
            HOMO=float(self.ParameterList[8][5])
            LOMO=float(self.ParameterList[8][6])
            MV=float(self.ParameterList[10][3])
        except:
            print "self.ParameterList"+str(self.ParameterList)
                    ###############################################################
                    
        Qmax=-1.0
        Qmin=1.0
        for i in range(len(self.NetAtomicCharges)):
            if (float(self.NetAtomicCharges[i][2])>Qmax):
                Qmax=float(self.NetAtomicCharges[i][2])
            if (float(self.NetAtomicCharges[i][2])<Qmin):
                Qmin=float(self.NetAtomicCharges[i][2])
        QHmax=-1.0
        QHmin=1.0
        QCmax=-1.0
        QCmin=1.0
        for i in range(len(self.NetAtomicCharges)):
            if(self.NetAtomicCharges[i][1]=='H'):
                if (float(self.NetAtomicCharges[i][2])>QHmax):
                    QHmax=float(self.NetAtomicCharges[i][2])
                if (float(self.NetAtomicCharges[i][2])<QHmin):
                    QHmin=float(self.NetAtomicCharges[i][2])
            if(self.NetAtomicCharges[i][1]=='C'):
                if (float(self.NetAtomicCharges[i][2])>QCmax):
                    QCmax=float(self.NetAtomicCharges[i][2])
                if (float(self.NetAtomicCharges[i][2])<QCmin):
                    QCmin=float(self.NetAtomicCharges[i][2])
                    ##################################################################
        #polarizability
        polarizability=0.0
        length=len(lines)-1
        while(length>=0):
            if(re.match('.*ISOTROPIC.*AVERAGE.*ALPHA.*',lines[length])!=None):
                lines[length].strip()
                List=list(lines[length].split(' '))
                while(1):
                    try:
                        List.remove('')
                    except:
                        break
                polarizability=float(List[4])
                
                break
            length=length-1
        print "mop parameter computation finished"
'''
m=Mopac('ben.mop')
m.Gasphase_MopToOut()
'''
#m.ParameterExtractFromOut("/home/est863/workspace/863program/src/formopac/ben/benGas.out")