# coding=utf-8
import os
import time
import random
import hashlib
import datetime
import threading


class ProMan(object):
    """docstring for ProMan."""

    isRunning = {}
    path = 'data/db'
    currentMode = ''
    data = {
        'date': None,  # 日期
        'user': '',  # 姓名
        'cfg': {
            'MetaTime': 25,  # 番茄时间（分钟）
            'PlanTime': 5  # 计划时间（分钟）
        },
        'al': {},  # 活动清单(Activity List)
        'tdtd': {},  # 今日待办(Todo Today)
        'r': {}  # 记录(Record)
    }

    def __init__(self, debug=False):
        super(ProMan, self).__init__()
        self.debug = debug
        self.isRunning['ProMan'] = True
        if not os.path.exists('data/'):
            os.mkdir('data')
        elif os.path.exists('data/db'):
            self.load()
        self.today = datetime.date.today()
        self.startInputStar()

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
        t_inputStar = threading.Thread(target=inputStar)
        t_inputStar.start()

    def help(self, cmd):
        if len(cmd) == 1:
            print('''
帮助

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
    act：应用模式
            ''')
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
        elif cmd[1] == 'fin':
            print('fin')
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
        elif cmd[0] == 'set':  # 设置
            self.setCFG(cmd[1], cmd[2:])
        elif cmd[0] == 'plan':  # 进入计划模式
            self.currentMode = 'plan'
        elif self.currentMode == 'plan':  # 计划模式
            if cmd[0] == 'do':  # 进入执行模式
                self.currentMode = 'do'
            elif cmd[0] == 'new':  # 新增活动清单项目
                self.newA(cmd[2:])
            elif cmd[0] == 'add':  # 添加到今日待办
                self.add2TDTD(cmd[2:])
        elif self.currentMode == 'do':  # 执行模式
            if cmd[0] == 'start':  # 启动
                pass
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
    def showAL(self):
        for i, each in enumerate(self.data['al'].keys()):
            text = '[{}]: {}'
            print(text.format(i + 1, self.data['al'][each]['name']))

    def showTDTD(self):
        for i, each in enumerate(self.data['tdtd'].keys()):
            text = '[{}]: {}'
            print(text.format(i + 1, self.data['tdtd'][each]['name']))

    def showR(self):
        for i, each in enumerate(self.data['r'].keys()):
            text = '[{}]: {}'
            print(text.format(i + 1, self.data['r'][each]['name']))

    def setCFG(self, key, value):
        if key in self.data['cfg'].keys():
            if value[0].isdigit():
                self.data['cfg'][key] = int(value[0])
            else:
                self.data['cfg'][key] = value[0]

    def newA(self, *arg):
        newItem = {}
        newItem['name'] = arg[0]
        newItem['des'] = arg[1]
        cmd = input('是否有时效性？[Y/n]:')
        if not cmd == 'n':
            print('=是')
            newItem['timeRequire'] = True
            print('[1]:之前')
            print('[2]:之间')
            print('[3]:某时')
            cmd = input('是哪一种时间要求？:')
            if cmd == '1':
                pass
            elif cmd == '2':
                pass
            elif cmd == '3':
                pass
        else:
            print('=否')
            newItem['timeRequire'] = False
        cmd = input('请输入预判的番茄数:')
        if cmd.isdigit():
            newItem['pot'] = int(cmd)

    def add2TDTD(self, *arg):
        pass

    # 私有
    def generate_hash(self):
        m = hashlib.md5()
        m.update(str(time.time()).encode("utf-8"))
        m.update(str(random.random()).encode("utf-8"))
        return m.hexdigest()

    def load(self):
        with open(self.path, 'r') as dbfile:
            self.data = json.loads(dbfile.read())
            self.data['date'] = datetime.date(*self.data['date'])

    def save(self):
        with open(self.path, 'w') as dbfile:
            dbfile.write(json.dumps(self.data))
            self.data['date'] = (
                self.data['date'].year,
                self.data['date'].month,
                self.data['date'].day
            )

if __name__ == '__main__':
    ProMan()
