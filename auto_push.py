#!/usr/bin/env python
# -*- coding:utf-8 -*-
import subprocess

from watchdog.observers import Observer
from watchdog.events import *
import time
import os

def push(change):
    print('-' * 76)
    os.system('git add .')
    os.system('git commit -m \" auto' + change + '\"')
    os.system("git fetch origin master && git rebase origin/master")
    os.system('git push origin master')
    print('-' * 76)


class FileEventHandler(RegexMatchingEventHandler):
    def __init__(self):
        # 过滤git文件目录
        RegexMatchingEventHandler.__init__(self, ignore_regexes=["./.git", "./.idea"])

    # 文件或文件夹移动
    def on_moved(self, event):
        print("file moved from {0} to {1}".format(event.src_path, event.dest_path))
        push("文件移动: {0} to {1}".format(event.src_path, event.dest_path))

    # 创建文件或文件夹
    def on_created(self, event):
        print("file created: {0}".format(event.src_path))
        push("创建文件: {0}".format(event.src_path))

    # 删除文件或文件夹
    def on_deleted(self, event):
        print("file deleted: {0}".format(event.src_path))
        push("删除文件: {0}".format(event.src_path))

    # 移动文件或文件夹
    def on_modified(self, event):
        print("file modified: {0}".format(event.src_path))
        push("文件修改: {0}".format(event.src_path))


if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    dis_dir = "./"
    observer.schedule(event_handler, dis_dir, True)
    observer.start()
    try:
        while True:
            # 设置监听频率(秒)
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
