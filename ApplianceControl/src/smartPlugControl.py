#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
Created on 2 Dec 2016

@author: sivakumar.natarajan
'''
import FF_utils as ff

print("hello")

for i in range(0,6):
    if (i%2)==0:
        ff.setOnOff("off","44A9")
        ff.setOnOff("off","DCF9")
        print("done  off time" + str(i))
    else:
        ff.setOnOff("on","44A9")
        ff.setOnOff("on","DCF9")
        print("done on  time" + str(i))