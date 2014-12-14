#!/usr/bin/python

from oss.oss_api import OssAPI

def get_oss_api():
    try:
        oss = OssAPI(host='host', 
          access_id="accessid", 
          secret_access_key='secret_key')
    except:
        return None
    return oss
