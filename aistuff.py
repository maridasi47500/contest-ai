# coding=utf-8
import sqlite3
import sys
import re
from model import Model

class Aistuff(Model):
    def __init__(self):
        self.con=sqlite3.connect(self.mydb)
        self.con.row_factory = sqlite3.Row
        self.cur=self.con.cursor()
        self.cur.execute("""create table if not exists aistuff(
        id integer primary key autoincrement,
        stuff_id text,
            ai_id text
    ,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP                );""")
        self.con.commit()
        #self.con.close()
    def getall(self):
        self.cur.execute("select * from aistuff")

        row=self.cur.fetchall()
        return row
    def deletebyuserid(self,myid,userid):

        self.cur.execute("delete from aistuff where stuff_id = ? and ai_id = ?",(myid,userid))
        job=self.cur.fetchall()
        self.con.commit()
        return None
    def deletebyid(self,myid):

        self.cur.execute("delete from aistuff where id = ?",(myid,))
        job=self.cur.fetchall()
        self.con.commit()
        return None
    def getbyuserid(self,myid):
        self.cur.execute("select id from aistuff where ai_id = ?",(myid,))
        job=self.cur.fetchall()
        hey=[]

        for k in job:
            hey.append(str(k["id"]))
        return hey
    def getidbyuserid(self,myid):
        self.cur.execute("select * from aistuff where ai_id = ?",(myid,))
        job=self.cur.fetchall()
        hey=[]

        for k in job:
            hey.append(str(k["id"]))
        return hey
    def getnamebyuserid(self,myid):
        self.cur.execute("select stuff.name from aistuff left join stuff on stuff.id = aistuff.stuff_id where aistuff.ai_id = ?",(myid,))
        job=self.cur.fetchall()
        hey=[]

        for k in job:
            hey.append(k["name"])
        return hey
    def getbyid(self,myid):
        self.cur.execute("select * from aistuff where id = ?",(myid,))
        row=dict(self.cur.fetchone())
        print(row["id"], "row id")
        job=self.cur.fetchall()
        return row
    def create(self,params):
        print("ok")
        myhash={}
        for x in params:
            if 'confirmation' in x:
                continue
            if 'envoyer' in x:
                continue
            if '[' not in x and x not in ['routeparams']:
                #print("my params",x,params[x])
                try:
                  myhash[x]=str(params[x].decode())
                except:
                  myhash[x]=str(params[x])
        print("M Y H A S H")
        print(myhash,myhash.keys())
        myid=None
        try:
          self.cur.execute("insert into aistuff (stuff_id,ai_id) values (:stuff_id,:ai_id)",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["aistuff_id"]=myid
        azerty["notice"]="votre aistuff a été ajouté"
        return azerty




