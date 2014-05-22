#coding:utf-8
import memcache

"""
sudo apt-get install python-memcache

pip install python-memcached

wget ftp://ftp.tummy.com/pub/python-memcached/python-memcached-latest.tar.gz

memcached -d -m 64 -p 11211 -u memcache -l 127.0.0.1 

启动参数说明：
 
-d 选项是启动一个守护进程
-m 是分配给Memcache使用的内存数量，单位是MB，默认64MB
-M return error on memory exhausted (rather than removing items)
-u 是运行Memcache的用户，如果当前为root 的话，需要使用此参数指定用户
-l 是监听的服务器IP地址，默认为所有网卡
-p 是设置Memcache的TCP监听的端口，最好是1024以上的端口
-c 选项是最大运行的并发连接数，默认是1024
-P 是设置保存Memcache的pid文件

保存数据
set(key,value,timeout) 把key映射到value，timeout指的是什么时候这个映射失效
add(key,value,timeout)   仅当存储空间中不存在键相同的数据时才保存
replace(key,value,timeout)   仅当存储空间中存在键相同的数据时才保存
获取数据
get(key) 返回key所指向的value
get_multi(key1,key2,key3,key4) 可以非同步地同时取得多个键值， 比循环调用get快数十倍
删除数据
delete(key, timeout) 删除键为key的数据，timeout为时间值，禁止在timeout时间内名为key的键保存新数据（set函数无效）


mc = PtMemcache()
mc.set("tset","test")
print mc.get("test")
"""

class PtMemcache(object):
    r = None
    def __init__(self,host='127.0.0.1', port=11211):        
        self.mc = memcache.Client([host+':'+str(port)])
    def get(self,key):        
        return self.mc.get(key)
    def set(self,key,value):
        self.mc.set(key, value)
        

