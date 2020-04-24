class czSettings(object):
    '''
    将课程表设置相关的参数集中到这个文件中，方便设置。
    '''
    _instance = None
    __configPath = 'config.json'
    __startTimeOfThisTerm = '2020/02/24 00:00' # 本学期正式开始第一节课的时间，时间戳的格式
    __totalWeeks = 20 # 这学期最长多少周
    __XNXQDM = '20192' # 'XNXQDM': '20192', # 学期代码
    __needDST = False # 是否需要夏令时

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        pass

    def getConfigPath(self):
        return self.__configPath

    def getStartTimeOfThisTerm(self):
        return self.__startTimeOfThisTerm

    def getTotalWeeks(self):
        return self.__totalWeeks

    def getXNXQDM(self):
        return self.__XNXQDM

    def getNeedDST(self):
        return self.__needDST