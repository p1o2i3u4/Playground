# -*- coding: utf-8 -*-
"""
    Ondemand Korea
"""

import os
import xbmcplugin, xbmcgui, sys
import urllib2, urllib, re
from BeautifulSoup import BeautifulSoup

# magic; id of this plugin's instance - cast to integer
_pluginName = (sys.argv[0])
_thisPlugin = int(sys.argv[1])
_connectionTimeout = 20
_header = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
tablet_UA = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19"


def listMainCategories():
    addDir("초고화질", " ", "High", '')  
    addDir("고화질", " ", "Med", '')
    addDir("저화질", " ", "Low", '')
    
def High_list(url):
    try:
        schedule='http://sports.news.naver.com/tv/onairScheduleList.nhn'
        req = urllib2.Request(schedule)
        response = urllib2.urlopen(req)
        onair=response.read()
        response.close()
        match=re.search('피츠버그',onair)
        if match:
            schedule='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch10%2F_definst_%2Fch10_2000.stream%2Fplaylist.m3u8'
            req = urllib2.Request(schedule)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            print link
            addLink('Pittsburg Pirates 중계', link, 'resolveAndPlayVideo', '') 
        
        match=re.search('다저스',onair)
        if match:
            url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad9%2Fad9_2000.stream%2Fplaylist.m3u8'
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            addLink('LA Dodgers 중계', link, 'resolveAndPlayVideo', '')

        match=re.search('텍사스',onair)
        if match:
            url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad8%2Fad8_2000.stream%2Fplaylist.m3u8'
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            addLink('Texas Rangers 중계', link, 'resolveAndPlayVideo', '')


        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch14%2F_definst_%2Fch14_2000.stream%2Fplaylist.m3u8'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        addLink('SPOTV Games', link, 'resolveAndPlayVideo', '')

        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch200%2F_definst_%2Fch200_2000.stream%2Fplaylist.m3u8'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        addLink('YTN', link, 'resolveAndPlayVideo', '')

        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch201%2F_definst_%2Fch201_2000.stream%2Fplaylist.m3u8'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        addLink('JTBC', link, 'resolveAndPlayVideo', '')

##        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad10%2Fad10_2000.stream%2Fplaylist.m3u8'
##        req = urllib2.Request(url)
##        req.add_header('User-Agent', _header)
##        req.add_header('Accept-Langauge', 'ko')
##        req.add_header('Cookie', 'language=kr')
##        response = urllib2.urlopen(req)
##        link=response.read()
##        response.close()
##        addLink('SBS Sports', link, 'resolveAndPlayVideo', '')
        
##        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad12%2Fad12_2000.stream%2Fplaylist.m3u8'
##        req = urllib2.Request(url)
##        req.add_header('User-Agent', _header)
##        req.add_header('Accept-Langauge', 'ko')
##        req.add_header('Cookie', 'language=kr')
##        response = urllib2.urlopen(req)
##        link=response.read()
##        response.close()
##        addLink('SBS', link, 'resolveAndPlayVideo', '')

        addDir('현재 생방송 목록 (채널명 모름)',' ','High_Live', '')
        
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def Med_list(url):
    try:
        schedule='http://sports.news.naver.com/tv/onairScheduleList.nhn'
        req = urllib2.Request(schedule)
        response = urllib2.urlopen(req)
        onair=response.read()
        response.close()
        match=re.search('피츠버그',onair)
        if match:
            schedule='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch10%2F_definst_%2Fch10_800.stream%2Fplaylist.m3u8'
            req = urllib2.Request(schedule)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            print link
            addLink('Pittsburg Pirates 중계', link, 'resolveAndPlayVideo', '') 
        
        match=re.search('다저스',onair)
        if match:
            url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad9%2Fad9_800.stream%2Fplaylist.m3u8'
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            addLink('LA Dodgers 중계', link, 'resolveAndPlayVideo', '')

        match=re.search('텍사스',onair)
        if match:
            url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad8%2Fad8_800.stream%2Fplaylist.m3u8'
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            addLink('Texas Rangers 중계', link, 'resolveAndPlayVideo', '')
                
        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch14%2F_definst_%2Fch14_800.stream%2Fplaylist.m3u8'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        addLink('SPOTV Games', link, 'resolveAndPlayVideo', '')

        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch200%2F_definst_%2Fch200_800.stream%2Fplaylist.m3u8'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        addLink('YTN', link, 'resolveAndPlayVideo', '')

        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch201%2F_definst_%2Fch201_800.stream%2Fplaylist.m3u8'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        addLink('JTBC', link, 'resolveAndPlayVideo', '')

        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad10%2Fad10_800.stream%2Fplaylist.m3u8'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        addLink('SBS Sports', link, 'resolveAndPlayVideo', '')
        
