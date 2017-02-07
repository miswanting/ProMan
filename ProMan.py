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
        self.startInputStar()

    def startInputStar(self):
        def inputStar():
            while self.isRunning['ProMan']:
                cmd = input('>')
                if cmd == '':
                    continue
                else:
                    cmd = cmd.split(' ')
                    if cmd == 'exit' or cmd == 'quit':
                        self.isRunning['ProMan'] = False
                    else:
                        self.doCMD(cmd)
        t_inputStar = threading.Thread(target=inputStar)
        t_inputStar.start()

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
            pass
        elif self.currentMode == 'plan':  # 计划模式
            if cmd[0] == 'do':  # 进入执行模式
                self.currentMode = 'do'
                pass
        elif self.currentMode == 'do':  # 执行模式
            if cmd[0] == 'start':  # 启动
                pass
            elif cmd[0] == 'pause':  # 中断
                pass
            elif cmd[0] == 'done':  # 提前结束（成功）
                pass
            elif cmd[0] == 'fail':  # 提前结束（失败）
                pass
            elif cmd[0] == 'fin':  # 手动结束今天
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
            print(text.format(i + 1, self.data['al'][each]['title']))

    def showTDTD(self):
        for i, each in enumerate(self.data['tdtd'].keys()):
            text = '[{}]: {}'
            print(text.format(i + 1, self.data['tdtd'][each]['title']))

    def showR(self):
        for i, each in enumerate(self.data['r'].keys()):
            text = '[{}]: {}'
            print(text.format(i + 1, self.data['r'][each]['title']))

    def setCFG(self, key, value):
        if key in self.data['cfg'].keys():
            if value[0].isdigit():
                self.data['cfg'][key] = int(value[0])
            else:
                self.data['cfg'][key] = value[0]

    # 私有
    def generate_hash(self):
        m = hashlib.md5()
        m.update(str(time.time()).encode("utf-8"))
        m.update(str(random.random()).encode("utf-8"))
        return m.hexdigest()

    def load(self):
        with open(self.path, 'r') as dbfile:
            self.data = json.loads(dbfile.read())

    def save(self):
        with open(self.path, 'w') as dbfile:
            dbfile.write(json.dumps(self.data))

if __name__ == '__main__':
    ProMan()
