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
## start retrieve the links from database
cur.execute('SELECT from_id,to_id FROM Links')
for (from_id,to_id) in cur:
    from_list.append(from_id)
    to_list.append(to_id)
## remove the repeated links
pairs = set(zip(from_list,to_list))
from_to = list(zip(*pairs))

from_list, to_list = from_to[0], from_to[1]
print(from_list)
print(to_list)