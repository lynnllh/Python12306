# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 10:50:09 2018

@author: Administrator
"""

import urllib.request
import re
import ssl
import urllib.parse
import http.cookiejar
import datetime
import time
import os
import random
import socket

class Ticket():
 #   headers='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
    headers = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]
    _startName=''
    _toName=''
    _startCode=''
    _toCode=''
    _isStudent=''
    _date=''
    student='0X00'
    adult='ADULT'
    _ticketType=''
    _alltrainno=[]
    _trainmap={}
    _userName=''
    _passWord=''
    _thisCode=''
    _thisSeat=''
    _secretStr=''
    _train_no=''
    _leftTicketStr=''
    _fromStationTelecode=''
    _toStationTelecode=''
    _train_location=''
    _token=''
    _key=''
    _orderid=''
    seatmargin={'9':'','M':'','O':'','1':'','6':'','4':'','3':''}
    seatposition={'9':32,'M':31,'O':30,'1':29,'6':21,'4':23,'3':28}
    name='***'
    passagerid='***'
    mobile='***'
    studentflag={'ADULT':'1','0X00':'3'}
##-------------------------
    def __init__(self):
        pass
    def __del__(self):
        pass
    def UrlGet(self,url,outtime):
        try:
            req=urllib.request.Request(url)
            req.add_header('User-Agent', random.choice(self.headers))
            reqdata=urllib.request.urlopen(req,timeout=outtime).read().decode('utf-8','ignore')
            return reqdata
        except:
            print('GET请求尝试重新连接，等待3s')
            time.sleep(3)
            return self.UrlGet(url,outtime)
               
    def UrlPost2(self,url,outtime,data):
        try:
            req=urllib.request.Request(url,data)
            req.add_header('User-Agent', random.choice(self.headers))
            reqdata=urllib.request.urlopen(req,timeout=outtime).read().decode('utf-8','ignore')
            return reqdata
        except:
            print('POST请求尝试重新连接，等待3s')
            time.sleep(3)
            return self.UrlPost2(url,outtime,data)
            
    def UrlPost(self,url,outtime,data):
        try:
            postdata=urllib.parse.urlencode(data).encode('utf-8')
            req=urllib.request.Request(url,postdata)
            req.add_header('User-Agent', random.choice(self.headers))
            reqdata=urllib.request.urlopen(req,timeout=outtime).read().decode('utf-8','ignore')
            return reqdata
        except:
            print('POST请求尝试重新连接，等待3s')
            time.sleep(3)
            return self.UrlPost(url,outtime,data)
            
    def ResultCheckout(self,data,message,code):
        pat1='"result_message":"(.*?)"'
        pat2='"result_code":.?(\d)'
        result_message=re.compile(pat1).findall(data)[0]
        result_code=re.compile(pat2).findall(data)[0]
        print('result_message='+result_message)
        print('result_code='+result_code)
        if (result_message==message and result_code==code):
            return True
        else:
            return False
            
    def StatusCheckout(self,data,status,submitstatus):
        pat1='"status":(.*?),'
        pat2='"submitStatus":(.*?),'
        result_status=re.compile(pat1).findall(data)[0]
        result_submitstatus=re.compile(pat2).findall(data)[0]
        if (result_status==status and result_submitstatus==submitstatus):
            return True
        else:
            return False
            
    def StatusCheckout2(self,data,status):
        pat1='"status":(.*?),'
        result_status=re.compile(pat1).findall(data)[0]
        if (result_status==status):
            return True
        else:
            return False
            
    def SearchICAO(self,str):
        dir=os.getcwd()
        f=open(dir+"\\ICAO.txt","r",encoding='UTF-8')
        line=f.readline()
        while line:
            if line.split()[1]==str:
                f.close
                return line.split()[0]
            else:
                line=f.readline()
        f.close
        return False
        
    def IsChinese(self,s):
      if s >= u'\u4e00' and s<=u'\u9fa5':
        return True
      else:
        return False
        
    def GetXY(self,pic):
        if(pic==1):
            xy=(35,45)
        if(pic==2):
            xy=(112,45)
        if(pic==3):
            xy=(173,45)
        if(pic==4):
            xy=(253,45)        
        if(pic==5):
            xy=(35,114)
        if(pic==6):
            xy=(112,114)
        if(pic==7):
            xy=(173,114)
        if(pic==8):
            xy=(253,114)
        return xy
    
    @property
    def start(self):
        return self._startName
    @start.setter
    def start(self,value):
        startcode=self.SearchICAO(value)
        if (startcode):
            self._startName=value
            self._startCode=startcode
        else:
            raise ValueError('无此站名')
            
    @property
    def to(self):
        return self._toName
    @to.setter
    def to(self,value):
        tocode=self.SearchICAO(value)
        if (tocode):
            self._toName=value
            self._toCode=tocode
        else:
            raise ValueError('无此站名')
            
    @property
    def isStudent(self):
        return self._isStudent
    @isStudent.setter
    def isStudent(self,value):
        if (value=='0' or value==0):
            self._isStudent=0
            self._ticketType=self.adult
        else:
            self._isStudent=1
            self._ticketType=self.student
            
    @property
    def date(self):
        return self._date
    @date.setter
    def date(self,value):
        try:
            time.strptime(value,'%Y-%m-%d')
            self._date=value
        except:
            raise ValueError('输入日期格式不合法')
    
    @property
    def tickettype(self):
        return self._ticketType
    
    @property
    def username(self):
        return self._userName
    @username.setter
    def username(self,value):
        self._userName=value
        
    @property
    def password(self):
        return self._passWord
    @password.setter
    def password(self,value):
        self._passWord=value
        
    @property
    def thiscode(self):
        return self._thisCode
    @thiscode.setter
    def thiscode(self,value):
        self._thisCode=value.upper()
        
    @property
    def thisseat(self):
        return self._thisSeat
    @thisseat.setter
    def thisseat(self,value):
        self._thisSeat=value.upper()
    
    #---------------------------------------
    def setssl(self):
        ssl._create_default_https_context=ssl._create_unverified_context
        
    def TicketLeft(self,timeout):
        url='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date='+self._date+'&leftTicketDTO.from_station='+self._startCode+'&leftTicketDTO.to_station='+self._toCode+'&purpose_codes='+self._ticketType
        reqdata=self.UrlGet(url,timeout)
        try:
            pat='"result":\[(.*?)\]'
            rst01=re.compile(pat).findall(reqdata)[0]
            self._alltrainno=rst01.split(',')
            pat2='"map":({.*?})'
            self._trainmap=eval(re.compile(pat2).findall(reqdata)[0])
        except:
            print('TicketLeft请求失败，尝试重新连接，等待3s')
            time.sleep(3)
            return self.TicketLeft(timeout)
        
    def PrintTicketLeft(self):
        print('{:<8} {:<6} {:<6} {:<6} {:<6} {:<6} {:<7} {:<7} {:<6} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8}'.format('车次','出发站名','到达站名','出发时间','到达时间','商务特等','一等座','二等座','高级软卧','软卧','动卧','硬卧','软座','硬座','无座'))
        for i in range(0,len(self._alltrainno)):
            try:
                thischeci=self._alltrainno[i].split('|')
                #[3]---code
                code=thischeci[3]
                #[6]---fromname
                fromname=thischeci[6]
                fromname=self._trainmap[fromname]
                #[7]---toname
                toname=thischeci[7]
                toname=self._trainmap[toname]
                #[8]---stime
                stime=thischeci[8]
                #[9]---atime
                atime=thischeci[9]
                #[21]---高级软卧
                gjrw=thischeci[21]
                #[23]---软卧
                rw=thischeci[23]
                #[24]---软座
                rz=thischeci[24]
                #[26]---无座
                wz=thischeci[26]
                #[28]---硬卧
                yw=thischeci[28]
                #[29]---硬座
                yz=thischeci[29]
                #[30]---二等座
                edz=thischeci[30]
                #[31]---一等座
                ydz=thischeci[31]
                #[32]---特等座
                tdz=thischeci[32]
                #[33]---动卧
                dw=thischeci[33] 
                print('{out:<{len}}'.format(out=code,len=10-len(code.encode('GBK'))+len(code)),end=' ')
                print('{out:<{len}}'.format(out=fromname,len=10-len(fromname.encode('GBK'))+len(fromname)),end=' ')
                print('{out:<{len}}'.format(out=toname,len=10-len(toname.encode('GBK'))+len(toname)),end=' ')
                print('{out:<{len}}'.format(out=stime,len=10-len(stime.encode('GBK'))+len(stime)),end=' ')
                print('{out:<{len}}'.format(out=atime,len=10-len(atime.encode('GBK'))+len(atime)),end=' ')
                print('{out:<{len}}'.format(out=str(tdz),len=10-len(str(tdz).encode('GBK'))+len(str(tdz))),end=' ')
                print('{out:<{len}}'.format(out=str(ydz),len=10-len(str(ydz).encode('GBK'))+len(str(ydz))),end=' ')
                print('{out:<{len}}'.format(out=str(edz),len=10-len(str(edz).encode('GBK'))+len(str(edz))),end=' ')
                print('{out:<{len}}'.format(out=str(gjrw),len=10-len(str(gjrw).encode('GBK'))+len(str(gjrw))),end=' ')
                print('{out:<{len}}'.format(out=str(rw),len=10-len(str(rw).encode('GBK'))+len(str(rw))),end=' ')
                print('{out:<{len}}'.format(out=str(dw),len=10-len(str(dw).encode('GBK'))+len(str(dw))),end=' ')
                print('{out:<{len}}'.format(out=str(yw),len=10-len(str(yw).encode('GBK'))+len(str(yw))),end=' ')
                print('{out:<{len}}'.format(out=str(rz),len=10-len(str(rz).encode('GBK'))+len(str(rz))),end=' ')
                print('{out:<{len}}'.format(out=str(yz),len=10-len(str(yz).encode('GBK'))+len(str(yz))),end=' ')
                print('{out:<{len}}'.format(out=str(wz),len=10-len(str(wz).encode('GBK'))+len(str(wz))))
            except Exception as err:
                pass
    def CookieProcess(self):
        cjar=http.cookiejar.CookieJar()
        opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
        urllib.request.install_opener(opener)
    
    def Login(self,timeout):
        print('正在登陆...')
        url="https://kyfw.12306.cn/otn/login/init"
        self.UrlGet(url,timeout)
        time.sleep(0.5)
        if (os.path.exists('D:\\tmp')==False):
            os.mkdir('D:\\tmp')
        yzmurl='https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'
        try:
            urllib.request.urlretrieve(yzmurl,'D:\\tmp\\12306_yzm.png')
            
        except:
            print('验证码获取超时，尝试重新连接，等待3s')
            time.sleep(3)
            return self.Login(timeout)
        yzm=input('请输入验证码，输入第几张图片即可\n')
        allpic=re.compile('\d').findall(yzm)
        allpicpos=''
        for i in allpic:
            thisxy=self.GetXY(int(i))
            for j in thisxy:
                allpicpos=allpicpos+str(j)+','
        allpicpos2=re.compile('(.*?).$').findall(allpicpos)[0]
        #print(allpicpos2)
        #post验证码验证
        time.sleep(0.5)
        yzmposturl='https://kyfw.12306.cn/passport/captcha/captcha-check'
        postdata={'answer':allpicpos2,'rand':'sjrand','login_site':'E'}
        reqdata=self.UrlPost(yzmposturl,timeout,postdata)
#        print(reqdata)
        if (self.ResultCheckout(reqdata,'验证码校验成功','4')):
            print('验证码校验成功')
        else:
            print('验证码校验失败，尝试重新连接，等待3s')
            time.sleep(3)
            return self.Login(timeout)
        time.sleep(1)
        loginposturl='https://kyfw.12306.cn/passport/web/login'
        postdata={'username':self._userName,'password':self._passWord,'appid':'otn'}
        reqdata=self.UrlPost(loginposturl,timeout,postdata)
        print(reqdata)
        if (self.ResultCheckout(reqdata,'登录成功','0')):
            print('账户及密码验证成功')
        else:
            print('账户及密码验证失败，尝试重新连接，等待3s')
            time.sleep(3)
            return self.Login(timeout)
        time.sleep(1)
        loginposturl2='https://kyfw.12306.cn/otn/login/userLogin'
        postdata={'_json_att':''}
        self.UrlPost(loginposturl2,timeout,postdata)
        loginposturl3="https://kyfw.12306.cn/passport/web/auth/uamtk"
        postdata={'appid':'otn'}
        reqdata=self.UrlPost(loginposturl3,timeout,postdata)
        if (self.ResultCheckout(reqdata,'验证通过','0')):
            print('uamtk验证通过')
        else:
            print('uamtk验证失败，尝试重新连接，等待3s')
            time.sleep(3)
            return self.Login(timeout)
        pat_req2='"newapptk":"(.*?)"'
        tk=re.compile(pat_req2,re.S).findall(reqdata)[0]
        time.sleep(1)
        loginposturl4="https://kyfw.12306.cn/otn/uamauthclient"
        postdata={'tk':tk}
        reqdata=self.UrlPost(loginposturl4,timeout,postdata)
        if (self.ResultCheckout(reqdata,'验证通过','0')):
            print('uamauthclient验证通过')
        else:
            print('uamauthclient验证失败，尝试重新连接，等待3s')
            time.sleep(3)
            return self.Login(timeout)
        time.sleep(1)
        centerurl='https://kyfw.12306.cn/otn/index/initMy12306'
        self.UrlGet(centerurl,timeout)
        print('登陆成功')
        
    def SearchLeftTicket(self,timeout):
        self.TicketLeft(timeout)
        for i in range(0,len(self._alltrainno)):
            try:
                thischeci=self._alltrainno[i].split('|')
#                print(thischeci)
                #[3]---code
                code=thischeci[3]
#                print(self._thisCode,code, self._thisCode == code)
                if (self._thisCode == code):
                    self._secretStr=thischeci[0].replace('"','')
                    self.seatmargin[self._thisSeat]=thischeci[self.seatposition[self._thisSeat]]
                    break
            except Exception as err:
                pass
        if (self._secretStr=='' or self.seatmargin[self._thisSeat]=='无'):
            print('当前无票，继续监控...')
            return False
        else:
            return True
                        
    def OrderTicket(self,timeout):
        initurl='https://kyfw.12306.cn/otn/leftTicket/init'
        self.UrlGet(initurl,timeout)
        time.sleep(1)
        while not self.SearchLeftTicket(timeout):
            time.sleep(1)
        time.sleep(0.5)
        print('正在订票中...')
        checkurl='https://kyfw.12306.cn/otn/login/checkUser'
        postdata={'_json_att':''}
        reqdata=self.UrlPost(checkurl,timeout,postdata)
        if (self.StatusCheckout2(reqdata,'true')):
            print('checkUser验证通过')
        else:
            print('checkUser验证失败，尝试重新连接，等待3s')
            time.sleep(3)
            return self.OrderTicket(timeout)
            
        backdate=datetime.datetime.now()
        backdate=backdate.strftime('%Y-%m-%d')
        time.sleep(0.5)
        submiturl='https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        postdata={'secretStr':self._secretStr,'train_date':self._date,'back_train_date':backdate,'tour_flag':'dc','purpose_codes':self._ticketType,'query_from_station_name':self._startName,'query_to_station_name':self._toName}
        submitdata=urllib.parse.urlencode(postdata)
        submitdata2=submitdata.replace('%25','%')
        submitdata3=submitdata2.encode('utf-8')
        reqdata=self.UrlPost2(submiturl,timeout,submitdata3)
        if (self.StatusCheckout2(reqdata,'true')):
            print('submitOrderRequest验证通过')
        else:
            print('submitOrderRequest验证失败，尝试重新连接，等待3s')
            time.sleep(3)
            return self.OrderTicket(timeout)
        
        time.sleep(0.5)    
        initdcurl='https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        postdata={'_json_att':''}
        reqdata=self.UrlPost(initdcurl,timeout,postdata)
        #获取train_no、leftTicketStr、fromStationTelecode、toStationTelecode、train_location
        train_no_pat="'train_no':'(.*?)'"
        leftTicketStr_pat="'leftTicketStr':'(.*?)'"
        fromStationTelecode_pat="'from_station_telecode':'(.*?)'"
        toStationTelecode_pat="'to_station_telecode':'(.*?)'"
        train_location_pat="'train_location':'(.*?)'"
        pattoken="var globalRepeatSubmitToken.*?'(.*?)'"
        patkey="'key_check_isChange':'(.*?)'"
#        pattrain_location="'tour_flag':'dc','train_location':'(.*?)'"
        try:
            train_no_all=re.compile(train_no_pat).findall(reqdata)
            if (len(train_no_all)!=0):
                self._train_no=train_no_all[0]
            else:
                raise Exception('train_no获取失败')
            leftTicketStr_all=re.compile(leftTicketStr_pat).findall(reqdata)
            if (len(leftTicketStr_all)!=0):
                self._leftTicketStr=leftTicketStr_all[0]
            else:
                raise Exception('leftTicketStr获取失败')
            fromStationTelecode_all=re.compile(fromStationTelecode_pat).findall(reqdata)
            if (len(fromStationTelecode_all)!=0):
                self._fromStationTelecode=fromStationTelecode_all[0]
            else:
                raise Exception('fromStationTelecode获取失败')
            toStationTelecode_all=re.compile(toStationTelecode_pat).findall(reqdata)
            if (len(toStationTelecode_all)!=0):
                self._toStationTelecode=toStationTelecode_all[0]
            else:
                raise Exception('toStationTelecode获取失败')
            train_location_all=re.compile(train_location_pat).findall(reqdata)
            if (len(train_location_all)!=0):
                self._train_location=train_location_all[0]
            else:
                raise Exception('train_location获取失败')
            tokenall=re.compile(pattoken).findall(reqdata)
            if (len(tokenall)!=0):
                self._token=tokenall[0]
            else:
                raise Exception('token获取失败')
            keyall=re.compile(patkey).findall(reqdata)
            if (len(keyall)!=0):
                self._key=keyall[0]
            else:
                raise Exception('key_check_isChange获取失败')
#            train_locationall=re.compile(pattrain_location).findall(reqdata)
#            if(len(train_locationall)!=0):
#                self._train_location=train_locationall[0]
#            else:
#                raise Exception("train_location获取失败")
            print('initDc验证通过')
        except:
            print('initDc验证失败，尝试重新连接，等待3s')
            time.sleep(3)
            return self.OrderTicket(timeout)
        time.sleep(0.5)
        #自动post网址4-获取乘客信息
        getuserurl="https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
        postdata={"REPEAT_SUBMIT_TOKEN":self._token,'_json_att':''}
        reqdata=self.UrlPost(getuserurl,timeout,postdata)
#        print(reqdata)
        if (self.StatusCheckout2(reqdata,'true')):
            print('getPassengerDTOs验证通过')
        else:
            print('getPassengerDTOs验证失败，尝试重新连接，等待3s')
            time.sleep(3)
            return self.OrderTicket(timeout)
            
    def SubmitOrder(self,timeout):
        checkOrderurl="https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
        postdata={
        "cancel_flag":2,
        "bed_level_order_num":"000000000000000000000000000000",
        "passengerTicketStr":self._thisSeat+",0,"+self.studentflag[self._ticketType]+","+self.name+",1,"+self.passagerid+","+self.mobile+",N",
        "oldPassengerStr":self.name+",1,"+self.passagerid+","+self.studentflag[self._ticketType]+"_",
        "tour_flag":"dc",
        "randCode":"",
        "whatsSelect":1,
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":self._token,
        }
        reqdata=self.UrlPost(checkOrderurl,timeout,postdata)
#        print(reqdata)
        if (self.StatusCheckout(reqdata,'true','true')):
            print('checkOrderInfo验证通过')
        else:
            print('checkOrderInfo验证失败，尝试重新连接，等待3s')
            time.sleep(3)
            return self.SubmitOrder(timeout)
            
        time.sleep(0.5) 
        
        getqueurl="https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
        #将日期转为格林时间
        #先将字符串转为常规时间格式
        thisdatestr=self._date#需要的买票时间
        thisdate=datetime.datetime.strptime(thisdatestr,"%Y-%m-%d").date()
        #再转为对应的格林时间
        gmt='%a+%b+%d+%Y'
        thisgmtdate=thisdate.strftime(gmt)
        leftstr2=self._leftTicketStr.replace("%","%25")
        getquedata="train_date="+str(thisgmtdate)+"+00%3A00%3A00+GMT%2B0800&train_no="+self._train_no+"&stationTrainCode="+self._thisCode+"&seatType=M&fromStationTelecode="+self._fromStationTelecode+"&toStationTelecode="+self._toStationTelecode+"&leftTicket="+leftstr2+"&purpose_codes=00&train_location="+self._train_location+"&_json_att=&REPEAT_SUBMIT_TOKEN="+str(self._token)
        getdata=getquedata.encode('utf-8')    
        reqdata=self.UrlPost2(getqueurl,timeout,getdata)
#        print(reqdata)
        if (self.StatusCheckout2(reqdata,'true')):
            print('getQueueCount验证通过')
        else:
            print('getQueueCount验证失败，尝试重新连接，等待3s')
            time.sleep(3)
            return self.SubmitOrder(timeout)
            
        time.sleep(0.5)
        confurl="https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
        postdata={
        "passengerTicketStr":self._thisSeat+",0,"+self.studentflag[self._ticketType]+","+self.name+",1,"+self.passagerid+","+self.mobile+",N",
        "oldPassengerStr":self.name+",1,"+self.passagerid+","+self.studentflag[self._ticketType]+"_",
        "randCode":"",
        "purpose_codes":"00",
        "key_check_isChange":self._key,
        "leftTicketStr":self._leftTicketStr,
        "train_location":self._train_location,
        "choose_seats":"",
        "seatDetailType":"000",
        "whatsSelect":"1",
        "roomType":"00",
        "dwAll":"N",
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":self._token
        }
        reqdata=self.UrlPost(confurl,timeout,postdata)
        print(reqdata)
        if (self.StatusCheckout(reqdata,'true','true}')):
            print('confirmSingleForQueue验证通过')
        else:
            print('confirmSingleForQueue验证失败，尝试重新连接，等待3s')
            time.sleep(3)
            return self.SubmitOrder(timeout)
            
        time.sleep(0.5)
        time1=time.time()
        while True:
             #总请求4-确认步骤2-获取orderid
            time2=time.time()
            if((time2-time1)//60>5):
                print("获取orderid超时，正在进行新一次抢购")
                return self.SubmitOrder(timeout)
            getorderidurl="https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random="+str(int(time.time()*1000))+"&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN="+str(self._token)
            reqdata=self.UrlGet(getorderidurl,timeout)
            print(reqdata)
            if (self.StatusCheckout2(reqdata,'true')):
                patorderid='"orderId":"(.*?)"'
                orderidall=re.compile(patorderid).findall(reqdata)
                if(len(orderidall)==0):
                    print("未获取到orderid，正在进行新一次的请求。")
                    continue
                else:
                    self._orderid=orderidall[0]
                    break
            else:
                print('orderid请求失败，尝试重新连接，等待1s')
                time.sleep(1)
                continue
        print("获取orderid完成，即将进行下一步")
        time.sleep(0.5)
        resulturl="https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue"
        resultdata="orderSequence_no="+self._orderid+"&_json_att=&REPEAT_SUBMIT_TOKEN="+str(self._token)
        resultdata2=resultdata.encode('utf-8')
        reqdata=self.UrlPost2(resulturl,timeout,resultdata2)
        print(reqdata)
        if (self.StatusCheckout(reqdata,'true','true')):
            print('resultOrderForDcQueue验证通过')
        else:
            print('resultOrderForDcQueue验证失败，尝试重新连接，等待3s')
            time.sleep(3)
            return self.SubmitOrder(timeout)
         
#        time.sleep(0.5)
    
#        payurl="https://kyfw.12306.cn/otn//payOrder/init"
##        ?random="+str(int(time.time()*1000))
#        paydata="_json_att=&REPEAT_SUBMIT_TOKEN="+str(self._token)
#        paydata2=paydata.encode('utf-8')
#        reqdata=self.UrlPost2(payurl,timeout,paydata2)
#        print(reqdata)
#        patpay='支付剩余时间：<(.*?)>'
#        payall=re.compile(patpay).findall(reqdata)
#        if (len(payall)!=0):
#            print("订单已经完成提交，您可以登录后台进行支付了。")
#        else:
#            print('payOrder验证失败，尝试重新连接，等待3s')
#            time.sleep(3)
#            return self.SubmitOrder(timeout)
            
        
            
            
            
if __name__=='__main__':
    socket.setdefaulttimeout(5.0)
    ticket=Ticket()
    ticket.start='南京'
    ticket.to='昆山'
    ticket.date='2018-06-22'
    ticket.isStudent='0'
    ticket.username='***@qq.com'
    ticket.password='***'
    ticket.setssl()
    ticket.TicketLeft(1)
    ticket.PrintTicketLeft()
    ticket.CookieProcess()
    ticket.Login(1)
    ticket.thiscode='G7247'
    ticket.thisseat='O'
    ticket.OrderTicket(1)
    ticket.SubmitOrder(1)
        