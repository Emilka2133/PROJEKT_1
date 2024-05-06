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

if __name__=="__main__":
    geo=Transformacje(model="wgs84") 

#hirv    
flh=[]
with open('wsp_inp.txt','r') as p:
    linie = p.readlines()
    wsp = linie[4:]
    for el in wsp:
        q=el.split(',')
        X=float(q[0])
        Y=float(q[1])
        Z=float(q[2])
        f,l,h=geo.hirvonen(X,Y,Z)
        flh.append([f,l,h])

with open('wyniki_xyz2flh.txt','w') as p:
    p.write ('f [deg], lam [deg], h [m] \n')
    for flh_list in flh:
        line = ','.join([str(wsp)for wsp in flh_list])
        t = p.writelines(line+'\n')


# flh2XYZ
    def nothir (self,f,l,h):
        N=self.a/np.sqrt(1-self.e2*np.sin(f)**2)
        X=(N+h)*np.cos(f)*np.cos(l)
        Y=(N+h)*np.cos(f)*np.sin(l)
        Z=(N*(1-self.e2)+h)*np.sin(f)
        return(X,Y,Z)  
    
    
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
        

# flh21992

    def flh21992 (self,f,l,l0):
        A0=1-self.e2/4-3*self.e2**2/64-5*self.e2**3/256
        A2=(3/8)*(self.e2+self.e2**2/4+15*self.e2**3/128)
        A4=(15/256)*(self.e2**2+3*self.e2**3/4)
        A6=(35*self.e2**3)/3072
        sigma=self.a*(A0*f-A2*np.sin(2*f)+A4*np.sin(4*f)-A6*np.sin(6*f))
        b2=self.a**2*(1-self.e2)
        e_2=(self.a**2-b2)/b2
        dl=l-l0
        t=np.tan(f)
        eta2=e_2*(np.cos(f))**2
        N=self.a/(np.sqrt(1-self.e2*np.sin(f)**2))
        Xgk=sigma+(dl**2/2)*N*np.sin(f)*np.cos(f)*((1+(dl**2/12)*(np.cos(f))**2*(5-t**2+9*eta2+4*eta2**2)+(dl**4/360)*np.cos(f)**4*(61-58*t**2+t**4+270*eta2-330*eta2*t**2)))
        Ygk=dl*N*np.cos(f)*(1+(dl**2/6)*(np.cos(f)**2)*(1-t**2+eta2)+((dl**4/120)*(np.cos(f)**4))*(5-18*t**2+t**4+14*eta2-58*eta2*t**2))
        M1992=0.9993
        X92=Xgk * M1992 - 5300000
        Y92=Ygk * M1992 + 500000
        return(X92,Y92)
    
#1992       
XY1992=[]
with open('wyniki_xyz2flh.txt','r') as p:
    linie = p.readlines()
    wsp = linie[1:]
    for el in wsp:
        q=el.split(',')
        f=float(q[0])
        l=float(q[1])
        h=float(q[2])
        l0=19*pi/180
        f=f*pi/180
        l=l*pi/180
        X1992,Y1992=geo.flh21992(f,l,l0)
        XY1992.append([X1992,Y1992])
