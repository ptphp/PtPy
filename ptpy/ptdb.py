#coding:utf-8

#from ptcore import trace_back
import datetime
import MySQLdb
import os
import sqlite3

from ptcore import makeDir,ptston
"""
linux下mysql的root密码忘记解决方
1．首先确认服务器出于安全的状态，也就是没有人能够任意地连接MySQL数据库。 
因为在重新设置MySQL的root密码的期间，MySQL数据库完全出于没有密码保护的 
状态下，其他的用户也可以任意地登录和修改MySQL的信息。可以采用将MySQL对 
外的端口封闭，并且停止Apache以及所有的用户进程的方法实现服务器的准安全 
状态。最安全的状态是到服务器的Console上面操作，并且拔掉网线。 
2．修改MySQL的登录设置： 
# vi /etc/my.cnf 
在[mysqld]的段中加上一句：skip-grant-tables 
例如： 
[mysqld] 
datadir=/var/lib/mysql 
socket=/var/lib/mysql/mysql.sock 
skip-grant-tables 
保存并且退出vi。 
3．重新启动mysqld 
# /etc/init.d/mysqld restart 
Stopping MySQL: [ OK ] 
Starting MySQL: [ OK ] 
4．登录并修改MySQL的root密码 
# /usr/bin/mysql 
Welcome to the MySQL monitor. Commands end with ; or \g. 
Your MySQL connection id is 3 to server version: 3.23.56 
Type 'help;' or '\h' for help. Type '\c' to clear the buffer. 
mysql> USE mysql ; 
Reading table information for completion of table and column names 
You can turn off this feature to get a quicker startup with -A 
Database changed 
mysql> UPDATE user SET Password = password ( 'new-password' ) WHERE User = 'root' ; 
Query OK, 0 rows affected (0.00 sec) 
Rows matched: 2 Changed: 0 Warnings: 0 
mysql> flush privileges ; 
Query OK, 0 rows affected (0.01 sec) 
mysql> quit 
Bye 
5．将MySQL的登录设置修改回来 
# vi /etc/my.cnf 
将刚才在[mysqld]的段中加上的skip-grant-tables删除 
保存并且退出vi。 
6．重新启动mysqld 
# /etc/init.d/mysqld restart 
Stopping MySQL: [ OK ] 
Starting MySQL: [ OK ]

Work for fun,Live for love!

"""
class PtDbo(object):
    conn = None
    cursor = None
    auto_commit = True
    type = ''
    def __init__(self,type = 'mysql'):
        self.type = type
    
    def commit(self):
        self.conn.commit() 
        self.auto_commit = True
        
    def rb(self):
        self.conn.rollback()    
        
    def bt(self):
        self.auto_commit = False        
        
    def where(self,condition):
        where = ""
        ww = []        
        if condition:
            for cc in condition:
                ww.append(cc+"= '"+str(condition[cc])+"'")
            where  = "where "+",".join(ww)
        return where
    
    def parseUpdate(self,table,param,condition):
        _sets = []
        for pp in param:
            if self.type == "mysql":
                _sets.append(pp+"= %s")
            else:
                _sets.append(pp+"= ?")            
            
        sets = "set "+",".join(_sets)        
        sql = "update %s %s %s" % (table,sets,self.where(condition))
        #print sql
        
        pp =  tuple(param.values())
        return sql,pp     
    
    def close(self):
        self.cursor.close()
        self.conn.close()
        
    def parseInsert(self,table,param):        
        sql = ""
        t = param.keys()
          
        if self.type == "mysql":
            _values = "%s," *len(t)
            fields = "`,`".join(t)       
            fields = "`"+fields+"`" 
        else:
            _values = "?," *len(t)
            fields = ",".join(t)      
        
        values =  _values[:-1]
        sql = "insert into %s(%s) values(%s) " % (table,fields,values)
        pp =  tuple(param.values())
        return sql,pp
    
    def insertid(self):
        return self.cursor.lastrowid     
    
    def update(self,table,param,condition):
        #print param,condition
        sql, pp = self.parseUpdate(table, param, condition)
        self.runSql(sql, pp)
        
    def insert(self,table, args):
        sql,param = self.parseInsert(table,args)
        self.runSql(sql, param)        
        return self.insertid()  
    
    def getAll(self,sql,param = None):
        self.query(sql, param)
        return self.cursor.fetchall()
    
    def getOne(self,sql,param = None):
        self.query(sql, param)
        return self.cursor.fetchone() 
    
    def query(self, sql,param = None):
        
        try:
            if param is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql,param)            
        except Exception , e:     
            print sql    
            #print trace_back()
            #error_log(e)
        else:                     
            return self      
        
    def getNow(self):    
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def runSql(self,sql,param = None):       
        try:
            if param is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql,param)            
        except Exception , e:
            if self.auto_commit != True:
                self.rb()
            #print trace_back()
            #error_log(e)
            
        else:            
            if self.auto_commit == True:
                self.commit()            
            return self.insertid() 
        
    #def __del__(self):
    #    self.cursor.close()
    #    self.conn.close()    
        
class PtMySql(PtDbo):
    def __init__(self,host, db, user=None, passwd=None,port = 3306):
        PtDbo.__init__(self) 
        self.auto_commit = False
        
        try:
            self.conn = MySQLdb.connect(host,user=user,passwd=passwd,port=int(port))
            self.conn.select_db(db)
            
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        except Exception,e:
            #print trace_back()
            print("Cannot connect to MySQL on %s", host)
        else:            
            self.conn.ping(True)
            self.cursor.execute("SET NAMES utf8")
        
        
    
class PtSqlite(PtDbo):
    def __init__(self):
        PtDbo.__init__(self,'sqlite')

    def open(self,dbname):
        dbpath =  os.path.abspath(dbname)
        makeDir(os.path.dirname(dbpath))
        try:
            self.conn = sqlite3.connect(dbpath)
        except Exception , e:
            #print trace_back()
            #error_log(trace_back())
            return False        
        self.conn.row_factory = self.dict_factory  
        self.conn.text_factory = str
        self.cursor = self.conn.cursor()        
        return self
        
    def dict_factory(self,cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
        
    def execute(self,sql):
        self.cursor.executescript(sql)  
        
    def deleteDb(self,dbname):        
        self.cursor.close()
        self.conn.close()
        os.remove(os.path.abspath(dbname))
    
@ptston
class PtSqliteS(PtSqlite):
    def __init__(self):
        pass#print "PtSqliteS init"