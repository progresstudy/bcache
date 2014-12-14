#!/usr/bin/python

import web
import bencode
from hashlib import sha1
import StringIO
import gzip

import util

urls = ("/", 'Upload')
render = web.template.render('templates/')
oss = util.get_oss_api()

# 15M
MAX_UPLOAD_SIZE = 15 * 1024 * 1024

class Upload:

    def GET(self):
        return render.index()

    def POST(self):
        global oss, MAX_UPLOAD_SIZE
        print web.ctx.env.get('CONTENT_TYPE')
        if web.ctx.env.get('CONTENT_LENGTH') > MAX_UPLOAD_SIZE :
            return {"errno": 102,
                    "errmsg": "File size cannot more than 15M." }
        x = web.input(myfile={})
        if not x.has_key('myfile') or x['myfile'] == '':
            return {"errno": 100,
                    "errmsg": "Invalid upload !"}
        try:
            web.debug(x['myfile'].filename) # This is the filename
            content = x['myfile'].value
            dc = bencode.bdecode(content)
            binfo = bencode.bencode(dc['info'])
            infohash = sha1(binfo).hexdigest()
            sio = StringIO.StringIO()
            gz = gzip.GzipFile(fileobj=sio, mode="wb")
            gz.write(content)
            gz.close()
            gzcontent = sio.getvalue()
            if oss:
                res = oss.put_object_from_string(bucket = "test2312", 
                        object = "%s.torrent" % infohash.upper(),
                        input_content = gzcontent,
                        headers = {"Content-Encoding": "gzip"})
            return {"gzcontent" : res.status,
                    "infohash": infohash}
        except:
            return {"errno": 101,
                    "errmsg": "Unknow error, sorry :("}

if __name__ == "__main__":
   app = web.application(urls, globals())
   app.run()
