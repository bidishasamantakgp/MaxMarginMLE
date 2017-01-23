'''
Created on 25-Oct-2015
Handles the operations related to the calculation of bursts in the network        
@author: unni
'''
import csv

from db_manager import connect_to_db
from dateutil import rrule
from datetime import datetime, timedelta
from analysis_tools import pearson

host_name = "10.5.23.213"
user_name = "root"
password = "root"

def calculate_user_burst(start_timestamp, end_timestamp, db_name, table):
    cursor_mysql = connect_to_db(host_name, user_name, password)
    cursor_mysql.execute("select distinct user_id_str from %s.%s"%(db_name,table))
    userid_list = [row[0] for row in  cursor_mysql.fetchall()]
    #Convert the time stamp strings to python datetime format
    time_format = '%Y-%m-%d %H:%M:%S'
    start_time = datetime.strptime(start_timestamp, time_format)    
    end_time = datetime.strptime(end_timestamp, time_format)
    
    burst_list = list() #Stores the list of user burst lists
    time_step = 5
    for user in userid_list :
        time_window_beg = start_time
        time_window_end = start_time+timedelta(hours=time_step)
        user_burst = [user] # list: [user_id, #tweets in time windows on a per hour basis]
        #print user, "\n--------------\n"
        
        while(time_window_end<=end_time):
            cursor_mysql.execute("select count(id_str) from %s.%s where created_at>= '%s' and created_at < '%s' and user_id_str = %s "
                                 %(db_name, table, time_window_beg.strftime(time_format), time_window_end.strftime(time_format), user))
            user_burst.extend([x[0] for x in cursor_mysql.fetchall()])
            #print time_window_beg, "-", time_window_end, user_burst[-1]
            time_window_beg, time_window_end = time_window_end, time_window_end+timedelta(hours =time_step) 
            
        #print user_burst
        burst_list.append(user_burst)
    #print burst_list
    print len(burst_list)
    return burst_list #list of list with sublist in the form [user_id, #tweets in time windows on a per hour basis]
def calculate_total_burst(start_timestamp, end_timestamp, db_name, table):
    """
        Calculates the overall burst in the network taking all users together
    """
    cursor_mysql = connect_to_db(host_name, user_name, password)
    time_format = '%Y-%m-%d %H:%M:%S'
    start_time = datetime.strptime(start_timestamp, time_format)    
    end_time = datetime.strptime(end_timestamp, time_format)
    time_step = 5
    time_window_beg = start_time
    time_window_end = start_time+timedelta(hours=time_step)
    
    total_burst = list()
    while(time_window_end<=end_time):
            cursor_mysql.execute("select count(id_str) from %s.%s where created_at>= '%s' and created_at < '%s' "
                                 %(db_name, table, time_window_beg.strftime(time_format), time_window_end.strftime(time_format)))
            total_burst.extend([x[0] for x in cursor_mysql.fetchall()])
            time_window_beg, time_window_end = time_window_end, time_window_end+timedelta(hours =time_step)
    return total_burst
if __name__ == '__main__':
    start_timestamp = "2014-12-06 00:30:35" #BASD2    
    end_timestamp = "2014-12-13 23:58:20"  #BASD2
    
    user_burst_list = calculate_user_burst(start_timestamp, end_timestamp, "Events", "BigAppShoppingDay")
    total_burst = calculate_total_burst(start_timestamp, end_timestamp, "Events", "BigAppShoppingDay")
    with open("burst_correlation.csv", "w") as csvfile :
        csv_writer = csv.writer(csvfile)
        for burst in user_burst_list :
            coeff = pearson(burst[1:], total_burst)
            csv_writer.writerow([burst[0], coeff])
        
    
    
