#!/usr/bin/python

from oss.oss_api import OssAPI

def get_oss_api():
    try:
        oss = OssAPI(host='oss-cn-qingdao-a.aliyuncs.com', 
          access_id="uiUaNNz4uHKKX34j", 
          secret_access_key='2w2d34QAvtnYaodyO3gOkIOZ1T0Hsg')
    except:
        return None
    return oss
