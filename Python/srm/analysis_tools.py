'''
Created on 26-Oct-2015
Implements operations for data analysis
@author: unni
'''
import numpy
def pearson(list1, list2):
    return numpy.corrcoef(list1, list2)[0, 1]