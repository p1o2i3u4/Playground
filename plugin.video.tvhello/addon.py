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
    addDir("드라마", " ", "dramaDate", '')
    addDir("예능/오락", " ", "varietyDate", '')
    addDir("시사/다큐", " ", "docuDate", '')
    #addDir("음식/요리", "http://www.ondemandkorea.com/food", "videoCategories", '')
    #addDir("뷰티/패션", "http://www.ondemandkorea.com/beauty", "videoCategories", '')
    #addDir("여성", "http://www.ondemandkorea.com/women", "videoCategories", '')
    #addDir("건강", "http://www.ondemandkorea.com/health", "videoCategories", '')
    addDir("스포츠", "http://www.tvhello.com/list/?cate=spt", "videoCategories", '')    
    addDir("기타", "http://www.tvhello.com/list/?cate=nor", "videoCategories", '')    
    addDir("유아/아동", "http://www.tvhello.com/list/?cate=kid", "videoCategories", '')    
    addDir("뉴스", "http://www.tvhello.com/list/?cate=new", "videoCategories", '')
             

def listdramaDate():
    addDir("최근 방영", "http://www.tvhello.com/list/?cate=dra", "videoCategories", '') 
    addDir("월요일", "http://live.hanindisk.com/tv_chart.php?week_day=2", "dramaCategories", '')  
    addDir("화요일", "http://live.hanindisk.com/tv_chart.php?week_day=3", "dramaCategories", '')
    addDir("수요일", "http://live.hanindisk.com/tv_chart.php?week_day=4", "dramaCategories", '')
    addDir("목요일", "http://live.hanindisk.com/tv_chart.php?week_day=5", "dramaCategories", '')
    addDir("금요일", "http://live.hanindisk.com/tv_chart.php?week_day=6", "dramaCategories", '')
    addDir("토요일", "http://live.hanindisk.com/tv_chart.php?week_day=7", "dramaCategories", '')
    addDir("일요일", "http://live.hanindisk.com/tv_chart.php?week_day=1", "dramaCategories", '')

def listvarietyDate():
    addDir("최근 방영", "http://www.tvhello.com/list/?cate=ent", "videoCategories", '') 
    addDir("월요일", "http://live.hanindisk.com/tv_chart.php?week_day=2", "varietyCategories", '')  
    addDir("화요일", "http://live.hanindisk.com/tv_chart.php?week_day=3", "varietyCategories", '')
    addDir("수요일", "http://live.hanindisk.com/tv_chart.php?week_day=4", "varietyCategories", '')
    addDir("목요일", "http://live.hanindisk.com/tv_chart.php?week_day=5", "varietyCategories", '')
    addDir("금요일", "http://live.hanindisk.com/tv_chart.php?week_day=6", "varietyCategories", '')
    addDir("토요일", "http://live.hanindisk.com/tv_chart.php?week_day=7", "varietyCategories", '')
    addDir("일요일", "http://live.hanindisk.com/tv_chart.php?week_day=1", "varietyCategories", '')

def listdocuDate():
    addDir("최근 방영", "http://www.tvhello.com/list/?cate=doc", "videoCategories", '') 
    addDir("월요일", "http://live.hanindisk.com/tv_chart.php?week_day=2", "docuCategories", '')  
    addDir("화요일", "http://live.hanindisk.com/tv_chart.php?week_day=3", "docuCategories", '')
    addDir("수요일", "http://live.hanindisk.com/tv_chart.php?week_day=4", "docuCategories", '')
    addDir("목요일", "http://live.hanindisk.com/tv_chart.php?week_day=5", "docuCategories", '')
    addDir("금요일", "http://live.hanindisk.com/tv_chart.php?week_day=6", "docuCategories", '')
    addDir("토요일", "http://live.hanindisk.com/tv_chart.php?week_day=7", "docuCategories", '')
    addDir("일요일", "http://live.hanindisk.com/tv_chart.php?week_day=1", "docuCategories", '')


def listVideoCategories(url):
    try:
        print "requesting url " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', tablet_UA)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        link=link.replace('&nbsp;',': ')
        
        match=re.compile('showplayer\((.*?),2\);"><img src="(.*?)" width').findall(link)
        match1=re.compile('\r\n\t\t\t\t\t  (.*?)                      <img src="../(.*?)/title_icon_.*?.png"').findall(link)
        match2=re.compile('\xb0\xa9\xec\x86\xa1\xec\x9d\xbc:\r\n                      (.*?) ([0-9][0-9]):').findall(link)
        match3=[(x+y+z) for x,y,z in zip(match,match1,match2)] #combine match and match2!
        
        for i in range(len(match3)):
            thumb = 'http://www.tvhello.com/' + match3[i][1]
	    dramaurl = 'http://www.tvhello.com/list/player.php?idx=' + match3[i][0] + '&mode=2'
            title = match3[i][2]+' - '+match3[i][4]
            match3[i] = (unicode(title, 'utf-8'), dramaurl, thumb)
              

        for name, url, thumbnail in match3:
            addLink(name, url, 'resolveAndPlayVideo', thumbnail)

        
        
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
        
