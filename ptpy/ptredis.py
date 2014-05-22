import redis
"""
easy_install redis

r = PtRedis()
r.set("tset","test")
print r.get("test")
"""

class PtRedis(object):
    r = None
    def __init__(self,host='localhost', port=6379, db=0):        
        self.r = redis.StrictRedis(host=host, port=port, db=db)
        
    def get(self,key):        
        return self.r.get(key)
    
    def set(self,key,value):
        self.r.set(key, value)