# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 11:48:51 2024

@author: emili
"""

import sys
import numpy as np
from math import *

class Transformacje:
    def __init__(self,model:str="wgs84"):
        """
        Parametry elipsoid:
            a - duża półoś elipsoidy
            b - mała półoś elipsoidy
            e2 - mimośród^2

        """
        if model=="wgs84":
            self.a=6378137
            self.b=6356752.31424518
        elif model=="grs80":
            self.a=6378137
            self.b=6356752.31414036
        elif model=="Krasowskiego":
            self.a=6378245
            self.b=6356863.0188
        else:
            raise NotImplementedError(f"{model} - ten model nie jest osbsługiwany przez ten kod")
        self.e2 = (self.a**2-self.b**2)/self.a**2
        



# XYZ2flh
    def xyz2flh(self,X,Y,Z):
        """
        Algorytm Hirvonena - transformacja współrzednych ortokartezjańskich (XYZ) na współrzędne geodezyjne (flh). 

        Parameters
        ----------
        X : float
        Y : float
        Z : float
        
        X,Y,Z - współrzędne w układzie ortokartezjańskim [m]

        Returns
        -------
        f - szerokość geodezyjna [stopnie dziesiętne]
        l - długość geodezyjna [stopnie dziesiętne]
        h - wysokość geodezyjna [m]
        
        output [str]

        """
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
    def flh2xyz (self,f,l,h):
        """
        Transformacja odwrotna do schematu Hirvonena. Zamiana współrzędnych geodezyjnych [flh] na współrzędne ortokartezjańskie [XYZ].

        Parameters
        ----------
        f,l,h - float
        f - szerokość geodezyjna [stopnie dziesiętne]
        l - długość geodezyjna [stopnie dziesiętne]
        h - wysokość geodezyjna [m]

        Returns
        -------
       X,Y,Z -str
        
        X,Y,Z - współrzędne w układzie ortokartezjańskim [m]

        """
        N=self.a/np.sqrt(1-self.e2*np.sin(f)**2)
        X=(N+h)*np.cos(f)*np.cos(l)
        Y=(N+h)*np.cos(f)*np.sin(l)
        Z=(N*(1-self.e2)+h)*np.sin(f)
        return(X,Y,Z)  

  
# flh22000

    def flh22000 (self,f,l,l0,nr):
        """
        Funkcja zamienia współrzędne geodezyjne (flh) na współrzędne płaskie w układzie PL-2000

        Parameters
        ----------
        f - szerokość geodezyjna [stopnie dziesiętne] -float
        l - długość geodezyjna [stopnie dziesiętne] -float
        l0 - południk zerowy (15/18/21/24 stopnie) -float
        nr : numer strefy (5/6/7/8) -int

        Returns
        -------
        X2000 - str [m]
        Y2000 - str [m]
        współrzędne X,Y w układzie PL-2000
        
        """
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
        M2000=0.999923
        X2000=Xgk*M2000
        Y2000=Ygk*M2000+nr*1000000+500000
        return(X2000,Y2000)
    
#python inf_proj1.py --wgs84 --xyz2flh wsp_inp.txt    
# flh21992

    def flh21992 (self,f,l,l0):
        """
        Funkcja zamienia współrzędne geodezyjne (flh) na współrzędne płaskie w układzie PL-1992

        Parameters
        ----------
        f - szerokość geodezyjna [stopnie dziesiętne] -float
        l - długość geodezyjna [stopnie dziesiętne] -float
        l0 - południk zerowy (19 stopnie) -float

        Returns
        -------
        X1992 - str [m]
        Y1992 - str [m]
        współrzędne X,Y w układzie PL-1992
        """
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
    
    def XYZ2neu(self,X,Y,Z,ref_X,ref_Y,ref_Z):
        """
        Jest to funkcja zamieniająca współrzędne ortokartezjańskie (XYZ) na współrzędne w układzie topocentrycznym (neu).

        Parameters
        ----------
       X,Y,Z - (float) współrzędne ortokartezjańskie [m]
        ref_X,ref_Y,ref_Z - (float) współrzędne referencyjne wpisane przez użytkownika [m]

        Returns
        -------
        n,e,u -(str) współrzędne układu topocentrycznego [m]

        """
        f,l,_=self.flh2xyz(ref_X,ref_Y,ref_Z)
        f = f*pi/180
        l = l*pi/180
        R=np.array([[-sin(f)*cos(l),-sin(l),cos(f)*cos(l)],
                    [-sin(f)*sin(l),cos(l),cos(f)*sin(l)],
                    [cos(f),0,sin(f)]])
        xyz_t = np.array([[X-ref_X],
                          [Y-ref_Y],
                          [Z-ref_Z]])
        n,e,u=R.T@xyz_t
        return(n,e,u)

if __name__ =="__main__":
   input_file_path = sys.argv[-1]
   model = sys.argv[-2]
   geo =Transformacje(model)
   if "--header_lines":
     numer_nagłówka = sys.argv[3]
   if "--xyz2flh" in sys.argv and '--flh2xyz' in sys.argv:
     print('zostało podane więcej niż jedna flaga')
   elif '--xyz2flh' in sys.argv:
       with open(input_file_path,'r') as p:
           linie = p.readlines()
           wsp=linie[int(numer_nagłówka):]
           flh=[]        
           for el in wsp:
               q=el.split(',')
               X=float(q[0])
               Y=float(q[1])
               Z=float(q[2])
               f,l,h=geo.xyz2flh(X,Y,Z)
               f=f*180/pi
               l=l*180/pi
               flh.append([f,l,h])
       with open('wyniki_xyz2flh.txt','w') as p:
           p.write ('f [deg] | lam [deg]|  h [m] \n')
           for flh_list in flh:
               f,l,h=flh_list
               line=f'{f:7.3f},{l:8.3f},{h:11.3f}'
               t = p.writelines(line+'\n')
   elif '--flh2xyz' in sys.argv:
       with open(input_file_path,'r') as p:
           linie = p.readlines()
           wsp = linie[int(numer_nagłówka):]
           XYZ=[]
           for el in wsp:
               q=el.split(',')
               f=float(q[0])
               l=float(q[1])
               h=float(q[2])
               f=f*pi/180
               l=l*pi/180
               X,Y,Z=geo.flh2xyz(f,l,h)
               XYZ.append([X,Y,Z])
       with open('wyniki_flh2xyz.txt','w') as p:
           p.write ('    X [m]   |   Y [m]    |    Z [m]   \n')
           for xyz_list in XYZ:
               x,y,z = xyz_list
               line = f'{x:6.3f}, {y:8.3f}, {z:8.3f}'
               t = p.writelines(line+'\n')
   elif '--xyz2neu' in sys.argv:  
         ref_X= float(input("Podaj wartość współrzędnej referencyjnej X:"))
         ref_Y= float(input("Podaj wartość współrzędnej referencyjnej Y:"))
         ref_Z= float(input("Podaj wartość współrzędnej referencyjnej Z:"))
         with open(input_file_path,'r') as p:
             linie = p.readlines()
             wsp = linie[int(numer_nagłówka):]
             neu=[]
             for el in wsp:
                 q=el.split(',')
                 X=float(q[0])
                 Y=float(q[1])
                 Z=float(q[2])
                 ref_X,ref_Y,ref_Z= (float(ref_X),float(ref_Y),float(ref_Z))
                 [[n],[e],[u]]=geo.XYZ2neu(X,Y,Z,ref_X,ref_Y,ref_Z)
                 neu.append([n,e,u])
         with open('wyniki_xyz2neu.txt','w') as p:
           p.write ('   n [m]      |   e [m]     |   u [m] \n')
           for neu_list in neu:
               n,e,u = neu_list
               line = f'{n:13.3f},{e:13.3f},{u:13.3f}'
               t = p.writelines(line+'\n')
   elif'--flh22000' in sys.argv:
       with open(input_file_path,'r') as p:
           linie = p.readlines()
           wsp = linie[int(numer_nagłówka):]
           XY2000=[]
           for el in wsp:
               q=el.split(',')
               f=float(q[0])
               l=float(q[1])
               h=float(q[2])
               if l >13.5 and l<16.5:
                   l0=15*pi/180
                   nr=5
               if l >16.5 and l<19.5:
                   l0=18*pi/180
                   nr=6
               if l >19.5 and l<22.5:
                   l0=21*pi/180
                   nr=7
               if l >22.5 and l<25.5:
                   l0=24*pi/180
                   nr=8
               f=f*pi/180
               l=l*pi/180
               X2000,Y2000=geo.flh22000(f,l,l0,nr)
               XY2000.append([X2000,Y2000])
       with open('wyniki_flh22000.txt','w') as p:
           p.write ('  X2000 [m]  | Y2000 [m] \n')
           for xy2000_list in XY2000:
               x2000,y2000 = xy2000_list
               line =  f'{x2000:12.3f},{y2000:12.3f}'
               t = p.writelines(line+'\n')
   elif '--flh21992' in sys.argv:
       with open(input_file_path,'r') as p:
           linie = p.readlines()
           wsp = linie[int(numer_nagłówka):]
           XY1992=[]
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
       with open('wyniki_flh21992.txt','w') as p:
           p.write ('  X1992 [m]  | Y1992 [m] \n')
           for xy1992_list in XY1992:
               x1992,y1992 = xy1992_list
               line = f'{x1992:12.3f},{y1992:12.3f}'
               t = p.writelines(line+'\n')


 
