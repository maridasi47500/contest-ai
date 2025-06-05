# coding=utf-8
import sqlite3
import sys
import re
from model import Model
from stuff import Stuff
from aistuff import Aistuff
from chercherimage import Chercherimage
from post import Post
import requests
from bs4 import BeautifulSoup
import urllib.request
from chaine import Chaine
import random
class Ai(Model):
    def __init__(self):
        self.con=sqlite3.connect(self.mydb)
        self.con.row_factory = sqlite3.Row
        self.dbPost=Post()
        self.cur=self.con.cursor()
        self.cur.execute("""create table if not exists ai(
        id integer primary key autoincrement,
        username text,
            user_id text,
            mypic text,
            name text,
            description text,
            gender text
    ,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP                );""")
        self.con.commit()
        self.Aistuff=Aistuff()
        self.Stuff=Stuff()
        #self.con.close()
    def getall(self):
        self.cur.execute("select * from ai")

        row=self.cur.fetchall()
        return row
    def deletebyid(self,myid):

        self.cur.execute("delete from ai where id = ?",(myid,))
        job=self.cur.fetchall()
        self.con.commit()
        return None
    def findbyuserid(self,myid):
        self.cur.execute("select * from ai where user_id = ?",(myid,))
        azer=self.cur.fetchone()
        row ={"name":"","mypic":"","gender":"","username":""}
        if azer is not None:
          row=dict(azer)
          print(row["id"], "row id")
        return row
    def getbyid(self,myid):
        self.cur.execute("select * from ai where id = ?",(myid,))
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
          self.cur.execute("insert into ai (username,user_id,mypic,name,description,gender) values (:username,:user_id,:mypic,:name,:description,:gender)",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["ai_id"]=myid
        azerty["notice"]="votre ai a été ajouté"
        return azerty
    def update(self,params):
        print("ok")
        myhash={}
        self.cur.execute("select * from ai where user_id = :user_id",(params["user_id"],))
        myai=self.cur.fetchone()
        aiid=myai["id"]
        myid=myai["id"]
        mystuff_ids=params["description"].split(",")
        random.shuffle(mystuff_ids)
        user_id=params["user_id"]
        allstuffs=self.Stuff.getall()
        allmystuffs=self.Aistuff.getbyuserid(aiid)
        allmystuffsarray=self.Aistuff.getidbyuserid(aiid)
        random.shuffle(allstuffs)
        hey=None
        self.cur.execute("select user.id as userid,country.* from user left join country on country.id = user.country_id where user.id = :user_id",(params["user_id"],))
        mycountry=self.cur.fetchone()["name"]
        post=None
        mypic=None
        hey=None
        mstring=None
        opener=None
        post=None
        z=None
        y=None
        for z in allstuffs:
            print("STUUUFFFFFFFF",z,z["id"],mystuff_ids)
            someid=str(z["id"])

            if someid not in mystuff_ids and someid in allmystuffsarray:
                try:
                    self.Aistuff.deletebyuserid(someid,aiid)
                    allmystuffs=self.Aistuff.getbyuserid(user_id)
                except:
                    print("hey")
            elif someid in mystuff_ids:
                self.Aistuff.create({"ai_id":aiid,"stuff_id":someid})
                mypic=("woman" if myai["gender"] == "f" else "man")+" "+mycountry+" "+z["name"]
                hey=Chercherimage(mypic).search()

                opener=urllib.request.build_opener()
                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582')]
                urllib.request.install_opener(opener)
                somename= f'./uploads/'+str(myai["gender"])+'_'+z["name"].replace(".","").replace(" ","_")+'_pic.jpg'
                mstring=Chaine().fichier(somename)
                urllib.request.urlretrieve(hey[0]["src"], './uploads/'+mstring)
                post=self.dbPost.create({"pic":mstring,"description":mypic,"ai_id":aiid})
        #for mystuff_id in mystuff_ids:
        #    print("STUUUFFFFFFFF => ",mystuff_id)
        #    if mystuff_id not in allstuffs:

        #        self.cur.execute("select * from stuff where id = ?",(mystuff_id,))
        #        y=self.cur.fetchone()
        #        mypic=("woman" if myai["gender"] == "f" else "man")+" "+mycountry+" "+y["name"]
        #        hey=Chercherimage(mypic).search()

        #        opener=urllib.request.build_opener()
        #        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582')]
        #        urllib.request.install_opener(opener)
        #        somename= f'./uploads/'+str(myai["gender"])+'_'+y["name"].replace(".","").replace(" ","_")+'_pic.jpg'
        #        mstring=Chaine().fichier(somename)
        #        urllib.request.urlretrieve(hey[0]["src"], './uploads/'+mstring)
        #        post=self.dbPost.create({"pic":mstring,"description":mypic,"ai_id":aiid})
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
        myai=None
        userid=None
        myname=None
        try:
          self.cur.execute("update ai set username = :username,mypic = :mypic,name = :name,description = :description,gender = :gender where user_id = :user_id",myhash)
          self.con.commit()
          self.cur.execute("select * from ai where user_id = :user_id",(params["user_id"],))
          myai=self.cur.fetchone()

          myid=myai["id"]
          userid=myai["user_id"]
          myname=myai["name"]
        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["ai_id"]=myid
        azerty["user_id"]=userid
        azerty["name"]=myname
        azerty["notice"]="votre ai a été modifié(e)"
        return azerty




