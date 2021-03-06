'''
Created on 2012-10-17

@author: est863
'''
import sys
sys.path.append("/usr/local/lib/")
import openbabel,pybel
import web
import threading
from  controllers import GaussianExecute
from  controllers import MopacExecute
from  controllers import DragonExecute
from  controllers.MolToGjfAndMop import *
class Cas:
    def POST(self):
        cas_info=web.input()
        #the smileNum interface for query from mysql
                    #####################################################
    
    
                    #####################################################
        #return cas_info
        return cas_info["cas"]
class Smile:
    def POST(self):
        smile_info=web.input()
        #the smileNum interface for query from mysql
                    #####################################################
        
        
                    #####################################################
        try:
            mymol=pybel.readstring('smi',str(smile_info["smile"]))
            mymol.addh()
            mymol.make3D()
            mymol.write('mol',str(smile_info["smile_name"])+".mol",overwrite=True)
        except(IOError):
            return "your input smile is invalid"
                
        return smile_info["smile_name"]       
class Files:
    def POST(self):
        input_info= web.input(myfile={})       
        if 'myfile' in input_info:
            filepath=input_info.myfile.filename
            filename=filepath.split('/')[-1]
            fout = open(filename,'w') # creates the file where the uploaded file should be stored
            fout.write(input_info.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
            self.InputWithUploadFile(filename)
            return 'file upload sucess'
    def InputWithUploadFile(self,filename):
        fileExt=filename.split('.')[-1]
        if cmp(fileExt,'gjf')==0:
            print 'input gjf file: '+str(filename)
            GaussianExecute.GuassianDisposal(filename)
        elif cmp(fileExt,'mop')==0:
            print 'input mop file'   
            MopacExecute.DealWithMopac(filename) 
        # when mol file is uploaded ,we start 3 thread to  act 
        # using Dragon Mopac and Gaussian respectively        
        elif cmp(fileExt,'mol')==0:
            #DragonExecute.DragonDisposal(filename)
            MolToGjfAndMop(filename)
            gjf_filename=filename.split('.')[0]+'.gjf'
            GaussianThread=threading.Thread(target=GaussianExecute.GuassianDisposal,args=(gjf_filename,))
            GaussianThread.start() 
            mop_filename=filename.split('.')[0]+'.mop'
            MopacThread=threading.Thread(target=MopacExecute.DealWithMopac,args=(mop_filename,))
            MopacThread.start()
            print 'input mol file'
        else:
            print 'illegal input file formation'