# coding: utf-8
__author__ = 'jwkuang'
import pymongo
from bson.objectid import ObjectId
TYPE_TEACHER = 1
TYPE_HOMEWORK = 2

REQUEST_STUDENT = 101
REQUEST_TEACHER = 102

mongoClient = pymongo.MongoClient('localhost', 27017)
db = mongoClient.jwkuang
collection = db.contentCollection


def insertContent(student, teacher, title, contenttype, description, contenturl, grade, homeworktype, homeworkurl):
    post = {"student": student,
            "teacher": teacher,
            "title": title,
            "type": contenttype,
            "description": description,
            "url": contenturl,
            "grade": grade,
            "homeworktype": homeworktype,
            "homeworkurl": homeworkurl}
    contentid = collection.insert_one(post).inserted_id
    return str(contentid)


def getContentList(requesttype, student, teacher):
    queryresult = []
    if requesttype == REQUEST_STUDENT:
        queryresult = collection.find({"$or": [{"student": student, "type": TYPE_HOMEWORK}, {"type": TYPE_TEACHER, "teacher": teacher}]})
    elif requesttype == REQUEST_TEACHER:
        queryresult = collection.find({"teacher": teacher})
    return queryresult


def updateContent(objectId, updateList):
    collection.update_one({"_id": ObjectId(objectId)},
                          {"$set": updateList})
    return


if __name__ == '__main__':
    contentid = insertContent("", "甜甜", "测试测试2", TYPE_TEACHER, "测试测试2", "www.baidu.com", 0, 0, "")
    print collection.find_one({"_id": ObjectId(contentid)})
    # result = getContentList(TYPE_HOMEWORK, "jwkuang", "甜甜")
    # for content in result:
    #     print content['description']
    updateList = {"student": "jwkuang"}
    updateContent(contentid, updateList)
    print collection.find_one({"_id": ObjectId(contentid)})
