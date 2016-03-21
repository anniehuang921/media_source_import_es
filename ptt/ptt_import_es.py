# coding: utf-8
#!/usr/bin/env python3
#encoding=utf-8
from time import *

t = process_time()
from imageuri import imageuri
import sys
import json
import getopt
import ast

import pandas as pd
import numpy as np
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.client import IndicesClient
import csv
import os
import logging
import datetime

es = Elasticsearch()
es_index=IndicesClient(es)

# set reactions for command
filename = sys.argv[1:][0]
print ("The filename is " + filename +".")

df = pd.read_csv(filename)
properties={
'platform':{ 'type': 'string'  },
'content':{ 'type': 'string'  },
'id':{ 'type': 'string'  },
'uri':{ 'type': 'string'  },
'time':{'type':   'date',
        'format': 'strict_date_optional_time||epoch_millis'},#"yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:SSZZ||epoch_millis"  },
'content_language':{ 'type': 'string'  },
'comments_count':{ 'type': 'integer'  },
'event':{ 'type': 'string'  },
'favorite_count':{ 'type': 'integer'  },
'from_parent_id':{ 'type': 'string'  },
'media_id':{ 'type': 'string'  },
'media_name':{ 'type': 'string'  },
'media_like_count':{ 'type': 'integer'  },
'from_user_category':{ 'type': 'string'  },
'from_user_id':{ 'type': 'string'  },
'from_user_like_count':{ 'type': 'integer'  },
'from_user_language':{ 'type': 'string'  },
'from_user_location':{ 'type': 'string'  },
'from_user_name':{ 'type': 'string'  },
'from_user_nick':{ 'type': 'string'  },
'from_user_realname':{ 'type': 'string'  },
'geo':{ 'type': 'geo_point'  },
'twi_hashtags':{ 'type': 'string'  },# array
'fb_hashtags':{ 'type': 'string'  },# array
'like_count':{ 'type': 'integer'  },
'post_type':{ 'type': 'string'  },
'share_target_uri':{ 'type': 'string'  },# array
'share_target_title':{ 'type': 'string'  },# array
'shared_domain':{ 'type': 'string'  },
'shared_initial_uri':{ 'type': 'string'  },
'shared_title':{ 'type': 'string'  },# array
'shared_uri':{ 'type': 'string'  },# array
'shares_count':{ 'type': 'integer'  },
'status_type':{ 'type': 'string'  },
'story_tag':{ 'type': 'string'  },#
'tags_id':{ 'type': 'string'  },#
'tags_name':{ 'type': 'string'  },#
'title':{ 'type': 'string'  },
'domain':{'type':'string'},
'update_time':{'type':   'date',
               'format': 'strict_date_optional_time||epoch_millis'  },
'image':{'type':'string'},
                }
rename={'forum':'media_name','author':'from_user_name','nick':'from_user_nick','ts':'time'}
#'forum', 'author', 'nick', 'title', 'content', 'ts', 'platform'

for i in rename.keys():
    if i in df.columns:
        df = df.rename(columns={i:rename[i]})      
    else:
        pass

if "geo_lat" in df.columns:
    geo=[]
    for i in range(len(df)):
        if np.isnan(df['geo_lat'][i]):
            geo.append(None)
        else:
            geo.append(str(df['geo_lat'][i])+","+str(df['geo_lng'][i]))
else:
    geo=None

df['geo']=geo
 
df['image']=list(map(lambda x: imageuri(x), df['content']))  
    
df['platform'] ='ptt'

if 'time' in df.columns:
    time=[]
    from datetime import datetime
    for i in df['time']:
        date = datetime.strptime(str(i),"%Y-%m-%d %H:%M:%S")
        time.append(datetime.isoformat(date)+'+08:00')
    df['time']= time

update_time = []
if 'update_time' in df.columns:
    from datetime import datetime
    for i in range(len(df)):
        if df['update_time'][i]!= None:
            date = datetimr.strptime(str(df['update_time'][i]),"%Y-%m-%d %H:%M:%S")
            update_time.append(datetime.isoformat(date)+'+08:00')
        else:
            update_time.append(df['time'][i])
else:
    update_time = time
df['update_time'] = update_time

for i in properties.keys():
    if i not in df.columns:
        df[i]= None

keys=list(map(lambda x: x, properties.keys()))
df =df[keys]

df.to_csv('ptt_data.csv', index =False,encoding="utf8")

def CSVimportES(indexName,typeName,fileName):
    if os.path.isfile(fileName) == False:
        print ("The file dose not exist.")
    if es_index.exists(indexName) == False:
        es.indices.create(
            index=indexName,
            body={'settings': {
                    'number_of_shards': 5,'number_of_replicas': 1,
                    'analysis': {"analyzer":{"default":{"type": "cjk"}}}},
                  'mappings': {
                    typeName: {
                        "date_detection": False,
                        "properties":properties
                    }

                }
                  #'mappings':{"_all":{"ignore_malformed": true}}
            },
            ignore=400)
    datas=[]
    with open(fileName,'r+') as p_file:
        raw_data=csv.DictReader(p_file)
        for item in raw_data:
            datas.append({"_index":indexName,"_type":typeName,"_source":item})
            #print (item)
    ttest=helpers.bulk(es,datas,chunk_size=100)
    # print (es_index.get_mapping(index=indexName,doc_type=typeName))
    print ("The situation of importing data (the first site is count number): "+str(ttest))
CSVimportES("platform","ptt","ptt_data.csv")
elapsed_time = process_time() - t
print ("The time you spend:"+ str(elapsed_time) + " seconds.")