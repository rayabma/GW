#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 17:02:55 2019

@author: rayabma
"""
import numpy as np
import math 
import matplotlib.pyplot as plt
import sys
from matplotlib import rc

from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D

fdisplay = 0
if len(sys.argv) > 1 :
    fdisplay = int(sys.argv[1])
print(' fdisplay=',fdisplay,' show plots 0=yes')

nn = 2000
if len(sys.argv) > 2 :
    nn = int(sys.argv[2])
print(' number of points to plot=',nn)

dt = 20.0  ### sample interval of IDA sensors in seconds
fmax = 1.0/(dt * 2.0)
n1 = 1576800  ### original time axis length
nfreq = np.int((n1+1)/2.0)
df = fmax/(nfreq-1)


#for iblock in range(0,500000,10000):
#for iblock in range(0,2,10000):
#for iblock in range(50000,50001,10000):
#for iblock in [230000,380000,390000,450000]:
#for iblock in [190000,200000,210000,220000,240000,250000]:
#for iblock in [300000,400000,600000,700000,800000]:
#for iblock in [420000,440000,460000,470000,490000]:
#for iblock in [40000,60000,70000]:
for iblock in [50000]:

    print(' data taken from Block =',iblock)
    npzfile = np.load('YBlock87_'+str(iblock)+'.npz')
    fglobe87 = npzfile['cglobe']
    
    #df = npzfile['df']
    nlat  =   npzfile['nlat']
    nlon  =   npzfile['nlon']
    npolarity =npzfile['npolarity']
    ifzero  =   npzfile['istart']
    latgrid =npzfile['latgrid']
    longrid =npzfile['longrid']



    nsamp = np.size(fglobe87,axis=3)


    maxes = np.zeros(nsamp) 
    idxs  = np.zeros(nsamp)
    crosscor = np.zeros(nsamp) 
    x =  np.zeros(nsamp)
    y =  np.zeros(nsamp)


    fzero = (ifzero-1)* df
    fmax = (ifzero+nsamp) * df
    if (fzero > 0):
        periodmax=(1.0/fzero)/60.0
    else:
         periodmax=99999.0
    
    periodmin=(1.0/fmax)/60.0
    print(' maximum period=',periodmax,'  minimum period=',periodmin)


    fzero = (ifzero-1)* df


    font = {'family': 'serif',
            'weight': 'normal',
            'size': 8,
            }

    xa1 = min(longrid)
    xa2 = max(longrid)
    ya1 = min(latgrid)
    ya2 = max(latgrid)
  
    globemap87=np.zeros((nlat,nlon,npolarity))


    for ifi in range(1,nsamp):

        if (ifi % 1000 == 0):
            print(' ifi=',ifi)

        freq = ifi * df + fzero
        if (freq == 0.0):
            period = 9999999.0
        else:
            period = (1.0/freq)/60.0

        for ilat in range(nlat) :
            for ilon in range(nlon) :
                for ipol in range(npolarity) :
                    globemap87[ilat,ilon,ipol]=np.abs(fglobe87[ipol,ilon,ilat,ifi] )

        fmaxall = 0.0
        fmaxacor = 0.0
        ipoint87 = -1
        for ipol in range(npolarity) :
            fmax= np.max(np.absolute(globemap87[:,:,ipol]))
            if fmax > fmaxall :
                fmaxall = fmax
                ipoint87 = ipol

        if (ipoint87 > -1):

            freq = ifi * df + fzero
            if (freq == 0.0):
                period = 9999999.0
            else:
                period = (1.0/freq)/60.0
    
            mmmx87 = globemap87[:,:,ipoint87]
            result = np.where(mmmx87 == np.amax(mmmx87))
            maxes[ifi] = np.amax(mmmx87)
            y[ifi] = ( result[0][0] - 15) * 90.0/15.0
            x[ifi] = ( result[1][0] -30 ) * 180.0/30.0
            y[ifi] =  result[0][0]
            x[ifi] =  result[1][0] 
            #print(' ifi,x,y=',ifi,x[ifi] , y[ifi] )
    
    
    allmaxs=np.zeros(nn)
    xs=np.zeros(nn)
    ys=np.zeros(nn)
    skymap = np.zeros((31,61))
    
    mxs = np.zeros(nsamp) 
    mxs = maxes
    #print(' mxs=',mxs)
    for i in range(0,nn):
        imx = np.argmax(mxs)
        allmaxs[i] = mxs[imx]
        mxs[imx]= 0.0
        xs[i] = x[imx]
        ys[i] = y[imx]
        ix = np.int(xs[i])
        iy = np.int(ys[i])
        #print(' ix,iy=',ix,iy)
        skymap[iy,ix] = skymap[iy,ix] + 1

        
    fig = plt.figure(figsize=[12.0,10.0])
    plt.subplots_adjust(hspace=0.35)
    speriodmin = '{:6.3f}'.format(periodmin)
    speriodmax = '{:6.3f}'.format(periodmax)

    plt.imshow(skymap,aspect='auto',extent=(xa1,xa2,ya1,ya2),cmap='jet')
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.colorbar()

    ttt = '1987 source coordinates \n '+\
    'periods '+speriodmax+' to '+speriodmin+' minutes \n'+\
    'Block '+str(iblock)+' points='+str(nn)
    plt.title(ttt)
    plt.savefig('Plot-Block-'+str(iblock)+'-'+str(nn)+'-Coord-1987-color.pdf',dpi=300)
    plt.savefig('Plot-Block-'+str(iblock)+'-'+str(nn)+'-Coord-1987-color.tiff',dpi=300)
    
    if (fdisplay == 0):
        plt.show()
    
