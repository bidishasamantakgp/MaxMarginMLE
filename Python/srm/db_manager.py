'''
Created on 25-Oct-2015

@author: unni
'''
import pymysql

host_name, user_name, password = None, None, None

cursor_mysql, conn = None, None
def connect_to_db(host, user, pw):
    """Establishes a connection to the DB specified by host with user and
    
    @return: the cursor object for the connection
    """
    global host_name, user_name, password, cursor_mysql, conn
    host_name, user_name, password = host, user, pw 
    
    conn = pymysql.connect (host = host,
                   user = user,
                   passwd = pw)
    cursor_mysql = conn.cursor ()
    return cursor_mysql, conn
def execute_sql(sql, params=()):
    if host_name == None : #If connection has not been established
        raise Exception("Please establish a connection first")
    cursor_mysql, conn = connect_to_db(host_name, user_name, password)
    cursor_mysql.execute(sql%params)
    result_set = cursor_mysql.fetchall()
    conn.close()
    return result_set

if __name__ == '__main__':
    pass
    #cursor_mysql, conn = connect_to_db("10.5.23.213", "root", "root")
    #execute_sql("SELECT hashtag, count(*)  FROM %s.%s group by hashtag order by count(*) desc",
    #            ("srm", "BigBillionDayHashtags"))    
    