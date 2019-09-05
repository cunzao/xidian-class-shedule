import requests
import traceback
import json
from bs4 import BeautifulSoup

from ics import Calendar, Event
from myOneLesson import oneLesson

class xidianClassShedule(object):
    '''
    暂时只做课表相关的应用
    因为有了这个ehall的cookies，大部分功能都能实现。
    到时候需要什么就再加吧
    API访问功能是通过session进行识别的
    保持session才行。
    '''
#     __czUser = czUser()
#     __headers = czHeaders()
    __czUser = None
    __headers = None
    __classSheduleJson = None
    __getClassSheduleJsonURL = "http://ehall.xidian.edu.cn/gsapp/sys/wdkbapp/modules/xskcb/xspkjgcx.do"
    __lessons = None
    
    
    def __init__(self, user, header):
        self.__czUser = user
        self.__headers = header
        
    def getClassSheduleJson(self):
        '''
        发送请求获取课程表的Json
        '''
        getClassSheduleJsonContents = {
            'XNXQDM': '20191',
            'XH': ''
        }
        getClassSheduleJsonHeaders = self.__headers.ehallWdkbappBehindHeaders
        reqS = self.__czUser.getReqS() # 我原以为是通过辨认cookies进行权限控制，实验才发现是session
        getClassSheduleJsonRequest = reqS.post(self.__getClassSheduleJsonURL, data=getClassSheduleJsonContents, headers = getClassSheduleJsonHeaders, allow_redirects=False,cookies=self.__czUser.czCookies)
        self.__classSheduleJson = getClassSheduleJsonRequest.json()
        print(self.__classSheduleJson)
        
    def saveClassSheduleJson(self):
        '''
        保存课程表Json到本地文件
        '''
        jsonFile = open("{}.json".format(self.__czUser.czUserClassName),'w',encoding="utf-8")
        json.dump(self.__classSheduleJson, jsonFile, ensure_ascii=False)
        jsonFile.close()
        print("{}.json文件保存成功！".format(self.__czUser.czUserClassName))
        
    def classSheduleJsonToIcs(self):
        '''
        将课程表输出成ics文件
        '''
        if(self.__lessons == None and self.__classSheduleJson):
            self.__lessons = self.__classSheduleJson["datas"]["xspkjgcx"]["rows"]
        elif(self.__classSheduleJson == None):
            print("你都没读取本地json，调用readLeasonsInFile()函数读取吧！")
            return
        c = Calendar()
        for week in range(1,18):
            for aLesson in self.__lessons:
                if(self.__canBeAdd(week, aLesson["ZCMC"])):
                    aClass = oneLesson(weeks=week, oneClassSheduleJson=aLesson)
                    c.events.add(aClass.oneLessonToIcsEvent())
        with open('{}.ics'.format(self.__czUser.czUserClassName), 'w', encoding='utf-8') as my_file:
            my_file.writelines(c)
        print("导出完成！")
        
    def readLeasonsInFile(self):
        '''
        读取保存在本地的json文件
        '''
        ClassSheduleJsonFile = open("{}.json".format(self.__czUser.czUserClassName), 'r', encoding='utf-8')
        self.__classSheduleJson = json.load(ClassSheduleJsonFile)
        ClassSheduleJsonFile.close()
        # kcbSize = fullKcbJson["datas"]["xspkjgcx"]["totalSize"]
        self.__lessons = self.__classSheduleJson["datas"]["xspkjgcx"]["rows"]
        print("本地课表读取完成！")
    
    def __produceWeekArray(self, aaa):
        '''
        解析aaa中说明的有效周，返回列表
        '''
        i = aaa
        weeksArray = []
        if("周" in i):
            if("双周" in i):
                print(i,'双周')
                ccc = i[:-2].split("-")
                startWeek = ccc[0]
                endWeek = ccc[1]
                for j in range(int(startWeek), int(endWeek)+1):
                    if(j%2 == 0):
                        weeksArray.append(j)
            elif("单周" in i):
                print(i,'单周')
                ccc = i[:-2].split("-")
                startWeek = ccc[0]
                endWeek = ccc[1]
                for j in range(int(startWeek), int(endWeek)+1):
                    if(j%2 == 1):
                        weeksArray.append(j)
            else:
                if("-" in i):
                    print(i,'    1')
                    ccc = i[:-1].split("-")
                    startWeek = ccc[0]
                    endWeek = ccc[1]
                    for j in range(int(startWeek), int(endWeek)+1):
                        weeksArray.append(j)
                else:
                    print(i,'   2')
                    weeksArray.append(int(i[:-1]))
        else:
            if("-" in i):
                ccc = i.split("-")
                startWeek = ccc[0]
                endWeek = ccc[1]
                for j in range(int(startWeek), int(endWeek)+1):
                    weeksArray.append(j)
            else:
                weeksArray.append(int(i))
        return weeksArray
    
    def __canBeAdd(self, week, aLesson:str):
        '''
        计算这周这门课需不需要加入
        变量名乱起了。。。
        '''
        aaa = aLesson
        weeksArray = []
        if("," in aaa):
            bbb = aaa.split(",")
            for i in bbb:
                weeksArray.extend(self.__produceWeekArray(i))
        else:
            weeksArray.extend(self.__produceWeekArray(aaa))
        if(week in weeksArray):
            return True
        else:
            return False
