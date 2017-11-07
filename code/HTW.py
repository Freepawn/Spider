# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import csv
import datetime
from datetime import timedelta
from collections import defaultdict

class HTW:
  def __init__(self,url,decode_mode,encode_mode,t_date,t_end,p_str):
    self.pageIndex = 1
    self.usr_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0)'+\
    'Gecko/20100101 Firefox/55.0'
    self.headers = {'User-Agent':self.usr_agent}
    self.enable = True
    self.inf = []
    self.t_end = t_end
    self.url = url
    self.decode_mode = decode_mode
    self.encode_mode = encode_mode
    self.p_str = p_str
    self.t_date = t_date

    
  def getPage(self):
    try:
      url = self.url + str(self.pageIndex)
      request = urllib2.Request(url,headers = self.headers)
      response = urllib2.urlopen(request)
      pagecode = response.read().decode(self.decode_mode)
      return pagecode
    except urllib2.URLError, e:
      if hasattr(e,"reason"):
        print 'URLEroor:',e.reason
        return None

  def getPageItems(self):
    pagecode = self.getPage()
    pattern = re.compile(self.p_str,re.S)

    items = re.findall(pattern,pagecode)
    PageItems = []
    for item in items:
      NA = item[0].encode(self.decode_mode).split('\n')
      #print len(NA)
      Name,add1,add2 = NA
      Name = Name.decode(self.decode_mode).encode(self.encode_mode)
      add = add1.split('：')[1].decode(self.decode_mode).encode(self.encode_mode)\
      +add2.split('：')[1].decode(self.decode_mode).encode(self.encode_mode)
      t_time = item[1].encode(self.encode_mode)
      method = item[-1].encode(self.encode_mode)
      PageItems.append([Name,t_time,add,method])
    return PageItems

  def getAllItems(self):
    PageItems_ = self.getPageItems()
    if PageItems_:
      self.pageIndex += 1
      self.inf.extend(PageItems_)
    while self.enable:
      PageItems = self.getPageItems()
      if PageItems[0] == PageItems_[0] or self.t_end in PageItems[0][1]:
        break
      self.inf.extend(PageItems)
      PageItems_ = PageItems
      self.pageIndex += 1
    


  def writeInCsv(self):
    
    with open('./data/'+tt+"--xjh.csv",'wb') as csvfile:
      wr = csv.writer(csvfile)
      for item in self.inf:
        
        
        #print type(item[0])
        
        if self.t_date in item[1]:
          t_time = item[1].split()
          if len(t_time)==1 :
            print item[0],item[1],item[2],item[3]
          
            wr.writerow([item[0],item[1],item[2],item[3]])
          else:
            print item[0],t_time[1],item[2],item[3]
            wr.writerow([item[0],t_time[1],item[2],item[3]])




decode_mode = 'utf-8'
encode_mode = 'gbk'

tt = raw_input('Please input the date:')
t_date = tt.decode(decode_mode)

one_day = timedelta(days=1)
tt_end = (datetime.datetime.strptime(tt,'%Y-%m-%d') + one_day).strftime('%Y-%m-%d')
t_end = tt_end.decode(decode_mode)

url = 'https://xjh.haitou.cc/bj/page-'
p_str = '<tr data.*?<td class=.*?<td class=.*?<a.*?title="(.*?)".*?'+\
        '<td class=.*?ymd">(.*?)</span>.*?<td class=.*?title="(.*?)">.*?'+\
        '</span>.*?<td class=.*?blank">(.*?)</a>.*?</tr>'
Spider = HTW(url,decode_mode,encode_mode,t_date,t_end,p_str)
Spider.getAllItems()
Spider.writeInCsv()
input('Press any key to exit!')

      
                    
    
