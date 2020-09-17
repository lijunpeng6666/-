# coding=utf-8

import sys


import PyHook3 as pyHook
import pythoncom
import pyautogui as pg
from pymouse import PyMouse
import time
from configparser import ConfigParser

coordinate_list = []


# 监听到鼠标事件调用
def onMouseEvent(event):
    if (event.MessageName == "mouse middle down"):  # 按下中键录制坐标
        x, y = pg.position()  # 获取当前鼠标的坐标（像素）
        coordinate_list.append((x, y))
        print("第%d个坐标已添加！" % len(coordinate_list))
    return True  # 为True才会正常调用，如果为False的话，此次事件被拦截


def onKeyEvent(event):
    cp = ConfigParser()
    cp.read("ini.cfg")
    section = cp.sections()[0]
    num_of_cycles = cp.getint(section, "num_of_cycles")
    Number_of_hits = cp.getint(section, "Number_of_hits")
    sleep = cp.getint(section, "sleep")
    if (event.MessageName == "key down" and event.Key == "Q"):  # 按下Q按钮清除记录列表中上一个点
        if len(coordinate_list) == 0:
            print("当前列表中无坐标，请做定位操作！")
        else:
            print("第%d个坐标已删除！" % len(coordinate_list))
            coordinate_list.pop()
    if (event.MessageName == "key down" and event.Key == "B"):  # 按B执行自动点击功能
        if len(coordinate_list) == 0:  # 判断列表是否为空
            print("当前列表中无录制点位！")
        else:
            c = 0
            print("自动点击开始！")
            while c < num_of_cycles:
                print("当前为%d次循环！" % (c + 1))
                for i in coordinate_list:
                    PyMouse().press(i[0], i[1], Number_of_hits)
                    time.sleep(sleep)
                c += 1
            print("自动点击结束！\n当前列表中点位为%s" % coordinate_list)
            print("1.点击鼠标中键可进行当前鼠标所在坐标记录！\n""2.点击Q可以清除上一次所记录的点\n""3.点击B可进行自动点击功能\n""4.点击A可清空所有坐标点位！\n""5.点击S可关闭脚本！（循环异常时可强行结束）")
    if (event.MessageName == "key down" and event.Key == "A"):
        coordinate_list.clear()
        print("当前列表中坐标点已清空！")
    if (event.MessageName == "key down" and event.Key == "S"):
        sys.exit()
    return True


def main():
    # 创建管理器
    hm = pyHook.HookManager()
    # 监听鼠标
    hm.MouseAll = onMouseEvent
    hm.HookMouse()
    hm.KeyAll = onKeyEvent
    hm.HookKeyboard()
    # 循环监听
    pythoncom.PumpMessages()





if __name__ == "__main__":
    print("1.点击鼠标中键可进行当前鼠标所在坐标记录！\n""2.点击Q可以清除上一次所记录的点\n""3.点击B可进行自动点击功能\n""4.点击S可关闭脚本！（循环异常时可强行结束）")
    main()
