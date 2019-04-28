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
beta = 0.85 ## dumping factor used in pagerank

try:
    cur.execute('SELECT from_id,to_id FROM Links LIMIT 1')
except:
    print('Failed to get links from database Links.')

if cur is None:
    print('Nothing in database Links, run crawler.py to get links.')
    cur.close()
else:
    many = input('Enter the maximum number of iterations(default 10): ')
    if (len(many) < 1) or (int(many) < 1):
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
    from_list, to_list = list(from_to[0]), list(from_to[1])
    
    ## initalize the DataFrame
    from_to_df = pd.DataFrame({'from_id':from_list,'to_id':to_list})
    id_rank_df = pd.DataFrame({'id':(list(set(from_list+to_list))),'rank':1})
    id_link_num = pd.DataFrame(from_to_df.groupby('from_id').count()).rename(columns={'to_id':'outlink#'}).reset_index()
    
    ## start pagerank
    for i in range(max_ite):
        ## calculate the points of each node gives to the ndoes it links to
        fromid_out = id_link_num.merge(id_rank_df,how='inner',left_on='from_id',right_on='id')
        fromid_out['assign'] = fromid_out['rank']/fromid_out['outlink#']
        fromid_out = fromid_out[['from_id','assign']]

        ## aggregate the points each node received
        from_to_ass = from_to_df.merge(fromid_out,how='left',left_on='from_id',right_on='from_id')
        id_rec = from_to_ass[['to_id','assign']].groupby('to_id').apply(np.sum)['assign'].reset_index()

        ## get the new rank of each node
        id_rank_df = id_rank_df.merge(id_rec,how='left',left_on='id',right_on='to_id')[['id','assign']]
        id_rank_df.rename(columns={'assign':'rank'}, inplace=True)
        id_rank_df.fillna(value={'rank':0},inplace=True)

        ### apply dumping factor incase of the deadend
        id_rank_df['rank'] = 1 - beta + beta * id_rank_df['rank']
    
    conn.commit()
    ## print out the top 10 pages
    print('Successfully finished pagerank, the top 10 is:')
    top_ten = id_rank_df.sort_values('rank',ascending=False)[:10]
    for i in range(len(top_ten)):
        url_id = top_ten.iloc[i]['id']
        rank = top_ten.iloc[i]['rank']
        try:
            cur.execute('SELECT url FROM Pages WHERE id =?',(url_id,))
            url = cur.fetchone()[0]
            print('rank: {}, url: {}'.format(rank,url))
        except:
            print('failed to retrieve the url of id: %s' %url_id)
            continue
    
    ## store the results into database
    for i in range(len(id_rank_df)):
        url_id = id_rank_df.iloc[i]['id']
        rank = id_rank_df.iloc[i]['rank']
        cur.execute('UPDATE Pages SET new_rank = ? WHERE id = ?',(rank,url_id))
    conn.commit()
    cur.close()