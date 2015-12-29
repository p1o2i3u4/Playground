# -*- coding: utf-8 -*-
"""
    NR live
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
        url='http://sports.news.naver.com/tv/onairScheduleList.nhn?gameId=&isScoreOn=true'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
    
        live=re.compile('<span class="blind" id=".*?">(.*?)</span>').findall(link)
        url=re.compile('params2="(.*?)"').findall(link)
        sport=re.compile('\r\n                            \r\n                            (.*?)\r\n').findall(link)
        title=re.compile('<span class="tema_live tit_event"><strong>(.*?)</strong>').findall(link)
        title2=[(a+' '+b) for a,b in zip(sport,title)]
       

        match3=list(zip(live, title2, url))

        for i in range(len(match3)):
            if match3[i][0]=='STARTEDY':
                addLink(match3[i][1], match3[i][2], 'resolveAndPlayVideo', '')
            else:
                continue

        addLink('SBS', 'rtmp://rtmpplay3.idol001.com/live/korea_sbs', 'livetv', '')
        addLink('MBC', 'rtmp://rtmpplay3.idol001.com/live/korea_mbc', 'livetv', '')
        addLink('KBS1', 'rtmp://rtmpplay3.idol001.com/live/korea_kbs1', 'livetv', '')
        addLink('KBS2', 'rtmp://rtmpplay3.idol001.com/live/korea_kbs2', 'livetv', '')
        addLink('JTBC', 'rtmp://rtmpplay3.idol001.com/live/korea_jtbc', 'livetv', '')
        addLink('ONSTYLE', 'rtmp://rtmpplay3.idol001.com/live/korea_onstyle', 'livetv', '')
        addLink('MBC MUSIC', 'rtmp://rtmpplay3.idol001.com/live/korea_mbcmusic', 'livetv', '')
        addLink('Mnet', 'rtmp://rtmpplay3.idol001.com/live/korea_mnet', 'livetv', '')
        addLink('TVN', 'rtmp://rtmpplay3.idol001.com/live/korea_tvn', 'livetv', '')
        addLink('arirang', 'rtmp://rtmpplay3.idol001.com/live/korea_arirang', 'livetv', '')
        addLink('SBS MTV', 'rtmp://rtmpplay3.idol001.com/live/korea_sbsmtv', 'livetv', '')
        addLink('MBC everyone', 'rtmp://rtmpplay3.idol001.com/live/korea_mbcevery1', 'livetv', '')

    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def Med_list(url):
    try:
        url='http://sports.news.naver.com/tv/onairScheduleList.nhn?gameId=&isScoreOn=true'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
    
        live=re.compile('<span class="blind" id=".*?">(.*?)</span>').findall(link)
        url=re.compile('params2="(.*?)"').findall(link)
        sport=re.compile('\r\n                            \r\n                            (.*?)\r\n').findall(link)
        title=re.compile('<span class="tema_live tit_event"><strong>(.*?)</strong>').findall(link)
        title2=[(a+' '+b) for a,b in zip(sport,title)]
       

        match3=list(zip(live, title2, url))

        for i in range(len(match3)):
            if match3[i][0]=='STARTEDY':
                addLink(match3[i][1], match3[i][2], 'resolveAndPlayVideo_med', '')
            else:
                continue
            
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def Low_list(url):
    try:
        url='http://sports.news.naver.com/tv/onairScheduleList.nhn?gameId=&isScoreOn=true'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
    
        live=re.compile('<span class="blind" id=".*?">(.*?)</span>').findall(link)
        url=re.compile('params2="(.*?)"').findall(link)
        sport=re.compile('\r\n                            \r\n                            (.*?)\r\n').findall(link)
        title=re.compile('<span class="tema_live tit_event"><strong>(.*?)</strong>').findall(link)
        title2=[(a+' '+b) for a,b in zip(sport,title)]
       

        match3=list(zip(live, title2, url))

        for i in range(len(match3)):
            if match3[i][0]=='STARTEDY':
                addLink(match3[i][1], match3[i][2], 'resolveAndPlayVideo_low', '')
            else:
                continue
            
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')


def resolveAndPlayVideo(url):
    try:
        url2='http://sports.news.naver.com/tv/index.nhn?gameId=' + url
        req = urllib2.Request(url2)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        
        ch=re.compile('"channelID":"high(.*?)"').search(link).group(1)

        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2F'+ch+'%2F_definst_%2F'+ch+'_2000.stream%2Fplaylist.m3u8'
            
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

        listItem = xbmcgui.ListItem(path=str(link))
        listItem.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
        
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def resolveAndPlayVideo_med(url):
    try:
        url2='http://sports.news.naver.com/tv/index.nhn?gameId=' + url
        req = urllib2.Request(url2)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        
        ch=re.compile('"channelID":"high(.*?)"').search(link).group(1)

        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2F'+ch+'%2F_definst_%2F'+ch+'_800.stream%2Fplaylist.m3u8'
            
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

        listItem = xbmcgui.ListItem(path=str(link))
        listItem.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
        
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')


def resolveAndPlayVideo_low(url):
    try:
        url2='http://sports.news.naver.com/tv/index.nhn?gameId=' + url
        req = urllib2.Request(url2)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        
        ch=re.compile('"channelID":"high(.*?)"').search(link).group(1)

        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2F'+ch+'%2F_definst_%2F'+ch+'_300.stream%2Fplaylist.m3u8'
            
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

        listItem = xbmcgui.ListItem(path=str(link))
        listItem.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
        
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def livetv(url):
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
    elif params["mode"] == 'resolveAndPlayVideo_med':
        resolveAndPlayVideo_med(urlUnquoted)
    elif params["mode"] == 'resolveAndPlayVideo_low':
        resolveAndPlayVideo_low(urlUnquoted)
    elif params["mode"] == 'livetv':
        livetv(urlUnquoted)        
xbmcplugin.endOfDirectory(_thisPlugin)        
