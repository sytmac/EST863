#! /usr/bin/env python
#coding=utf-8
from controllers.XmlCreate import write_xml
from controllers.CmdChoice import CmdChoice
import threading
import subprocess
import time
from Gaussian import Gaussian

#wx = write_xml()
#wx.set_tag("/home/est863/Desktop/2012-PL-Zhanghongliang/PL model mol files/51-79-6urethane.mol","/home/est863/Desktop/sytmac/result.txt")

def GuassianDisposal(GuassianFile):
    
    c=Gaussian(GuassianFile)      
    c.FluentPhaseParameterCompute()   
    c.GasPhaseParameterCompute()
    c.GasPhase_MolecularVolume()
    c.GasPhase_MolecularHOMOAndLUMOAndAbsolut_Hardness()
    c.Gaussian_electronstaticpotential_chkTofchk()
    c.Gaussian_electronstaticpotential_fckTocub()
    c.Gaussian_electronstaticpotential_output()
    c.GasBindEnergy()
    c.GasPhase_IonizationPotential()
    c.GasPhase_ElectronAffinity()
    c.GasPhase_EnergyProtonation()
    c.Gaussian_electronstaticpotential_parameterCompute() 
    c.GasPhase_QmaxAndQmin()
    c.GasPhase_PPCG()
    c.GasPhase_RNGG()
    c.GasPhase_AverageAbsoluteValue() 
    #c.FluentPhaseParameterCompute()
    print 'Gaussian finished'

t1=threading.Thread(target=GuassianDisposal,args=('3D2TA-QMMM-insidegauss-ligand.gjf',))
t1.start() 

        