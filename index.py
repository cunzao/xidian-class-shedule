from CZHeaders import czHeaders
from CZUser import czUser
from XIDIANClassShedule import xidianClassShedule

if __name__ == "__main__":
    user = czUser()
    user.login()
    header = czHeaders()
    aaa = xidianClassShedule(user, header)
    aaa.getClassSheduleJson()
    aaa.saveClassSheduleJson()
    aaa.classSheduleJsonToIcs()