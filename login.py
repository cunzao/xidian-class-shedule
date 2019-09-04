import requests
from bs4 import BeautifulSoup
import json
from myParser import myKcb

def loginAndGetLessons(name, stuNum, passWord):
    loginActionURL = "http://ids.xidian.edu.cn/authserver/login"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362",
    "Host": "ids.xidian.edu.cn",
    "Accept": "text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8",    
    "Accept-Language": "zh-Hans-CN, zh-Hans; q=0.5"
    }

    reqS = requests.session()
    req = reqS.get(loginActionURL, headers=headers)

    loginSoup = BeautifulSoup(req.content,"html.parser")

    tickets = loginSoup.find('input', attrs={'name': 'lt'}).get('value')
    execution = loginSoup.find('input', attrs={'name': 'execution'}).get('value')

    cookies = req.cookies
    cookies.set("org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE","zh_CN")

    contents = {
        "username":  stuNum,
        "password":  passWord,
        "submit": '',
        "lt": tickets,# LT-330234-kJqWCnrzjjbvZWCVTCde***************
        "execution": execution,
        "_eventId": "submit",
        "rmShown": 1
    }
    postLoginHeaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '154',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ids.xidian.edu.cn',
        'Origin': 'http://ids.xidian.edu.cn',
        'Referer': 'http://ids.xidian.edu.cn/authserver/login',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    }
    postLoginReq = reqS.post(loginActionURL, data=contents, headers = postLoginHeaders, cookies=cookies)


    kcbAPI = "http://ehall.xidian.edu.cn/gsapp/sys/wdkbapp/*default/index.do"
    kcbContents = {
        'XNXQDM': '20191',
        'XH': ''
    }
    kcbHeaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'http://ids.xidian.edu.cn',
        'Host': 'ehall.xidian.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }

    kcbReq = reqS.post(kcbAPI, headers=kcbHeaders, allow_redirects=False, cookies=cookies,data = kcbContents)
    for i in kcbReq.cookies:
        cookies.set(i.name,i.value)
    newURL = kcbReq.headers['Location']
    kcbReq = reqS.get(newURL, headers=headers, allow_redirects=False, cookies=cookies)

    lashLoginHeaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'ehall.xidian.edu.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    }
    for i in kcbReq.cookies:
        cookies.set(i.name,i.value)
    newURL = kcbReq.headers['Location']
    kcbReq = reqS.get(newURL, headers=lashLoginHeaders, allow_redirects=False, cookies=cookies)

# 每次跳转都会增加新的Cookies内容
    for i in kcbReq.cookies:
        cookies.set(i.name,i.value)
    newURL = kcbReq.headers['Location']
    kcbReq = reqS.get(newURL, headers=lashLoginHeaders, allow_redirects=False, cookies=cookies)

    initURL = "http://ehall.xidian.edu.cn/gsapp/sys/wdkbapp/modules/xskcb/cspzcx.do"
    APIURL = "http://ehall.xidian.edu.cn/gsapp/sys/wdkbapp/modules/xskcb/xspkjgcx.do"
    APIHeaders = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://ehall.xidian.edu.cn',
        'Referer': 'http://ehall.xidian.edu.cn/gsapp/sys/wdkbapp/*default/index.do',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    initContnets = {
        'CSDM': 'pkgl_xqdyt'
    }
    APIContents = {
        'XNXQDM': '20191',
        'XH': ''
    }
    initReq = reqS.post(initURL, data=initContnets, headers = APIHeaders, cookies=cookies, allow_redirects=False)
    lastKcbReq = reqS.post(APIURL, data=APIContents, headers = APIHeaders, cookies=cookies, allow_redirects=False)
    BeautifulSoup(lastKcbReq.content)
    kcbJson = lastKcbReq.json()
    jsonFile = open("{}.json".format(name),'w',encoding="utf-8")
    json.dump(kcbJson, jsonFile, ensure_ascii=False)
    jsonFile.close()

if __name__ == "__main__":
    name = "test" # 给生成的文件起名
    stuNum = "123456789" # 学号
    passWord = "12345678" # 密码
    configFile = open("config.json", 'r', encoding="utf-8")
    config = json.load(configFile)
    stuNum = config["stuNum"]
    passWord = config["passWord"]
    loginAndGetLessons(name, stuNum, passWord)
    kcb = myKcb(name)
    kcb.produceKcbICS()
