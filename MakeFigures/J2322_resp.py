#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 17:02:55 2019

@author: rayabma
"""
import numpy as np
import math 
import matplotlib.pyplot as plt
from matplotlib import rc

from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D

source = 'J2322'
operiod = 20.01368263397               # orbital period, minutes
print(' orbital period =', operiod)
harmonic = 2
print(' harmonic =', harmonic)



dt = 20.0  ### sample interval of IDA sensors in seconds
#dt = 10.0  ### sample interval of IDA sensors in seconds
fmax = 1.0/(dt * 2.0)
print(' old fmax=',fmax)
n1 = 1576800  ### original time axis length
print('n1=',n1)
freq = np.fft.rfftfreq(n1, d=dt)

nfreq = np.int((n1+1)/2.0)
print(' old number of frequencies=',nfreq)

nfreq = freq.size
fmax = freq[nfreq-1]
print(' new fmax=',fmax)
print(' number of frequencies=',nfreq)

#df = fmax/(nfreq-1)
df = np.longdouble(fmax)/(nfreq-1)
print(' old freqency increment=',df)
df = (freq[nfreq-1]-freq[0])/nfreq
print(' freqency increment=',df)

operiods = operiod * 60.0        # orbital period, seconds
period = operiods / harmonic    # divide by the harmonic to get signal period
print(' orbital period=',operiod,' minutes')
print(' orbital period=',operiods,' seconds')
print(' signal period=',period)

finter =  1.0/period
print(' finter=',finter)

ifnum = np.int(np.round( finter/df)  )
print(' df=',df)
print(' ifnum=',ifnum)
ifnum = math.floor(ifnum/10000)
ifnum = ifnum * 10000
ifnum = np.int(ifnum)
print(' data needed from Block =',ifnum)


print(' reading input file')
npzfile = np.load('YBlock87_'+str(ifnum)+'.npz')
fglobe87 = npzfile['cglobe']

#df = npzfile['df']
nlat  =   npzfile['nlat']
nlon  =   npzfile['nlon']
npolarity =npzfile['npolarity']
ifzero  =   npzfile['istart']
print(' ifzero for 1987=',ifzero)
latgrid =npzfile['latgrid']
longrid =npzfile['longrid']
print(' finished extracting input file 87')

print(' fglobe87 shape=',np.shape(fglobe87))

nsamp = np.size(fglobe87,axis=3)
print(' number of samples=',nsamp)

#fzero = (ifzero-1)* df
fzero = ifzero* df
fmax = (ifzero+nsamp-1) * df
if (fzero > 0):
    periodmax=(1.0/fzero)/60.0
else:
     periodmax=999999999.0

periodmin=(1.0/fmax)/60.0
print(' maximum period=',periodmax,'  minimum period=',periodmin)
print(' nlat=',nlat,' nlon=',nlon)


fzero = np.longdouble(ifzero * df)

print(' original index=',np.round( finter/df) )
#ifi = np.int(np.round( finter/df) - ifzero ) +1
ifi = np.int(np.round( finter/df) - ifzero ) 

font = {'family': 'serif',
        'weight': 'normal',
        'size': 8,
        }

ifisave = ifi

indx = ifisave + ifzero
ftemp = (indx * df)
pertemp = (1.0/ftemp)*2.0/60.0
ftemp = (ifisave*df) + fzero
pertemp = (1.0/ftemp)*2.0/60.0

pertemp = (1.0/ftemp)*2.0/60.0

xa1 = min(longrid)
xa2 = max(longrid)
ya1 = min(latgrid)
ya2 = max(latgrid)
  
globemap87=np.zeros((nlat,nlon,npolarity))

nplot = 3
nyplot = 6
nxplot = int(nplot/nyplot + 1.0)
if (nplot < nyplot):
    nyplot = nplot
    nxplot = 1
print('nplot=',nplot,'nxplot=',nxplot,' nyplot=',nyplot)
fig = plt.figure(figsize=[nyplot*4.0,nxplot*11.0/3.0])
plt.subplots_adjust(hspace=0.35)
ipcnt = 0
ixcnt = 1
iycnt = 1
nofplot = np.int(nplot/2.0)
for ifi in range(ifisave-nofplot,ifisave+nofplot+1):

    if (ifi < 0):
        sys.exit()

    freq = ifi * df + fzero
    period =  (1.0/freq)/60.0 
    operiod = period * harmonic 
    #if ( ifi%1000 == 0):
    print('ifi=',ifi,' freq=',freq,' operiod=',operiod)
    print('operiod=',operiod*60.0,'seconds')



    for ilat in range(nlat) :
        for ilon in range(nlon) :
            for ipol in range(npolarity) :
                globemap87[ilat,ilon,ipol] = np.abs( fglobe87[ipol,ilon,ilat,ifi] )
            
    fmaxall = 0.0
    fmaxacor = 0.0
    ipoint87 = -1
    for ipol in range(npolarity) :
        fmax= np.max(np.absolute(globemap87[:,:,ipol]))
        if fmax > fmaxall :
            fmaxall = fmax
            ipoint87 = ipol

################################################
    if ifi == ifisave:
        ipoint87 = 4
################################################

    rc('font',family='serif')

    if (ipoint87 > -1):


        if ( 1 == 1):
            ipcnt = ipcnt + 1
            print(' ipcnt=',ipcnt,' ixcnt=',ixcnt,'iycnt=',iycnt)
            plt.subplot(nxplot,nyplot,ipcnt)
            mmmx = globemap87[:,:,ipoint87]
            plt.imshow( mmmx ,aspect='auto',extent=(xa1,xa2,ya1,ya2),cmap='jet')
            ttt = source+' 1987 \n '\
            ' orbital period='+str("%3.8f" % operiod)+' min.\n'+\
            ' signal period='+str("%3.8f" % period)+' min.'
            plt.title(ttt, fontdict=font)
            plt.xlabel('longitude')
            plt.ylabel('latitude')
            plt.colorbar()

            ixcnt = ixcnt + 1
            if (ixcnt > nxplot):
                ixcnt = 1
                iycnt = iycnt + 1


plotname=source+'-87-harm'+str(harmonic)+'-resp.pdf'
plt.savefig(plotname)
plt.show()

#



