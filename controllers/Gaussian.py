#! /usr/bin/env python
#coding=utf-8
'''
Created on 2012-7-12

@author: sytmac
'''
from config.settings import  globalpath
import subprocess
from controllers.PathInit import ParseInitPath
import shutil
import re
import time
import os
import traceback
#调用不同的分子计算符软件进行分子描述符计算参数分别为DRAGON,GAUSSIAN,MOPAC

class Gaussian():
    InputExceptionFlag=False
    __ElectronstaticPotentialMeanValue= 0
    __PositiveElectronstaticPotentialMeanValue=0
    __NegativeElectronstaticPotentialMeanValue=0
    __MostPositiveElectronstaticPotential=0
    __MostNegativeElectronstaticPotential=0
    __outputNegativeNumbers=0
    __outputPositiveNumbers=0
    __averageDispersion=0
    __varianceOfNegativeElectronstaticPotential=0
    __varianceOfPositiveElectronstaticPotential=0
    __BalanceConstant=0
    
    __AtomicCharges=[]
    __Qmin=0.0
    __Qmax=0.0
    
    __BindEnergy=0.0
    __IonizationPotential=0.0
    __ElectronAffinity=0.0
    __ElectronProtonation=0.0
     
    __LUMO=0
    __HOMO=0
    __AbsoluteHardness=0
    __ChemicalPotential=0
    __ElectrophilicityIndex=0
    __CCR=0
    togo=0;
    def __init__(self,filePath):
        self.parse=ParseInitPath(globalpath+'config/InitPath.xml')
        #dragon的filepath是xmlCreate生成的xml路径，默认在此文件夹中
        self.OrderPath=self.parse.get_xml_data(globalpath+'config/InitPath.xml','GAUSSIAN')

        self.Inputfilename=filePath
        #to gain input file name without extension such as i.gif
        self.InputfilenameWithoutExt=self.Inputfilename.split('.')[0]
        try:   
            os.mkdir(globalpath+'forguassian/'+self.InputfilenameWithoutExt)
        except:
            None
        self.InputFilepath=globalpath+'forguassian/'+self.InputfilenameWithoutExt+'/'   
        try:
                shutil.move(filePath, self.InputFilepath+self.Inputfilename)
        except:
                print 'no file of .gjf to move'     
        #to amend parameter of the input file such as %chk % nproc % mem
        #################################################################################### 
        regex="%chk=.*"
        regex1="%nproc.*=[1-9]"
        regex2="%mem=\d{0,3}[g,G][b,B]"        
        f=open(self.InputFilepath+self.Inputfilename,'r')
        num=0
        lines=f.readlines()      
        f.close()
        lineNum=0
        for line in lines:
            if re.match(regex,line)!=None:
                num=num+1
                lines[lineNum]=re.sub(regex,"%chk="+self.InputfilenameWithoutExt+".chk",line)       
            if re.match(regex1,line)!=None:
                num=num+1
                lines[lineNum]=re.sub(regex1,'%nproc=2',line) 
            if re.match(regex2,line)!=None:
                num=num+1
                lines[lineNum]=re.sub(regex2,'%mem=2GB',line) 
            if num==3:
                break;
            lineNum=lineNum+1
        f=open(self.InputFilepath+self.Inputfilename,'w')
        f.writelines(lines)
        f.close()
        #####################################################################################
    #得到各个分子计算符软件的路径,进行命令行操作               
    def GjfParameterChange(self,Filename,regex,CommandGasPhase):
        #regex="#p.*"
        #CommandGasPhase='#p rb3lyp/6-31+g(d,p) opt freq polar'
        f=open(Filename,'r')
        lines=f.readlines()
        lineNum=0
        for line in lines: 
            if re.match(regex,line)!=None:
                lines[lineNum]=re.sub(regex,CommandGasPhase,line) 
                break
            lineNum=lineNum+1
        lines.append('\n\r')
        lines.append('\n\r')
        f.close()
        f=open(Filename,'w')
        f.writelines(lines)
        f.close()
    def GjfParameterChangeAndSaveChanged(self,Filename,regex,CommandGasPhase,savedFile):
        regex1="#p.*"
        CommandGasPhase1='#p sp'
        regex2='^0.?1'
        CommandGasPhase2='12'
        f=open(Filename,'r')
        lines=f.readlines()
        lineNum=0
        ReplaceNum=0
        for line in lines: 
            if re.match(regex1,line)!=None:
                lines[lineNum]=re.sub(regex1,CommandGasPhase1,line) 
                ReplaceNum=ReplaceNum+1
            if re.match(regex2,line)!=None:
                lines[lineNum]=re.sub(regex2,CommandGasPhase2,line) 
                ReplaceNum=ReplaceNum+1
            if(ReplaceNum==2):
                break
            lineNum=lineNum+1
        f.close()
        f=open(savedFile,'w')
        f.writelines(lines)
        f.close()
    def InputFileValidityCheck(self,filelines,length,regex):
        #print filelines     
        if(re.match(regex,filelines[length-3])!=None):
            print "error termination"
            return False
    def GasPhaseParameterCompute(self):
        path=self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog'
        if(os.path.exists(path)==False):
            self.GjfParameterChange(self.InputFilepath+self.Inputfilename,'#p.*','#p rb3lyp/6-31+g(d,p) opt freq polar')       
                                #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
            Cmd=self.OrderPath+self.InputFilepath+self.Inputfilename+' '+self.InputfilenameWithoutExt+'.Gasoptlog'
            subprocess.Popen(Cmd,shell=True)
            while(1):
                try:
                    f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')
                    break
                except:
                    continue
        #####################################################################to check the file to the end
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')
        lines=f.readlines();
        length=len(lines)
        regex=".*Normal termination.*"
        regex2=".*Error termination.*"
        while(length==0):
            lines=f.readlines();
            length=len(lines)
        while(re.match(regex,lines[length-1])==None):
            time.sleep(1)                  
            if(length==0):
                continue
            else:
                f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')
                lines =f.readlines()            
                length=len(lines)
                f.close()
                #print lines[length-1]
                if(self.InputFileValidityCheck(lines,length,regex2)==False):
                    self.InputExceptionFlag=True
                    return;
                
        f.close()
                    ###################################################################
        #search for Mulliken atomic charges:
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')
        lines=f.readlines()
        length=len(lines)
        f.close()
        while(length):
            length=length-1
            #to eject ' ' appeared in first and last position
            lines[length]=str(lines[length]).strip()
            #to find and save element and atomic charges to list
            if(re.match('Mulliken atomic charges:',lines[length])!=None):
                j=2
                line=lines[length+j].split(' ')
                while(re.match('Sum.*',line[0])==None):
                    List=list(line)

                    while(1):
                        try:
                            List.remove('')
                        except:
                            break
                    List.pop(0)
                    j=j+1
                    line=lines[length+j].split(' ')
                    self.__AtomicCharges.append(List)

                break
        print "GasPhaseParameterCompute has been finished"
    def Gasoptlogfile_produce(self):
        self.GjfParameterChange(self.InputFilepath+self.Inputfilename,'#p.*','#p rb3lyp/6-31+g(d,p) opt freq polar')       
                            #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
        Cmd=self.OrderPath+self.InputFilepath+self.Inputfilename+' '+self.InputfilenameWithoutExt+'.Gasoptlog'
        subprocess.Popen(Cmd,shell=True)
        #####################################################################to check the file to the end
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')
        lines=f.readlines();
        length=len(lines)
        regex=".*Normal termination.*"
        while(length==0):
            lines=f.readlines();
            length=len(lines)
        while(re.match(regex,lines[length-1])==None):
            time.sleep(1)                  
            if(length==0):
                continue
            else:
                f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')
                lines =f.readlines()            
                length=len(lines)
                f.close()
                print str(length)+' '+lines[length-1]
        f.close()
        ###################################################################               
        print "Gasoptlogfile_produce has been finished " 
    def IPlogfile_produce(self):
        #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
        Cmd=self.OrderPath+self.InputFilepath+self.Inputfilename+' '+self.InputfilenameWithoutExt+'.IPlog'
        subprocess.Popen(Cmd,shell=True)
        while(1):
            try:
                f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.IPlog','r')
            except:
                continue
            else:
                break
        #####################################################################to check the file to the end
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.IPlog','r')
        lines=f.readlines();
        length=len(lines)
        regex=".*Normal termination.*"
        while(length==0):
            lines=f.readlines();
            length=len(lines)
        while(re.match(regex,lines[length-1])==None):
            time.sleep(1)                  
            if(length==0):
                continue
            else:
                f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.IPlog','r')
                lines =f.readlines()            
                length=len(lines)
                f.close()
                print str(length)+' '+lines[length-1]
        f.close()
                    ###################################################################
        print "IPlogfile_produce has been finished "
    def EAlogfile_produce(self):
                #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
        Cmd=self.OrderPath+self.InputFilepath+self.Inputfilename+' '+self.InputfilenameWithoutExt+'.EAlog'
        subprocess.Popen(Cmd,shell=True)
        while(1):
            try:
                f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.EAlog','r')
            except:
                continue
            else:
                break
        #####################################################################to check the file to the end
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.EAlog','r')
        lines=f.readlines();
        length=len(lines)
        regex=".*Normal termination.*"
        while(length==0):
            lines=f.readlines();
            length=len(lines)
        #print "length of Gasoptlog:"+str(length)
        while(re.match(regex,lines[length-1])==None):
            time.sleep(1)                  
            if(length==0):
                continue
            else:
                f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.EAlog','r')
                lines =f.readlines()            
                length=len(lines)
                f.close()
                print str(length)+' '+lines[length-1]
                #break
        f.close()
                    ###################################################################
        print "EAlogfile_produce has been finished "
    def EPlogfile_produce(self):
                        #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
        Cmd=self.OrderPath+self.InputFilepath+self.Inputfilename+' '+self.InputfilenameWithoutExt+'.EPlog'
        subprocess.Popen(Cmd,shell=True)
        while(1):
            try:
                f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.EPlog','r')
            except:
                continue
            else:
                break
        #####################################################################to check the file to the end
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.EPlog','r')
        lines=f.readlines();
        length=len(lines)
        regex=".*Normal termination.*"
        while(length==0):
            lines=f.readlines();
            length=len(lines)
        while(re.match(regex,lines[length-1])==None):
            time.sleep(1)                  
            if(length==0):
                continue
            else:
                f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.EPlog','r')
                lines =f.readlines()            
                length=len(lines)
                f.close()
                print str(length)+' '+lines[length-1]
                #break
        f.close()
                    ###################################################################
    def GasPhase_MolecularDipoleMoment(self):
        #first search for'completed'appeared first time 
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')       
        lines =f.readlines()
        f.close()
        for i in range(len(lines)):
            if(re.match('.*completed.*',lines[i])!=None):
                print lines[i]
                print '\n'
                j=i+1
                while(j<len(lines)):
                    if(re.match('.*Tot=.*',lines[j])!=None):
                        DipoleMomentline=re.findall('Tot=.*',lines[j])
                        DipoleMoment=float(str(DipoleMomentline[0]).split(' ')[-1])
                        print DipoleMoment
                        break
                    j=j+1
                break
        
        return DipoleMoment
    def GasPhase_MolecularPolarizability(self):
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')
        lines =f.readlines()
        f.close()
        for i in range(len(lines)):
            if(re.match('.*Isotropic polarizability.*',lines[i])!=None):
                print lines[i]
                Polarizability=float(str(lines[i]).split(' ')[-2])
                print Polarizability
                print '\n'
                break
        del lines
        return Polarizability
    def GasPhase_MolecularVolume(self):
        #to create gjf file for computing
        # save standard orientation in log file
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')
        lines =f.readlines()
        f.close()
        lineNum=len(lines)-1
        while((lineNum>=0)and(re.match('.*Standard orientation:.*',lines[lineNum])==None)):
            lineNum=lineNum-1
        lineNum=lineNum+5
        orientationLines=[]
        #lines of standard orientation
        orientationLineNum=0
        while(re.match('.*----.*',lines[lineNum])==None):
            orientationLines.append(lines[lineNum].split()[-3]+' '+lines[lineNum].split()[-2]+' '+lines[lineNum].split()[-1])
            orientationLineNum=orientationLineNum+1
            lineNum=lineNum+1
        #print orientationLines
            ##########################################################################################################
            #to revise .gjf file with standard orientation 
        regex="#p.*"
        CommandGasPhase='#p rb3lyp/6-31+g(d,p) sp volume polar'
        f=open(self.InputFilepath+self.Inputfilename,'r')
        GjfLines=f.readlines()
        #print "GjfLines: "+str(GjfLines)
        lineNum=0
        for line in GjfLines: 
            if re.match(regex,line)!=None:
                GjfLines[lineNum]=re.sub(regex,CommandGasPhase,line) 
                break
            lineNum=lineNum+1
            
        lineNum=len(GjfLines)-1
        #print lineNum
        while(cmp(GjfLines[lineNum],'\r\n')==0):
            lineNum=lineNum-1
        #print orientationLineNum
        oritationLineNum=0
        for i in range(lineNum-orientationLineNum+1,lineNum+1):  
                    
            try:
                s=' '+GjfLines[i].split(' ')[1]+'        '+orientationLines[oritationLineNum].split(' ')[0]+'    '+orientationLines[oritationLineNum].split(' ')[1]+'    '+orientationLines[oritationLineNum].split(' ')[2]+'\r\n'
                oritationLineNum=oritationLineNum+1
                GjfLines[i]=s
            except:
                #print "volume compute except: "+str(GjfLines[i].split(' '))
                pass
        GjfLines.append("\n\r")
        GjfLines.append("\n\r")
        f.close()
        f=open(self.InputFilepath+self.Inputfilename,'w')
        f.writelines(GjfLines)
        f.close()
        del GjfLines
        
        ############################################################################################################
        Cmd=self.OrderPath+self.InputFilepath+self.Inputfilename
        subprocess.Popen(Cmd,shell=True)
        #search the prduced .log file for Molar volme
        wait=1
        while(wait):
            try:
                f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')
            except:
                None
            else:
                wait=0
        #time.sleep(3)
        Loglines=f.readlines()
        f.close()        
        regex=".*Molar volume =.*"
        for Logline in Loglines:      
            if (re.match(regex,Logline)!=None):
                volume=Logline.split(' ')[-2]
                print 'volume: '+volume
                break
    def GasPhase_MolecularHOMOAndLUMOAndAbsolut_Hardness(self):
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')
        lines =f.readlines()
        f.close()
        regex='.*Alpha  occ. eigenvalues.*'
        for lineNum in range(len(lines)):
            if(re.match(regex,lines[lineNum])!=None):
                while(re.match(regex,lines[lineNum])!=None):
                    lineNum=lineNum+1
                    #print lines[lineNum]
                List=list(lines[lineNum].split(' '))
                while(1):
                    try:
                        List.remove('')
                    except:
                        break
                self.__LUMO=List[4]
                self.__HOMO=lines[lineNum-1].split(' ')[-1]
                break
        self.__AbsoluteHardness=(float(self.__HOMO)-float(self.__LUMO))/2
        #print 'AbsoluteHardness: '+str(self.__AbsoluteHardness)
        self.__ChemicalPotential=(float(self.__HOMO)+float(self.__LUMO))/2
        try:
            self.__ElectrophilicityIndex=pow(float(self.__ChemicalPotential),2)/(2*self.__AbsoluteHardness)
        except:
            print "divisor self.__AbsoluteHardness:" +str(self.__AbsoluteHardness)
        #print self.__ElectrophilicityIndex
        del lines

    def GasPhase_CCR(self):      
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')
        lines =f.readlines()
        f.close()
        regex='.*N-N=.*'
        lineNum=len(lines)-1
        while(lineNum>=0):
            if(re.match(regex,lines[lineNum])!=None):
                List=list(lines[lineNum].split(' '))
                while(1):
                    try:
                        List.remove('')
                    except:
                        break
                self.__CCR=List[1]
                #print self.__CCR
                break
            lineNum=lineNum-1
    def GasBindEnergy(self):
        path=self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog'
        if(os.path.exists(path)==False):
            self.Gasoptlogfile_produce()    
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')
        lines =f.readlines() 
        f.close()  
        #os.remove(self.InputFilepath+self.InputfilenameWithoutExt+'.log')
        length=len(lines)-1
        while(length>=0):
            if(re.match('.*SCF Done.*',lines[length])!=None):
                List=list(lines[length].split(' '))
                while(1):
                        try:
                            List.remove('')
                        except:
                            break
                self.__BindEnergy=float(List[4])            
                break
            length=length-1

    def GasPhase_IonizationPotential(self):
        path=self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog'
        if(os.path.exists(path)==False):
            self.Gasoptlogfile_produce() 
            #to create gjf file for computing
        # save standard orientation in log file
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')
        lines =f.readlines()
        f.close()
        lineNum=len(lines)-1
        while((lineNum>=0)and(re.match('.*Standard orientation:.*',lines[lineNum])==None)):
            lineNum=lineNum-1
        lineNum=lineNum+5
        orientationLines=[]
        orientationLineNum=0
        while(re.match('.*----.*',lines[lineNum])==None):
            orientationLines.append(lines[lineNum].split()[-3]+' '+lines[lineNum].split()[-2]+' '+lines[lineNum].split()[-1])
            orientationLineNum=orientationLineNum+1
            lineNum=lineNum+1
        #print "orientationLineNum is"+str(orientationLines)
            ##########################################################################################################3
            #to reviese .ipgjf
        regex1="#p.*"
        CommandGasPhase1='#p sp'
        regex2='^0.?1'
        CommandGasPhase2='1 2'
        f=open(self.InputFilepath+self.Inputfilename,'r')
        lines=f.readlines()
        lineNum=0
        ReplaceNum=0
        for line in lines: 
            if re.match(regex1,line)!=None:
                lines[lineNum]=re.sub(regex1,CommandGasPhase1,line) 
                ReplaceNum=ReplaceNum+1
            if re.match(regex2,line)!=None:
                lines[lineNum]=re.sub(regex2,CommandGasPhase2,line) 
                ReplaceNum=ReplaceNum+1
            if(ReplaceNum==2):
                break
            lineNum=lineNum+1
        f.close()
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.IPgjf','w')
        f.writelines(lines)
        f.close()
        #print lines
            ##########################################################################################################
            #to revise .ipgjf file with standard orientation 
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.IPgjf','r')
        GjfLines=f.readlines()
        f.close()
        lineNum=len(GjfLines)-1
        #print lineNum
        while(cmp(GjfLines[lineNum],'\r\n')==0):
            lineNum=lineNum-1
        #print orientationLineNum
        oritationLineNum=0
        for i in range(lineNum-orientationLineNum+1,lineNum+1):
            try:   
                s=' '+GjfLines[i].split(' ')[1]+'     '+orientationLines[oritationLineNum].split(' ')[0]+'    '+orientationLines[oritationLineNum].split(' ')[1]+'    '+orientationLines[oritationLineNum].split(' ')[2]+'\r\n'
                oritationLineNum=oritationLineNum+1
                GjfLines[i]=s
            except:
                pass
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.IPgjf','w')
        f.writelines(GjfLines)
        f.close()
        del GjfLines
        ###################################################################################################
        #to produce .IPlog file 
        path=self.InputFilepath+self.InputfilenameWithoutExt+'.IPlog'
        if(os.path.exists(path)==False):
            self.IPlogfile_produce()
        #######################################################################################################3
            #to search scf done in IPlog file
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.IPlog','r')
        lines =f.readlines() 
        f.close()  
        #os.remove(self.InputFilepath+self.InputfilenameWithoutExt+'.log')
        length=len(lines)-1
        while(length>=0):
            if(re.match('.*SCF Done.*',lines[length])!=None):
                List=list(lines[length].split(' '))
                while(1):
                        try:
                            List.remove('')
                        except:
                            break
                self.__IonizationPotential=float(List[4])            
                break
            length=length-1       
    def GasPhase_ElectronAffinity(self):
        path=self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog'
        if(os.path.exists(path)==False):
            self.Gasoptlogfile_produce() 
            #to create gjf file for computing
        # save standard orientation in log file
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')
        lines =f.readlines()
        f.close()
        lineNum=len(lines)-1
        while((lineNum>=0)and(re.match('.*Standard orientation:.*',lines[lineNum])==None)):
            lineNum=lineNum-1
        #print lines[lineNum]
        #print '\n'
        lineNum=lineNum+5
        orientationLines=[]
        #lines of standard orientation
        orientationLineNum=0
        while(re.match('.*----.*',lines[lineNum])==None):
            orientationLines.append(lines[lineNum].split()[-3]+' '+lines[lineNum].split()[-2]+' '+lines[lineNum].split()[-1])
            #print orientationLines[orientationLineNum]
            #print'\n'
            orientationLineNum=orientationLineNum+1
            lineNum=lineNum+1
            ##########################################################################################################3
            #to reviese .ipgjf
        regex1="#p.*"
        CommandGasPhase1='#p sp'
        regex2='^0.?1'
        CommandGasPhase2='-1 2'
        f=open(self.InputFilepath+self.Inputfilename,'r')
        lines=f.readlines()
        lineNum=0
        ReplaceNum=0
        for line in lines: 
            if re.match(regex1,line)!=None:
                lines[lineNum]=re.sub(regex1,CommandGasPhase1,line) 
                ReplaceNum=ReplaceNum+1
            if re.match(regex2,line)!=None:
                lines[lineNum]=re.sub(regex2,CommandGasPhase2,line) 
                ReplaceNum=ReplaceNum+1
            if(ReplaceNum==2):
                break
            lineNum=lineNum+1
        f.close()
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.EAgjf','w')
        f.writelines(lines)
        f.close()
            ##########################################################################################################
            #to revise .ipgjf file with standard orientation 
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.EAgjf','r')
        GjfLines=f.readlines()
        f.close()
        lineNum=len(GjfLines)-1
        #print lineNum
        while(cmp(GjfLines[lineNum],'\r\n')==0):
            lineNum=lineNum-1
        #print orientationLineNum
        oritationLineNum=0
        for i in range(lineNum-orientationLineNum+1,lineNum+1):           
            try:
                s=' '+GjfLines[i].split(' ')[1]+'        '+orientationLines[oritationLineNum].split(' ')[0]+'    '+orientationLines[oritationLineNum].split(' ')[1]+'    '+orientationLines[oritationLineNum].split(' ')[2]+'\r\n'
                oritationLineNum=oritationLineNum+1
                GjfLines[i]=s
            except:
                pass
            #print s
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.EAgjf','w')
        f.writelines(GjfLines)
        f.close()
        del GjfLines
        ###################################################################################################
        #to produce .IPlog file 
        path=self.InputFilepath+self.InputfilenameWithoutExt+'.EAlog'
        if(os.path.exists(path)==False):
            self.EAlogfile_produce()
            #######################################################################################################3
            #to search scf done in IPlog file
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.EAlog','r')
        lines =f.readlines() 
        f.close()  
        #os.remove(self.InputFilepath+self.InputfilenameWithoutExt+'.log')
        length=len(lines)-1
        while(length>=0):
            if(re.match('.*SCF Done.*',lines[length])!=None):
                List=list(lines[length].split(' '))
                while(1):
                        try:
                            List.remove('')
                        except:
                            break
                self.__ElectronAffinity=float(List[4])            
                break
            length=length-1
        #print 'ElectronAffinity: '+str(self.__ElectronAffinity)
        
    def GasPhase_EnergyProtonation(self):
        print "GasPhase_EnergyProtonation begins"
        path=self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog'
        if(os.path.exists(path)==False):
            self.EPlogfile_produce() 
            #to create gjf file for computing
        # save standard orientation in log file
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Gasoptlog','r')
        lines =f.readlines()
        f.close()
        lineNum=len(lines)-1
        while((lineNum>=0)and(re.match('.*Standard orientation:.*',lines[lineNum])==None)):
            lineNum=lineNum-1
        lineNum=lineNum+5
        orientationLines=[]
        #lines of standard orientation
        orientationLineNum=0
        while(re.match('.*----.*',lines[lineNum])==None):
            orientationLines.append(lines[lineNum].split()[-3]+' '+lines[lineNum].split()[-2]+' '+lines[lineNum].split()[-1])

            orientationLineNum=orientationLineNum+1
            lineNum=lineNum+1
            ##########################################################################################################3
            #to reviese .ipgjf
        regex1="#p.*"
        CommandGasPhase1='#p sp'
        regex2='^0.?1'
        CommandGasPhase2='1 1'
        f=open(self.InputFilepath+self.Inputfilename,'r')
        lines=f.readlines()
        lineNum=0
        ReplaceNum=0
        for line in lines: 
            if re.match(regex1,line)!=None:
                lines[lineNum]=re.sub(regex1,CommandGasPhase1,line) 
                ReplaceNum=ReplaceNum+1
            if re.match(regex2,line)!=None:
                lines[lineNum]=re.sub(regex2,CommandGasPhase2,line) 
                ReplaceNum=ReplaceNum+1
            if(ReplaceNum==2):
                break
            lineNum=lineNum+1
        f.close()
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.EPgjf','w')
        f.writelines(lines)
        f.close()
            ##########################################################################################################
            #to revise .ipgjf file with standard orientation 
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.EPgjf','r')
        GjfLines=f.readlines()
        f.close()
        lineNum=len(GjfLines)-1
        #print lineNum
        while(cmp(GjfLines[lineNum],'\r\n')==0):
            lineNum=lineNum-1
        #print orientationLineNum
        oritationLineNum=0
        for i in range(lineNum-orientationLineNum+1,lineNum+1):           
            try:
                s=' '+GjfLines[i].split(' ')[1]+'        '+orientationLines[oritationLineNum].split(' ')[0]+'    '+orientationLines[oritationLineNum].split(' ')[1]+'    '+orientationLines[oritationLineNum].split(' ')[2]+'\r\n'
                oritationLineNum=oritationLineNum+1
                GjfLines[i]=s
            except:
                pass
            #print s
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.EPgjf','w')
        f.writelines(GjfLines)
        f.close()
        del GjfLines
        ###################################################################################################
        #to produce .IPlog file 
        path=self.InputFilepath+self.InputfilenameWithoutExt+'.EPlog'
        if(os.path.exists(path)==False):
            self.EPlogfile_produce()
            #######################################################################################################3
            #to search scf done in IPlog file
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.EPlog','r')
        lines =f.readlines() 
        f.close()  
        #os.remove(self.InputFilepath+self.InputfilenameWithoutExt+'.log')
        length=len(lines)-1
        while(length>=0):
            if(re.match('.*SCF Done.*',lines[length])!=None):
                List=list(lines[length].split(' '))
                while(1):
                        try:
                            List.remove('')
                        except:
                            break
                self.__ElectronProtonation=float(List[4])       
                break
            length=length-1
        print 'GasPhase_EnergyProtonation has been finished : '
    def GasPhase_QmaxAndQmin(self):

            ##########################################################################################################################
        #compute the parameter that required
        Qmin=0.0
        Qmax=0.0
        for i in range(len(self.__AtomicCharges)):
            if(float(self.__AtomicCharges[i][1])>Qmax):
                Qmax=float(self.__AtomicCharges[i][1])
            elif(float(self.__AtomicCharges[i][1])<Qmin):
                Qmin=float(self.__AtomicCharges[i][1])
        self.__Qmax=Qmax
        self.__Qmin=Qmin
            ##########################################################################################################################
    def GasPhase_QAB(self,A,B):
        sum=0
        for i in range(len(self.__AtomicCharges)):
            if((cmp(self.__AtomicCharges[i][0],A)==0)or(cmp(self.__AtomicCharges[i][0],B)==0)):
                sum=sum+float(self.__AtomicCharges[i][1])
        return sum
    def GasPhase_QTSquare(self):
        squareSum=0
        for i in range(len(self.__AtomicCharges)):
            squareSum= squareSum+pow(float(self.__AtomicCharges[i][1]),2)
        #print 'GasPhase_QTSquare: '+str(squareSum)
        return squareSum
    def GasPhase_QASquare(self,A):
        squareSum=0
        for i in range(len(self.__AtomicCharges)):
            if(cmp(self.__AtomicCharges[i][0],A)==0):
                squareSum= squareSum+pow(float(self.__AtomicCharges[i][1]),2)
        #print 'GasPhase_QASquare: '+str(squareSum)
        return squareSum   
    def GasPhase_AverageAbsoluteValue(self):
        SumOfAbsoluteValue=0.0
        for i in range(len(self.__AtomicCharges)):
            SumOfAbsoluteValue=SumOfAbsoluteValue+abs(float(self.__AtomicCharges[i][1]))
        AverageAbsoluteValue=SumOfAbsoluteValue/len(self.__AtomicCharges)
        print 'GasPhase_AverageAbsoluteValue: '+str(AverageAbsoluteValue)
        return AverageAbsoluteValue
    def GasPhase_PPCG(self):
        Qmax=self.__Qmax
        PositiveSum=0
        for i in range(len(self.__AtomicCharges)):
            if(float(self.__AtomicCharges[i][1])>0):
                PositiveSum= PositiveSum+float(self.__AtomicCharges[i][1])
        PPCG=Qmax/PositiveSum
        #print 'PPCG'+str(PPCG)
        return PPCG
    def GasPhase_RNGG(self):
        Qmin=self.__Qmin
        NegativeSum=0
        for i in range(len(self.__AtomicCharges)):
            if(float(self.__AtomicCharges[i][1])<0):
                NegativeSum= NegativeSum+float(self.__AtomicCharges[i][1])
        RNGG=Qmin/NegativeSum
        #print 'RNGG'+str(RNGG)
        return RNGG
    def FluentPhaseParameterCompute(self):
        path=self.InputFilepath+self.InputfilenameWithoutExt+'.Fluoptlog'
        if(os.path.exists(path)==False):
            self.GjfParameterChange(self.InputFilepath+self.Inputfilename,'#p.*','#p rb3lyp/6-31+g(d,p) opt freq scrf=(iefpcm,solvent=water)')       
                                #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
            Cmd=self.OrderPath+self.InputFilepath+self.Inputfilename+' '+self.InputfilenameWithoutExt+'.Fluoptlog'
            subprocess.Popen(Cmd,shell=True)
            while(1):
                try:
                    f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Fluoptlog','r')
                    break
                except:
                    continue
            f.close()
        ################################################################################################to ensure the file to the end 
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Fluoptlog','r')
        lines=f.readlines();
        length=len(lines)
        regex=".*Normal termination.*"
        while(length==0):
            lines=f.readlines();
            length=len(lines)
        #print "length of Fluoptlog:"+str(length)
        while(re.match(regex,lines[length-1])==None):
            time.sleep(1)                  
            if(length==0):
                continue
            else:
                f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Fluoptlog','r')
                lines =f.readlines()            
                length=len(lines)
                f.close()
                #print str(length)+' '+lines[length-1]
                break
        f.close()
            ####################################################################################################
        #search for Mulliken atomic charges:
        f=open(self.InputFilepath+self.InputfilenameWithoutExt+'.Fluoptlog','r')
        lines=f.readlines()
        #print length
        length=len(lines)
        f.close()
        while(length):
            length=length-1
            #to eject ' ' appeared in first and last position
            lines[length]=str(lines[length]).strip()
            #to find and save element and atomic charges to list
            if(re.match('Mulliken atomic charges:',lines[length])!=None):
                j=2
                line=lines[length+j].split(' ')
                while(re.match('Sum.*',line[0])==None):
                    List=list(line)
                    #print lines[length+j][0]
                    #print '\n'
                    #print
                    while(1):
                        try:
                            List.remove('')
                        except:
                            break
                    List.pop(0)
                    j=j+1
                    line=lines[length+j].split(' ')
                    self.__AtomicCharges.append(List)
                    #print AtomicCharges
                    #print '\n'
                break
    #compute electronstaticpotential with gsgrid
    def Gaussian_electronstaticpotential_chkTofchk(self):
            while(1):              
                if(os.path.isfile(globalpath+self.InputfilenameWithoutExt+'.chk')):
                    Cmd='formchk '+globalpath+self.InputfilenameWithoutExt+'.chk'                            
                    subprocess.Popen(Cmd,shell=True)
                    print "formchk has been finished"
                    # to produce fchk file completely
                    time.sleep(2)
                    break
                else:
                    print globalpath+self.InputfilenameWithoutExt+'.chk'
                    print"chk file doesn't exist"
                    continue
            while(1):
                try:
                    shutil.move(globalpath+self.InputfilenameWithoutExt+'.fchk', self.InputFilepath+self.InputfilenameWithoutExt+'.fchk')
                    break;
                except:
                    print 'no file of .fck to move'
    #transform fchk into cub in globalpath and other path doesn't work
    def Gaussian_electronstaticpotential_fckTocub(self):
                #time.sleep(2)
                Cmd='cubegen 0 density=scf '+self.InputFilepath+self.InputfilenameWithoutExt+'.fchk'+' '+globalpath+self.InputfilenameWithoutExt+'_density.cub 0 h'
                #print Cmd
                subprocess.Popen(Cmd,shell=True)
                Cmd='cubegen 0 potential=scf '+self.InputFilepath+self.InputfilenameWithoutExt+'.fchk'+' '+globalpath+self.InputfilenameWithoutExt+'_potential.cub 0 h'
                subprocess.Popen(Cmd,shell=True)
                #print Cmd
         
    def Gaussian_electronstaticpotential_output(self):
        time.sleep(5)
        arg1=globalpath+self.InputfilenameWithoutExt+'_density.cub'
        arg2='12'
        arg3='0.0001'
        arg4='4'
        arg5=globalpath+self.InputfilenameWithoutExt+'_potential.cub'

        #print arg5
        arg6='y'
        p=subprocess.Popen(['/home/est863/gsgrid1.7_src/gsgrid',],stdin=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
        p.stdin.write('\''+arg1+'\''+'\n')
        #print arg1
        p.stdin.write(arg2+'\n')
        p.stdin.write(arg3+'\n')
        p.stdin.write(arg4+'\n')
        p.stdin.write('\''+arg5+'\''+'\n')
        p.stdin.write(arg6+'\n')
       
    def Gaussian_electronstaticpotential_parameterCompute(self):
        print "Gaussian_electronstaticpotential_parameterCompute begins"
        #deal with output.txt  output_positive.txt output_negtive.txt 
        #first move them to InputFilepath dictionary
        while(1):
            if(os.path.isfile('output.txt')):
                shutil.move('output.txt',self.InputFilepath+'output.txt')
                break;
            else:
                continue
        while(1):
            if(os.path.isfile('output_positive.txt')):
                shutil.move('output_positive.txt',self.InputFilepath+'output_positive.txt')
                break;
            else:
                continue
        while(1):
            if(os.path.isfile('output_negative.txt')):
                shutil.move('output_negative.txt',self.InputFilepath+'output_negative.txt')
                break;
            else:
                continue
        #to get __PositiveElectronstaticPotentialMeanValue,__MostPositiveElectronstaticPotential,__varianceOfPositiveElectronstaticPotential
        sum=0
        MostPositiveElectronstaticPotential=0.000001
        while(1):
            try:
                Positivelines=list(open(self.InputFilepath+'output_positive.txt'))
                break
            except:
                time.sleep(0.1)
        for i in range(0,len(Positivelines)):
            tempFloat=float(Positivelines[i].split(' ')[-1])
            if(tempFloat>MostPositiveElectronstaticPotential):
                MostPositiveElectronstaticPotential=tempFloat
            sum=sum+float(Positivelines[i].split(' ')[-1])
        self.__PositiveElectronstaticPotentialMeanValue=sum/len(Positivelines)
        self.__MostPositiveElectronstaticPotential=MostPositiveElectronstaticPotential
        PositiveVarianceSum=0.0
        for i in range(0,len(Positivelines)):
            tempFloat=float(Positivelines[i].split(' ')[-1])
            PositiveVarianceSum=PositiveVarianceSum+pow((tempFloat-self.__PositiveElectronstaticPotentialMeanValue),2)
        self.__varianceOfPositiveElectronstaticPotential=PositiveVarianceSum/len(Positivelines)
        #print str(self.__varianceOfPositiveElectronstaticPotential)+'\n'
        #print'self.__MostPositiveElectronstaticPotential'+str(self.__MostPositiveElectronstaticPotential)+'\n'
        #print 'self.__PositiveElectronstaticPotentialMeanValue: '+str(self.__PositiveElectronstaticPotentialMeanValue)+'\n'
        #to gain __negativeEkectronstaticPotentianlMeanValue,__MostNegativeElectronstaticPotential,__varianceOfNegativeElectronstaticPotential
        sum=0
        MostNegativeElectronstaticPotential=-0.000001
        while(1):
            try:
                Negativelines=list(open(self.InputFilepath+'output_negative.txt'))
                break
            except:
                time.sleep(0.1)
        for i in range(0,len(Negativelines)):
            tempFloat=float(Negativelines[i].split(' ')[-1])
            if(tempFloat<MostNegativeElectronstaticPotential):
                MostNegativeElectronstaticPotential=tempFloat           
            sum=sum+float(Negativelines[i].split(' ')[-1])
        self.__MostNegativeElectronstaticPotential=MostNegativeElectronstaticPotential
        self.__NegativeElectronstaticPotentialMeanValue=sum/len(Negativelines)
        NegativeVarianceSum=0
        for i in range(0,len(Negativelines)):
            tempFloat=float(Negativelines[i].split(' ')[-1])
            NegativeVarianceSum=NegativeVarianceSum+pow((tempFloat-self.__NegativeElectronstaticPotentialMeanValue),2)
        self.__varianceOfNegativeElectronstaticPotential=NegativeVarianceSum/len(Negativelines)
        
        #print str(self.__varianceOfNegativeElectronstaticPotential)+'\n'
        #print 'self.__MostNegativeElectronstaticPotential'+str(self.__MostNegativeElectronstaticPotential)+'\n'
        #print 'self.__NegativeElectronstaticPotentialMeanValue: '+str(self.__NegativeElectronstaticPotentialMeanValue)+'\n'
        #to get __ElectronstaticPotentialMeanValue
        sum=0
        while(1):
            try:
                lines=list(open(self.InputFilepath+'output.txt'))
                break
            except:
                time.sleep(0.1)
        for i in range(0,len(lines)):
            sum=sum+float(lines[i].split(' ')[-1])
        self.__ElectronstaticPotentialMeanValue=sum/len(lines)
        #print '__ElectronstaticPotentialMeanValue: '+str(self.__ElectronstaticPotentialMeanValue)+'\n'
            
        sum=0
        #to get averageDispersion
        lines=list(open(self.InputFilepath+'output.txt'))
        for i in range(0,len(lines)):
            tempFloat=float(lines[i].split(' ')[-1])
            if(tempFloat<=-0.000001):
                self.__outputNegativeNumbers=self.__outputNegativeNumbers+1
            elif(tempFloat>=0.000001):
                self.__outputPositiveNumbers=self.__outputPositiveNumbers+1
            sum=sum+abs(tempFloat-self.__ElectronstaticPotentialMeanValue)
        self.__averageDispersion=sum/len(lines)
        print 'averageDispersion is'+str(self.__averageDispersion)+'\n'
        print '__outputNegativeNumbers:'+str(self.__outputNegativeNumbers)+'\n'
        print '__outputPositiveNumbers:'+str(self.__outputPositiveNumbers)
        #to get  balanceOncstant
        self.__BalanceConstant=(self.__varianceOfNegativeElectronstaticPotential*self.__varianceOfPositiveElectronstaticPotential)/pow((self.__varianceOfNegativeElectronstaticPotential+self.__varianceOfPositiveElectronstaticPotential),2)
        print 'self.__BalanceConstant: '+str(self.__BalanceConstant)+'\n'
        #remove file in src
        try:
            '''
            while ( os.path.isfile(self.InputfilenameWithoutExt+'_density.cub')==False):
                continue
                '''
            shutil.move(globalpath+self.InputfilenameWithoutExt+'_density.cub',self.InputFilepath+self.InputfilenameWithoutExt+'_density.cub')
            '''
            while ( os.path.isfile(self.InputfilenameWithoutExt+'_potential.cub')==False):
                continue
                '''
            shutil.move(globalpath+self.InputfilenameWithoutExt+'_potential.cub',self.InputFilepath+self.InputfilenameWithoutExt+'_potential.cub')
        except Exception, e:
            exstr=traceback.format_exc()
            print exstr
        