#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 08-Dec-2015
Some of the DB schemas needs to be cleaned up to improve DB designs. This module does that. 
@author: unni
'''
#import pymysql
from db_manager import connect_to_db
import traceback
import datetime

host_name = "10.5.23.213"
user_name = "root"
password = "root"

def make_hashtag_table(db_name, table):
    """
    Creates a hashtag table from the hashtags included as comma seperated values in the original design. 
    """
    hashtag_table = table+"Hashtags"
    cursor_mysql, conn = connect_to_db(host_name, user_name, password)
    cursor_mysql.execute("select id_str, hashTags from %s.%s"%(db_name,table))
    
    for row in cursor_mysql.fetchall() :
        id_str = row[0]
        hashtags = row[1].split(",")
        for hashtag in hashtags :
            print hashtag, id_str
            try :
                cursor_mysql.execute("insert into %s.%s values('%s', '%s')"%(db_name, hashtag_table, id_str, hashtag))
            except:
                traceback.print_stack()
                
    conn.commit()
    conn.close()
      
        
if __name__ == '__main__':
    make_hashtag_table("srm", "BASD3")
    
    
    
    
    
        