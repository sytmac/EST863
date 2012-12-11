# -* -coding: utf-8 -*- 
'''
Created on 2012-11-26

@author: songyang
'''
import sys,os,shutil
sys.path.append("/usr/local/lib/")
import openbabel,pybel
from config.settings import globalpath
from controllers.Mopac import Mopac
from controllers.MolToGjfAndMop import Mol2GjfandMop
class SmileToMol():
    '''
    to transfer from smile numbers to mol file:
    input parameter is a string,and multi_smiles is splited by ','
    such as [number1,number2,number3]
'''
    def __init__(self, smilenum= None):
        self.__invalid_smile = []
        self.__opt_smilenum = []
        self.__unopt_smilenum = []
        if smilenum == "":
            raise Exception,"error input with 0 valid smilenum"
        else:
            self.__smilenum_list = smilenum.split(',')
            
        #for test
        for smilenum in self.__smilenum_list:
            self.__unopt_smilenum.append(smilenum)
        self.__smilenum_list = self.__unopt_smilenum
    def check_smilenum(self): 
            #for query in mysql;
            #if smilenum in database,it means that the mol file has been optimized
            #or we need optimize the mol file with mopac 
            #we use self.__opt_smilenum and self.__unopt_smilenum to mark off optimized or unoptimized mol file
            #using the following code
            
            #for smilenum in self.smilenum_list:
            #    try: 
            #        models.objects.get(smile=smilenum)
            #        self.opt_smilnum.append(smilenum)
            #    exception DoesNotExist:
            #        self.unopt_smilnum.append(smilenum)
            pass
    def smile2_3d(self,smilenum):
            mymol=pybel.readstring('smi',smilenum)
            mymol.addh()
            mymol.make3D()
            mymol.write('mol',smilenum+".mol",overwrite=True)
            
    def optimize_mol(self):
        for smilenum in self.__unopt_smilenum:
            #1: smile number to 3d structure
            try:
                self.smile2_3d(smilenum)
            except:
                self.__invalid_smile.append(smilenum)
                continue
            #2: mol to mop file
            Mol2GjfandMop(os.getcwd()+'/'+smilenum+'.mol',mop=True)
            #3:mop file into formopac folder

            dst = globalpath+'formopac/'+smilenum
            if not os.path.exists(dst):
                os.mkdir(dst)
            real_dst = os.path.join(dst, smilenum+'.mop')
            if os.path.exists(real_dst):
                os.remove(os.getcwd()+'/'+smilenum+'.mop')
            else:
                shutil.move(os.getcwd()+'/'+smilenum+'.mop',globalpath+'formopac/'+smilenum)

        # to remove invalide smilenum from self.__unopt_smilenum
        for num in self.__invalid_smile:
            self.__unopt_smilenum.remove(num) 
    def get_unopt_smilelist(self):
        return self.__unopt_smilenum
    def get_opt_smilelist(self):
        return self.__opt_smilenum
    def get_invalid_smile(self):
        return self.__invalid_smile
    def get_smilenum_list(self):
        return self.__smilenum_list
    def mol2tdragon_dictionary(self):
        for smilenum in self.__smilenum_list:
            #delete mol file in current folder and move it to dragon dictionary
            dst = globalpath+'fordragon/'+smilenum+'/'
            if not os.path.exists(dst):
                os.mkdir(dst)
            if not os.path.exists(dst+smilenum+'.mol'):
                shutil.move(os.getcwd()+'/'+smilenum+'.mol',dst)
            mop = Mopac(smilenum+'.mop')
            mop.opt4dragon()
'''
sm = SmileToMol('cab,cc,cd,ce,ccc')
sm.optimize_mol()
sm.mol2tdragon_dictionary()
print sm.get_invalid_smile()
print sm.get_smilenum_list()
'''