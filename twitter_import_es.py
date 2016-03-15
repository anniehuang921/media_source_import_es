# coding: utf-8
#!/usr/bin/env python3
#encoding=utf-8
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

df = pd.read_excel(filename)
df=df.rename(columns = {'from_user_lang':'from_user_language'})
df=df.rename(columns = {'location':'from_user_location'})
df=df.rename(columns = {'created_at':'time'})
df=df.rename(columns = {'text':'content'})
df=df.rename(columns = {'to_user_id':'tags_id'})
df=df.rename(columns = {'to_user_name':'tags_name'})
df['platform'] ='twitter'

time=[]
from datetime import datetime
for i in df['time']:
    date = datetime.strptime(str(i),"%Y-%m-%d %H:%M:%S")
    time.append(datetime.isoformat(date)+'+08:00')
df['time']= time
geo=[]
for i in range(len(df)):
    if np.isnan(df['geo_lat'][i]):
        geo.append(None)
    else:
        geo.append(str(df['geo_lat'][i])+","+str(df['geo_lng'][i]))
df['geo']=geo
df =df[['platform','id','time','from_user_name','from_user_id','from_user_language','from_user_realname'
    ,'from_user_location','geo','content','favorite_count','tags_name','tags_id']]
df.to_csv('twitter_data.csv', index =False,encoding="utf8")

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
               'format': 'strict_date_optional_time||epoch_millis'  }
                }

def CSVimportES(indexName,typeName,fileName):
    if os.path.isfile(fileName) == False:
        print ("The file dose not exist.")
    if es_index.exists(indexName) == False:
        es.indices.create(
            index=indexName,
            body={'settings': {
                    'number_of_shards': 5,'number_of_replicas': 1,
                    'analysis': {"analyzer":{"default":{"type": "smartcn"}}}},
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
    ttest=helpers.bulk(es,datas,chunk_size=100)
    print ("The situation of importing data (the first site is count number): "+str(ttest))
CSVimportES("platform","twitter","twitter_data.csv")
