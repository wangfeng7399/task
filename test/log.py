#!/bin/env python3
#coding:utf-8

import  os
import time
import re
import MySQLdb
def mysqlinsert(sql):
    conn=MySQLdb.Connect(host="127.0.0.1",user="root",passwd="task",db="task",charset="utf8")
    cur = conn.cursor()
    Recoue=cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
t=time.strftime("%Y-%m-%d",time.localtime())
insettime=time.strftime("%Y-%m-%d",time.localtime(time.time()-86400))
for i in os.listdir(t):
    l=i.split("_")[1:3]
    print(l)
    database=("-".join(l))
    try:
        with open("{0}/{1}".format(t,i),"r+")as f:
            lines=f.read()
            linelist=re.split("# Query \\d+",lines)
            for line in linelist:
                times=re.findall("# Count(.*?)# Lock time",line,re.S)
                if times:
                    times=times[0].split()
                    sqlall=re.findall("((select|insert|SELECT).*?\\\\G)",line,re.S)
                    if sqlall:
                        sql=list(set(sqlall))[0][0].strip()
                    insertsql='insert into web_slow(date,datab,maxtime,avgtime,mintime,insql,count) VALUES("{0}","{1}",{2},{3},{4},"{5}",{6})'.\
                                format(insettime,database,times[8][0],times[9][0],times[7][0],sql,times[0])
                    print(insertsql)
                    #mysqlinsert(insertsql)

    except Exception:
        with open("{0}/{1}".format(t,i),"r+",encoding="gbk")as f:
            lines=f.read()
            linelist=re.split("# Query \\d+",lines)
            for line in linelist:
                times=re.findall("# Count(.*?)# Lock time",line,re.S)
                if times:
                    times=times[0].split()
                    sqlall=re.findall("((select|insert|SELECT).*?\\\\G)",line,re.S)
                    if sqlall:
                        sql=list(set(sqlall))[0][0].strip()
                    insertsql='insert into web_slow(date,datab,maxtime,avgtime,mintime,insql,count) VALUES("{0}","{1}",{2},{3},{4},"{5}",{6})'.\
                                format(insettime,database,times[8][0],times[9][0],times[7][0],sql,times[0])
                    print(insertsql)
                    #mysqlinsert(insertsql)
