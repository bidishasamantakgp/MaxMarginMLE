
# coding: utf-8

# In[20]:
from __future__ import unicode_literals
import sqlite3
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import ast
import operator
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

# -*- coding: ascii -*-


# In[21]:
def generateDataFromFile(filename):
    f = open(filename)
    hashtaglist = []
    for line in f:
        hashtaglist.append(line)
    return hashtaglist

# In[4]:

def setupconnection():
    conn = sqlite3.connect("/home/bidisha/Data2017Hashtag/dataKDD/random_sample_processed.db")
    return conn


# In[5]:

def getuniquehashtag(c):
    results = c.execute("Select distinct(Hashtag) from hashtagUsageInfo")
    hashtagName = [row[0] for row in results]
    return hashtagName


# In[8]:

def relativetimestamp(hashtags, c):
    dicthashtag = defaultdict(list)
    mintimestamp = 1374696959
    for hashtag in hashtags:
        timestamps = [row[0] for row in c.execute('Select UnixTimeStamp from hashtagUsageInfo where Hashtag='+'\"'+hashtag+'\"'+'order by UnixTimeStamp')]
        relativetimestamps = [(x - mintimestamp) for x in timestamps]
        tempstr=','.join(str(x) for x in relativetimestamps)
        dicthashtag[hashtag] = relativetimestamps
    return dicthashtag


# In[10]:

def timestamp(hashtags, c):
    dicthashtag = defaultdict(list)
    for hashtag in hashtags:
        timestamps = [row[0] for row in c.execute('Select UnixTimeStamp from hashtagUsageInfo where Hashtag='+'\"'+hashtag+'\"'+'order by UnixTimeStamp')]
        relativetimestamps = [(x - timestamps[0]) for x in timestamps]
        tempstr=','.join(str(x) for x in relativetimestamps)
        dicthashtag[hashtag] = relativetimestamps
    return dicthashtag


# In[11]:

def plotData(data, start, end):
    count = 0
    bins = np.linspace(start, end, 100)
    colors = cm.rainbow(np.linspace(0, 1, len(data.keys())))
    #print colors
    #colors = ['r', 'b', 'g', 'w', 'y', 'o', ''
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
    plt.legend(loc='upper right', prop={'size':10})
    plt.xlabel('Tweeted time', fontsize=18)
    plt.ylabel('Tweet volume', fontsize=18)
    plt.show()



# In[13]:

def topKHahstag(dicthashtag, starttime, endtime, k):
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


# In[93]:

#mintimestamp = 1374696959;


# In[22]:

#topK = topKHahstag(dicthashtag.keys()[0], 0, 864000, 10)
#dicthashtag = generateDataFromFile("HashtagTimeStamp.txt")


# In[ ]:

if __name__ == "__main__":
    conn = setupconnection()
    c = conn.cursor()
    hashtagList = generateDataFromFile('TempName.txt')
    #getuniquehashtag(c)
    hashdict = relativetimestamp(hashtagList, c)
    resultdict = topKHahstag(hashdict, sys.argv[1], sys.argv[2], sys.argv[3])
    f = open(sys.argv[4],"a")
    #for hashtag in hashtagList:
    #    f.write(hashtag+"\n")
    for hashtag in resultdict.keys():
	 f.write(hashtag+"\n")	
    f.close()
    conn.close()
    
    


# In[2]:

#topK = topKHahstag(dicthashtag, 60000, 518400, 10)
#print topK
#plotData(topK, 0, 60000)
#plotData(topK, 60000, 180000)

