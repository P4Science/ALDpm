# -*- coding: utf-8 -*-
"""
@author: Peter M. Piechulla,
publlished under GNU General Public License v3.0 
15th July 2025

"""


# %%  support categories as for pie chart
import numpy as np
import pandas as pd
import copy
import utils


mtdata=utils.getMT()

suppDict = {
    'MH': "Metal compounds (excl. oxides)",
    'MN': "Metal compounds (excl. oxides)",
    'MHD': "Metal compounds (excl. oxides)",
    'MC': "Metal compounds (excl. oxides)",
    'MS': "Metal compounds (excl. oxides)",
    'MX': "Metal compounds (excl. oxides)",
    'C' : "Carbons", 
    'CC': "Coated carbons",
    'M': "Metals\nincl. alloys", 
    'MO': "Oxides",
    'SC': "Semiconductors",
    'SM': "Metals\non support",
    'mof': "MOFs", 
    'na': "Not specified",
    'org': "Organics", 
    'other': "Others",
    'poly': "Organics"} 


allSupp=mtdata['supportsCat'].dropna()
allSuppRed=allSupp.map(suppDict)
mtdataRed=copy.copy(mtdata)
mtdataRed['supportsCat']=allSuppRed

redCats, redOcc = np.unique(allSuppRed,return_counts=True)

sortSupp=pd.DataFrame(columns=["support category", "Occurence"])
sortSupp["support category"]=redCats
sortSupp["Occurence"]=redOcc
sortSupp=sortSupp.sort_values("Occurence",ascending=False)


tX=5
topX=sortSupp[:tX].copy()

others = pd.DataFrame(data = {
    "support category" : ['Others'],
    "Occurence" : [sortSupp['Occurence'][tX:].sum()]
})

topXandothers = pd.concat([topX, others])

#%% size histogram data

def getHistData(mtdata):
    size=np.array(mtdata["particlesize"])
    sizerange=np.zeros((len(size),3))
    bins=np.logspace(-9,-2,25)
    sizerange[:,2]=utils.avgCol(size)
    return sizerange, bins

sizerange, bins = getHistData(mtdataRed)




#%% small histogram for each material


from matplotlib.gridspec import GridSpec


mm=1/25.4
fsize=8

slpx=0.02
slpy=0.80

fig = plt.figure(figsize=(80*mm, 110*mm))
gs = GridSpec(5, 2)

ax_pie = fig.add_subplot(gs[:2,:])


axes = [None]*6
axes[0]=fig.add_subplot(gs[2,0])

for i in range(1,3):
    axes[i]=fig.add_subplot(gs[i+2,0])
    
for i in range(0,3):
    axes[i+3]=fig.add_subplot(gs[i+2,1])


import matplotlib.ticker as ticker


histCategories=[cat for cat in sortSupp['support category'].iloc[:tX]]
summedUpCategories=[cat for cat in sortSupp['support category'].iloc[tX:]]
allCats=histCategories+summedUpCategories
histCategories.append(allCats)
reorder=[5,0,1,2,3,4]
histCategories=[histCategories[i] for i in reorder]


nBins=16
bins=np.logspace(-9,-2,nBins+1)
cmap=plt.get_cmap('tab10')
colors=[cmap(i) for i in range(10)]
colors.append('grey')
matplotlib.rcParams['hatch.linewidth'] = 0.25
hatches = ['////', '\\\\', '||||||', '----', '++++','xxxx']
histcolors=['grey']+colors
histhatches=['']+hatches



for i, suppCat in enumerate(histCategories):
    filterlist=[('supportsCat',suppCat,'in')]
    thisMT=utils.filterCriteria(mtdataRed,filterlist)
    size=utils.avgCol(np.array(thisMT["particlesize"]))
    ax=axes[i]
    thisHist, bins, patches = ax.hist(1e-6*size,bins=bins,log=True,
                                      rwidth=0.8,color=histcolors[i],hatch=histhatches[i])
    ax.set_xscale('log')
    ax.set_yscale('linear')
 
    
plt.subplots_adjust(hspace=0.1)


xlim=axes[0].get_xlim()
for ax in axes[1:3]:
    ax.set_xlim(xlim)
    ax.spines['top'].set_visible(False)
    
for ax in axes[4:6]:
    ax.spines['top'].set_visible(False)



xt=np.logspace(-9,-2,8)
yt=[[0,200],[0,200],[0,10],[0,10],[0,10],[0,10],[0,200]]
histlabels=['b)','c) ','d)','e)','f)','g)','h) all materials']
for i,ax in enumerate(axes):
    ax.set_yticks(yt[i])
    ax.tick_params(labelsize=fsize) #,pad=0.04)
    ax.tick_params(axis='y',pad=0.04)
    ax.set_xticks(xt)
    ax.text(slpx,slpy,histlabels[i],transform=ax.transAxes,size=fsize)


fig.text(0.5,0,"Particle size (m)",ha='center',va='bottom',fontsize=fsize)
axes[1].set_ylabel('Frequency (#)',fontsize=fsize,labelpad=0.1)

def si2str(x):
    return x

secpad=0.06
secax = axes[0].secondary_xaxis('top', functions=(si2str, si2str))
secax.set_xticks(xt)
secax.set_xticklabels(['nm','','','µm','','','mm',''])
secax.tick_params(labelsize=fsize,pad=secpad)
secax.xaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=[], numticks=10))

secax2 = axes[3].secondary_xaxis('top', functions=(si2str, si2str))
secax2.set_xticks(xt)
secax2.set_xticklabels(['nm','','','µm','','','mm',''])
secax2.tick_params(labelsize=fsize,pad=secpad)
secax2.xaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=[], numticks=10))


axes[0].set_xticklabels([])
for ax in axes[:2]:
    ax.set_xticklabels([])
for ax in axes[3:5]:
    ax.set_xticklabels([])
    
axes[5].set_xticklabels(['$10^{-9}$','','','$10^{-6}$','','','$10^{-3}$',''])    
axes[2].set_xticklabels(['$10^{-9}$','','','$10^{-6}$','','','$10^{-3}$',''])    
    
sa=60
wedges, texts, pcttexts=ax_pie.pie(topXandothers["Occurence"], labels=topXandothers["support category"],autopct='%1.1f%%',startangle=sa,
           colors=colors[:tX+1],hatch=hatches[:tX+1], textprops={'fontsize': fsize},pctdistance=0.70)

ax_pie.set_aspect('equal')  # Keep pie chart circular

for tx in pcttexts:
    tx.set_color("white") 
    tx.set_fontweight("bold")


ax_pie.text(slpx,slpy,"a)",transform=ax_pie.transAxes,size=fsize)
plt.subplots_adjust(right=0.99,bottom=0.09,top=0.90)
pos = ax_pie.get_position()  
oversize=0.35
ax_pie.set_position([pos.x0-oversize/3, pos.y0+oversize/20, pos.width*(1+oversize),pos.height+oversize/3]) 
