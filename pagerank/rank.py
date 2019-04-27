'''
This program used to retrieve the links stored in the database,
apply the pagerank algorithm to the links.
'''

import pandas as pd
import numpy as np
import sqlite3

conn = sqlite3.connect('pagerank.sqlite')
cur = conn.cursor()

from_list = []
to_list = []

try:
    cur.execute('SELECT from_id,to_id FROM Links LIMIT 1')
except:
    print('Failed to get links from database Links.')

if cur is None:
    print('Nothing in database Links, run crawler.py to get links.')
    cur.close()
else:
    many = input('Enter the maximum number of iterations(default 10): ')
    if (len(many) < 0) or (int(many) < 1):
        max_ite = 10
    else:
        max_ite = int(many)
    ## start retrieve the links from database
    cur.execute('SELECT from_id,to_id FROM Links')
    for (from_id,to_id) in cur:
        from_list.append(from_id)
        to_list.append(to_id)

    ## remove the repeated links
    pairs = set(zip(from_list,to_list))
    from_to= list(zip(*pairs))
    from_list, to_list = from_to[0], from_to[1]
    
    from_to_df = pd.DataFrame({'from_id':from_list,'to_id':to_list})
    id_rank_df = pd.DataFrame({'id':from_list,'rank':np.array([1]*len(from_list))})
    fromid_link_num = pd.DataFrame(from_to_df.groupby('from_id').count()).rename(columns={'to_id':'outlink#'}).reset_index()
    id_received = pd.DataFrame({'id':to_list,'received':np.array([0]*len(to_list))})
    for i in range(max_ite):
        
        continue