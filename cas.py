from urllib.request import urlopen
import time
import requests
import execjs
from bs4 import BeautifulSoup


def jlu_oa(url,session,rsa,ul,pl,sl,lt,excution,eventId):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36 Edg/125.0.0.0'
    }
    params = {
        'rsa': rsa,
        'ul': ul,
        'pl': pl,
        'sl': sl,
        'lt': lt,
        'execution': excution,
        '_eventId': eventId
    }
    r = session.post(url, data=params, headers=headers)  # 带着参数去网址进行登录
    # print(r.text, str(session.cookies.get_dict()))
    requests.adapters.DEFAULT_RETRIES = 5
    session.keep_alive = False
    url_new = ''#要访问的二级网址
    try:
        response = session.get(url_new,verify = False,headers=headers)
        time.sleep(10)
        soup = BeautifulSoup(response.text, 'lxml')
        print(soup.text)
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"
        print(r)

def cas_download():
    # 获取一次lt
    url = str(input("请输入要测试的url："))
    if len(url) == 0 :
        url = 'https://cas.jlu.edu.cn/tpass/login?service=https%3A%2F%2Fehall.jlu.edu.cn%2Fsso%2Flogin%3Fredirect_uri%3Dhttps%253A%252F%252Fehall.jlu.edu.cn%252Fsso%252Foauth2%252Fauthorize%253Fscope%253Ddata%252Bintrospect%252Bprofile%252Btask%252Btriple%252Bprofile_edit%252Bprocess%2526response_type%253Dcode%2526redirect_uri%253Dhttps%25253A%25252F%25252Fehall.jlu.edu.cn%25252Fjlu_portal%25252Fwall%25252Fendpoint%25253FretUrl%25253Dhttps%2525253A%2525252F%2525252Fehall.jlu.edu.cn%2525252Fjlu_portal%2525252Findex%2526client_id%253D4epTvP90dDuVNU5waqBT%26x_client%3Dcas'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47"
    }
    session = requests.session()  # 建立session会话
    response = session.get(url, headers=headers)
    requests.packages.urllib3.disable_warnings()
    response.encoding = response.apparent_encoding
    html = BeautifulSoup(response.text, 'html.parser')
    content = str(html.find('input', id='lt'))
    lt_list = content.split('"',-1)
    print("获取lt为：",lt_list[7])
    # 获取execution
    content = str(html.find('input', attrs={'name': "execution"}))
    excution_list = content.split('"',-1)
    excution = excution_list[5]
    print("获取excution：",excution)
    # 获取_eventId
    content = str(html.find('input',attrs={'name': "_eventId"}))
    eventId_list = content.split('"',-1)
    eventId = eventId_list[5]
    print("获取eventId：",eventId)
    # 放入用户名和密码
    username = ""
    password = ""
    # 获取长度，得到ul和pl，并对sl定义为0
    ul = len(username)
    pl = len(password)
    sl = 0
    # 核心部分，计算rsa
    # 首先调用cas-des.js
    # 需要先将即将执行的代码块编译一下，这里的cas-des.js文件最好是引用绝对地址
    compile_code = execjs.compile(open('./cas-des.js', 'r', encoding='utf-8').read())
    #compile_code = execjs.compile(open('cas-des.js','r',encoding = 'utf-8').read())
    # 使用编译后的代码块call函数调用js文件中的hello_world函数
    code_fist = username + password + lt_list[7]
    result = compile_code.call('strEnc',code_fist,'1' , '2' , '3')
    print("计算rsa：",result)
    rsa_ok = result
    # 调用模拟登录函数
    jlu_oa(url,session,rsa_ok,ul,pl,sl,lt_list[7],excution,eventId)




if __name__ == "__main__":
    cas_download()
