#!/bin/python3
import sqlalchemy as db
import json
import sys
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# setting the connection and the session for uploading data
engine = db.create_engine("mysql+mysqlconnector://artmaster:ArtMaster51@artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com:3306/artmaster")

Base = declarative_base()
metadata = db.MetaData()
connection = engine.connect()
session = sessionmaker()
session.configure(bind=engine)
mysession = session()


# class for the metaTag
class metaTag(Base):
    # associating the class with metaTag Table
    __tablename__ = 'metaTag'
    id = db.Column(db.BIGINT, primary_key=True)
    metaDataId = db.Column(db.Integer)
    tagName = db.Column(db.String)
    value = db.Column(db.String)
    timeStamp = db.Column(db.Date)

    def __int__(self, metaID, Tagname, val, time):
        self.metaDataId = metaID
        self.tagName = Tagname
        self.value = val
        self.timeStamp = time

    def __repr__(self):
        return " id: {0} metaDataId {1} tagName {2} value {3} timeStamp {4}" \
               "\n".format(self.id, self.metaDataId, self.tagName, self.value, self.timeStamp)


postBody = sys.stdin.read()
keys = json.loads(postBody)
metaDataId = -1
for result in keys:
    if result == 'metaDataId':
        metaDataId = result['metaDataId']
    else:
        mysession.add(metaTag(metaDataId, result, result["value"], datetime.datetime.utcnow))

mysession.commit()
