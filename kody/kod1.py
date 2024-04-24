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