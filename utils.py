# -*- coding: utf-8 -*-
"""
@author: Peter M. Piechulla,
publlished under GNU General Public License v3.0 
15th July 2025

"""



import numpy as np
import re
import pandas as pd


def getMT():
    mtdata = pd.read_excel('2025-07-09_DOI-10.5281-zenodo.12700975.xlsx')
    # removing long column names, keeping short identifiers
    mtdata = mtdata.drop(0)
    mtdata.fillna("",inplace=True)
    return mtdata


def filterCriteria(datatable,filterlist,expand='no',exact=True):
    """
    datatable: dataframe to filter e.g. mtdata
    
    filterlist: list of 3-tuple strings, (key, val, in/ex)
    example: [('supportsCat','C','in')]
            val can also be a list
    
    expand: default 'no'
            some fields are only filled for one line per paper, e.g. area. 
            expand fills all lines of a given key, e.g. area, with the value.
    
    exact: default True, i.e. looking for exact and complete match
                if False: includes entries where val is a substring of the cell content. Works only if val is a single value, not a list
                
    returns a filtered list.
    
    """
    
    fdata=datatable.copy() 
    fdata.fillna("",inplace=True)
    dois=np.unique(fdata['DOI'])


    for doi in dois:
        mask=fdata['DOI']==doi
        subind=fdata.index[np.array(mask).flatten()]
        filen=fdata.loc[subind[0],'first author']
        fdata.loc[subind,'first author']=filen #.item()
        if expand!='no':
            expval=fdata.loc[subind[0],expand]
            fdata.loc[subind,expand]=expval #.item()

    for filt in filterlist:
        key=filt[0]
        val=filt[1]
        inex=filt[2]
        if type(val) is str:
            if inex=='in':
                if exact:
                    fdata=fdata.iloc[np.where(fdata[key]==val)[0]]     
                else:
                    find=[]
                    for i in fdata.index:
                        if val in fdata[key].loc[i]:
                            find.append(i)
                    fdata=fdata.loc[find]
            elif inex=='ex':
                fdata=fdata.iloc[np.where(fdata[key]!=val)[0]]
        if type(val) is list:
            print("Criterium is a list of values: "+str(val))
            find=[]
            for i in fdata.index:
                if fdata[key].loc[i] in val and inex=='in':
                    find.append(i)
                if fdata[key].loc[i] not in val and inex=='ex':
                    find.append(i)
            fdata=fdata.loc[find]
    return fdata

def avgCol(qty):
    """getting the mean of a column if multiple values are in one cell. Fill the empty cells with zeros to maintain the index.
    qty is given as a string array of the respective column, e.g., as mtdata['qty']"""
    numbers=np.zeros(qty.shape)
    searchpattern=r"[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?"
    for i,b in enumerate(qty):
        if b=='' or b is None:
            continue
        b= re.sub(r"(?<=\d)-(?=\d)", ";", b)
        nums=[]
        for num in re.findall(searchpattern,b):
            nums.append(num)
        numbers[i]=np.mean(np.array(nums, dtype=float))
    return numbers

def condenseNumbers(qty):
    """returns an array of values for a quantity. If a range or multiple values are given in the same cell
    they will all be in the list"""
    numbers=[]
    searchpattern=r"[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?"
    for b in qty:
        if b=='':
            continue
        b= re.sub(r"(?<=\d)-(?=\d)", ";", b)
        for num in re.findall(searchpattern,b):
            numbers.append(num)
    numbers=np.array(numbers,dtype=float)
    return numbers


