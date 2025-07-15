# -*- coding: utf-8 -*-
"""
@author: Peter M. Piechulla,
publlished under GNU General Public License v3.0 
15th July 2025

"""



import utils
import copy
import numpy as np
from matplotlib.ticker import MultipleLocator

mtdata=utils.getMT()

supps=['Oxides',
       'Carbons',
       'Metals on support',
       'Organics',
       'Metals incl. alloys']

suppDict = {
    'MH': "Metal compounds (excl. oxides)",
    'MN': "Metal compounds (excl. oxides)",
    'MHD': "Metal compounds (excl. oxides)",
    'MC': "Metal compounds (excl. oxides)",
    'MS': "Metal compounds (excl. oxides)",
    'MX': "Metal compounds (excl. oxides)",
    'C' : "Carbons", 
    'CC': "Coated carbons",
    'M': "Metals incl. alloys", 
    'MO': "Oxides",
    'SC': "Semiconductors",
    'SM': "Metals on support",
    'mof': "MOFs", 
    'na': "Not specified",
    'org': "Organics", 
    'other': "Others",
    'poly': "Organics"} 



mtdata_redsupp=copy.copy(mtdata)
mtdata_redsupp['supportsCat']=mtdata_redsupp['supportsCat'].map(suppDict)


cmap=plt.get_cmap('tab10')


def geometricSSA(density,sizes):
    density*=1e-12 # converting from g/cm3 to g/um3, since sizes are given in um
    r=sizes/2
    return 3/(r*density)*1e-12 #the last missing factor converts um2 to m2

f, (ax,axPores)=plt.subplots(nrows=2,height_ratios=[2,1],figsize=(5,6))


markers=['o','^','v','<','>','s']
matplotlib.rcParams['hatch.linewidth'] = 0.4
hatches = ['////', '\\\\', '||||', '----', '++++','oooo','xxxx']
bins=np.arange(0,55,2)
binvals=np.zeros([bins.shape[0]-1])

for i, supp in enumerate(supps):
    filterlist=[('supportsCat',supp,'in')]
    fildata=utils.filterCriteria(mtdata_redsupp,filterlist,expand='area',exact=True)
    dia=utils.avgCol(fildata['particlesize'])
    ssa=utils.avgCol(fildata['areaSSA'])
    dia_ssa=dia[np.where(ssa!=0)]
    dia_ssa=dia_ssa[np.where(dia_ssa!=0)]
    ssa_dia=ssa[np.where(dia!=0)]
    ssa_dia=ssa_dia[np.where(ssa_dia!=0)]
    ax.scatter(dia_ssa,ssa_dia,color=cmap(i),s=5,marker=markers[i])
    ax.scatter(np.median(dia_ssa),np.median(ssa_dia),marker=markers[i],facecolors='w',color=cmap(i),zorder=3,s=60,label=supp)
    dp=np.array(fildata['dp'],dtype=str)
    numbersdp=utils.condenseNumbers(dp)
    
    binval,bins,patches=axPores.hist(numbersdp,bins=bins,bottom=binvals,
                                     rwidth=0.75,color=cmap(i),hatch=hatches[i],
                                     label=supp)
    binvals+=binval
    

slpx=-0.15
slpy=1.0
fsize=10

sizearray=np.logspace(-3,4,500)
geoSSA=geometricSSA(2.7,sizearray)
ax.plot(sizearray,geoSSA,'k--',linewidth=0.7,label='Sphere with $\\rho=2.7$ g/cm$^3$')
geoSSA_light=geometricSSA(1,sizearray)
ax.plot(sizearray,geoSSA_light,'k-.',linewidth=0.7,label='Sphere with $\\rho=1.0$ g/cm$^3$')

ax.legend(ncols=1,fontsize=9,frameon=False)
ax.axis([2e-3,4e3,8e-3,2e3])
ax.set_xlabel('Particle size ($\mu$m)')
ax.set_ylabel('Specific surface area (m$^2$/g)')
ax.set_xscale('log')
ax.set_yscale('log')
ax.text(slpx,slpy,"a)",transform=ax.transAxes,size=10)

maxy=80
axPores.vlines(2,0,maxy,color='k',linestyle='--',linewidth=0.75)
axPores.text(1,maxy,'Micropores', ha='right',va='top',fontsize=fsize,rotation='vertical')
axPores.text(27,maxy-3,'Mesopores', ha='center',va='top',fontsize=fsize)
axPores.vlines(50,0,maxy,color='k',linestyle='--',linewidth=0.75)
axPores.text(51,maxy-3,'Macro-\npores', ha='left',va='top',fontsize=fsize)
axPores.axis([-2,60,0,maxy])
axPores.xaxis.set_minor_locator(MultipleLocator(2))
axPores.set_xticks(np.arange(0,61,10))
axPores.legend(fontsize=9)
axPores.set_xlabel('Pore diameter (nm)')
axPores.set_ylabel('Frequency (#)')
axPores.text(slpx,slpy,"b)",transform=axPores.transAxes,size=10)

plt.tight_layout(h_pad=0.1,pad=0)
