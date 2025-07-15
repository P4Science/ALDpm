# -*- coding: utf-8 -*-
"""
@author: Peter M. Piechulla,
publlished under GNU General Public License v3.0 
15th July 2025

"""

import numpy as np
from matplotlib.ticker import MultipleLocator
    
import pandas as pd
import utils


mtdata=utils.getMT()

filterlist=[('reactD','dummy','ex')]
mtdata=utils.filterCriteria(mtdata,filterlist,expand='year',exact=True)

reactdict={'(flow-type)': 'Packed bed',
           'flow-type': 'Packed bed',
           'fluidized bed': 'Fluidized bed',
           'viscous flow': 'Powder tray fixture',
           '(viscous flow)': 'Powder tray fixture',
           'rotary': 'Rotary drum'}
           

bins=np.arange(1985,2023.5,1,dtype=int)
def fillYears(ye,oc):
    filledyears=bins
    fillocc=np.zeros(filledyears.shape)
    for i,y in enumerate(filledyears):
        try:
            fillocc[i]=oc[np.where(ye==y)][0] 
        except:
            continue
        
    return filledyears,fillocc


yearreact=pd.DataFrame(columns=['year','operation principle'])
yearreact['operation principle']=mtdata['operation principle'].loc[mtdata['operation principle']!=''].replace(reactdict)
yearreact['year']=np.array(mtdata['year'].loc[mtdata['operation principle']!=''],dtype=int)

    
ald_reacts,counts=np.unique(yearreact['operation principle'],return_counts=True)
ald_reacts=ald_reacts[np.argsort(counts)[::-1]]
counts=counts[np.argsort(counts)[::-1]]



f,ax=plt.subplots(1,figsize=(100/25.4,75/25.4))

plotreacts=['Packed bed','Fluidized bed','Powder tray fixture','Rotary drum']

colors=['b','r','g','m']
symbs=['o','s','d','^']

allplotdata=np.zeros((bins.shape[0],5))
allplotdata[:,0]=bins

for i,react in enumerate(plotreacts):
    print(react)
    thisReact=yearreact.loc[yearreact['operation principle']==react]
    years,occ=np.unique(thisReact['year'],return_counts=True)
    years,occ=fillYears(years,occ)
    allplotdata[:,i+1]=occ



matplotlib.rcParams['hatch.linewidth'] = 0.4
hatches = ['////', '\\\\', '||||', '----', '++++']

ax.stackplot(allplotdata[:,0],allplotdata[:,1],allplotdata[:,2],allplotdata[:,3],allplotdata[:,4],
             labels=plotreacts,
             hatch=hatches)

ax.legend()
ax.axis([1989,2023,0,60])
ax.xaxis.set_minor_locator(MultipleLocator(1))


ax.set_xlabel("Year of publication")
ax.set_ylabel("Number of published articles")


plt.tight_layout()