
# coding: utf-8

# In[73]:

from matplotlib.backends.backend_pdf import PdfPages
import sys
import pandas as pd
#import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#%matplotlib notebook
import operator
import time
import ast
import scipy
import scipy.stats
import seaborn as sns
import numpy as np
import powerlaw
from collections import defaultdict
from srm.db_manager import connect_to_db, execute_sql


# In[85]:

db_name, table = sys.argv[1], sys.argv[2]
cursor_mysql, conn = connect_to_db("localhost", "root", "root")


# In[63]:

def plotData(data, start, end):
    count = 0
    bins = np.linspace(start, end, 10)
    colors = cm.rainbow(np.linspace(0, 1, len(data.keys())))
    #print colors
    #colors = ['r', 'b', 'g', 'w', 'y', 'o', ''
    
    plt.figure(figsize=(20,20))
    moddata=defaultdict(list)
    
    for k in data.keys():
        timestamp=data[k]
        for time in timestamp:
            if time>=start and time<=end :
                moddata.setdefault(k,[]).append(time)
    
    for (c,k) in zip(colors, data):
        #print k
        #k = unicode(k, "utf-8")
        count+=1
        plt.hist(moddata[k], bins, label = k, histtype='step', color = c)
    plt.yscale('log')
    plt.legend(loc='upper right', prop={'size':10})
    plt.xlabel('Tweeted time', fontsize=18)
    plt.ylabel('Tweet volume', fontsize=18)
    plt.show()


# In[12]:

def getuniquehashtag():
    results = execute_sql("Select distinct(hashTags) from %s.%s", (db_name, table))
    #hashtagMod1, hashtagMod2, hashtagMod3))
    hashtagName = []               
    for row in results:
        #print row[0]
        if (row[0] is None):
            continue
        hashtagName.extend(row[0].split(','))
    return list(set(hashtagName))


# In[18]:

def relativetimestamp(hashtags):
    dicthashtag = defaultdict(list)
    mintimestamp = [row[0] for row in execute_sql('Select min(created_at) from %s.%s',(db_name, table))]
    mintimestamp = int(time.mktime(mintimestamp[0].timetuple()))
    for hashtag in hashtags:
        hashtagMod1 = '\"%'+hashtag.strip()+',%\"'
        hashtagMod2 = '\"%,'+hashtag.strip()+'%\"'
        hashtagMod3 = '\"'+hashtag.strip()+'\"'
        timestamps = [row[0] for row in execute_sql("Select created_at from %s.%s where (hashTags like %s OR hashTags like %s OR hashTags like %s)         order by created_at;", (db_name, table, hashtagMod1, hashtagMod2, hashtagMod3))]
        relativetimestamps = [(int(time.mktime(x.timetuple())) - mintimestamp) for x in timestamps]
        tempstr=','.join(str(x) for x in relativetimestamps)
        dicthashtag[hashtag] = relativetimestamps
    return dicthashtag


# In[31]:

def generatehtFromFile(filename):
    f = open(filename)
    hashtaglist = []
    for line in f:
        hashtaglist.append(line)
    return hashtaglist


# In[32]:

def timestamp(hashtags):
    dicthashtag = defaultdict(list)
    for hashtag in hashtags:
        hashtagMod1 = '\"%'+hashtag.strip()+',%\"'
        hashtagMod2 = '\"%,'+hashtag.strip()+'%\"'
        hashtagMod3 = '\"'+hashtag.strip()+'\"'
        timestamps = [row[0] for row in execute_sql("Select created_at from %s.%s where (hashTags like %s OR hashTags like %s OR hashTags like %s)         order by created_at;", (db_name, table, hashtagMod1, hashtagMod2, hashtagMod3))]
        relativetimestamps = [(int(time.mktime(x.timetuple())) - int(time.mktime(timestamps[0].timetuple()))) for x in timestamps]
        tempstr=','.join(str(x) for x in relativetimestamps)
        dicthashtag[hashtag] = relativetimestamps
    return dicthashtag

# In[ ]:

def generateDataFromFile(filename):
    f = open(filename)
    dicthashtag = defaultdict(list)
    for line in f:
        tokens = line.strip().split("\t")
        hashtag = tokens[0]
        timestamp = ast.literal_eval(tokens[1])
        dicthashtag[hashtag] = timestamp
    return dicthashtag


# In[71]:

def calculateRank(dicthashtag, starttime, endtime, k):
    popularity_count = defaultdict(int)
    for key in dicthashtag.keys():
        timestamplist = dicthashtag[key]
        #print key,timestamplist
        for ts in timestamplist:
            if(ts>=starttime and ts<=endtime):
                popularity_count.setdefault(k, 0)
                popularity_count[key]+=1
    #print popularity_count
    sortedpc = sorted(popularity_count.items(), key=operator.itemgetter(1), reverse=True)
    #sortedpc = sorted(popularity_count, key=popularity_count.get, reverse=True)
    #print sortedpc
    topk = [row[0] for row in sortedpc[:k]]
    print topk
    resultDict = defaultdict(int)
    for tk in topk:
        #print defaultdict[tk]
        resultDict[tk] = dicthashtag[tk]
    return resultDict
    


# In[ ]:

hashtagList = getuniquehashtag()
hashtagmap = timestamp(hashtagList)
f = open("/home/bidisha/2017-hashtag-code/Data/Baseline"+table+"relative.txt","a")
countmap = defaultdict(list)
for hashtag in hashtagmap.keys():
    timestamps = hashtagmap[hashtag]
    if len(timestamps) > 200:
        countmap[hashtag] = len(timestamps)
	f.write(hashtag+"\t"+"["+",".join([str(x) for x in timestamps])+"]\n")
f.close()


# In[65]:

#hashtagdict = generateDataFromFile("/home/bidisha/2017-hashtag-code/Data/ICCT20relative.txt")

#hashtagList = generatehtFromFile("/home/bidisha/2017-hashtag-code/Data/ICCT20mini.txt")

#newhtdict = defaultdict(list)
#for key in hashtagList:
#    key = key.strip()
#    newhtdict[key] = hashtagdict[key]

#print newhtdict
#plotData(newhtdict, 0,1296000)
#plotData(newhtdict, 432000,1296000)


# In[79]:

#tempdict = calculateRank(newhtdict, 0, 1296000, 20)
#print tempdict
#tempdict = calculateRank(newhtdict, 0, 86400, 20)
#tempdict = calculateRank(newhtdict, 86400, 259200, 20)

