# -*- coding: utf-8 -*-

'''

@Author: Jinyong HU

@License: (C) Copyright 2013-2017, Personal use only.

@Contact: hujinyong1995@outlook.com

@File: pollution.py

@Create date: 2017/8/14 上午11:33

@Desc: Catch Water-Pollution Data

'''

import re
import sys
import urllib
import urllib2
import cookielib
import json
import time
import pymysql as db
from urllib import unquote
from datetime import datetime
from datetime import timedelta
import chardet

#PROVINCE_NUM = 21

def get_city_num(p_num, num_retries=3):

    # TODO Get Original Resoponse

    c = getCookies()
    url = 'http://www.ipe.org.cn/data_ashx/GetAirData.ashx'
    para = {
        'cmd': 'getSpaces',
        'p_val': p_num
    }
    try:
        postData = urllib.urlencode(para)
        req = urllib2.Request(url, postData)
    except urllib2.URLError as e:
        print "下载失败：", e.reason
        response = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return getResponse(p_num, num_retries - 1)
        else:
            return 0

    req.add_header('Host', 'www.ipe.org.cn')
    req.add_header('Origin', 'http://www.ipe.org.cn')
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')
    req.add_header('Referer', 'http://www.ipe.org.cn/MapPollution/Pollution.aspx?q=4&type=2')
    req.add_header('Cookie', '_ga=GA1.3.1125901999.1502762910; acw_tc=AQAAAPMjx01xIAYAsM54aukLbuCS9jaL; safedog-flow-item=; ASP.NET_SessionId=bhtcnpfokdn2v5010hzzogye; __utma=105455707.1125901999.1502762910.1503479969.1522291751.11; __utmc=105455707; __utmz=105455707.1522291751.11.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; acw_sc__=5abc5f3c6012486c9cbbb98550a2392ca2343fd7; ajaxkey='+str(c))

    try:
        resp = urllib2.urlopen(req, timeout=5)
        response = resp.read()
        print response
        #print chardet.detect(response)

    except urllib2.URLError as e:
        print "下载失败：", e.reason
        response = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return get_city_num(p_num, num_retries - 1)
        else: response = None

    return response


def getResponse(city_num, p_num, num_retries=3):

    # TODO Get Original Resoponse

    #time.sleep(1000)
    c = getCookies()
    url = 'http://www.ipe.org.cn/data_ashx/GetAirData.ashx'
    para = {
        'time': '',
        'headers[Cookie]': '_ga=GA1.3.1125901999.1502762910; acw_tc=AQAAAPMjx01xIAYAsM54aukLbuCS9jaL; safedog-flow-item=; ASP.NET_SessionId=bhtcnpfokdn2v5010hzzogye; __utma=105455707.1125901999.1502762910.1503479969.1522291751.11; __utmc=105455707; __utmz=105455707.1522291751.11.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; acw_sc__=5abc5f3c6012486c9cbbb98550a2392ca2343fd7; ajaxkey='+str(c),
        'cmd': 'getpollution_totalmap',
        'province': p_num,
        'city': city_num,
        'key': '',
        'pollution': 0,
        'enterprisids':'0/1/2/3',
        'standrdis':'0/1/2/3',
        'feedback': '0/1/2',
        'type': 2,
        'mapprovice': '',
        'level': 6,
        'nostr': '',
        'time': '',
        'issearch': 1
    }
    try:
        postData = urllib.urlencode(para)
        req = urllib2.Request(url, postData)
    except urllib2.URLError as e:
        print "下载失败：", e.reason
        response = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return getResponse(city_num, num_retries - 1)
        else:
            return None

    req.add_header('Host', 'www.ipe.org.cn')
    req.add_header('Origin', 'http://www.ipe.org.cn')
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')
    req.add_header('Referer', 'http://www.ipe.org.cn/MapPollution/Pollution.aspx?q=4&type=2')
    req.add_header('Cookie', '_ga=GA1.3.1125901999.1502762910; acw_tc=AQAAAPMjx01xIAYAsM54aukLbuCS9jaL; safedog-flow-item=; ASP.NET_SessionId=bhtcnpfokdn2v5010hzzogye; __utma=105455707.1125901999.1502762910.1503479969.1522291751.11; __utmc=105455707; __utmz=105455707.1522291751.11.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; acw_sc__=5abc5f3c6012486c9cbbb98550a2392ca2343fd7; ajaxkey='+str(c))

    try:
        resp = urllib2.urlopen(req, timeout=5)
        response = resp.read()

    except urllib2.URLError as e:
        print "下载失败：", e.reason
        response = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return getResponse(city_num, p_num, num_retries - 1)
    return response

