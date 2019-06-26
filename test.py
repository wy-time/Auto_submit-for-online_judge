from bs4 import BeautifulSoup
import configparser
import os
import re
import requests

"""
class DriectionError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)  # ?????
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


url = "http://codeforces.com/enter"
try:
    headers_info = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }
    session = requests.session()
    r = session.get(url, headers=headers_info)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    csrf_token = soup.find('input', attrs={"name": "csrf_token"})
    csrf_token = csrf_token["value"]
    login_data = {
        'csrf_token': csrf_token,
        'action': 'enter',
        'handleOrEmail': '1142942494@qq.com',
        'password': '00zxc7585245300',
        '_tta': '96',
    }
    # print(login_data)
    r = session.post(url, headers=headers_info, data=login_data)
    r = session.get("http://codeforces.com/settings/general",
                    headers=headers_info, verify=False)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    # print(cookie)
    print(soup.prettify())
except Exception:
    print('error')
info = {}
abs_dir = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read(abs_dir+"/config.ini")
kkk = conf.items("codeforce")
for temp in kkk:
    info[temp[0]] = temp[1]
print(info)
fin = open("config.conf", 'r', encoding='UTF-8')
for line in fin.readlines():
    line = line.strip()
    k = line.split(' ')[0]
    v = line.split(' ')[1]
    info[k] = v
print(info['username'])
fin = open("/home/time/桌面/脚本/quick_submit/config.ini", "r")
print(fin)
print(type(fin.read()))
s1 = "<span class='verdict-rejecteds'>Wrong answer on test <span class='verdict-format-judgeds'>1</span></span>"
s2 = re.match(r'<.*>(.*)<.*>(\d+).*', s1)
print(s2.group(1))
print(s2.group(2))
"""
fin=open("/home/time/桌面/脚本/quick_submit/config.ini",'r')
fout=open("/home/time/桌面/脚本/quick_submit/1"+".cpp",'w')
fout.write(fin.read())
fin.close()
fout.close()
