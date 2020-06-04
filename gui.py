# -*- coding:utf-8 -*-

import requests
from requests.exceptions import RequestException
import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import bs4
from tkinter import *
from tkinter.filedialog import askdirectory
import os
import csv
import time
import china
import threading


class DB():
    def __init__(self):
        self.window = tk.Tk()  #创建window窗口
        self.window.title("百度地图")  # 定义窗口名称
        self.window.resizable(0,0)  # 禁止调整窗口大小
        self.shen = ttk.Combobox(self.window,width=10)
        self.shi = ttk.Combobox(self.window,width=10)
        self.qu = ttk.Combobox(self.window,width=10)
        self.path = StringVar()
        self.lab1 = tk.Label(self.window, text = "目标路径:")
        self.lab2 = tk.Label(self.window, text="爬取的行业:")
        self.lab3 = tk.Label(self.window, text="省/直辖市")
        self.lab5=tk.Label(self.window,text="市")
        self.lab6=tk.Label(self.window,text="区")
        self.lab4=tk.Label(self.window,text="密码:")
        self.ak=tk.Entry(self.window,width=20)
        #self.lab4 = tk.Label(self.window, text="爬取的行业：")
        self.carear= tk.Entry(self.window, width=20)
        #self.addre = tk.Entry(self.window, width=20)#爬取的地址
        self.input = tk.Entry(self.window, textvariable = self.path, width=80)  # 创建一个输入框,显示图片存放路径
        self.info = tk.Text(self.window, height=20,width=100)   # 创建一个文本展示框，并设置尺寸
        self.shen['value']=['北京市', '天津市', '河北省', '山西省', '内蒙古', '辽宁省', '吉林省', '黑龙江省', '上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省', '广西', '海南省', '重庆市', '四川省', '贵州省', '云南省', '西藏', '陕西省', '甘肃省', '青海省', '宁夏', '新疆', '台湾省', '澳门', '香港']
        # 添加一个按钮，用于选择保存路径
        self.t_button = tk.Button(self.window, text='选择路径', relief=tk.RAISED, width=8, height=1, command=self.select_Path)
        # 添加一个按钮，用于触发爬取功能
        self.t_button1 = tk.Button(self.window, text='爬取', relief=tk.RAISED, width=8, height=1,command=lambda:self.thread_it(self.download))
        # 添加一个按钮，用于触发清空输出框功能
        self.c_button2 = tk.Button(self.window, text='清空输出', relief=tk.RAISED,width=8, height=1, command=self.cle)
        self.stop1=tk.Button(self.window,text='停止爬取', relief=tk.RAISED,width=8, height=1, command=self.stop)
    def gui_arrang(self):
        """完成页面元素布局，设置各部件的位置"""
        self.lab1.grid(row=0,column=0,sticky=E)
        self.lab2.grid(row=1, column=0,sticky=E)
        self.lab3.grid(row=2, column=0,sticky=E,columnspan=1)
        self.lab4.grid(row=3,column=0,sticky=E)
        self.lab5.grid(row=2,column=2,sticky=W)
        self.lab6.grid(row=2,column=4,sticky=W)
        self.ak.grid(row=3,column=1,columnspan=2,sticky=W)
        self.carear.grid(row=1,column=1,columnspan=2,sticky=W)
        self.shen.grid(row=2, column=1,sticky=W)
        self.shi.grid(row=2, column=3,sticky=W)
        self.qu.grid(row=2, column=5,sticky=W)
        self.input.grid(row=0,column=1,columnspan=8,sticky=W)
        self.info.grid(row=4,rowspan=5,column=0,columnspan=10,padx=15,pady=15,sticky=W)
        self.t_button.grid(row=0,column=11,padx=5,pady=5,sticky=tk.W)
        self.t_button1.grid(row=1,column=12)
        self.c_button2.grid(row=0,column=12,padx=5,pady=5,sticky=tk.W)
        self.stop1.grid(row=3,column=12,padx=5,pady=5,sticky=tk.W)
        self.shen.bind('<<ComboboxSelected>>',self.changeshi)
        self.shi.bind('<<ComboboxSelected>>',self.changequ)
    def changequ(self,k):
        value=['all']
        shen=self.shen.get()
        shi=self.shi.get()
        for item in china.division:
            if item['name']==shen:
                for a in item['city']:
                    if a['name']==shi:
                        for b in a['area']:
                            value.append(b)
        self.qu['value']=value
    def changeshi(self,k):
        value=[]
        shen=self.shen.get()
        for item in china.division:
            if item['name']==shen:
                for a in item['city']:
                    value.append(a['name'])
        self.shi['value']=value
    def select_Path(self):
        """选取本地路径"""
        path_ = askdirectory()
        self.path.set(path_)
    def stop(self):
        exit()
    def download(self):
        root_dir = self.input.get()
        query=self.carear.get()
        #region=self.addre.get()
        shen=self.shen.get()
        shi=self.shi.get()
        qu=self.qu.get()
        if qu=='all':
            region=self.qu['value'][1:]
        else:
            region=[qu]
        #ak=self.ak.get()
        f=root_dir+'\\' +shen+shi+qu+query+'.csv'
        out=open(f,'a',newline='')
        csv_write=csv.writer(out,dialect='excel')        
        for j in region:
            urls=[]
            addr=shen+shi+j
            ak = '########'  #换自己申请的ak
            url1='http://api.map.baidu.com/place/v2/search?query='+query+'&region='+addr+'&coord_type=1&page_size=20&page_num=0&output=json&ak='+ak
            todata=requests.get(url1)
            todata=todata.json()
            total=todata['total']
            self.info.insert('end','正在爬取'+addr+'\n')
            self.info.insert('end','总计'+str(total)+'\n')
            self.info.update()
            for i in range(0,(int(total)%20)+1):
                page_num=str(i)
                url='http://api.map.baidu.com/place/v2/search?query='+query+'&region='+addr+'&coord_type=1&page_size=20&page_num='+str(page_num)+'&output=json&ak='+ak
                urls.append(url)
            for url in urls:
                time.sleep(2)
                #print(url)
                html=requests.get(url)#获取网页信息
                data=html.json()#获取网页信息的json格式数据
                #print(data)
                for item in data['results']:
                    jname1 = item['province']
                    jname2 = item['city']
                    jname3 = item['area']
                    jname4 = item['name']
                    jname=jname2+jname3+jname4
                    #j_uid=item['uid']
                    #jstreet_id=item.get('street_id')
                    jlat=item['location']['lat']
                    jlon=item['location']['lng']
                    jaddress=item['address']
                    jphone=item.get('telephone')
                    j_str=(jname1,jname2,jname3,jname4,str(jlat),str(jlon),jaddress,jphone)
                    self.info.insert('end',str(j_str)+'\n')
                    #time.sleep(0.1)
                    self.info.update()
                    #print(j_str)
                    csv_write.writerow(j_str)
                    self.info.see(END)
                    #print("write over")#  f.write(j_str)
        self.info.insert('end','爬取完成')
        self.info.update()
    def thread_it(self,func):
        t = threading.Thread(target=func) 
        t.setDaemon(True) 
        t.start()
    def cle(self):
        """定义一个函数，用于清空输出框的内容"""
        self.info.delete(1.0,"end")  # 从第一行清除到最后一行


def main():
    t = DB()
    t.gui_arrang()
    tk.mainloop()

if __name__ == '__main__':
    main()