##        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad12%2Fad12_800.stream%2Fplaylist.m3u8'
##        req = urllib2.Request(url)
##        req.add_header('User-Agent', _header)
##        req.add_header('Accept-Langauge', 'ko')
##        req.add_header('Cookie', 'language=kr')
##        response = urllib2.urlopen(req)
##        link=response.read()
##        response.close()
##        addLink('SBS', link, 'resolveAndPlayVideo', '')
##        
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def Low_list(url):
    try:
        schedule='http://sports.news.naver.com/tv/onairScheduleList.nhn'
        req = urllib2.Request(schedule)
        response = urllib2.urlopen(req)
        onair=response.read()
        response.close()
        match=re.search('피츠버그',onair)
        if match:
            schedule='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch10%2F_definst_%2Fch10_300.stream%2Fplaylist.m3u8'
            req = urllib2.Request(schedule)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            print link
            addLink('Pittsburg Pirates 중계', link, 'resolveAndPlayVideo', '') 
        
        match=re.search('다저스',onair)
        if match:
            url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad9%2Fad9_300.stream%2Fplaylist.m3u8'
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            addLink('LA Dodgers 중계', link, 'resolveAndPlayVideo', '')

        match=re.search('텍사스',onair)
        if match:
            url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad8%2Fad8_300.stream%2Fplaylist.m3u8'
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            addLink('Texas Rangers 중계', link, 'resolveAndPlayVideo', '')

        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch14%2F_definst_%2Fch14_300.stream%2Fplaylist.m3u8'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        addLink('SPOTV Games', link, 'resolveAndPlayVideo', '')

        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch200%2F_definst_%2Fch200_300.stream%2Fplaylist.m3u8'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        addLink('YTN', link, 'resolveAndPlayVideo', '')

        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch201%2F_definst_%2Fch201_300.stream%2Fplaylist.m3u8'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        addLink('JTBC', link, 'resolveAndPlayVideo', '')

        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad10%2Fad10_300.stream%2Fplaylist.m3u8'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        addLink('SBS Sports', link, 'resolveAndPlayVideo', '')
##        
##        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad12%2Fad12_300.stream%2Fplaylist.m3u8'
##        req = urllib2.Request(url)
##        req.add_header('User-Agent', _header)
##        req.add_header('Accept-Langauge', 'ko')
##        req.add_header('Cookie', 'language=kr')
##        response = urllib2.urlopen(req)
##        link=response.read()
##        response.close()
##        addLink('SBS', link, 'resolveAndPlayVideo', '')
        
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')


