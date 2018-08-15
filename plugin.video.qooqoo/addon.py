# -*- coding: utf-8 -*-
"""
    Baykoreans
"""

import os
import xbmcplugin, xbmcgui, sys
import urllib2, urllib, re
import json
from xbmcswift2 import Plugin
#from YDStreamExtractor import getVideoInfo
from BeautifulSoup import BeautifulSoup

# magic; id of this plugin's instance - cast to integer
plugin = Plugin()
_pluginName = (sys.argv[0])
_thisPlugin = int(sys.argv[1])
_connectionTimeout = 20
_header = 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.65 Mobile Safari/537.36'
tablet_UA = "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.65 Mobile Safari/537.36"
USER_AGENT = 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.65 Mobile Safari/537.36'

headers = {'User-Agent': USER_AGENT,
           'Accept': '*/*',
           'Connection': 'keep-alive'}
def listMainCategories():
#    addDir("사랑만 할래", "http://drama.baykoreans.net/index.php?mid=drama&search_target=title&search_keyword=사랑만 할래", "EntCategoryContent", '')
#s    addDir("내일도 칸타빌레", "http://drama.baykoreans.net/index.php?mid=drama&search_target=title&search_keyword=칸타빌레", "EntCategoryContent", '')
    addDir("드라마", "https://qooqootv.pro/category/%EB%93%9C%EB%9D%BC%EB%A7%88/", "Shows", '')
    #addDir("드라마", " ", "dramaDate", '')
    #addDir("예능/오락", " ", "varietyDate", '')
    addDir("예능/오락", "https://qooqootv.pro/category/%EC%98%88%EB%8A%A5%EC%98%A4%EB%9D%BD/", "Shows", '')
    #addDir("시사/다큐", " ", "docuDate", '')
    addDir("시사/다큐", "https://qooqootv.pro/category/%EC%8B%9C%EC%82%AC%EA%B5%90%EC%96%91/", "Shows", '') 
    #addDir("기분 좋은 날", "http://www.torrentbon.com/bbs/board.php?bo_table=view_d&sca=&sfl=wr_subject&stx=%EA%B8%B0%EB%B6%84&sop=and&x=35&y=13", 'listhappycategories', "")
    #addDir("스포츠", "http://baykoreans.net/sports", "EntCategoryContent", '')

#    addDir("영화", "http://drama.baykoreans.net/movie", "EntCategoryContent", '')
#    addDir("세바퀴", "http://drama.baykoreans.net/?act=&vid=&mid=entertain&category=19114892319082&search_target=title&search_keyword=세바퀴", "EntCategoryContent", '')
#    addDir("시사/다큐", "http://baykoreans.net/current", "Shows", '')
#    addDir("영화", "http://baykoreans.net/movie", "MovieCategories", '')  



def Shows(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        
        soup=BeautifulSoup(link, fromEncoding='utf-8')
        items = []
 
        for item in soup.findAll("li", {"class":"entry-category"}):

            title = item.a.string
            href = item.a['href']
            items.append({'3title':title, 'url':href})

        items.sort(reverse=False)
        
        for i in range(len(items)):
            items[i] = (items[i]['3title'], items[i]['url'])

        
        for title, did in items:
            addDir(title, did, 'Episodes', '')
  
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
                
def Episodes(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        soup=BeautifulSoup(link, fromEncoding='utf-8')
        #match=re.compile('<img src="(.*?)" alt.*?>\n.*?</div>\n.*?</a>\n.*?</div>\n\t\t\t\t\t\t.*?\n.*?\n.*?\n.*?\n.*?<p class="title">\n.*?<a href=".+?mid=(.+?)\&.+?document_srl=(.+?)" class="title" >(.*?)</a>').findall(link)
        items = []
            # looking for tags td and something that has attribute class="title"
        for item in soup.findAll("div", {"class":"td-module-thumb"}):

            thumb = item.img['src']
            title = item.a['title'].replace('&amp;','&').encode('utf-8')
            href = item.a['href']
            items.append({'3title':title, 'url':href, 'thumbnail':thumb})

        for i in range(len(items)):
            items[i] = (items[i]['3title'], items[i]['url'], items[i]['thumbnail'])
                  

        for title, url, thumbnail in items:
            addLink(title, url, 'Play', thumbnail)

    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
    
        
def Play(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        soup=BeautifulSoup(link, fromEncoding='utf-8')
        soup2=soup.find("div", {"class":"linkcontents"})

        items = []
        
        for item in soup2.findAll("li"):

            t=item.find("span", {"class":"linkhigh"})
            if t:
                title = item.find("span", {"class":"link01"}).string
                href = item.a['val'].encode('utf-8')
                items.append({'title':title, 'href':href})
            else:
                continue


        for i in range(len(items)):
            items[i] = (items[i]['title'], items[i]['href'])

        items.sort()
        for title, url in items:

           #if title =='HDvid ':
           #     hdvid(url)
                #addLink(title, url, 'hdvid', '')
           #     break
            if title =='K-vid ':
                #addLink(title, url, 'kvid', '')
                kvid(url)
                break
            else:
                continue
  
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

##        for i in range(len(match)):
##            playurl = 'http://baykoreans.net/' + match[i][1] +'/' + match[i][2]
##            match[i] = (playurl, unicode(match[i][3], 'utf-8'), match[i][0])
##    
##        for url, title, thumbnail, in match:
##            addDir(title, url, 'listvideourl2', thumbnail)
        
#        match2=re.compile('page=(.+?)">.+?</a> <a href').findall(link)
#        match3=re.compile('<div class="pagination"> <a href=".+?category=(.+?)"').findall(link)
#        baseurl = 'http://drama.baykoreans.net/' + match[1][1]
#        
#        if match2:
#            for i in range(len(match2)):
#                Pgurl = baseurl + '&page=' + match2[i][0]
#                Pgname = match2[i][0] + ' 페이지'
#                match2[i] = (Pgurl, Pgname)
#            print url
#
#            addDir("1 페이지", baseurl, 'Episodes', "")
#            for url, name in match2:
#                addDir(name, url, 'Episodes', "")

   
def kvid(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')        
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        soup=BeautifulSoup(link, fromEncoding='utf-8')

        
        videourl=re.compile('file: \'(.*?)\'').search(link).group(1)
        print videourl
        item = xbmcgui.ListItem(path = videourl)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
    
def hdvid(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')        
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        soup=BeautifulSoup(link, fromEncoding='utf-8')

        
        videourl=re.compile('file:\"(.*?)\"').search(link).group(1)
        print videourl
        item = xbmcgui.ListItem(path = videourl)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
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
    if params["mode"] == 'Shows':
        Shows(urlUnquoted)
    elif params["mode"] == 'Episodes':
        Episodes(urlUnquoted)
    elif params["mode"] == 'Play':
        Play(urlUnquoted)
    elif params["mode"] == 'kvid':
        kvid(urlUnquoted)
    elif params["mode"] == 'hdvid':
        hdvid(urlUnquoted)

xbmcplugin.endOfDirectory(_thisPlugin)        
