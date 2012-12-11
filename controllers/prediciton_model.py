'''
Created on 2012-12-4

@author: SongYang
'''
import sys
from controllers.Dragon import Dragon
class PredictionModel(object):
    '''
    all the prediction model are in this class 
    which is showed and computed in different methods
    method is named by model name
    '''
    def __init__(self , modelname=None ,para={}):
                    {
         "logKOA" :  lambda para:self.logKOA(para),
         
        }[modelname](para)
    def logKOA(self,para):
        '''
        logKOA model computation
        '''
        self.predict_result = {}
        if not para['smilestring']:
            self.predict_result['warning'] = 'Cannot find your input smile numbers'
            print self.predict_result
            sys.exit()
        d = Dragon(para["smilestring"])
        d.mol2drs()
        abstract_value = d.abstractparameter(["X1sol", "Mor13v", "HATS5v", "RDF035m","Mor15u" ,"RDF090m", "H-050", "nRCOOR", "R5v", "T(O..Cl)", "RCI","nRCOOR"])
        for smilenum in abstract_value.keys():
            self.predict_result[smilenum] = 0.509 + 0.986*float(abstract_value[smilenum]['X1sol'])-1.018*float(abstract_value[smilenum]['Mor13v'])+1.384*float(abstract_value[smilenum]['H-050'])-1.528*float(abstract_value[smilenum]['R5v'])-0.015*float(abstract_value[smilenum]['T(O..Cl)'])+0.043*float(abstract_value[smilenum]['HATS5v'])-0.026*float(abstract_value[smilenum]['RDF035m'])-0.197*float(abstract_value[smilenum]['RCI'])-0.130*float(abstract_value[smilenum]['nRCOOR'])-0.077*float(abstract_value[smilenum]['Mor15u'])-0.077*float(abstract_value[smilenum]['RDF090m'])
        self.predict_result["invalidnums"] = d.invalidnums
        print self.predict_result
            
para ={
       "smilestring":"CCCCC",
       "filepath"   :"",
       }
pm = PredictionModel("logKOA", para)