def getCookies():

    # TODO Get Danamic Cookies

    # 声明一个CookieJar对象实例来保存cookie
    cookie = cookielib.CookieJar()
    # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    handler = urllib2.HTTPCookieProcessor(cookie)
    # 通过handler来构建opener
    opener = urllib2.build_opener(handler)
    # 此处的open方法同urllib2的urlopen方法，也可以传入request
    response = opener.open('http://www.ipe.org.cn/MapPollution/Pollution.aspx?q=4&type=2')
    print str(cookie)
    return cookie

def proData(pro_num, pro_name):

    # TODO Load in Json Format

    response = get_city_num(pro_num)
    if not response:
        print "Fail"
    else:
        response = response[24:-2]
        #print response
        response = unquote(response)
        #print response
        response = re.sub('<option value="0">%u57CE%u5E02/%u76F4%u8F96%u5E02%u533A%u53BF</option><option value="', '',
                      response)
        response = re.sub('">', ' ', response)
        response = re.sub('</option><option value="', ' ', response)
        response = re.sub('</option>', '', response)

        city_data = response.split(' ', -1)

        i = 0
        while i < len(city_data):
            city_data[i] = re.sub('%', r"\\", city_data[i]).decode('unicode_escape')
            #print city_data[i]
            #print chardet.detect(city_data[i])
            i = i + 1

    # TODO 遍历所有的城市

    i = 0

    while i < len(city_data):

        res = getResponse(city_data[i], pro_num)
        if not res:
            print "Fail"
        else:
            #print res
            try:
                j = json.loads(res, strict=False)
                data = j['Data']
                savein_DB(data, city_data[i+1], pro_name)
                #print len(city_data)
                #print "i = ", i
            except:
                print("老出错的地方：196行!")
        time.sleep(10)
        i = i + 2

    print "Finish City Iteration!"


def getSpec():

    time.sleep(10)
    res = getResponse('', 32)
    if not res:
        print "Fail"
    else:
        print res
        j = json.loads(res, strict=False)
        data = j['Data']
        savein_DB(data, '', '天津')
    time.sleep(10)
    res = getResponse('', 33)
    if not res:
        print "Fail"
    else:
        #print res
        j = json.loads(res, strict=False)
        data = j['Data']
        savein_DB(data, '', '北京')
    time.sleep(10)
    res = getResponse('', 4)
    if not res:
        print "Fail"
    else:
        print res
        j = json.loads(res, strict=False)
        data = j['Data']
        savein_DB(data, '', '重庆')
    time.sleep(10)
    res = getResponse('', 24)
    if not res:
        print "Fail"
    else:
        print res
        j = json.loads(res, strict=False)
        data = j['Data']
        savein_DB(data, '', '上海')


