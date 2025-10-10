# coding=utf-8
import sqlite3
import sys
import re
from ai import Ai
from model import Model
class User(Model):
    def __init__(self):
        self.con=sqlite3.connect(self.mydb)
        self.con.row_factory = sqlite3.Row
        self.cur=self.con.cursor()
        self.cur.execute("""create table if not exists user(
        id integer primary key autoincrement,
        email text,
        mypic text,
        country_id text,
        phone text,
        gender text,
            password text,
            nomcomplet text
                    );""")
        self.con.commit()
        #self.con.close()
    def getall(self):
        self.cur.execute("select * from user")

        row=self.cur.fetchall()
        return row
    def deletebyid(self,myid):

        self.cur.execute("delete from user where id = ?",(myid,))
        job=self.cur.fetchall()
        self.con.commit()
        return None
    def getbyemailpwsecurity(self,email,pw):

        try:
          self.cur.execute("select * from user where email = ? and password = ? ",(email,pw,))
          myrow=dict(self.cur.fetchone())
          print(myrow["id"], "row id")
          row={}
          ai=Ai().findbyuserid(myrow["id"])
          row["notice"]="vous êtes connecté"
          row["name"]=myrow["nomcomplet"]
          row["user_id"]=myrow["id"]
          row["ai_id"]=ai["id"]
          row["email"]=myrow["email"]
        except Exception as e:
          row={"notice":str(e)+"votre connexion n'a pas fonctionné","name":"","email":""}
        return row
    def getbyid(self,myid):
        self.cur.execute("select * from user where id = ?",(myid,))
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
        ai=None
        aiid=None
        msg=""
        try:
          self.cur.execute("insert into user (email,country_id,phone,password,mypic,gender,nomcomplet) values (:email,:country_id,:phone,:password,:mypic,:gender,:nomcomplet)",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
          ai=Ai().create({"username":myhash["nomcomplet"],"name":myhash["nomcomplet"],"description":"","gender":myhash["gender"],"mypic":myhash["mypic"],"user_id":myid})
        except Exception as e:
          print("my error"+str(e))
          msg+=str(e)
        azerty={}
        try:
          if myid and myid is not None:
            azerty["user_id"]=myid
            azerty["ai_id"]=ai["ai_id"]
            azerty["name"]=myhash["nomcomplet"]
            azerty["email"]=myhash["email"]
            azerty["notice"]="votre user a été ajouté"
          else:
            azerty["user_id"]=""
            azerty["ai_id"]=""
            azerty["name"]=""
            azerty["email"]=""
            azerty["notice"]="votre inscription n'a pas fonctionné"+msg
        except Exception as ee:
          azerty["user_id"]=""
          azerty["name"]=""
          azerty["ai_id"]=""
          azerty["email"]=""
          azerty["notice"]="votre inscription n'a pas fonctionné"+msg+str(ee)
        self.con.close()
        return azerty




