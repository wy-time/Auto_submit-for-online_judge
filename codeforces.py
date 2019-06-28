from bs4 import BeautifulSoup
import time
import configparser
import os
import re
import requests


info = {}  # 配置信息


class DriectionError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)  # 初始化父类别
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


def init():  # 读取配置文件
    abs_dir = os.path.dirname(os.path.abspath(__file__))
    conf = configparser.ConfigParser()
    conf.read(abs_dir+"/config.ini", encoding='UTF-8')
    res = conf.items("codeforce")
    for da in res:
        info[da[0]] = da[1]
    if(info['username'] == 'username'):
        print("请填写配置文件")
        exit()


def login(baseurl, session):  # 登录
    headers_info = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }
    try:
        response = session.get(baseurl, headers=headers_info)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        res = soup.find("input", attrs={"name": "csrf_token"})
        csrf_token = res["value"]
        login_data = {
            'csrf_token': csrf_token,
            'action': 'enter',
            'handleOrEmail': info['username'],
            'password': info['password'],
            '_tta': '96',
        }
        session.post(baseurl, headers=headers_info, data=login_data)
    except Exception as e:
        print("登录失败"+e)


def get_dir(url):  # 获取存储位置
    try:
        kv = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        }
        r = requests.get(url, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string
        # 切分字串, 正则的s代表空格或者tab, 即以' - '分割字符串
        titles = re.split(r'\s+-\s+', title)
        title = titles[1]
        titles = re.match(r'(.*)\sRound\s(.*)', title)  # ()代表分组
        website = titles.group(1)
        roun = titles.group(2)
        dir = info['save_path']
        flag = 1
        if(re.match(r'.*Codeforces.*', website)):
            dir += "cf/"
            if(re.match(r'.*Educational.*', website)):
                temp = re.match(r'.*(\d\d+).*(\d+).*', roun)
                if(temp):
                    dir += "div"+temp.group(2)+"/edu/"
                    dir += temp.group(1)+"/"
                else:
                    flag = 0
            elif(re.match(r'.*Global.*', website)):
                dir += "Codeforces_Global/"
                dir += roun+"/"
            else:
                temp = re.match(r'.*(\d\d\d+).*(\d+).*', roun)
                if(temp):
                    dir += "div"+temp.group(2)+"/"
                    dir += temp.group(1)+"/"
                else:
                    flag = 0
        else:
            flag = 0
            raise DriectionError("未识别到cf页面")
        if(flag == 1):
            return dir
        else:
            raise DriectionError("dir error")
    except DriectionError as e:
        print(e)
        print(dir)
    except Exception:
        print("连接失败")


def submit(contest_id, problem_id, session, url):
    try:
        kv = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        }
        # 获取csrf_token
        url += "/submit"
        response = session.get(url, headers=kv)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        res = soup.find("input", attrs={"name": "csrf_token"})
        csrf_token = res['value']
        # 提交
        url += "?csrf_token="+csrf_token
        path = info['work_path']
        source_code = open(path, 'r', encoding='UTF-8')
        submit_data = {
            'csrf_token': csrf_token,
            'action': 'submitSolutionFormSubmitted',
            'contestId': contest_id,
            'submittedProblemIndex': problem_id,
            'programTypeId': info['language'],
            'source': source_code.read(),
            'tabSize': '4',
            'sourceFile': '',
            '_tta': '96'
        }
        source_code.close()
        session.post(url, headers=kv, data=submit_data)
    except Exception as e:
        print("提交失败"+e)


def get_status(url, session):
    headers_info = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }
    url += "/my"
    flag = True
    try:
        while(flag):
            time.sleep(1)
            response = session.get(url, headers=headers_info)
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            tables = soup.find_all("table")
            table = []
            if(len(tables) == 4):
                table = tables[2]
            else:
                table = tables[1]
            trs = table.find_all("tr")
            tr = trs[1]
            tds = tr.find_all("td")
            td = tds[5]
            if(td['waiting'] != 'true'):
                spans = td.find_all("span")
                span = spans[1]
                if(span['class'][0] == "verdict-rejected"):
                    flag = False
                    s1 = str(span)
                    s2 = re.match(r'<.*>(.*)<.*>(\d+).*', s1)
                    print(s2.group(1)+s2.group(2))
                elif(span['class'][0] == "verdict-accepted"):
                    flag = False
                    print(span.string)
                    return str(span.string)
            else:
                spans = td.find_all("span")
                if(len(spans) != 0):
                    span = spans[0]
                    s1 = str(span)
                    s2 = re.match(r'<.*>(.*)<.*>(\d+).*', s1)
                    print(s2.group(1)+s2.group(2))
                else:
                    print(td.string)
    except Exception as e:
        print("获取结果失败"+e)


def save_code(dir, problem_id):
    work_path = info['work_path']
    source_code = open(work_path, 'r', encoding='UTF-8')
    folder = os.path.exists(dir)
    if not folder:
        os.makedirs(dir)
    fout = open(dir+problem_id+".cpp", 'w', encoding='UTF-8')
    fout.write(source_code.read())
    source_code.close()
    fout.close()


if __name__ == '__main__':
    init()
    baseurl = "http://codeforces.com"
    contest_url = baseurl+"/contest/"
    contest_info = input()
    contest_info = re.split(r'\s+', contest_info)
    contest_id = contest_info[1]
    problem_id = contest_info[2]
    problem_id = problem_id.upper()
    contest_url += contest_id
    dir = get_dir(contest_url)
    session = requests.session()
    login(baseurl+"/enter", session)  # 登录
    submit(contest_id, problem_id, session, contest_url)  # 提交
    result = get_status(contest_url, session)  # 获得返回结果
    if(result == "Accepted" or result == "Pretests passed"):
        save_code(dir, problem_id)
