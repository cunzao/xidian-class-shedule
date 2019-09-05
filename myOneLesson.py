import json
import datetime
import time
import uuid
from ics import Calendar, Event

class oneLesson(object):
    '''
    一节课类
    拥有以下属性：
    oneLessonID 这门课的ID 对应json的 KCDM
    nameOfTheLesson 这门课的名称 对应json的 KCMC
    dayOfTheWeek 星期几开课的 对应Json的 XQ
    numOfTheLesson 这天的第几门课 对应json的 KSJCDM
    addressOfTheLesson 上课的地点 对应json的 JASMC
    numOfWeeks 上课的周数 对应json的 ZCMC
    teacherNameOfTheLesson 教师姓名 对应json的 JSXM
    
    weeks # 第几周
    startTime # 课程开始的具体时间
    endTime  # 课程结束的具体时间
    '''
    __oneLessonID = "" # 这门课的ID 对应json的 KCDM
    __nameOfTheLesson = "" # 这门课的名称 对应json的 KCMC
    __dayOfTheWeek = 0 # 星期几开课的 对应Json的 XQ
    __numOfTheLesson = 0 # 这天的第几门课 对应json的 KSJCDM
    __addressOfTheLesson = "" #上课的地点 对应json的 JASMC
    __numOfWeeks = 0 # 上课的周数 对应json的 ZCMC
    __teacherNameOfTheLesson = ""# 教师姓名 对应json的 JSXM
    
    __weeks = 0 # 第几周
    __startTime = "" # 课程开始的具体时间
    __endTime = "" # 课程结束的具体时间
    
    __startTimeOfThisTerm = time.mktime(time.strptime("2019/09/02 00:00", "%Y/%m/%d %H:%M")) #学期第一节课的开始时间，时间戳的格式
    __oneLessonTime = 60*15
    __oneDayShedule = {
        "1": 30600, # 510,  "08:30",
        "2": 33600, # 560,  "09:20",
        "3": 37500, # 625,  "10:25",
        "4": 40500, # 675,  "11:15",
        "5": 52200, # 870,  "14:30",
        "6": 55200, # 920,  "15:20",
        "7": 58500, # 975,  "16:15",
        "8": 61500, # 1025,  "17:05",
        "9": 70200, # 1170,  "19:30",
        "10": 72900, # 1215,  "20:15",
        "11": 75600, # 1260,  "21:00",
    }
    __boundaryLine = 1569859200
    
    def __init__(self, weeks:int, oneClassSheduleJson):
        self.oneLessonID = oneClassSheduleJson["KCDM"]
        self.nameOfTheLesson = oneClassSheduleJson["KCMC"]
        self.dayOfTheWeek = oneClassSheduleJson["XQ"]
        self.numOfTheLesson = oneClassSheduleJson["KSJCDM"]
        self.addressOfTheLesson = oneClassSheduleJson["JASMC"]
        self.numOfWeeks = oneClassSheduleJson["ZCMC"]
        self.teacherNameOfTheLesson = oneClassSheduleJson["JSXM"]
        self.weeks = weeks
        print("初始化完成！")
    
    @property
    def oneLessonID(self):
        return self.__oneLessonID
    
    @oneLessonID.setter
    def oneLessonID(self,value:str):
        print("oneLessonID的值改变，从 {} 变到 {}".format(self.__oneLessonID,value))
        self.__oneLessonID = value
        
    @property
    def nameOfTheLesson(self):
        return self.__nameOfTheLesson
    
    @nameOfTheLesson.setter
    def nameOfTheLesson(self, value:str):
        print("nameOfTheLesson，从 {} 变到 {}".format(self.__nameOfTheLesson,value))
        self.__nameOfTheLesson = value
        
    @property
    def dayOfTheWeek(self):
        return self.__dayOfTheWeek
    
    @dayOfTheWeek.setter
    def dayOfTheWeek(self, value:int):
        print("dayOfTheWeek，从 {} 变到 {}".format(self.__dayOfTheWeek,value))
        self.__dayOfTheWeek = value
        
    @property
    def numOfTheLesson(self):
        return self.__numOfTheLesson
    
    @numOfTheLesson.setter
    def numOfTheLesson(self, value:int):
        print("numOfTheLesson，从 {} 变到 {}".format(self.__numOfTheLesson,value))
        self.__numOfTheLesson = value
        
    @property
    def addressOfTheLesson(self):
        return self.__addressOfTheLesson
    
    @addressOfTheLesson.setter
    def addressOfTheLesson(self, value:str):
        print("addressOfTheLesson，从 {} 变到 {}".format(self.__addressOfTheLesson,value))
        self.__addressOfTheLesson = value
        
    @property
    def numOfWeeks(self):
        return self.__numOfWeeks
    
    @numOfWeeks.setter
    def numOfWeeks(self, value:int):
        print("numOfWeeks，从 {} 变到 {}".format(self.__numOfWeeks,value))
        self.__numOfWeeks = value
        
    @property
    def teacherNameOfTheLesson(self):
        return self.__teacherNameOfTheLesson
    
    @teacherNameOfTheLesson.setter
    def teacherNameOfTheLesson(self, value:str):
        print("teacherNameOfTheLesson，从 {} 变到 {}".format(self.__teacherNameOfTheLesson,value))
        self.__teacherNameOfTheLesson = value
        
    @property
    def weeks(self):
        return self.__weeks
    
    @weeks.setter
    def weeks(self, value):
        print("weeks，从 {} 变到 {}".format(self.__weeks,value))
        self.__weeks = value
    
    @property
    def startTime(self):
        '''
        真实的开始时间
        1.计算这天的时间戳
        公式：学期开始时间 + （周数-2）*一周的秒数 + （礼拜几 -1 ）* 一天的时间的秒数 
        2.将时间戳转换成时间，格式 %Y-%m-%d %H:%M:%S
        3.将小时、分钟替换成 self.__oneDayShedule[self.__numOfTheLesson]
        
        冬令时的时候下午的时间会比夏令时晚30分钟
        '''  
        thisDayTimeStamp = self.__startTimeOfThisTerm + (self.weeks-2)*(7*24*3600) + (self.dayOfTheWeek - 1)*(24*3600) + self.__oneDayShedule[str(self.numOfTheLesson)] - 8*3600
        if(self.numOfTheLesson >= 5 and self.__boundaryLine <= thisDayTimeStamp):
            thisDayTimeStamp -= 30*60
        thisDayDatetime = datetime.datetime.strftime(datetime.datetime.fromtimestamp(thisDayTimeStamp), "%Y-%m-%d %H:%M:%S")
        print(thisDayDatetime)
        return thisDayDatetime
    
    @property
    def endTime(self):
        '''
        相比起开始时间，结束时间晚了45分钟
        '''
        thisDayTimeStamp = self.__startTimeOfThisTerm + (self.weeks-2)*(7*24*3600) + (self.dayOfTheWeek - 1)*(24*3600) + 45*60 + self.__oneDayShedule[str(self.numOfTheLesson)] - 8*3600
        if(self.numOfTheLesson >= 5 and self.__boundaryLine <= thisDayTimeStamp):
            thisDayTimeStamp -= 30*60
        thisDayDatetime = datetime.datetime.strftime(datetime.datetime.fromtimestamp(thisDayTimeStamp), "%Y-%m-%d %H:%M:%S")
        return thisDayDatetime
    
    def oneLessonToIcsEvent(self):
        e = Event()
        e.name = "({}){}".format(self.addressOfTheLesson, self.nameOfTheLesson)
        # e.uid = self.oneLessonID
        e.uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.__str__()))
        e.description = "任课老师：{} \n 周数：{}".format(self.teacherNameOfTheLesson, self.__weeks)
        e.location = self.addressOfTheLesson
        e.begin = self.startTime
        e.end = self.endTime
        return e
    
    def __str__(self):
        return "课程号：{}，课程名：{}，这个礼拜的第{}天上课，这是这天的第{}节课，这是第{}个礼拜的课。".format(self.oneLessonID,self.nameOfTheLesson,self.dayOfTheWeek,self.numOfTheLesson,self.weeks)