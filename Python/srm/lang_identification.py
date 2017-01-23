
'''
Created on 05-Nov-2015

@author: unni
'''



import langid
from db_manager import connect_to_db

host_name = "10.5.23.213"
user_name = "root"
password = "root"


def find_lang(db_name, table):
    cursor_mysql = connect_to_db(host_name, user_name, password)
    cursor_mysql.execute("select distinct tweetText from %s.%s"%(db_name,table))
    lang_dict = {'hi':0, 'en':0}
    for row in cursor_mysql.fetchall():
        lang = langid.classify(row[0])
        lang_dict[lang[0]]+=1
    print lang_dict 
if __name__ == '__main__':
    langid.set_languages(['hi', 'en'])   
    #find_lang('Events', 'BigBillionDay')
    print langid.classify('yeh hindi hein')