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

#  flh2XYZ
    def nothir (self,f,l,h):
        N=self.a/np.sqrt(1-self.e2*np.sin(f)**2)
        X=(N+h)*np.cos(f)*np.cos(l)
        Y=(N+h)*np.cos(f)*np.sin(l)
        Z=(N*(1-self.e2)+h)*np.sin(f)
        return(X,Y,Z)  

if __name__=="__main__":
    geo=Transformacje(model="wgs84") 
    
    
#nothir  
  
XYZ=[]
with open('wyniki_xyz2flh.txt','r') as p:
    linie = p.readlines()
    wsp = linie[1:]
    for el in wsp:
        q=el.split(',')
        f=float(q[0])
        l=float(q[1])
        h=float(q[2])
        X,Y,Z=geo.nothir(f,l,h)
        XYZ.append([X,Y,Z])

with open('wyniki_flh2xyz.txt','w') as p:
    p.write ('X [m], Y [m], Z [m] \n')
    for xyz_list in XYZ:
        line = ','.join([str(wsp)for wsp in xyz_list])
        t = p.writelines(line+'\n')