#! /usr/bin/env python
#coding=utf-8
from controllers.Dragon import Dragon
def DragonDisposal(dragonFile):
    dragon=Dragon(dragonFile)
    dragon.DealWithMolFile()