def High_Live_List(url):
    try:
        f=range(1,15)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highch'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)
            ch='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_2000.stream%2Fplaylist.m3u8'
            req = urllib2.Request(ch)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            name='채널 '+str(i)
            if match == 'on':
                addLink(name, link, 'resolveAndPlayVideo', '')
                
        f=range(100,102)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highch'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)
            ch='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_2000.stream%2Fplaylist.m3u8'
            req = urllib2.Request(ch)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            name='채널 '+str(i)
            if match == 'on':
                addLink(name, link, 'resolveAndPlayVideo', '')

        f=range(200,212)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highch'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)
            ch='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_2000.stream%2Fplaylist.m3u8'
            req = urllib2.Request(ch)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            name='채널 '+str(i)
            if match == 'on':
                addLink(name, link, 'resolveAndPlayVideo', '')
                
        f=range(1,15)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highad'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)
            ch='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad'+str(i)+'%2F_definst_%2Fad'+str(i)+'_2000.stream%2Fplaylist.m3u8'
            req = urllib2.Request(ch)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            name='ad채널 '+str(i)
            if match == 'on':
                addLink(name, link, 'resolveAndPlayVideo', '')
      
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def Med_Live_List(url):
    try:
        f=range(1,15)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highch'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)
            ch='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_800.stream%2Fplaylist.m3u8'
            req = urllib2.Request(ch)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            name='채널 '+str(i)
            if match == 'on':
                addLink(name, link, 'resolveAndPlayVideo', '')
                
        f=range(100,102)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highch'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)
            ch='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_800.stream%2Fplaylist.m3u8'
            req = urllib2.Request(ch)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            name='채널 '+str(i)
            if match == 'on':
                addLink(name, link, 'resolveAndPlayVideo', '')

        f=range(200,212)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highch'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)
            ch='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_800.stream%2Fplaylist.m3u8'
            req = urllib2.Request(ch)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            name='채널 '+str(i)
            if match == 'on':
                addLink(name, link, 'resolveAndPlayVideo', '')
                
        f=range(1,15)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highad'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)
            ch='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad'+str(i)+'%2F_definst_%2Fad'+str(i)+'_800.stream%2Fplaylist.m3u8'
            req = urllib2.Request(ch)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            name='ad채널 '+str(i)
            if match == 'on':
                addLink(name, link, 'resolveAndPlayVideo', '')
      
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def Low_Live_List(url):
    try:
        f=range(1,15)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highch'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)
            ch='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_300.stream%2Fplaylist.m3u8'
            req = urllib2.Request(ch)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            name='채널 '+str(i)
            if match == 'on':
                addLink(name, link, 'resolveAndPlayVideo', '')
                
        f=range(100,102)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highch'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)
            ch='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_300.stream%2Fplaylist.m3u8'
            req = urllib2.Request(ch)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            name='채널 '+str(i)
            if match == 'on':
                addLink(name, link, 'resolveAndPlayVideo', '')

        f=range(200,212)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highch'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)
            ch='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_300.stream%2Fplaylist.m3u8'
            req = urllib2.Request(ch)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            name='채널 '+str(i)
            if match == 'on':
                addLink(name, link, 'resolveAndPlayVideo', '')
                
        f=range(1,15)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highad'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)
            ch='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad'+str(i)+'%2F_definst_%2Fad'+str(i)+'_300.stream%2Fplaylist.m3u8'
            req = urllib2.Request(ch)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            name='ad채널 '+str(i)
            if match == 'on':
                addLink(name, link, 'resolveAndPlayVideo', '')
      
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
        
def resolveAndPlayVideo(url):
    try:
        listItem = xbmcgui.ListItem(path=str(url))
        listItem.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
        
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
    
def addLink(name,url,mode,iconimage):
    u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty("IsPlayable","true");
    ok=xbmcplugin.addDirectoryItem(handle=_thisPlugin,url=u,listitem=liz,isFolder=False)
    return ok

def addDir(name,url,mode,iconimage):
    u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)#+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=_thisPlugin,url=u,listitem=liz,isFolder=True)
    return ok

def getparams():
    """
    Pick up parameters sent in via command line
    @return dict list of parameters
    @thanks Team XBM - I lifted this straight out of the
    shoutcast addon
    """
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

params = getparams()

try:
    url = params["url"]
    urlUnquoted = urllib.unquote_plus(url)
except:
    url = None
  
if url == None:
    #do listing
    listMainCategories()
else:
    if params["mode"] == 'High':
        High_list(urlUnquoted)
    elif params["mode"] == 'Med':
        Med_list(urlUnquoted)
    elif params["mode"] == 'Low':
        Low_list(urlUnquoted)

    elif params["mode"] == 'High_Live':
        High_Live_List(urlUnquoted)
    elif params["mode"] == 'Med_Live':
        Med_Live_List(urlUnquoted)
    elif params["mode"] == 'Low_Live':
        Low_Live_List(urlUnquoted)
        
    elif params["mode"] == 'resolveAndPlayVideo':
        resolveAndPlayVideo(urlUnquoted)


        
xbmcplugin.endOfDirectory(_thisPlugin)        
