import requests
import traceback
import json
import re
from bs4 import BeautifulSoup
from CZHeaders import czHeaders
from settings import czSettings
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import random
import base64
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms

class czUser(object):
    '''
    将所有的登录操作封装在user类里
    主要用于登录以及获取cookies
    '''
    __czCookies = None
    __stuNum = ""
    __passWord = ""
    __pwdDefaultEncryptSalt = "iOmFc10bomgIw9ve"
    __czUserClassName = ""
    __headers = czHeaders()
    __URLs = None
    __reqS = requests.session()
    __settings = None
    __configPath = "config.json"
    
    def __init__(self):
        self.__settings = czSettings()
        self.__configPath = self.__settings.getConfigPath()
        try:
            configFile = open(self.__configPath, 'r', encoding="utf-8")
            config = json.load(configFile)
            self.__stuNum = config["stuNum"]
            self.__passWord = config["passWord"]
            self.__czUserClassName = config["name"]
            self.__URLs = {
                "idsLoginURL":"http://ids.xidian.edu.cn/authserver/login",
                "wdkbappURL":"http://ehall.xidian.edu.cn/gsapp/sys/wdkbapp/*default/index.do",
            }
            configFile.close()
            print("初始化成功！czUserClassName: {}".format(self.__czUserClassName))
        except:
            print("没有初始化成功！是不是config.json有问题？{}".format(traceback.format_exc()))
    
    @property
    def czCookies(self):
        return self.__czCookies
    
    @czCookies.setter
    def czCookies(self, cookiesJar):
        '''
        更改__czCookies 的 = 操作，将替换改为更新
        '''
        for i in cookiesJar:
            # print("czCookies增加：{}={}".format(i.name,i.value))
            self.__czCookies.set(i.name,i.value)
        print("本次更新后的cookies：{}".format(self.czCookies))
        
    @property
    def czUserClassName(self):
        return self.__czUserClassName
    
    def __idsLoginGet(self):
        '''
        访问ids页面
        返回登录需要的tikcets和excution
        '''
        idsLoginGetURL = self.__URLs["idsLoginURL"]
        idsLoginGetHeaders = self.__headers.idsLoginGetHeaders
        idsLoginGetRequst = self.__reqS.get(idsLoginGetURL,headers=idsLoginGetHeaders)
        idsLoginGetSoup = BeautifulSoup(idsLoginGetRequst.content,"html.parser")
        ids_script = idsLoginGetSoup.find_all("script", {'type': 'text/javascript'})
        for temp_script in ids_script:
            temp_str = str(temp_script.string)
            if "pwdDefaultEncryptSalt" in temp_str:
                self.__pwdDefaultEncryptSalt = temp_str.split("=")[-1].split("\"")[1]
                # print(self.__pwdDefaultEncryptSalt)
        idsLoginPostTickets = idsLoginGetSoup.find('input', attrs={'name': 'lt'}).get('value')
        idsLoginPostExecution = idsLoginGetSoup.find('input', attrs={'name': 'execution'}).get('value')
        self.__czCookies = idsLoginGetRequst.cookies
        self.__czCookies.set("org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE","zh_CN")
        return idsLoginPostTickets,idsLoginPostExecution
    
    def __idsLoginPost(self, tickets, execution):
        '''
        就是进行登录操作
        成功了就会显示302
        失败了显示200，200就是回到当前页面重新登录
        '''
        idsLoginPostTickets, idsLoginPostExecution = tickets, execution
        idsLoginPostHeaders = self.__headers.idsLoginPostHeaders
        idsLoginPostURL = self.__URLs["idsLoginURL"]
        encrypted_password = self.encrypt(self.__passWord)
        idsLoginPostContents = {
            "username":  self.__stuNum,
            "password":  encrypted_password,
            "lt": idsLoginPostTickets,# LT-330234-kJqWCnrzjjbvZWCVTCde***************
            "execution": idsLoginPostExecution,
            "_eventId": "submit",
            "dllt": "userNamePasswordLogin",
            "captchaResponse": "",
            "rmShown": "1"
        }
        idsLoginPostRequst = self.__reqS.post(idsLoginPostURL, data=idsLoginPostContents, headers = idsLoginPostHeaders, cookies=self.__czCookies)
        # print("idsLoginPostRequst的状态码：{} {}".format(idsLoginPostRequst.status_code, idsLoginPostRequst.headers))
        # print("password：{} salt:{} password:{}".format(encrypted_password, self.__pwdDefaultEncryptSalt, self.__passWord))

    def __getTrueCookies(self):
        '''
        cookies授权过程涉及多次跳转，每次跳转都操作类似但又不可缺少
        因为刚刚登录了ids这个网页，但是ehall这里还没有进行授权
        发送get请求就会获得302状态码，跳转到ids这个页面
        然后ids会判断这个cookies是否登录
        登录了就会给附带tickets的授权页面网址，接着访问那个网址再次进行授权
        最后再会跳转回到wdkbapp，整个授权过程完成，获取的cookies就可以访问各个API
        '''
        wdkbAppURL = self.__URLs["wdkbappURL"]
        wdkbAppHeaders = self.__headers.ehallWdkbappPreHeaders
        wdkbAppReq = self.__reqS.get(wdkbAppURL, headers=wdkbAppHeaders, allow_redirects=False, cookies=self.__czCookies)
        self.czCookies =  wdkbAppReq.cookies
        firstRedirectURL = wdkbAppReq.headers['Location']
        firstRedirectHeaders = self.__headers.idsLoginGetHeaders
        firstRedirectRequst = self.__reqS.get(firstRedirectURL, headers=firstRedirectHeaders, allow_redirects=False, cookies=self.__czCookies)
        self.czCookies =  firstRedirectRequst.cookies
        # print(firstRedirectRequst.headers)

        secondRedirectURL = firstRedirectRequst.headers['Location']
        secondRedirectHeaders = self.__headers.ehallWdkbappBehindHeaders
        secondRedirectrequest = self.__reqS.get(secondRedirectURL, headers=secondRedirectHeaders, allow_redirects=False, cookies=self.__czCookies)
        self.czCookies =  secondRedirectrequest.cookies

        thirdRedirectURL = secondRedirectrequest.headers['Location']
        thirdRedirectHeaders = secondRedirectHeaders
        thirdRedirectRequest = self.__reqS.get(thirdRedirectURL, headers=thirdRedirectHeaders, allow_redirects=False, cookies=self.__czCookies)
        print("thirdRedirectRequest的状态码：{} ".format(thirdRedirectRequest.status_code))
    
    def getFormartedCookies(self):
        '''
        读取cookiesJar的时候转换成浏览器开发者工具看到的字符串形式
        '''
        cookies = ""
        for i in self.__czCookies:
            cookies = "{}{}={};".format(cookies, i.name, i.value)
        return cookies
    
    def getReqS(self):
        '''
        获取同一个session用于身份识别
        '''
        return self.__reqS
    
    def login(self):
        idsLoginPostTickets,idsLoginPostExecution = self.__idsLoginGet()
        self.__idsLoginPost(idsLoginPostTickets, idsLoginPostExecution)
        self.__getTrueCookies()

    def __pkcs7_padding(self, text):
        """
        pkcs7padding
        :return: 补全后的text
        """
        if not isinstance(text, bytes):
            text = text.encode()
        padder_temp = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder_temp.update(text) + padder_temp.finalize()
        return padded_data

    def encrypt(self, text):
        """
        AES加密函数
        使用AES 的 CBC加密方法加密
        :return:
        """
        # key = 'VNJqWuK6zjeE3dl3'.encode('utf-8')
        key = self.__pwdDefaultEncryptSalt.encode('utf-8')
        mode = AES.MODE_CBC
        iv = self.__rds(16).encode('utf-8')
        text = self.__pkcs7_padding(self.__rds(64) + text)
        cryptos = AES.new(key, mode, iv)
        cipher_text = cryptos.encrypt(text)
        return base64.b64encode(cipher_text)

    def __rds(self, length):
        """
        填充函数，返回指定长度的字符串
        :return:
        """
        _chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
        _chars_len = len(_chars)
        retStr = ''
        i = 0
        while (i < length):
            retStr += _chars[random.randint(0, _chars_len - 1)]
            i += 1
        return retStr