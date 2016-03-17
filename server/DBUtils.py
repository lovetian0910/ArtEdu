# coding: utf-8
__author__ = 'jwkuang'
import pymongo
from bson.objectid import ObjectId
TYPE_TEACHER = 1
TYPE_HOMEWORK = 2

REQUEST_STUDENT = 101           # 学生请求数据列表（包括老师分享数据和作业数据）
REQUEST_TEACHER_SHARE = 102     # 老师分享数据列表
REQUEST_TEACHER_HOMEWORK = 103  # 作业数据列表

mongoClient = pymongo.MongoClient('localhost', 27017)
db = mongoClient.jwkuang
collection = db.contentCollection
studentCollection = db.student


def insertContent(student, teacher, title, contenttype, description, contenturl, grade, homeworktype, homeworkurl):
    """InsertContent to DB.

    将一条内容写入DB
    :param student: 学生姓名
    :param teacher: 老师姓名
    :param title: 标题
    :param contenttype: 数据类型
    :param description: 描述
    :param contenturl:
    :param grade: 评分（作业类型需要）
    :param homeworktype: 作业类型，图片、视频、音频等
    :param homeworkurl: 作业URL
    :return:
    """
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
    elif requesttype == REQUEST_TEACHER_SHARE:
        queryresult = collection.find({"type": TYPE_TEACHER, "teacher": teacher})
    elif requesttype == REQUEST_TEACHER_HOMEWORK:
        queryresult = collection.find({"student": student, "type": TYPE_HOMEWORK})
    return queryresult


def updateContent(objectId, updateList):
    collection.update_one({"_id": ObjectId(objectId)},
                          {"$set": updateList})
    return


def insertStudentInfo(name, tel, password, type, teacher, registertime):
    post = {"name": name,
            "tel": tel,
            "password": password,
            "type": type,
            "teacher": teacher,
            "registertime": registertime}
    studentCollection.insert_one(post)


if __name__ == '__main__':
    contentid = insertContent("", "甜甜", "测试测试2", TYPE_TEACHER, "测试测试2", "www.baidu.com", 0, 0, "")
    print collection.find_one({"_id": ObjectId(contentid)})
    # result = getContentList(TYPE_HOMEWORK, "jwkuang", "甜甜")
    # for content in result:
    #     print content['description']
    updateList = {"student": "jwkuang"}
    updateContent(contentid, updateList)
    print collection.find_one({"_id": ObjectId(contentid)})
