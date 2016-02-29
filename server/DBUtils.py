__author__ = 'jwkuang'

import pymongo

TYPE_TEACHER = 1
TYPE_STUDENT = 2


mongoClient = pymongo.MongoClient('localhost', 27017)
db = mongoClient.jwkuang
collection = db.contentCollection

def insertContent(student, teacher, title, contenttype, description, url):
    post = {"student": student,
            "teacher": teacher,
            "title": title,
            "type": contenttype,
            "description": description,
            "url": url}
    posts = collection.posts
    posts.insert_one(post)
    return

def getContentList(contenttype, student, teacher):
    
    return
