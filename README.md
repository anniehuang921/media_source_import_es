# media_source_import_es


There are different forlder for import data in elasticsearch.
And also give the empty field null vale.

Such schema (in elasticsearch, called mapping) as following kind: 
[fielde design gdoc](https://docs.google.com/spreadsheets/d/1z7PAA2OEveqExxWWTuY6G_mA_gR8x0xpj0HbopZK1tU/edit#gid=589125606)
```python
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
'image':{'type':'string'}
                }
```
---
# imageuri.py

The function **imageuri( )**, which input string(content) and output array(image uri).
And detect containg "http://o.ooooo/xxxx.jpg" or "http://imgur.com/xxxxx"

You can run `python imageuri.py` and remove the hash marks (#) from the last line "# test()",
it'll run some tests.

The imageuri.py has been added in each folder (ptt, twitter, news), and cause can't import such file outside the folder. 
If you have solution for it, please go to the issue #2 to solve it. Thanks!
