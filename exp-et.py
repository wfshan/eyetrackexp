# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 01:00:54 2016

@author: wfshan

20161020更新
"""

import wx
import wx.richtext as rt
import random
import time
import sys  
import os
import thread
import win32api
from ctypes import *
from iViewXAPI import  *
from iViewXAPIReturnCodes import * 
reload(sys)  
sys.setdefaultencoding('gb18030')



# ---------------------------------------------
#---- connect to iView
# ---------------------------------------------

res = iViewXAPI.iV_SetLogger(c_int(1), c_char_p("iViewXSDK_Python_GazeContingent_Demo.txt"))
res = iViewXAPI.iV_Connect(c_char_p('127.0.0.1'), c_int(4444), c_char_p('127.0.0.1'), c_int(5555))

res = iViewXAPI.iV_GetSystemInfo(byref(systemData))
print "iV_GetSystemInfo: " + str(res)
print "Samplerate: " + str(systemData.samplerate)
print "iViewX Verion: " + str(systemData.iV_MajorVersion) + "." + str(systemData.iV_MinorVersion) + "." + str(systemData.iV_Buildnumber)
print "iViewX API Verion: " + str(systemData.API_MajorVersion) + "." + str(systemData.API_MinorVersion) + "." + str(systemData.API_Buildnumber)
iViewXAPI.iV_StartRecording()
iViewXAPI.iV_PauseRecording()
# ---------------------------------------------
#---- configure and start calibration
# ---------------------------------------------

#calibrationData = CCalibration(5, 1, 0, 0, 1, 250, 220, 2, 20, b"")
#res = iViewXAPI.iV_SetupCalibration(byref(calibrationData))


#print "iV_SetupCalibration " + str(res)
#res = iViewXAPI.iV_Calibrate()
#print "iV_Calibrate " + str(res)
#res = iViewXAPI.iV_Validate()
#print "iV_Validate " + str(res)

#res = iViewXAPI.iV_GetAccuracy(byref(accuracyData), 1)
#print "iV_GetAccuracy " + str(res)
#print "deviationXLeft " + str(accuracyData.deviationLX) + " deviationYLeft " + str(accuracyData.deviationLY)
#print "deviationXRight " + str(accuracyData.deviationRX) + " deviationYRight " + str(accuracyData.deviationRY)


class main_page(wx.Frame):
    def __init__(self):
#the main page


        wx.Frame.__init__(self,None,-1,'wfs',size = wx.DisplaySize()) 
        size = wx.DisplaySize()
        self.ww = size[0]
        self.yy = size[1]
        self.panel = wx.Panel(self)
        self.button2 = wx.Button(self.panel,-1,u'开始实验',pos = ((self.ww-200)/2,500),size = (200,100))
        self.button2.Bind(wx.EVT_LEFT_DOWN,self.preguide)
        self.chocond = wx.RadioBox(self.panel,-1,'choice exp condition',pos = (650,280),size = (200,100),choices = ['condition1','condition2'])
#here to choose exp condition  chocond = 0 none eyetracking，chocond = 1 with eyetracking                
        wx.StaticText(self.panel,-1,u'编号',(350,255))
        wx.StaticText(self.panel,-1,u'姓名',(350,285))
        wx.StaticText(self.panel,-1,u'专业',(350,315))
        wx.StaticText(self.panel,-1,u'出生年月',(350,345))
        wx.StaticText(self.panel,-1,u'性别',(350,375))
        
        self.iid = wx.TextCtrl(self.panel,-1,'',(400,250))
        self.nname= wx.TextCtrl(self.panel,-1,'',(400,280))
        #self.bbirthday= wx.TextCtrl(self.panel,-1,'',(400,340))
        self.mmagor= wx.TextCtrl(self.panel,-1,'',(400,310))
        y = range(1985,2005)
        for i in range(20):
            y[i] = '%s'%y[i]            
        m = ['01','02','03','04','05','06','07','08','09','10','11','12',]  
        self.birthdayy = wx.Choice(self.panel, -1,(400,340),(60,40),y)
        self.birthdaym = wx.Choice(self.panel, -1,(460,340),(50,40),m)
        
        cho = ['male','female']
        self.ggender= wx.Choice(self.panel, -1,(400,370),(100,40),cho)#wx.TextCtrl(self.panel,-1,'',(400,310))
        
        
        self.dic = {0:u'囊泡',
                    1:u'中微子',
                    2:u'植物热值',
                    3:u'戒断症状',
                    4:u'暗物质',
                    5:u'基因组',
                    6:u'原子钟',
                    7:u'气穴栓塞',
                    8:u'承灾体脆弱性',
                    9:u'集约化养殖',
                    10:u'蜂群衰竭',
                    11:u'高压脊',
                    12:u'陈化烟叶',
                    13:u'乙烯',
                    14:u'人巨细胞病毒',
                    15:u'中心型占位',
                    16:u'流行病学',
                    17:u'分子机制',
                    18:u'肌肉能量技术',
                    19:u'自噬作用',
                    20:u'病原体',
                    21:u'网络协议',
                    22:u'量子效应',
                    23:u'小世界网络',
                    24:u'热泵',
                    25:u'馈源舱',
                    26:u'薪酬体系',
                    27:u'语义信息',
                    28:u'民族文化',
                    29:u'城市化',
                    30:u'乖讹—消解理论',
                    31:u'教育方式',
                    32:u'低碳发展',
                    33:u'网络舆论暴力',
                    34:u'花序',
                    35:u'配送组织网格化'}#the dic for num and keyword for exp material
        self.l = ()#
        self.mlist = [1,3,4,6,7,8,9,10,16,18,19,34,21,22,23,24,25,27,29,33]
        self.i = 0#material num
        self.t = ''#exp material text
        self.h = ''#exp material hint meggage  
        
        self.info = []#subject's information
        self.readtime = []
        self.answertime = []
        self.answerselect = []
        self.pinjiatime = []
        self.pingjiaselect = [] 
        self.magtime = []
        self.trialnum = 1
        self.datalabel = ['systime',u'condition',u'id',u'name',u'gender',u'age',u'major','trialnum',u'materialnum',u'readtime',u'answer',u'answertime',u'pj1',u'pj2',u'pj3',u'pj4',u'pjtime',u'magtime','magcount']
        self.tri1 = 0
        self.tleavelabel = 0
        self.tenterlabel = 0
        self.tleavemag = 0
        self.tentermag = 0
        self.entermagtri = 0
        self.leavemagtri = 0
        self.enterlabeltri = 0
        self.leavelabeltri = 0
        self.magtimebegin = 0
        self.magtimeend = 0
        self.ivtri = 0
        
    def mouse2eye(self,tri):
        while tri:
            if self.tri == 1:
                iViewXAPI.iV_GetEvent(byref(eventData))
                POSX = eventData.positionX
                POSY = eventData.positionY
                win32api.SetCursorPos((int(POSX),int(POSY)))
            else:
                thread.exit_thread()

    def eyecal(self):
        calibrationData = CCalibration(5, 1, 0, 0, 1, 250, 220, 2, 20, b"")
        res = iViewXAPI.iV_SetupCalibration(byref(calibrationData))
    
        res = iViewXAPI.iV_Calibrate()
        res = iViewXAPI.iV_Validate()
        res = iViewXAPI.iV_GetAccuracy(byref(accuracyData), 0)
        deviationXLeft = float(accuracyData.deviationLX)
        deviationYLeft = float(accuracyData.deviationLY)
        deviationXRight = float(accuracyData.deviationRX)
        deviationYRight = float(accuracyData.deviationRY)
        if deviationXLeft<0.5 and deviationYLeft<0.5 and deviationXRight<0.5 and deviationYRight<0.5:
            self.panel.Hide()
            self.eyecalpanel = wx.Panel(self,-1,size = wx.DisplaySize())
            t = 'deviationXLeft  : %f \n\n deviationYLeft  : %f \n\n deviationXRight  : %f \n\n deviationYRight  : %f \n\n'%(deviationXLeft,deviationYLeft,deviationXRight,deviationYRight)
            result = wx.StaticText(self.eyecalpanel,-1,t,(600,255))
            wx.StaticText(self.eyecalpanel,-1,u'校准完成，按空格键结束校准',(600,655))
            result.SetFocus()
            result.Bind(wx.EVT_KEY_DOWN,self.eyecal2)
            self.eyecaltri = 1
        
        else:
            self.eyecalpanel = wx.Panel(self,-1,size = wx.DisplaySize())
            self.panel.Hide()
            t = 'deviationXLeft  : %f \n\n deviationYLeft  : %f \n\n deviationXRight  : %f \n\n deviationYRight  : %f \n\n'%(deviationXLeft,deviationYLeft,deviationXRight,deviationYRight)
            result = wx.StaticText(self.eyecalpanel,-1,t,(600,255))
            wx.StaticText(self.eyecalpanel,-1,u'校准失败，按空格键重新校准',(600,655))
            result.SetFocus()
            result.Bind(wx.EVT_KEY_DOWN,self.eyecal2)
            self.eyecaltri = 0

    def eyecal2(self,event):
        self.eyecalpanel.Destroy()
        if self.ivtri < 6:
            if self.eyecaltri == 1:
                self.guide()
            else:
                self.eyecal()
        else:
            self.thanku()
        
    def preguide(self,event):
        
        self.cho = self.chocond.GetSelection()
        self.id = self.iid.GetValue()
        self.name = self.nname.GetValue()
        self.gender = self.ggender.GetStringSelection()
        self.birthday = self.birthdayy.GetStringSelection()+self.birthdaym.GetStringSelection()
        self.magor = self.mmagor.GetValue()
        self.info = [self.cho,self.id,self.name,self.gender,self.birthday,self.magor]
        
        f = open('data\%s_%s_%s.csv'%(self.cho,self.id,self.name),'a')
        t = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
        for i in self.datalabel:
            s = str('%s,'%i)
            f.write(s)
        f.write('\n')
        f.write('%s,'%t)
        for i in self.info:
            s = str('%s,'%i)
            f.write(s)

        f.close()
        
        if self.id=='' or self.name=='' or self.gender=='' or self.birthday == '' :
            dlg = wx.MessageDialog(self, u'请完善信息','meg',wx.OK|wx.ICON_INFORMATION)
            if dlg.ShowModal() == wx.ID_OK:
                dlg.Close(True)
        else:
            self.eyecal()
            
    def guide(self):
        self.g_panel = wx.Panel(self,-1,size = wx.DisplaySize())
        self.g_txt = rt.RichTextCtrl(self.g_panel,pos = ((self.ww-790)/2,150),size = (790,330),style = rt.RE_MULTILINE|rt.RE_READONLY)
        font = wx.Font(18,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
        self.g_txt.BeginLineSpacing(13)
        self.g_txt.BeginFont(font)
        
        self.cho = self.chocond.GetSelection()

        
        if self.cho:
            self.g_txt.WriteText(u'欢迎参加本实验，实验中你将看到数段文本材料，每个材料中都有一个\n带有灰色背景的词，将鼠标光标移到灰色区域则出现能辅助你理解该文\n本的附加信息，移开鼠标则信息消失。\n1.请在完成一遍阅读之后立即按下键盘上的空格键按钮，你将进入到\n测试页面，超过一定时间则自动跳入测试页面；\n2.作答完成后点击‘确定’按钮你将进入针对材料的评价页面;\n3.评价完毕后将进行数次数学运算，运算结束则进行下一篇材料的阅读。\n4.本实验将对您的阅读速度和答题正确率进行考察。若明白请点击‘开\n始实验’进行实验。')
        else:
            self.g_txt.WriteText(u'欢迎参加本实验，实验中你将看到数段文本材料，每个材料中都有一个带\n有灰色背景的词，阅读材料下方将呈现该词组的注释以帮你理解阅读。\n1.请在完成一遍阅读之后立即按下键盘上的空格键按钮，你将进入到测试\n页面，超过一定时间则自动跳入测试页面；\n2.作答完成后点击‘确定’按钮你将进入针对材料的评价页面；\n3.评价完毕后将进行数次数学运算，运算结束则进行下一篇材料的阅读；\n4.本实验将对您的阅读速度和答题正确率进行考察。若明白请点击‘开始\n实验’进行实验。')
        
        self.g_txt.EndLineSpacing()
        self.g_txt.EndFont()
        button = wx.Button(self.g_panel,-1,u'开始实验',pos = ((self.ww-150)/2,600),size = (150,50))
        button.Bind(wx.EVT_LEFT_DOWN,self.exp_start)
        f3 = open('eyedata\entermagtime%s_%s_%s.csv'%(self.cho,self.id,self.name),'a')
        f3.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'%('condition','id','name','gender','age','major','trialnum','matenum','starttime','stoptime','starttime','stoptime','starttime','stoptime','starttime','stoptime','starttime','stoptime','starttime','stoptime'))        
        f3.close()
        
            
    def exp_start(self,event):
        #iViewXAPI.iV_Disconnect()
        #os.system('python pracexp.py')
        #iViewXAPI.iV_Connect(c_char_p('127.0.0.1'), c_int(4444), c_char_p('127.0.0.1'), c_int(5555))
        
        
        self.g_panel.Destroy()
#decide which condition to be in        
        if self.cho == 0 :
            self.l = self.mlist#range(36)
            random.shuffle(self.l)
            #creat a random list for trial sequence to present material text
            #i.e the first trial was i=0,and the first element in list _l[0]= 5,then show N.5 material
            self.condition1()
        elif self.cho == 1 :
            self.l = self.mlist#range(36)
            random.shuffle(self.l)
            self.condition2()
            
    def condition1(self):
        #iViewXAPI.iV_Connect(c_char_p('127.0.0.1'), c_int(4444), c_char_p('127.0.0.1'), c_int(5555))
        if self.i == 0:
            self.Focus_panel = wx.Panel(self,-1,size = wx.DisplaySize())
            s = str(u'请注视红色圆圈内的十字开始实验')
            label = wx.StaticText(self.Focus_panel,-1,s,pos = ((self.ww-400)/2,220),size=(50,30))
            font = wx.Font(20,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
            label.SetFont(font)
            imag = wx.Image('zhunbei.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            focu = wx.StaticBitmap(self.Focus_panel,-1,imag,pos = ((self.ww-50)/2,330))
#            font = wx.Font(48,wx.DEFAULT,wx.NORMAL,wx.BOLD)
#            focu = wx.StaticText(self.Focus_panel,-1,'+',pos = ((self.ww-50)/2,300),size = (60,60),style=wx.ALIGN_CENTER)
#            focu.SetFont(font)        
#            focu.SetForegroundColour('red')
#            focu.SetBackgroundColour('white')        
            
            focu.Bind(wx.EVT_ENTER_WINDOW,self.imag)
            self.Focus_panel.Refresh()
        else:
            self.Focus_panel.Show()
    def imag(self,event):
        time.sleep(0.5)
        self.Focus_panel.Hide()
        self.r_condition1()     
    def r_condition1(self):
        #---- start recording  from iViewX
        a = self.l[int(self.i)]
        iViewXAPI.iV_ContinueRecording('%s'%a)
        
        self.con_time = time.clock()         
        self.c1_panel = wx.Panel(self,-1,size = wx.DisplaySize())
        #here to get material Text
        
        
        f0 = open('data\%s_%s_%s.csv'%(self.cho,self.id,self.name),'a')
        f0.write('%d,'%self.trialnum)
        self.trialnum += 1
        s = str('%d,'%a)
        f0.write(s)
        f0.close()
        
        f = open('mate\%d.txt' % a,'r')
        self.t = f.read()
        f.close()
        #here to get hint Text
        f2 = open('mate\%d_h.txt' % a,'r')
        self.h = f2.read()
        f2.close()
        print a
        #here to get gain the position of keyword
        self.keyword = self.dic[a]
        if self.t.find(self.keyword):
            index = self.t.index(self.keyword)    
        else:
            index = 0
        
        font = wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
        self.hanzikuan = 29
        self.hanzigao = 53
        self.x = index%28*self.hanzikuan#the width of a single Chinese character'''#x coordition in statictext
        self.y = index/28*self.hanzigao#the heigth of a single Chinese character
        
        a = len(self.t)
        b = a/56#28 character in a line  ,a char equal to 2 unit
        s = ''
        for i in range(b+1):#i ref to lines num
            s += (self.t[56*i:56*(i+1)] + '\n')
        s = s[0:len(s)-1]
        s = '%s'%s
        
        txt = rt.RichTextCtrl(self.c1_panel,pos = ((self.ww-850)/2,150),size = (850,530),style = rt.RE_MULTILINE|rt.RE_READONLY)#wx.TE_WORDWRAP  line wrap 
        txt.SetFont(font)
        txt.SetBackgroundColour('white')
        txt.BeginLineSpacing(17)
        txt.BeginFont(font)
        try:
            txt.WriteText(s)
        except UnicodeDecodeError,e:
            print e           
        txt.EndLineSpacing()
        txt.EndFont()
        txt.Bind(wx.EVT_LEFT_DOWN,self.nothing)
        txt.Bind(wx.EVT_RIGHT_DOWN,self.nothing)

        note2 = wx.StaticText(self.c1_panel,-1,'',pos = ((self.ww-369)/2-2,738),size = (373,92),style=wx.ALIGN_LEFT|wx.TE_WORDWRAP)
        note2.SetBackgroundColour('grey')
        note = wx.StaticText(self.c1_panel,-1,self.h,pos = ((self.ww-369)/2,740),size = (369,88),style=wx.ALIGN_LEFT|wx.TE_WORDWRAP) #(dic[n])
        font2 = wx.Font(16,wx.DEFAULT,wx.NORMAL,wx.NORMAL)        
        note.SetFont(font2)
        note.SetBackgroundColour('white') 
        #button = wx.StaticText(self.c1_panel,-1,' ',pos = (self.ww-220,750),size = (120,50))
        note.Bind(wx.EVT_KEY_DOWN,self.question)
        note.SetFocus()
        
        labe2 = wx.StaticText(self.c1_panel,-1,'%s' %self.keyword,pos = ((self.ww-850)/2+self.x+7,157+self.y),size = (len(self.keyword)*self.hanzikuan,self.hanzigao*2/3),style=wx.ALIGN_CENTER|wx.TE_WORDWRAP)
        labe2.SetBackgroundColour([190,190,190])
        labe2.SetFont(font)
#----------------------------------
#hide cursor
        self.c1_panel.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))
        txt.SetTextCursor(wx.StockCursor(wx.CURSOR_BLANK))
        note.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))
        note2.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))
        labe2.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))
        
        self.c1_panel.Refresh()

    def nothing(self,event):
        pass
        
    def condition2(self):
        #iViewXAPI.iV_Connect(c_char_p('127.0.0.1'), c_int(4444), c_char_p('127.0.0.1'), c_int(5555))
        self.tri = 1
        thread.start_new_thread(self.mouse2eye,(1,))
    
        if self.i == 0:
            self.Focus_panel = wx.Panel(self,-1,size = wx.DisplaySize())
            label = wx.StaticText(self.Focus_panel,-1,u'请注视圆圈内的十字以开始实验',pos = ((self.ww-400)/2,220),size=(100,100))
            font = wx.Font(20,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
            label.SetFont(font)
            imag = wx.Image('zhunbei.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            focu = wx.StaticBitmap(self.Focus_panel,-1,imag,pos = ((self.ww-50)/2,330))
#            font = wx.Font(48,wx.DEFAULT,wx.NORMAL,wx.BOLD)
#            focu = wx.StaticText(self.Focus_panel,-1,'+',pos = ((self.ww-50)/2,300),size = (60,60),style=wx.ALIGN_CENTER)
#            focu.SetFont(font)        
#            focu.SetForegroundColour('red')
#            focu.SetBackgroundColour('white')        
            
            focu.Bind(wx.EVT_ENTER_WINDOW,self.imag2)
        else:
            self.Focus_panel.Show()
        self.Focus_panel.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))
    def imag2(self,event):
        time.sleep(0.5)
        self.Focus_panel.Hide()
        self.r_condition2()    
    def r_condition2(self):
        a = self.l[int(self.i)]
        iViewXAPI.iV_ContinueRecording('%s'%a)######record ETdata
        
        self.con_time = time.clock()
        self.c2_panel = wx.Panel(self,-1,size = wx.DisplaySize())
        
        f0 = open('data\%s_%s_%s.csv'%(self.cho,self.id,self.name),'a')
        f0.write('%d,'%self.trialnum)
        self.trialnum += 1
        s = str('%d,'%a)
        f0.write(s)
        f0.close()
        
        f = open('mate\%d.txt' % a,'r')
        self.t = f.read()
        f.close()

        f2 = open('mate\%d_h.txt' % a,'r')
        self.h = f2.read()
        f2.close()        
        self.keyword = self.dic[a]
        if self.t.find(self.keyword):
            index = self.t.index(self.keyword)           
        else:
            index = 0  
            
        f3 = open('eyedata\entermagtime%s_%s_%s.csv'%(self.cho,self.id,self.name),'a')
        f3.write('\n%s,%s,%s,%s,%s,%s,%d,%d,'%(self.cho,self.id,self.name,self.gender,self.birthday,self.magor,(self.trialnum - 1),a))        
        f3.close()
        
        font = wx.Font(22,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
        self.hanzikuan = 29
        self.hanzigao = 50
        self.x = index%28*self.hanzikuan
        self.y = index/28*self.hanzigao
        
        a = len(self.t)
        b = a/56
        s = ''
        for i in range(b+1):#
            s += (self.t[56*i:56*(i+1)] + '\n')
        s = s[0:len(s)-1]
       
        #make up the keyword label
        #labe = wx.StaticText(self.c2_panel,-1,pos = (165+self.x,87+self.y-self.hanzigao/4),size = (len(self.keyword)*self.hanzikuan,self.hanzigao*2/3+self.hanzigao/2))
        labe = wx.StaticText(self.c2_panel,-1,'%s' %self.keyword,pos = ((self.ww-850)/2+self.x+7,157+self.y-10),size = (len(self.keyword)*self.hanzikuan,self.hanzigao*2/3+25),style=wx.ALIGN_CENTER|wx.TE_WORDWRAP)
        labe.Bind(wx.EVT_ENTER_WINDOW,self.enterlabel)
        labe.Bind(wx.EVT_LEAVE_WINDOW,self.leavelabel)
        
        self.note2 = wx.StaticText(self.c2_panel,-1,pos = ((self.ww-850)/2+9+self.x+len(self.keyword)*self.hanzikuan/2,62+self.y),size = (376,95))
        self.note2.Bind(wx.EVT_ENTER_WINDOW,self.entermag)
        self.note2.Bind(wx.EVT_LEAVE_WINDOW,self.leavemag)
        self.note2.Show(False)
        
        txt = rt.RichTextCtrl(self.c2_panel,pos = ((self.ww-850)/2,150),size = (850,530),style = rt.RE_MULTILINE|rt.RE_READONLY)#
        txt.SetBackgroundColour('white')
        txt.BeginLineSpacing(20)
        txt.BeginFont(font)
        try:
            txt.WriteText(str(s))
        except UnicodeDecodeError,e:
            print e   
        txt.EndLineSpacing()
        txt.EndFont()

        txt.Bind(wx.EVT_LEFT_DOWN,self.nothing)
        txt.Bind(wx.EVT_RIGHT_DOWN,self.nothing)
        
        #here is another keyword label .one for show ,one for trigger event
        #labe2 = wx.StaticText(self.c2_panel,-1,'%s' %self.keyword,pos = (165+self.x,87+self.y),size = (len(self.keyword)*self.hanzikuan,self.hanzigao*2/3),style=wx.ALIGN_CENTER|wx.TE_WORDWRAP)
        labe2 = wx.StaticText(self.c2_panel,-1,'%s' %self.keyword,pos = ((self.ww-850)/2+self.x+7,157+self.y),size = (len(self.keyword)*self.hanzikuan,self.hanzigao*2/3+5),style=wx.ALIGN_CENTER|wx.TE_WORDWRAP)
        labe2.SetBackgroundColour([190,190,190])
        labe2.SetFont(font)
        button = wx.StaticText(self.c2_panel,-1,' ',pos = (self.ww-220,750),size = (120,50))
        button.Bind(wx.EVT_KEY_DOWN,self.question)
        button.SetFocus()
        

#---------------
# hide cursor
        self.c2_panel.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))
        txt.SetTextCursor(wx.StockCursor(wx.CURSOR_BLANK))
        labe.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))
        
        self.mag()
        self.magframe.Show(False)
        self.magframe.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))
        self.c2_panel.Refresh()
        #---- stop recording from iViewX
        #iViewXAPI.iV_StopRecording()
        
        #outputfile = path + filename
        #res = iViewXAPI.iV_SaveData(str('data\%s_%s_%s'%(self.cho,self.id,self.name), str(description), str(user), 1)
        #print 'iV_SaveData' + str(res)
        #print "data saved to: " + outputfile
        #iViewXAPI.iV_Disconnect()
        
    def mag(self):
        self.magframe = wx.Panel(self.c2_panel,-1,pos = ((self.ww-850)/2+9+self.x+len(self.keyword)*self.hanzikuan/2,62+self.y),size = (376,95))
        font = wx.Font(16,wx.DEFAULT,wx.NORMAL,wx.NORMAL) 
        panel = wx.Panel(self.magframe,-1,pos = (2,2),size = (376,95))
        panel.SetBackgroundColour('grey')
        self.note = wx.StaticText(panel,-1,self.h,pos = (2,2),size = (369,88),style= wx.ALIGN_LEFT|wx.TE_WORDWRAP)
        self.note.SetBackgroundColour('white')
        self.note.SetFont(font)
        self.magframe.Refresh()
        
        
        
    def entermag(self,event):
        self.tentermag = time.time()
        self.magtimebegin = time.time()
        self.entermagtri = 1
        f = open('eyedata\entermagtime%s_%s_%s.csv'%(self.cho,self.id,self.name),'a')#record time stamp of every entermag event
        f.write(str('%s,'%self.tentermag))
        f.close()

    def leavemag(self,event):
        self.tleavemag = time.time()
#        f = open('eyedata\entermagtime%s_%s_%s.csv'%(self.cho,self.id,self.name),'a')#record time stamp of every entermag event
#        f.write(str('%s,' %self.tleavemag))
#        f.close()
        d = thread.start_new_thread(self.timer4,())
        
        

    def enterlabel(self,event):
        self.tenterlabel = time.time()
        b = thread.start_new_thread(self.timer2,())
        a = thread.start_new_thread(self.timer1,())
        

    def leavelabel(self,event):
        self.tleavelabel = time.time()
        self.leavelabeltri = 1
        c = thread.start_new_thread(self.timer3,())
        

    def timer1(self):
        time.sleep(0.5)
        if self.tri1 == 1:
            try:
                self.magframe.Show()
                self.note2.Show()
            except wx._core.PyDeadObjectError:
                pass
            #self.magtimebegin = time.time()
            self.tri1 = 0

    def timer2(self):
        time.sleep(0.45)
        t = self.tleavelabel - self.tenterlabel
        self.tleavelabel = 0
        self.tenterlabel = 0
        if t>0 and t<0.5:
            pass
        else:
            self.tri1 = 1

    
    def timer3(self):
        time.sleep(0.95)
        if self.entermagtri == 1:
            self.entermagtri = 0
        else:
            self.magtimeend = time.time()
            a = self.magtimeend - self.magtimebegin
            
            if a < 1000 and self.magtimebegin > 0:
                self.magtime.append(a)
                
            self.magtimeend = 0
            self.magtimebegin = 0
            
            try:
                self.magframe.Show(False)
                self.note2.Show(False)
            except wx._core.PyDeadObjectError:
                pass
        
    def timer4(self):
        time.sleep(0.4)
        t = self.tentermag - self.tleavemag
        if t>0 and t<0.4:
            pass
        else:
            self.magtimeend = time.time()
            f = open('eyedata\entermagtime%s_%s_%s.csv'%(self.cho,self.id,self.name),'a')#record time stamp of every entermag event
            f.write(str('%s,' %self.magtimeend))
            f.close()
            a = self.magtimeend - self.magtimebegin
            if a > 0.9 and self.magtimebegin > 0:
                self.magtime.append(a)
                
            self.magtimeend = 0
            self.magtimebegin = 0
            try:
                self.magframe.Show(False)
                self.note2.Show(False)
            except wx._core.PyDeadObjectError:
                pass
        
        
    def question(self,event):
                #---- stop recording from iViewX
        iViewXAPI.iV_PauseRecording()

        
        self.tri = 0#stop the mouse2eye proceeding

        
        #gain time for this circle
        self.que_t = time.clock()
        t = self.que_t - self.con_time #reading time 
        a = self.l[int(self.i)]
        self.readtime.append('%d_%f'%(a,t))
        
        f = open('data\%s_%s_%s.csv'%(self.cho,self.id,self.name),'a')
        s = str('%s,'%t)
        f.write(s)
        f.close()
        #gain THE quetion 
        if self.cho == 0:
            self.c1_panel.Destroy()
        else:
            self.c2_panel.Destroy()
            
        a = self.l[int(self.i)]
        f3 = open('mate\%d_q.txt' % a,'r')
        title = f3.readline()
        cho1 = f3.readline()
        cho2 = f3.readline()
        cho3 = f3.readline()
        cho = ['']
        cho.append(cho1)
        cho.append(cho2)
        cho.append(cho3)
        f3.close()
        
        self.q_panel = wx.Panel(self,-1,size = wx.DisplaySize())
        font = wx.Font(18,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
        self.answer = wx.RadioBox(self.q_panel, -1,title, ((self.ww-150)/2-200, 280), (700,120),cho, 1, wx.RA_SPECIFY_COLS)
        self.answer.SetFont(font)
        button = wx.Button(self.q_panel,-1,u'确定',pos = ((self.ww-150)/2,550),size = (150,50))
        button.Bind(wx.EVT_LEFT_DOWN,self.pingjia)
        
    def pingjia(self,event):
        self.pin_t = time.clock()
        t = self.pin_t-self.que_t
        a = self.l[int(self.i)]
        #self.answertime.append('%d_%f'%(a,t)) 
        #print 'answertime',self.answertime
        answer = self.answer.GetSelection()        
        f = open('data\%s_%s_%s.csv'%(self.cho,self.id,self.name),'a')
        f.write(str('%s,'%answer))
        f.write(str('%f,'%t))
        f.close()

        
        self.q_panel.Destroy()
        self.p_panel = wx.Panel(self,-1,size = wx.DisplaySize())
        t = wx.StaticText(self.p_panel,-1,u'请根据自己的真实想法作答',pos = (400,120),size = (600,50),style=wx.ALIGN_LEFT|wx.TE_WORDWRAP)
        font1 = wx.Font(20,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
        t.SetFont(font1)
        
        font = wx.Font(18,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
        cho = ['','1      ','2      ','3      ','4      ','5      ']
        t1 = wx.StaticText(self.p_panel,-1,u'一、以上文本材料对你来说是',pos = (230,230),size = (600,50),style=wx.ALIGN_LEFT|wx.TE_WORDWRAP)
        self.pj1 = wx.RadioBox(self.p_panel,-1,u'1-代表很简单，5-代表很难',(230,280),(330,50),cho,1, wx.RA_SPECIFY_ROWS)
        t2 = wx.StaticText(self.p_panel,-1,u'二、以上注释信息对你理解文本是否有帮助',pos = (770,230),size = (600,50),style=wx.ALIGN_LEFT|wx.TE_WORDWRAP)
        self.pj2 = wx.RadioBox(self.p_panel,-1,u'1-代表完全没有帮助，5-代表很有帮助',(770,280),(400,50),cho, 6, wx.RA_SPECIFY_COLS)
        t3 = wx.StaticText(self.p_panel,-1,u'三、你在作答时的选择依据来源于',pos = (230,450),size = (400,50),style=wx.ALIGN_LEFT|wx.TE_WORDWRAP)
        cho2 = ['',u'对以上文本材料的理解 ',u'自身原有经验   ',u'猜测 ']
        self.pj3 = wx.RadioBox(self.p_panel,-1,u'',(230,500),(400,50),cho2,1, wx.RA_SPECIFY_COLS)
        t4 = wx.StaticText(self.p_panel,-1,u'四、以上材料所述内容对你来说的熟悉度是',pos = (770,450),size = (600,50),style=wx.ALIGN_LEFT|wx.TE_WORDWRAP)
        self.pj4 = wx.RadioBox(self.p_panel,-1,u'1-代表非常陌生，5-代表非常熟悉',(770,500),(400,50),cho, 6, wx.RA_SPECIFY_COLS)
        
        t1.SetFont(font)
        t2.SetFont(font)
        t3.SetFont(font)
        t4.SetFont(font)
        font2 = wx.Font(16,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
        self.pj1.SetFont(font2)
        self.pj2.SetFont(font2)
        self.pj3.SetFont(font2)
        self.pj4.SetFont(font2)

        button = wx.Button(self.p_panel,-1,u'确定,下一个',pos = ((self.ww-150)/2,650),size = (150,50))
        button.Bind(wx.EVT_LEFT_DOWN,self.ganrao)
        self.p_panel.Refresh()
    
#disturb for a break ，minus three operation 
    def ganrao(self,event):
        
        self.gan_t = time.clock()
        t = self.gan_t - self.pin_t
        a = self.l[int(self.i)]
#        self.pinjiatime.append('%d_%f'%(a,t))         
#        print 'pinjiatime',self.pinjiatime
        self.p1 = self.pj1.GetSelection()
        self.p2 = self.pj2.GetSelection()
        self.p3 = self.pj3.GetSelection()
        self.p4 = self.pj4.GetSelection()
#        self.pingjiaselect.append('%d_%s_%s_%s'%(a,str(self.p1),str(self.p2),str(self.p3))) 
#        print 'pingjiaselect',self.pingjiaselect
        f = open('data\%s_%s_%s.csv'%(self.cho,self.id,self.name),'a')

        f.write('%d,'%self.p1)
        f.write('%d,'%self.p2)
        f.write('%d,'%self.p3)
        f.write('%d,'%self.p4)
        f.write(str('%f,'%t))
        f.write(str('%f,'%sum(self.magtime)))
        a = len(self.magtime)
        f.write(str('%f,\n'%a))
        f.write('1,')
        for i in self.info:
            f.write('%s,'%i)
        f.close() 
        self.magtime = []
        
        self.p_panel.Destroy()
        self.ganrao_panel = wx.Panel(self,-1,size = wx.DisplaySize())
        self.lnum = random.randint(500,600)
        font = wx.Font(35,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
        self.leftnum = wx.StaticText(self.ganrao_panel,-1,'%s - 3 = '%self.lnum,pos = ((self.ww-280)/2,350),size = (180,50))
        self.leftnum.SetFont(font)
        a = self.lnum - 3
        b = random.randint(480,580)
        c = random.randint(480,580)
        d = random.randint(480,580)
        l = [a,b,c,d]
        random.shuffle(l)        
        
        an1 = wx.StaticText(self.ganrao_panel,-1,'%s'%l[0],pos = ((self.ww-280)/2+260,300),size = (80,50))
        an2 = wx.StaticText(self.ganrao_panel,-1,'%s'%l[1],pos = ((self.ww-280)/2+260,400),size = (80,50))
        an3 = wx.StaticText(self.ganrao_panel,-1,'%s'%l[2],pos = ((self.ww-280)/2+410,300),size = (80,50))
        an4 = wx.StaticText(self.ganrao_panel,-1,'%s'%l[3],pos = ((self.ww-280)/2+410,400),size = (80,50))
        an1.SetBackgroundColour('grey')
        an2.SetBackgroundColour('grey')
        an3.SetBackgroundColour('grey')
        an4.SetBackgroundColour('grey')
        an1.SetFont(font)
        an2.SetFont(font)
        an3.SetFont(font)
        an4.SetFont(font)
        an1.Bind(wx.EVT_LEFT_DOWN,self.circle)
        an2.Bind(wx.EVT_LEFT_DOWN,self.circle)
        an3.Bind(wx.EVT_LEFT_DOWN,self.circle)
        an4.Bind(wx.EVT_LEFT_DOWN,self.circle)        
             
#        self.rightnum = wx.TextCtrl(self.ganrao_panel,-1,'',pos = ((self.ww-280)/2+260,350),size = (100,50),style = wx.TE_PROCESS_ENTER)
#        font = wx.Font(35,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
#        self.leftnum.SetFont(font)
#        self.rightnum.SetFont(font)
#        self.rightnum.SetFocus()
        self.cir = 0
#        self.rightnum.Bind(wx.EVT_TEXT_ENTER,self.circle)
    def circle(self,event):
        if self.cir<5:
            self.cir += 1
            self.lnum = self.lnum-3
            font = wx.Font(35,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
            self.leftnum = wx.StaticText(self.ganrao_panel,-1,'%s - 3 = '%self.lnum,pos = ((self.ww-280)/2,350),size = (180,50))       
            self.leftnum.SetFont(font)
                
            a = self.lnum - 3
            b = random.randint(480,580)
            c = random.randint(480,580)
            d = random.randint(480,580)
            l = [a,b,c,d]
            random.shuffle(l)        
        
            an1 = wx.StaticText(self.ganrao_panel,-1,'%s'%l[0],pos = ((self.ww-280)/2+260,300),size = (80,50))
            an2 = wx.StaticText(self.ganrao_panel,-1,'%s'%l[1],pos = ((self.ww-280)/2+260,400),size = (80,50))
            an3 = wx.StaticText(self.ganrao_panel,-1,'%s'%l[2],pos = ((self.ww-280)/2+410,300),size = (80,50))
            an4 = wx.StaticText(self.ganrao_panel,-1,'%s'%l[3],pos = ((self.ww-280)/2+410,400),size = (80,50))
            an1.SetBackgroundColour('grey')
            an2.SetBackgroundColour('grey')
            an3.SetBackgroundColour('grey')
            an4.SetBackgroundColour('grey')
            an1.SetFont(font)
            an2.SetFont(font)
            an3.SetFont(font)
            an4.SetFont(font)
            an1.Bind(wx.EVT_LEFT_DOWN,self.circle)
            an2.Bind(wx.EVT_LEFT_DOWN,self.circle)
            an3.Bind(wx.EVT_LEFT_DOWN,self.circle)
            an4.Bind(wx.EVT_LEFT_DOWN,self.circle) 
        
        else:
            self.nextone()
            self.ganrao_panel.Destroy()
            
    def nextone(self):
        self.i += 1
        if self.i < 20:
            if self.cho == 0:
                self.condition1()
            else:
                self.condition2()
        else:
            self.thanku()
            
    def thanku(self):
        #结束页
        iViewXAPI.iV_StopRecording()
        path = os.getcwd() + "\\eyedata\\"
        filename = '%s_%s_%s'%(self.cho,self.id,self.name)
        outputfile = path + filename + '.idf'
        iViewXAPI.iV_SaveData(str(outputfile),str(self.cho), str(self.name), 1)

        iViewXAPI.iV_Disconnect()

        self.t_panel = wx.Panel(self,-1,size = wx.DisplaySize())
        t_txt = wx.StaticText(self.t_panel,-1,u'谢谢参与本实验，请联系主试',pos = ((self.ww-500)/2,250),size = (600,100),style=wx.ALIGN_LEFT|wx.TE_WORDWRAP)
        font = wx.Font(28,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
        t_txt.SetFont(font)
        
   
if __name__=='__main__':    
    app = wx.App()
    frame = main_page()
    frame.Show()
    app.MainLoop()


