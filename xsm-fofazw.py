import base64
import os
import random
import re
from urllib.parse import urlparse
import mmh3
import requests
import urllib3
# 禁用 InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

user_agent = ['Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.8.1) Gecko/20061010 Firefox/2.0',
                    'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.6 Safari/532.0',
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1 ; x64; en-US; rv:1.9.1b2pre) Gecko/20081026 Firefox/3.1b2pre',
                    'Opera/10.60 (Windows NT 5.1; U; zh-cn) Presto/2.6.30 Version/10.60','Opera/8.01 (J2ME/MIDP; Opera Mini/2.0.4062; en; U; ssr)',
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; ; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                    'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr; rv:1.9.2.4) Gecko/20100523 Firefox/3.6.4 ( .NET CLR 3.5.30729)',
                    'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
                    'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5']

headers = {'User-Agent': random.choice(user_agent)}
head = ['\033[31m', '\033[32m']
tail = '\033[0m'
text = rf'''{head[0]}                                _           _                            
__  __ ___  _ __ ___          / _|  ___   / _|  __   ______      __
\ \/ // __|| '_ ` _ \  _____ | |_  / _ \ | |_  / _` ||_  /\ \ /\ / /
 >  < \__ \| | | | | ||_____||  _|| (_) ||  _|| (_| | / /  \ V  V / 
/_/\_\|___/|_| |_| |_|       |_|   \___/ |_|   \__,_|/___|  \_/\_/  
                                                                                                            
一款来自雪山盟成员的web指纹提取工具（用于提取网页指纹并输出fofa语法） version:1.0.0{tail}{head[1]}
[*]BY.雪山盟-表面
[*]联系方式:YY1127viv
[*]交流基地:2294413043
[*]Github:https://github.com/biaomian09/xsm-fofazw
'''
def url_host(urls):
    try:
        response = requests.get(urls, headers=headers, timeout=2, verify=False)
        if response.status_code == 200:
            return True
    except Exception as e:
        print(f"{head[0]}主机解析失败: {e}{tail}")
        return False

def zhiwen():
    try:
        response = requests.get(url, headers=headers, timeout=3, verify=False)
        response.encoding = 'utf-8'
        r'''
        ["/']指的是匹配单双引号，之前的写法只匹配了双引号，\s*指的是这里允许有空格;
        [^"\'] 匹配以单双引号开头的任意内容，例如href = "/image/age/favicon.ico，会将路径都匹配到;
        (?:ico|png|jpg) 只允许以这三个结尾的，re.I忽略大小写
        '''
        ico = re.compile(r'href\s*=\s*["\']([^"\']*?favicon\.(?:ico|png|jpg))["\']', re.I)
        icon = ico.findall(response.text)
        host = re.findall('https?://.*?/', response.url)[0]
        # print(response.text)
        if icon:
            # print(icon)
            icon = icon[0]
            icon = urlparse(icon).path
            # print(icon)
            if icon.startswith('/'):
                icon = icon[1:]
            ico_url = host + icon
            # print(ico_url)
            ico_response = requests.get(ico_url, timeout=3, verify=False)
            icon_hash = str(mmh3.hash(base64.encodebytes(ico_response.content)))
            print(f'{head[1]}指纹图片地址：{ico_url}{tail}')
            print(f'{head[1]}FOFA语法：icon_hash="{icon_hash}"{tail}')
            return
        elif not icon:
            dirname = os.path.join(os.getcwd())
            dirnames = dirname + r'\zhiwen.txt'
            found = False
            with open(dirnames, 'r', encoding='utf-8') as f:
                for i in f:
                    icon = i.strip()
                    ico_url = host + icon
                    ico_response = requests.get(ico_url, timeout=3, verify=False)
                    if ico_response.status_code == 200:
                        icon_hash = str(mmh3.hash(base64.encodebytes(ico_response.content)))
                        print(f'{head[1]}指纹图片地址：{ico_url}{tail}')
                        print(f'{head[1]}FOFA语法：icon_hash="{icon_hash}"{tail}')
                        found = True
                        break
                if not found:
                    print(f'{head[0]}未找到指纹图片{tail}')
        else:
            print(f'{head[0]}未找到指纹图片{tail}')
    except Exception as e:
        print(e)
print(text)
url = input('请输入您要检测的域名/ip：')
if not url_host(url):
    exit()
else:
    zhiwen()