def savein_DB(data, city_name, pro_name):

    # TODO Save in Database

    ISOTIMEFORMAT = '%Y%m%d'
    cu_time = str(time.strftime(ISOTIMEFORMAT, time.localtime()))
    print cu_time

    conn = db.connect(host='localhost', port=3306, user='root', passwd='root', db='Water_Pollution', charset='utf8')
    cur = conn.cursor()
    sql = ("CREATE TABLE IF NOT EXISTS " + pro_name + cu_time + "("
                "id varchar(40),"
                "lat varchar(40),"
                "lng varchar(40),"
                "company_name varchar(1000),"
                "pol_name varchar(40),"
                "average varchar(40),"
                "standard varchar(40),"
                "multiple varchar(40),"
                "date varchar(40),"
                "city varchar(40))")

    cur.execute(sql)

    count = 0

    while count < len(data):

        #print data[count][3].encode("utf-8")
        #print data[count][4].encode("utf-8")
        sql = "INSERT INTO " + pro_name.encode('utf-8') + cu_time + " ( id, lat, lng, company_name, pol_name, average, standard, multiple, date, city) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (data[count][0].encode("utf-8"), data[count][1].encode("utf-8"), data[count][2].encode("utf-8"), data[count][3].encode("utf-8"), data[count][4].encode("utf-8"), data[count][5].encode("utf-8"), data[count][6].encode("utf-8"), data[count][7].encode("utf-8"), data[count][9].encode("utf-8"), city_name.encode('utf-8'))
        print sql
        cur.execute(sql)
        conn.commit()
        count = count + 1
        print count, "items has been saved"

    print "Finish catch" + city_name + "data!"

    cur.close()
    conn.close()

def getPro():

    s = '''2'>安徽</option><option value='3'>内蒙古</option><option value='5'>福建</option><option value='6'>甘肃</option><option value='7'>广东</option><option value='8'>广西</option><option value='9'>贵州</option><option value='10'>海南</option><option value='11'>河北</option><option value='12'>河南</option><option value='13'>黑龙江</option><option value='14'>湖北</option><option value='15'>湖南</option><option value='16'>吉林</option><option value='17'>江苏</option><option value='18'>辽宁</option><option value='19'>江西</option><option value='20'>青海</option><option value='21'>山东</option><option value='22'>山西</option><option value='23'>陕西</option><option value='25'>四川</option><option value='27'>浙江</option><option value='28'>西藏</option><option value='30'>新疆</option><option value='31'>云南</option><option value='35'>宁夏'''
    s = re.sub("<option value='", ' ', s)
    s = re.sub("'>", ' ', s)
    s = re.sub("</option><option value='", ' ', s)
    s = re.sub('</option>', '', s)

    data = s.split(' ', -1)
    #print data

    i = 0
    while i < len(data):
        data[i] = re.sub('%', r"\\", data[i]).decode('utf-8')
        print data[i]
        i = i + 1
    return data


def main():

    # TODO Iterate normal province

    reload(sys)
    sys.setdefaultencoding('utf-8')

    data = getPro()

    i = 0

    while i < len(data):

        proData(data[i], data[i+1])
        time.sleep(10)
        i = i + 2

    # TODO Iteration Tianjin and Beijing

    getSpec()

    print "Finish today catch!"


if __name__ == '__main__':

    day = 0
    hour = 24
    minute = 0
    second = 0

    # 初始化时间
    now = datetime.now()
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    tm_hour = time.localtime(time.time()).tm_hour
    tm_date = str(time.localtime(time.time()).tm_year) + str(time.localtime(time.time()).tm_mon) + str(
        time.localtime(time.time()).tm_mday)
    print "now:", strnow

    # 第一次执行
    print "first task"
    main()

    period = timedelta(days=day, hours=hour, minutes=minute, seconds=second)
    next_time = now + period
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    print "next run:", strnext_time

    while True:

        # Get system current time
        iter_now = datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if str(iter_now_time) >= str(strnext_time):
            # Get every start work time
            print "start work: %s" % iter_now_time
            # Call task function
            main()
            print "task done."
            # Get next iteration time
            iter_time = iter_now + period
            strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
            print "next_iter: %s" % strnext_time
            # sleep for 1 hour
            time.sleep(3600)
            # Continue next iteration
            continue


