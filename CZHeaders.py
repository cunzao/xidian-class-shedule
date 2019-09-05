class czHeaders(object):
    '''
    将所用到的headers都放在类里，方便调用和修改
    '''
    def __init__(self):
        print("czHeaders对象创建成功！")
        
    @property
    def idsLoginGetHeaders(self):
        headers = {
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362",
           "Host": "ids.xidian.edu.cn",
           "Accept": "text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8",    
           "Accept-Language": "zh-Hans-CN, zh-Hans; q=0.5"
        }
        return headers
    
    @property
    def idsLoginPostHeaders(self):
        headers = {
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
        return headers
    
    @property
    def ehallWdkbappPreHeaders(self):
        '''
        第一次访问wdkbApp需要的headers
        '''
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'http://ids.xidian.edu.cn',
            'Host': 'ehall.xidian.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        return headers
    
    @property
    def ehallWdkbappBehindHeaders(self):
        '''
        授权跳转时需要的headers
        '''
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'ehall.xidian.edu.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        }
        return headers
    
    def classSheduleJsonAPIHeaders(self):
        '''
        获取课程表的Json数据需要的headers
        '''
        headers =  {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://ehall.xidian.edu.cn',
            'Referer': 'http://ehall.xidian.edu.cn/gsapp/sys/wdkbapp/*default/index.do',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        return headers