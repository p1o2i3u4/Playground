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
_header = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
_header = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
tablet_UA = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19"


def listMainCategories():
#    addDir("사랑만 할래", "http://drama.baykoreans.net/index.php?mid=drama&search_target=title&search_keyword=사랑만 할래", "EntCategoryContent", '')
#s    addDir("내일도 칸타빌레", "http://drama.baykoreans.net/index.php?mid=drama&search_target=title&search_keyword=칸타빌레", "EntCategoryContent", '')
    addDir("드라마", "http://drama.baykoreans.net/drama", "videoCategories", '')
    #addDir("드라마", " ", "dramaDate", '')
    addDir("예능/오락", " ", "varietyDate", '')
    addDir("시사/다큐", " ", "docuDate", '')
    addDir("기분 좋은 날", "http://baykoreans.net/index.php?mid=current&search_target=title&search_keyword=%EA%B8%B0%EB%B6%84%EC%A2%8B%EC%9D%80%EB%82%A0", 'videoCategoryContent', "")
    addDir("스포츠", "http://drama.baykoreans.net/sports", "EntCategoryContent", '')

#    addDir("영화", "http://drama.baykoreans.net/movie", "EntCategoryContent", '')
#    addDir("세바퀴", "http://drama.baykoreans.net/?act=&vid=&mid=entertain&category=19114892319082&search_target=title&search_keyword=세바퀴", "EntCategoryContent", '')
#    addDir("시사/다큐", "http://baykoreans.net/current", "videoCategories", '')
#    addDir("영화", "http://baykoreans.net/movie", "MovieCategories", '')  

def listdramaDate():
    addDir("최근 방영", "http://drama.baykoreans.net/drama", "videoCategories", '') 
    addDir("월요일", "http://live.hanindisk.com/tv_chart.php?week_day=2", "dramaCategories", '')  
    addDir("화요일", "http://live.hanindisk.com/tv_chart.php?week_day=3", "dramaCategories", '')
    addDir("수요일", "http://live.hanindisk.com/tv_chart.php?week_day=4", "dramaCategories", '')
    addDir("목요일", "http://live.hanindisk.com/tv_chart.php?week_day=5", "dramaCategories", '')
    addDir("금요일", "http://live.hanindisk.com/tv_chart.php?week_day=6", "dramaCategories", '')
    addDir("토요일", "http://live.hanindisk.com/tv_chart.php?week_day=7", "dramaCategories", '')
    addDir("일요일", "http://live.hanindisk.com/tv_chart.php?week_day=1", "dramaCategories", '')

def listvarietyDate():
    addDir("최근 방영", "http://drama.baykoreans.net/entertain", "EntCategoryContent", '') 
    addDir("월요일", "http://live.hanindisk.com/tv_chart.php?week_day=2", "varietyCategories", '')  
    addDir("화요일", "http://live.hanindisk.com/tv_chart.php?week_day=3", "varietyCategories", '')
    addDir("수요일", "http://live.hanindisk.com/tv_chart.php?week_day=4", "varietyCategories", '')
    addDir("목요일", "http://live.hanindisk.com/tv_chart.php?week_day=5", "varietyCategories", '')
    addDir("금요일", "http://live.hanindisk.com/tv_chart.php?week_day=6", "varietyCategories", '')
    addDir("토요일", "http://live.hanindisk.com/tv_chart.php?week_day=7", "varietyCategories", '')
    addDir("일요일", "http://live.hanindisk.com/tv_chart.php?week_day=1", "varietyCategories", '')

def listdocuDate():
    addDir("최근 방영", "http://drama.baykoreans.net/current", "EntCategoryContent", '') 
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
        req.add_header('User-Agent', _header)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        match=re.compile('<option value="(.+?)" > (.+?)</option>').findall(link)

        addDir("최근 방영", "http://drama.baykoreans.net/drama", "EntCategoryContent", '')
        
        for i in range(len(match)):
	    dramaurl = 'http://drama.baykoreans.net/index.php?mid=drama&category=' + match[i][0]
            match[i] = (dramaurl, match[i][1])

        
        for url, name in match:
            addDir(name, url, 'videoCategoryContent', "")
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
                
