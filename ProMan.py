# coding=utf-8
import os
import json
import time
import random
import hashlib
import datetime as dt
import threading

doc = {
    'help': '''帮助

有关某个命令的详细信息，请键入 “help 命令名”

通用：
    help：显示本帮助
    show：显示各种数据
    set：设置软件参数

流程：
    本程序具有四个标准流程，其顺序为：
        plan → do → check → act

        plan：进入计划模式
    plan：计划模式
        new：新增活动清单项目
        add：添加到今日待办
        do：进入执行模式
    do：执行模式
        start：启动
        pause：中断
        done：提前结束（成功）
        fail：提前结束（失败）
        finish：手动结束今天的执行模式
        check：进入评估模式
    check：评估模式
        act：进入应用模式
    act：应用模式'''
}


class ProMan(object):
    """docstring for ProMan."""

    isRunning = {}
    path = 'data/db.json'
    currentMode = ''
    data = {
        'now': None,  # 日期
        'user': '',  # 姓名
        'cfg': {
            'MetaTime': 25,  # 番茄时间（分钟）
            'PlanTime': 5  # 计划时间（分钟）
        },
        'al': [],  # 活动清单(Activity List)
        'tdtd': [],  # 今日待办(Todo Today)
        'r': [],  # 记录(Record)
        'db': {},  # 存放所有索引与内容的数据库
        'current': {
            'status': 'idle',  # 时钟状态
            'activity': '',  # 当前活动
            'count_down': 0  # 当前倒计时
        }
    }

    def __init__(self, debug=False):
        super(ProMan, self).__init__()
        self.debug = debug
        self.isRunning['ProMan'] = True
        if os.path.exists(self.path):
            self.load()
        elif not os.path.exists('data/'):
            os.mkdir('data')
        self.today = dt.date.today()
        self.startInputStar()
        self.startTimerStar()
        self.t_inputStar.join()
        self.t_timerStar.join()

    def startInputStar(self):
        def inputStar():
            os.system('title ProMan')
            print('Welcome to ProMan!')
            print('You can type "help" to get help.')
            while self.isRunning['ProMan']:
                cmd = input('>')
                if cmd == '':
                    continue
                else:
                    cmd = cmd.split(' ')
                    if cmd[0] == 'exit' or cmd[0] == 'quit':
                        self.isRunning['ProMan'] = False
                    elif cmd[0] == 'help':
                        self.help(cmd)
                    else:
                        self.doCMD(cmd)
        self.t_inputStar = threading.Thread(target=inputStar)
        self.t_inputStar.start()

    def startTimerStar(self):
        def timerStar():
            while self.isRunning['ProMan']:
                time.sleep(1)
                self.data['now'] = dt.datetime.now()
                if self.data['current']['status'] == 'idle':
                    pass
                elif self.data['current']['status'] == 'start':
                    self.data['current']['status'] = 'started'
                    pot = self.data['db'][
                        self.data['current']['activity']]['pot']
                    metaTime = self.data['cfg']['MetaTime']
                elif self.data['current']['status'] == 'started':
                    self.data['current']['count_down'] -= 1
                    if self.data['current']['count_down'] == 0:
                        self.data['current']['status'] = 'finish'
                elif self.data['current']['status'] == 'finish':
                    self.data['current']['status'] = 'idle'
                self.generate_title()
        self.t_timerStar = threading.Thread(target=timerStar)
        self.t_timerStar.start()

    def help(self, cmd):
        if len(cmd) == 1:
            print(doc['help'])
        elif cmd[1] == 'show':
            print('show')
            # TODO: help show
        elif cmd[1] == 'set':
            print('set')
            # TODO: help set
        elif cmd[1] == 'plan':
            print('plan')
            # TODO: help plan
        elif cmd[1] == 'do':
            print('do')
            # TODO: help do
        elif cmd[1] == 'new':
            print('new')
            # TODO: help new
        elif cmd[1] == 'add':
            print('add')
            # TODO: help add
        elif cmd[1] == 'start':
            print('start')
            # TODO: help start
        elif cmd[1] == 'pause':
            print('pause')
            # TODO: help pause
        elif cmd[1] == 'done':
            print('done')
            # TODO: help done
        elif cmd[1] == 'fail':
            print('fail')
            # TODO: help fail
        elif cmd[1] == 'finish':
            print('finish')
            # TODO: help finish
        elif cmd[1] == 'check':
            print('check')
            # TODO: help check
        elif cmd[1] == 'act':
            print('act')
            # TODO: help act

    def doCMD(self, cmd):
        if cmd[0] == 'show':  # 显示
            if cmd[1] == 'al':  # 活动清单(Activity List)
                self.showAL()
            elif cmd[1] == 'tdtd':  # 今日待办(Todo Today)
                self.showTDTD()
            elif cmd[1] == 'r':  # 记录(Record)
                self.showR()
            elif cmd[1] == 'raw':  # 调试
                print(self.data)

        elif cmd[0] == 'set':  # 设置
            self.setCFG(cmd)

        elif cmd[0] == 'plan':  # 进入计划模式
            self.currentMode = 'plan'

        elif self.currentMode == 'plan':  # 计划模式
            if cmd[0] == 'new':  # 新增活动清单项目
                self.newA(cmd)
            elif cmd[0] == 'add':  # 添加到今日待办
                self.add2TDTD(cmd[2:])
            elif cmd[0] == 'do':  # 进入执行模式
                self.currentMode = 'do'

        elif self.currentMode == 'do':  # 执行模式
            if cmd[0] == 'choose':  # 选择计划
                self.chooseTDTD()
            elif cmd[0] == 'start':  # 启动
                self.startA()
            elif cmd[0] == 'pause':  # 中断
                pass
            elif cmd[0] == 'done':  # 提前结束（成功）
                pass
            elif cmd[0] == 'fail':  # 提前结束（失败）
                pass
            elif cmd[0] == 'finish':  # 手动结束今天
                pass
            elif cmd[0] == 'check':  # 进入评估模式
                self.currentMode = 'check'
                pass

        elif self.currentMode == 'check':  # 评估模式
            if cmd[0] == 'act':  # 进入应用模式
                self.currentMode = 'act'
                pass

        elif self.currentMode == 'act':  # 应用模式
            pass

        else:
            pass

    # 公共
    def showAL(self, select=0):
        for i, each in enumerate(self.data['al']):
            if select == 0:
                text = '[{}]: {}'
                print(text.format(i + 1, self.data['db'][each]['name']))
            elif select == i + 1:
                return each

    def showTDTD(self, select=0):
        for i, each in enumerate(self.data['tdtd']):
            if select == 0:
                text = '[{}]: {}'
                print(text.format(i + 1, self.data['db'][each]['name']))
            elif select == i + 1:
                return each

    def showR(self):
        for i, each in enumerate(self.data['r']):
            text = '[{}]: {}'
            print(text.format(i + 1, self.data['db'][each]['name']))

    def setCFG(self, cmd):
        if cmd[1] in self.data['cfg'].keys():
            if cmd[2].isdigit():
                self.data['cfg'][key] = int(cmd[2])
            else:
                self.data['cfg'][key] = cmd[2]

    def newA(self, cmd):
        newItem = {
            'name': '',
            'des': '',
            'timeRequire': None,
            'timeMode': '',
            'pot': 0,
            'his': []
        }
        if len(cmd) == 1:
            newItem['name'] = input('请输入活动名称：')
            newItem['des'] = input('请输入活动描述：')
        elif len(cmd) == 2:
            newItem['name'] = cmd[1]
            newItem['des'] = input('请输入活动描述：')
        else:
            newItem['name'] = cmd[1]
            newItem['des'] = cmd[2]
        cmd = input('是否有时效性？[Y/n]:')
        if not cmd == 'n':
            print('=是')
            newItem['timeRequire'] = True
            print('[1]:之前')
            print('[2]:之间')
            print('[3]:某时')
            cmd = input('是哪一种时间要求？:')
            if cmd == '1':
                newItem['timeMode'] = 'before'
            elif cmd == '2':
                newItem['timeMode'] = 'during'
            elif cmd == '3':
                newItem['timeMode'] = 'at'
        else:
            print('=否')
            newItem['timeRequire'] = False
        cmd = input('请输入预判的番茄数:')
        if cmd.isdigit():
            newItem['pot'] = int(cmd)
        identity = self.generate_hash()
        self.data['db'][identity] = newItem
        self.data['al'].append(identity)

    def add2TDTD(self, *arg):
        self.showAL()
        select = input('请输入编号把活动项目加入今日待办：')
        if select.isdigit():
            identity = self.showAL(int(select))
            if not identity in self.data['tdtd']:
                self.data['tdtd'].append(identity)

    def chooseTDTD(self):
        self.showTDTD()
        select = input('请输入编号选择现在要完成的活动：')
        if select.isdigit():
            identity = self.showTDTD(int(select))
            self.data['current']['activity'] = identity

    def startA(self):
        if self.data['current']['status'] == 'idle':
            self.data['current']['status'] = 'start'
            history = {
                'time': self.dt2l(self.data['now']),
                'data': 'start'
            }
            self.data['db'][self.data['current'][
                'activity']]['his'].append(history)
            self.data['current']['count_down'] = self.data[
                'cfg']['MetaTime'] * 60

    # 私有
    def generate_hash(self):
        m = hashlib.md5()
        m.update(str(time.time()).encode("utf-8"))
        m.update(str(random.random()).encode("utf-8"))
        return m.hexdigest()

    def load(self):
        with open(self.path, 'r') as dbfile:
            self.data = cache = json.loads(dbfile.read())
            self.data['now'] = self.l2dt(cache['now'])

    def save(self):
        try:
            with open(self.path, 'w') as dbfile:
                cache = dict(self.data)
                cache['now'] = self.dt2l(self.data['now'])
                dbfile.write(json.dumps(cache))
        except:
            print('!')

    def dt2l(self, v_dt):  # datetime to list
        v_l = [v_dt.year, v_dt.month, v_dt.day,
               v_dt.hour, v_dt.minute, v_dt.second]
        return v_l

    def l2dt(self, v_l):  # list to datetime
        v_dt = dt.datetime(v_l.year, v_l.month, v_l.day,
                           v_l.hour, v_l.minute, v_l.second)
        return v_dt

    def set_title(self, title=''):
        if title == '':
            os.system('title ProMan')
        else:
            os.system('title ProMan - {}'.format(title))

    def generate_title(self):
        title = 'title ProMan'
        if 'currentMode' in dir(self):
            title += ' - ' + self.data['current']['status']
        if self.data['current']['status'] == 'started':
            title += ' - ' + str(self.data['current']['count_down'])
        os.system(title)

if __name__ == '__main__':
    ProMan()
