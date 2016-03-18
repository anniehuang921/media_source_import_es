#!/usr/bin/env python3
#encoding=utf-8
import sys
import json
import getopt
import ast
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.client import IndicesClient

es = Elasticsearch()
es_index=IndicesClient(es)

set_ids = set()

is_dryrun = False
action = ''

# set reactions for command 
opts, args = getopt.getopt(sys.argv[1:], '', ["action=", 'file=', 'dryrun', 'insert-diff'])
for opt in opts:
    if opt[0] == '--action':
        action = opt[1]
    elif opt[0] == '--file':
        filename = opt[1]
    elif opt[0] == '--dryrun':
        is_dryrun = True
    elif opt[0] == '--insert-diff':
        is_insert_diff = True


if len(action) == 0:
    sys.stderr.write("--action is required\n");


if action == 'import':
    f = open(filename, 'r')

    counter = 0
    total = 0
    title = ""
    content = ""
    obj = None
    datas=[]

    
    is_exists = False
    update_count = 0
    insert_count = 0
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

    for line in f:
        line = line.strip('\n')
        counter = counter+1

        if total % 1000 == 0 and counter % 3 == 0:
            print("count: %s, insert_count: %s, update_count: %s" % (total, insert_count, update_count))
        if counter == 1:
            obj = None
            obj = json.loads(line)
            id = obj['id']
            if id in set_ids:
                is_exists = True
            else:
                set_ids.add(id)
                is_exists = False

            need = ['normalized_id','url','created_at','source']#need = ['id','normalized_id','url']
            item = {key:obj[key] for key in need} 
            change = {'normalized_id':'domain','url':'uri','created_at':'time','source':'media_id'}
            for i in change.keys():
                if i == "created_at":
                    item['created_at'] = (item['created_at']+'000')
                else:
                    pass
                item[change[i]] = item.pop(i) 
            continue
            

        if counter == 2:
            line = line.strip('"').replace('\\n', '\n').replace('\\r', '\r').replace('\\/', '/')
            item['title'] = line

            continue

        if counter == 3:
            total = total + 1

            line = line.strip('"').replace('\\n', '\n').replace('\\r', '\r')
            line = line.strip('"').replace('\\n', '\n').replace('\\r', '\r').replace('\\/', '/')
            item['content'] = line
            counter = 0
        
        item['platform'] ='twitter'
        item['update_time'] = item['time']
        for i in properties.keys():
            if i not in item.keys():
                item[i]= None

        datas.append({"_index":"platform","_type":"news","_source":item})
        
ttest=helpers.bulk(es,datas,chunk_size=100)


print("Finished: " + str(ttest))
f.close()