def listVideosInCategory(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        match=re.compile('<img src="(.*?)" alt.*?>\n.*?</div>\n.*?</a>\n.*?</div>\n\t\t\t\t\t\t.*?\n.*?\n.*?\n.*?\n.*?<p class="title">\n.*?<a href=".+?mid=(.+?)\&.+?document_srl=(.+?)" class="title" >(.*?)</a>').findall(link)
        
        for i in range(len(match)):
            playurl = 'http://drama.baykoreans.net/' + match[i][1] +'/' + match[i][2]
            match[i] = (playurl, unicode(match[i][3], 'utf-8'), match[i][0])
    
        for url, title, thumbnail, in match:
            addDir(title, url, 'listvideourl2', thumbnail)
        
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
#            addDir("1 페이지", baseurl, 'videoCategoryContent', "")
#            for url, name in match2:
#                addDir(name, url, 'videoCategoryContent', "")

    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
   
def listvideourl(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')        
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()

        dmotion=re.compile('<a href="http://baykoreans.com/dmotion/\?xink=(.+?)" class=".*?" target=".*?"><span>(.+?) \| BayKoreans.com</span>').findall(link) 
        for url, title, in dmotion:
            addLink(title, url, 'playVideo', "")

        tudou=re.compile('<a href="baykoreans.com/tudou.y/\?xink=(.+?)" class="button black xLarge" target="_blank"><span>').findall(link)
        for url, title, in tudou:
            addLink(title, url, 'resolveAndPlayVideo', "")
        
        #tudou2=re.compile('<a href="http://baykoreans.com/tudou.y/\?xink=(.+?)" class="button black xLarge" target="_blank"><span>(.+?) \|').findall(link)
        #for i in range(len(dmotion)):
        #    tudou2_url = "http://vr.tudou.com/v2proxy/v2?it=%s&st=52&pw=" + tudou2[i][0]
        #    tudou2[i] = (tudou2_url, tudou2[i][1])
        #for url, title, in tudou2:
        #    addLink(title, url, 'resolveAndPlayVideo', "")
            

    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def playVideo(url):
    listitem = xbmcgui.ListItem(path=getStreamUrl(url))
    xbmcplugin.setResolvedUrl(_thisPlugin, True, listitem)


def getStreamUrl(url):
    content = getUrl2('http://www.dailymotion.com/embed/video/'+url)
    if content.find('"statusCode":410') > 0 or content.find('"statusCode":403') > 0:
        xbmc.executebuiltin('XBMC.Notification(Info:,'+translation(30022)+' (DailyMotion)!,5000)')
        return ""
    
    else:
        get_json_code = re.compile(r'dmp\.create\(document\.getElementById\(\'player\'\),\s*(\{.*?)"\}\]\}.*\}\);').findall(content)[0]
        get_json_code += '"}]}}}'
        print get_json_code
        cc= json.loads(get_json_code)['metadata']['qualities']  #['380'][0]['url']
        print cc
        if '1080' in cc.keys():
            #print 'found hd'
            return cc['1080'][0]['url']
        elif '720' in cc.keys():
            return cc['720'][0]['url']
        elif '480' in cc.keys():
            return cc['480'][0]['url']
        elif '380' in cc.keys():
            return cc['380'][0]['url']
        elif '240' in cc.keys():
            return cc['240'][0]['url']
        elif 'auto' in cc.keys():
            return cc['auto'][0]['url']
        else:
            xbmc.executebuiltin('XBMC.Notification(Info:, No playable Link found (DailyMotion)!,5000)')

def getUrl2(url):

    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
    req.add_header('Cookie', 'language=kr') 
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link

##
##def resolveAndPlayVideo(url):
##    try:
##        quality = '2'
##        info = getVideoInfo(url, quality=quality, resolve_redirects=True)
##        
##        if info:
##            streams = info.streams()
##            plugin.log.debug("num of streams: %d" % len(streams))
##            from xbmcswift2 import xbmc, xbmcgui
##            pl = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
##            pl.clear()
##            for stream in streams:
##                li = xbmcgui.ListItem(stream['title'], iconImage="DefaultVideo.png")
##                li.setInfo( 'video', { "Title": stream['title'] } )
##                pl.add(stream['xbmc_url'], li)
##
##            #xbmc.Player().play(pl)
##
##            xbmcplugin.setResolvedUrl(_thisPlugin, True, li)
##        else:
##            plugin.log.warning('Fail to extract')
##            plugin.play_video({'path':url, 'is_playable':True})
##            
##    except urllib2.URLError:
##        addLink("성용이를 불러주세용.", '', '', '')

def listRecentCategories(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        match=re.compile('<img src="(.*?)" alt="" />\n.*?</div>\n.*?</a>\n.*?</div>\n\t\t\t\t\t\t.*?\n.*?\n.*?\n.*?\n.*?<p class="title">\n.*?<a href="/(.*?)/(.*?)" class="title" >(.*?)</a>').findall(link)
        
        for i in range(len(match)):
            playVideoUrl = 'http://drama.baykoreans.net/' + match[i][1] + '/' + match[i][2]
            match[i] = (playVideoUrl, unicode(match[i][3], 'utf-8'), match[i][0])
    
        for url, title, thumbnail, in match:
            addDir(title, url, 'listvideourl2', thumbnail)
        
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
#            addDir("1 페이지", baseurl, 'videoCategoryContent', "")
#            for url, name in match2:
#                addDir(name, url, 'videoCategoryContent', "")

    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')        

def listEntInCategory(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        match=re.compile('<p class="title">\n.*?<a href="/(.*?)/(.*?)" class=.*?>(.*?)</a>').findall(link)
        #match=re.compile('<p class="title">\n.*?<a href=".+?mid=(.+?)\&.+?document_srl=(.+?)" class="title" >(.*?)</a>').findall(link)
        
        for i in range(len(match)):
            playVideoUrl = 'http://drama.baykoreans.net/' + match[i][0] + '/' + match[i][1]
            match[i] = (playVideoUrl, unicode(match[i][2], 'utf-8'))
    
        for url, title in match:
            addDir(title, url, 'listvideourl2', "")

        
        match2=re.compile('page=([0-9]+)">[0-9]+</a>').findall(link)
        match3=re.compile('<a href="/(.+?)" class="prevEnd"').findall(link)
        baseurl = 'http://baykoreans.net/index.php?mid=' + match3[0]
        
        addDir("1 페이지", baseurl, 'videoCategoryContent', "")
        
        if match2:
            for i in range(len(match2)):
                Pgurl = baseurl + '&page=' + match2[i]
                Pgname = match2[i] + ' 페이지'
                match2[i] = (Pgurl, Pgname)
                
        
            for url, name in match2:
                addDir(name, url, 'videoCategoryContent', "")

        print match2
        
        

    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
###########################

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
	    videourl = 'http://baykoreans.net/index.php?vid=category&mid=drama&search_target=title&search_keyword=' + match[i][1]
	    title = unicode(match[i][1], 'utf-8') + unicode(match[i][2], 'utf-8') + unicode(match[i][3], 'utf-8')
            match[i] = (title, videourl)
        
        for name, url in match:
            addDir(name, url, 'videoCategoryContent', '')
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
	    videourl = 'http://baykoreans.net/?act=&vid=&mid=entertain&category=&search_target=title&search_keyword=' + match[i][1]
	    title = unicode(match[i][1], 'utf-8') + unicode(match[i][2], 'utf-8') + unicode(match[i][3], 'utf-8')
            match[i] = (title, videourl)
        
        for name, url in match:
            addDir(name, url, 'videoCategoryContent', '')
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
	    videourl = 'http://baykoreans.net/?act=&vid=&mid=current&category=&search_target=title&search_keyword=' + match[i][1]
	    title = unicode(match[i][1], 'utf-8') + unicode(match[i][2], 'utf-8') + unicode(match[i][3], 'utf-8')
            match[i] = (title, videourl)
        
        for name, url in match:
            addDir(name, url, 'videoCategoryContent', '')
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
        
##def listEntUrl(url):
##    try:
##        req = urllib2.Request(url)
##        req.add_header('User-Agent', _header)
##        req.add_header('Accept-Langauge', 'ko')
##        req.add_header('Cookie', 'language=kr')        
##        response = urllib2.urlopen(req, timeout = _connectionTimeout)
##        link=response.read()
##        response.close()
##
##        dmotion=re.compile('<a href="http://baykoreans.com/.+?/\?xink=(.+?)" class').findall(link)
##        for i in range(len(dmotion)):
##            dmotion_url = 'http://www.dailymotion.com/video/'+dmotion[i]
##            dmotion[i] = (dmotion_url, 'DMOTION')
##        for url, title, in dmotion:
##            addLink(title, url, 'resolveAndPlayVideo', "")
##
##        tudou=re.compile('<a href="baykoreans.com/tudou.y/\?xink=(.+?)" class="button black xLarge" target="_blank"><span>').findall(link)
##        for url, title, in tudou:
##            addLink(title, url, 'resolveAndPlayVideo', "")    
##    except urllib2.URLError:
##        addLink("성용이를 불러주세용.", '', '', '')
        
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
    elif params["mode"] == 'videoCategoryContent':
        listVideosInCategory(urlUnquoted)
    elif params["mode"] == 'resolveAndPlayVideo':
        resolveAndPlayVideo(urlUnquoted)
    elif params["mode"] == 'RecentCategories':
        listRecentCategories(urlUnquoted)
    elif params["mode"] == 'EntCategoryContent':
        listEntInCategory(urlUnquoted)
##    elif params["mode"] == 'listEntUrl2':
##        listEntUrl(urlUnquoted)
    elif params["mode"] == 'resolveAndPlayMovie':
        resolveAndPlayMovie(urlUnquoted)
    elif params["mode"] == 'listvideourl2':
        listvideourl(urlUnquoted)

    elif params["mode"] == 'SearchedContent':
        listSearchedCategories(urlUnquoted)

    elif params["mode"] == 'playVideo':
        playVideo(urlUnquoted)

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
