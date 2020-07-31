import os
import pandas as pd
import numpy as np
import math 
import PIL # just to make sure Pillow is installed
import imageio

x2droot ='2ddata'
assets='./assets/'
x2dindex ='INDEX.csv'
x2dindexpath = assets+'/'+x2droot+'/'+x2dindex

def read_2d_names():
    data=pd.read_csv(x2dindexpath, sep='\s+')
    data['hazardgrid']=assets+x2droot+"/grid/HAZARDMAP/"+data['hazardmap']
    data['riskgrid']=assets+x2droot+"/grid/RISKMAP/"+data['riskmap']
    return data

def interp(indexdata, val):
    level=indexdata['level'].to_numpy()    
    damage=indexdata['dmgmilusd'].to_numpy()
    damage=np.interp(val,level, damage)
    ind = indexdata.index.to_numpy()
    findex = np.interp(val, level, ind)
    ind2=math.ceil(findex)
    w2=ind2-findex
    ind1=math.floor(findex)
    w1=findex-ind1
    hazard=indexdata['hazardmap'].to_numpy()
    risk=indexdata['riskmap'].to_numpy()
    return damage, findex, [ind1, ind2], [w1, w2], hazard, risk

def nearest_image(indexdata, val):
    res=interp(indexdata, val)
    dmg=res[0]
    w1, w2=res[-3]
    ind1, ind2=res[-4]
    if w2>w1: 
        fname1=x2droot+"/"+res[-2][ind1]+".png"
        fname2=x2droot+"/"+res[-1][ind1]+".png"
        
    else:
        fname1=x2droot+"/"+res[-2][ind2]+".png"
        fname2=x2droot+"/"+res[-1][ind2]+".png"
        
    return res[0], fname1, fname2 #imageio.imread(fname1), imageio.imread(fname2)
    

def get_image(indexdata, val):
    return nearest_image(indexdata, val)

if __name__ == "__main__":
    data=read_2d_names()
    res=get_image(data, 2.15)
    
    print(res[0])
    from matplotlib import pyplot as plt
    plt.subplot(1, 2, 1)
    plt.imshow(res[1])
    plt.subplot(1, 2, 2)
    plt.imshow(res[2])
    plt.show()
    