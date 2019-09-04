from myOneLesson import oneLesson
from ics import Calendar, Event
import json

class myKcb(object):
    kcbName = ""
    lessons = None
    
    def __init__(self, name):
        self.kcbName = name
        self.readLeasons()
    
    def readLeasons(self):
        fullKcbJsonFile = open("{}.json".format(self.kcbName), 'r', encoding='utf-8')
        fullKcbJson = json.load(fullKcbJsonFile)
        fullKcbJsonFile.close()
        # kcbSize = fullKcbJson["datas"]["xspkjgcx"]["totalSize"]
        self.lessons = fullKcbJson["datas"]["xspkjgcx"]["rows"]
        print("课表读取完成！")
    
    def produceWeekArray(self, aaa):
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
    
    def canBeAdd(self, week, aLesson:str):
        '''
        计算这周这门课需不需要加入
        变量名乱起了。。。
        '''
        aaa = aLesson
        weeksArray = []
        if("," in aaa):
            bbb = aaa.split(",")
            for i in bbb:
                weeksArray.extend(self.produceWeekArray(i))
        else:
            weeksArray.extend(self.produceWeekArray(aaa))
        if(week in weeksArray):
            return True
        else:
            return False

    def produceKcbICS(self):
        c = Calendar()
        for week in range(1,18):
            for aLesson in self.lessons:
                if(self.canBeAdd(week, aLesson["ZCMC"])):
                    aClass = oneLesson(weeks=week, oneClassSheduleJson=aLesson)
                    c.events.add(aClass.oneLessonToIcsEvent())
        with open('{}.ics'.format(self.kcbName), 'w', encoding='utf-8') as my_file:
            my_file.writelines(c)