def listSearchedCategories(url):
    try:
        print "requesting url " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', tablet_UA)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        link=link.replace('&nbsp;',': ')
        
        match=re.compile('showplayer\((.*?),2\);"><img src="(.*?)" width').findall(link)
        match1=re.compile('<font color=\'orange\'>(.*?)</font>(.*?)                      <img').findall(link)
        match2=re.compile('\xb0\xa9\xec\x86\xa1\xec\x9d\xbc:\r\n                      (.*?) ([0-9][0-9]):').findall(link)
        match3=[(x+y+z) for x,y,z in zip(match,match1,match2)] #combine match and match2!
        
        for i in range(len(match3)):
            thumb = 'http://www.tvhello.com/' + match3[i][1]
	    dramaurl = 'http://www.tvhello.com/list/player.php?idx=' + match3[i][0] + '&mode=2'
            title = match3[i][2]+  match3[i][3] +' - '+match3[i][4]
            match3[i] = (unicode(title, 'utf-8'), dramaurl, thumb)
              

        for name, url, thumbnail in match3:
            addLink(name, url, 'resolveAndPlayVideo', thumbnail)

        
        
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def resolveAndPlayVideo(url):
    try:
        tablet_UA = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19"

        req = urllib2.Request(url)
        req.add_header('User-Agent', tablet_UA)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
            
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        match=re.compile('file: "(.*?)&ia="').search(link).group(1)
        url=match+'123'
        listItem = xbmcgui.ListItem(path=str(url))
        listItem.setProperty('IsPlayable', 'true')
        
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
        

    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
        
def listdramaCategories(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', tablet_UA)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
            
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        soup=BeautifulSoup(link)
        
        table = soup.findAll('table')
        video = table[0]
        match=re.compile('<a href="./(.*?)"> (.*?)</a>(.*?)<span>(.*?)</span>').findall(str(video))
             
        for i in range(len(match)):
	    videourl = 'http://www.tvhello.com/list/?cate=&strkey=' + match[i][1]
	    title = unicode(match[i][1], 'utf-8') + unicode(match[i][2], 'utf-8') + unicode(match[i][3], 'utf-8')
            match[i] = (title, videourl)
        
        for name, url in match:
            addDir(name, url, 'SearchedContent', '')
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
        

   
def listvarietyCategories(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', tablet_UA)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
            
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        soup=BeautifulSoup(link)
        
        table = soup.findAll('table')
        video = table[1]
        match=re.compile('<a href="./(.*?)"> (.*?)</a>(.*?)<span>(.*?)</span>').findall(str(video))
             
        for i in range(len(match)):
	    videourl = 'http://www.tvhello.com/list/?cate=&strkey=' + match[i][1]
	    title = unicode(match[i][1], 'utf-8') + unicode(match[i][2], 'utf-8') + unicode(match[i][3], 'utf-8')
            match[i] = (title, videourl)
        
        for name, url in match:
            addDir(name, url, 'SearchedContent', '')
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
        
def listdocuCategories(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', tablet_UA)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
            
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        soup=BeautifulSoup(link)
        
        table = soup.findAll('table')
        video = table[2]
        match=re.compile('<a href="./(.*?)"> (.*?)</a>(.*?)<span>(.*?)</span>').findall(str(video))
             
        for i in range(len(match)):
	    videourl = 'http://www.tvhello.com/list/?cate=&strkey=' + match[i][1]
	    title = unicode(match[i][1], 'utf-8') + unicode(match[i][2], 'utf-8') + unicode(match[i][3], 'utf-8')
            match[i] = (title, videourl)
        
        for name, url in match:
            addDir(name, url, 'SearchedContent', '')
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
    if params["mode"] == 'videoCategories':
        listVideoCategories(urlUnquoted)
    elif params["mode"] == 'SearchedContent':
        listSearchedCategories(urlUnquoted)
    elif params["mode"] == 'resolveAndPlayVideo':
        resolveAndPlayVideo(urlUnquoted)


    elif params["mode"] == 'dramaDate':
        listdramaDate()  
    elif params["mode"] == 'varietyDate':
        listvarietyDate()
    elif params["mode"] == 'docuDate':
        listdocuDate()
    elif params["mode"] == 'dramaCategories':
        listdramaCategories(urlUnquoted)   
    elif params["mode"] == 'varietyCategories':
        listvarietyCategories(urlUnquoted)
    elif params["mode"] == 'docuCategories':
        listdocuCategories(urlUnquoted)
        

        
xbmcplugin.endOfDirectory(_thisPlugin)        
