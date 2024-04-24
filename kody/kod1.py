# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 11:48:51 2024

@author: emili
"""

import numpy as np

class Transformacje:
    def __init__(self,model:str="wgs84"):
        if model=="wgs84":
            self.a=6378137
            self.b=6356752.31424518
        elif model=="grs80":
            self.a=6378137
            self.b=6356752.31414036
        elif model=="mars":
            self.a=3396900
            self.b=3376097.80585952
        else:
            raise NotImplementedError(f"{model} model not implemented")
        self.e2 = (self.a**2-self.b**2)/self.a**2
        
# XYZ2flh
    def hirvonen(self,X,Y,Z):
        l=np.arctan2(Y,X)
        p=np.sqrt(X**2+Y**2)
        f=np.arctan(Z/(p*(1-self.e2)))
        while True:
            N=self.a/np.sqrt(1-self.e2*np.sin(f)**2)
            h=p/np.cos(f)-N
            fs=f
            f=np.arctan(Z/(p*(1-(self.e2*(N/(N+h))))))
            if np.abs(f-fs)<(0.000001/206265):
                break
            return(f,l,h) 