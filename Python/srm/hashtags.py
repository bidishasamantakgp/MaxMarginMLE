'''
Created on 09-Dec-2015
*** Make sure you change the company handles from '951522626','57947109' in case the event is not of Flipkart 
@author: unni
'''
from db_manager import connect_to_db, execute_sql
import traceback
import datetime

host_name = "10.5.23.213"
user_name = "root"
password = "root"
def hashtag_count_vs_time(db_name, table, top_tags=[], is_tweet_volume = True):
    """
    Find the volume of tweets/count of users who tweeted a certain hashtag during the event window.
    top_tags : Top hashtags from the DB
    is_tweet_volume: If false, the count of users is considered.
    
    Return : 
        1. hashtag_count - dict. hashtag: (date range list, hashtagcount list)
        2. hashtag_reply_timestamps - dict. hashtag: (timestamps at which the company handle replied)
    The first return value hashtag_count is generated in a way to plot as date range vs hashtag count graph
    Second return value indicates the timestamps at which the company handle replied. Used to mark these 
    points in a graph to see the effectiveness of reply.  
    """
    #time_format = '%Y-%m-%d %H:%M:%S'
    cursor_mysql, conn = connect_to_db(host_name, user_name, password)
    cursor_mysql.execute("select min(created_at), max(created_at) from %s.%s"%(db_name, table))
    min_date, max_date = cursor_mysql.fetchall()[0]
    
    print "Date range", min_date, max_date
    max_date = max_date+datetime.timedelta(hours = 1) #To make sure that tweets from last windows are counted fully 
    #print type(min_date)
    hash_tag_count, hashtag_reply_timestamps = dict(), dict()   
    for hashtag in top_tags :
        min_time_stamp = min_date
        max_time_stamp = min_date+datetime.timedelta(hours = 1)
        while(max_time_stamp <= max_date):
            reply_timestamps = execute_sql("select created_at from %s.%s where \
                reply_tweet_id in (select id_str from %s.%s where hashTags like '%s') and \
                user_id_str in ('951522626','57947109')", (db_name, table, db_name, table, "%"+hashtag+"%"))
            if len(reply_timestamps) == 0 : # For this tweet, no reply was given
                break
            
            if is_tweet_volume :
                sql = "select count(*) from %s.%s where hashTags like '%s'\
                    and created_at >= '%s' and created_at < '%s';"
            else:
                sql = "select count(distinct(user_id_str)) from %s.%s where hashTags like '%s' \
                    and created_at >= '%s' and created_at < '%s'"
            cursor_mysql.execute(sql %(db_name, table,'%'+hashtag+'%',str(min_time_stamp), str(max_time_stamp)))
            tweet_count = int(cursor_mysql.fetchall()[0][0])
            #print hashtag, tweet_count, min_time_stamp, max_time_stamp
            if not hash_tag_count.has_key(hashtag):
                hash_tag_count[hashtag] = list()
            hash_tag_count[hashtag].append((max_time_stamp,tweet_count))
            min_time_stamp, max_time_stamp = max_time_stamp, max_time_stamp+datetime.timedelta(hours = 1)
        if len(reply_timestamps) > 0 :
            hashtag_reply_timestamps[hashtag] = reply_timestamps
    #print hash_tag_count    
    #print sum( x[1] for x in hash_tag_count['CheckSnapdealToday'])
    
    """for hashtag in hash_tag_count.keys():
        print hashtag
        print  ",".join([str(x[0]) for x in hash_tag_count[hashtag]])
        print ",".join([str(x[1]) for x in hash_tag_count[hashtag]])
    """   
    return hash_tag_count, hashtag_reply_timestamps   
    conn.close()
    
    
        
if __name__ == '__main__':
    cursor_mysql, conn = connect_to_db(host_name, user_name, password)
    """reply_timestamps = execute_sql("select created_at from srm.BigBillionDay where \
                reply_tweet_id in (select id_str from srm.BigBillionDay where hashTags like '%s') and \
                user_id_str in ('951522626','57947109')", ("%flipkart%"))
    #print company_reply_timestamps
    top_hashtags = [ x[0] for x in execute_sql("SELECT hashtag  FROM srm.BigBillionDayHashtags group by hashtag order by count(*) desc limit 5")]
    #print top_hashtags
    hashtag_count_vs_time("srm", "BigBillionDay", top_hashtags, False)
    """