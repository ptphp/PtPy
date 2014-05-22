import qiniu.rs
import qiniu.io
import qiniu.conf

qiniu.conf.ACCESS_KEY = ""
qiniu.conf.SECRET_KEY = ""


class PtQn(object):
    uptoken = None
    buk = ''
    def __init__(self,buk):
        self.buk = buk
    def remove(self,key):
        ret, err = qiniu.rs.Client().delete(self.buk, key)
        print ret
        if err is not None:
            print err
            return False
        if ret is None:
            return False
        else:
            return ret 
    def checkExist(self,key):
        ret, err = qiniu.rs.Client().stat(self.buk, key)
        if err is not None:
            #print err
            return False
        if ret is None:
            return False
        else:
            return ret        
    def upload(self,key,localfile):
        if self.uptoken is None:            
            policy = qiniu.rs.PutPolicy(self.buk)
            self.uptoken = policy.token()
        ret, err = qiniu.io.put_file(self.uptoken, key, localfile)
        if err is not None:
            print err
            return False
        if ret is None:
            return False
        else:
            return ret    