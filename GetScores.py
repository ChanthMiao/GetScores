# coding=utf8
import requests
import json
from prettytable import PrettyTable
from prettytable import DEFAULT
# 尝试导入先前用户信息
try:
    ins = open('user.json', 'r')
    payload_1 = json.load(ins)
    ins.close()
except Exception as err:
    # 失败则要求输入密码
    username = input(u'输入账号')
    password = input(u'输入密码')
    # 设置登录所需的字典
    payload_1 = {
        'j_username': username,
        'j_password': password,
        'j_captcha1': 'error',
    }
# 新建一个requests
session_requests = requests.session()
# 指定访问url
login_url = 'http://202.115.47.141/j_spring_security_check'
# post登录
result = session_requests.post(login_url, data=payload_1)
# 生成新url
new_url = 'http://202.115.47.141//student/integratedQuery/scoreQuery/schemeScores/callback'
# GET操作获取分数页面数据
Score_page = session_requests.get(new_url)
res = Score_page.json()
# 分离数据，制表
dict_res = res[0]
cjList = dict_res['cjList']
ScoreTable = PrettyTable(
    ['课程号', '课程名', '分数', '绩点', '学分', '课程属性'], encoding='utf-8')
for EachCourse in cjList:
    ScoreTable.add_row([
        EachCourse['id']['courseNumber'], EachCourse['courseName'],
        EachCourse['cj'], EachCourse['gradePointScore'], EachCourse['credit'],
        EachCourse['courseAttributeName']
    ])
Summary = PrettyTable(['培养方案', '已修读总学分', '通过门数', '未通过门数'], encoding='utf-8')
Summary.add_row([
    dict_res['cjlx'], dict_res['yxxf'], dict_res['tgms'],
    dict_res['zms'] - dict_res['tgms']
])
# 设置表样式
ScoreTable.set_style(DEFAULT)
Summary.set_style(DEFAULT)
# ScoreTable.sortby = '课程名'
# ScoreTable.header = True
ScoreTable.align['课程名'] = 'l'
# 输出
print(ScoreTable)
print(Summary)
# 存储用户信息
with open('user.json', 'w') as output:
    json.dump(payload_1, output)
