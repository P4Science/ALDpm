# -*- coding: utf-8 -*-
"""
@author: Peter M. Piechulla,
publlished under GNU General Public License v3.0 
15th July 2025

"""

mtdata=utils.getMT()


# Get all articles that use Pt for electrocatalysts

filterlist=[('area','electrocatalysis','in')]
thisdata=utils.filterCriteria(mtdata,filterlist,exact=True)

filterlist=[('coating','Pt','in')]
thisdata=utils.filterCriteria(thisdata,filterlist,exact=False)

print("\nArticles using Pt for electrocatalysts:\n")
print(np.unique(thisdata['DOI']))



# Articles using plasma in B reaction

filterlist=[('reactB','plasma','in')]
thisdata=utils.filterCriteria(mtdata,filterlist,exact=False)

print("\nArticles using plasma in B reaction:\n")
print(np.unique(thisdata['DOI']))

