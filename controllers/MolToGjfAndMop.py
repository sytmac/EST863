#! /usr/bin/env python
#coding=utf-8
'''
Created on 2012-7-30

@author: sytmac
'''
import shutil
import re
def MolToGjfAndMop(file):
    #to gain input file name such as i.gif
    Inputfilename=file.split('/')[-1]
    #to gain input file name without extension such as i.gif
    InputfilenameWithoutExt=Inputfilename.split('.')[0]
    GjfList=[]
    OritationList=[]
    MopList=[]
    GjfList.append('%chk='+InputfilenameWithoutExt+'.chk\n')
    GjfList.append('%nproc=2\n')
    #GjfList.append('\n')
    GjfList.append('%mem=2GB\n')
    GjfList.append('#p rb3lyp/6-31+g(d,p)\n')
    GjfList.append('\n')
    GjfList.append('Title Card Required\n')
    GjfList.append('\n')
    GjfList.append('0 1\r')
    MopList.append(' PM6 CHARGE=0 GNORM=0.100 ESP static\n')
    MopList.append('\n\r\n')
    f=open(file,'r')
    lines=f.readlines()
    f.close()
    for lineNum in range(len(lines)):
        try:
            List=list(lines[lineNum].split(' '))
            while(1):
                try:
                    List.remove('')
                except:
                    break
            if(List[3]>'A'and List[3]<'Z'):        
                #print  List   
                OritationList.append(' '+List[3]+'             '+List[0]+'    '+List[1]+'    '+List[2]+'\n')               
        except:
            continue
    GjfList.extend(OritationList)
    GjfList.append('\n\n')
    MopList.extend(OritationList)
    f=open(file.split('.')[0]+'.gjf','w')
    f.writelines(tuple(GjfList))
    f.close()
    f=open(file.split('.')[0]+'.mop','w')
    f.writelines(tuple(MopList))
    f.close()
#MolToGjfAndMop('/home/est863/Desktop/ben.mol')