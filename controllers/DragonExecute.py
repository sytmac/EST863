#! /usr/bin/env python
#coding=utf-8
from controllers.Dragon import Dragon

d = Dragon("Clc2cccc3Oc1ccccc1Oc23,cc")
d.mol2drs()
print d.abstractparameter(["X1sol", "Mor13v", "HATS5v", "RDF035m","Mor15u" ,"RDF090m", "H-050", "nRCOOR", "R5v", "T(O..Cl)", "RCI","nRCOOR"])