# -*- coding: utf-8 -*-
"""
    KR Live
"""

import os
import xbmcplugin, xbmcgui, sys
import urllib2, urllib, re, cookielib
from BeautifulSoup import BeautifulSoup

username = 'anonymous'
password = 'anonymous'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'mode' : 'login_now', 'Login_id' : username, 'Login_passwd' : password})
opener.open('http://live.hanindisk.com/login_check.php', login_data)

# magic; id of this plugin's instance - cast to integer
_pluginName = (sys.argv[0])
_thisPlugin = int(sys.argv[1])
_connectionTimeout = 20
_header = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

def listMainCategories():
    addDir("최근 방영", "http://live.hanindisk.com/tv_list.php?cate=1", "RecentCategories", '')  
    addDir("드라마", " ", "dramaDate", '')
    addDir("예능/오락", " ", "varietyDate", '')
    addDir("시사/다큐", " ", "docuDate", '')
    addDir("스포츠", " ", "sportsDate", '')
    addDir("뉴스", " ", "newsDate", '')
    addDir("케이블", " ", "cableDate", '')

def listRecentCategories(url):
    try:

        resp = opener.open(url)
        link = resp.read()
        resp.close()
        soup=BeautifulSoup(link)

        #match=re.compile('<A href="./tv_view.php\?title=(.*?)"><.*? src="http://haninlive.com/scrshot/(.*?)/(.+?)"></A>\r\n\t\t\t\t\t\t\t<H3><A href=".*?">(.*?)</A> <span class=\'numb\'>(.*?)</span>').findall(link)
        match=re.compile('<A href="./(.*?)"><.*? src=".*?"></A>\r\n\t\t\t\t\t\t\t<H3><A href=".*?">(.*?)</A> <span class=\'numb\'>(.*?)</span></H3>\r\n\t\t\t\t\t\t\t<P>.*?</P>\r\n\t\t\t\t\t\t\t<P>\xb9\xe6\xbf\xb5\xc0\xcf\xc0\xda : (.*?) </P>').findall(link)
        
        for i in range(len(match)):
            dramaurl = 'http://live.hanindisk.com/' + match[i][0]
	    Title = unicode(match[i][1], 'euc-kr') + ' : ' + unicode(match[i][2], 'euc-kr') + ' - ' + unicode(match[i][3], 'euc-kr')
            match[i] = (Title, dramaurl)

        #match.sort(reverse=True)
        
        for title, url in match:
            addLink(title, url, 'resolveAndPlayVideo', '')

        page = soup.find('ul', {'class': 'paginate'})
        match2=re.compile('<a href="(.*?)" class="page_link"><span class="on">(.+?)</span>').findall(str(page))
        if match2:
            for i in range(len(match2)):
                Pgurl = 'http://live.hanindisk.com/tv_list.php?cate=1\&page=' + match2[i][1]
                Pgname = match2[i][1] + ' 페이지'
                match2[i] = (Pgurl, Pgname)
                
            for url, name in match2:
                addDir(name, url, 'RecentCategories', '')

    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def listRecentCategories2(url):
    try:

        resp = opener.open(url)
        link = resp.read()
        resp.close()
        soup=BeautifulSoup(link)

        #match=re.compile('<A href="./tv_view.php\?title=(.*?)"><.*? src="http://haninlive.com/scrshot/(.*?)/(.+?)"></A>\r\n\t\t\t\t\t\t\t<H3><A href=".*?">(.*?)</A> <span class=\'numb\'>(.*?)</span>').findall(link)
        match=re.compile('<A href="./(.*?)"><.*? src=".*?"></A>\r\n\t\t\t\t\t\t\t<H3><A href=".*?">(.*?)</A> <span class=\'numb\'>.*?</span></H3>\r\n\t\t\t\t\t\t\t<P>.*?</P>\r\n\t\t\t\t\t\t\t<P>\xb9\xe6\xbf\xb5\xc0\xcf\xc0\xda : (.*?) </P>').findall(link)
        
        for i in range(len(match)):
            dramaurl = 'http://live.hanindisk.com/' + match[i][0]
	    Title = unicode(match[i][1], 'euc-kr') + ' : ' + unicode(match[i][2], 'euc-kr')
            match[i] = (Title, dramaurl)

        #match.sort(reverse=True)
        
        for title, url in match:
            addLink(title, url, 'resolveAndPlayVideo', '')

        page = soup.find('ul', {'class': 'paginate'})
        match2=re.compile('<a href=\'(.*?)\' class=\'page_link\'><SPAN class=\'on\'>(.*?)</SPAN>').findall(link)

        if match2:
            for i in range(len(match2)):
                Pgurl = 'http://live.hanindisk.com/' + match2[i][0]
                Pgname = match2[i][1] + ' 페이지'
                match2[i] = (Pgurl, Pgname)
                
            for url, name in match2:
                addDir(name, url, 'RecentCategories2', '')
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
        
def listdramaDate():
    addDir("월요일", "http://live.hanindisk.com/tv_chart.php?week_day=2", "dramaCategories", '')  
    addDir("화요일", "http://live.hanindisk.com/tv_chart.php?week_day=3", "dramaCategories", '')
    addDir("수요일", "http://live.hanindisk.com/tv_chart.php?week_day=4", "dramaCategories", '')
    addDir("목요일", "http://live.hanindisk.com/tv_chart.php?week_day=5", "dramaCategories", '')
    addDir("금요일", "http://live.hanindisk.com/tv_chart.php?week_day=6", "dramaCategories", '')
    addDir("토요일", "http://live.hanindisk.com/tv_chart.php?week_day=7", "dramaCategories", '')
    addDir("일요일", "http://live.hanindisk.com/tv_chart.php?week_day=1", "dramaCategories", '')

def listvarietyDate():
    addDir("최근 방영", "http://live.hanindisk.com/tv_list.php?cate=2", "RecentCategories2", '') 
    addDir("월요일", "http://live.hanindisk.com/tv_chart.php?week_day=2", "varietyCategories", '')  
    addDir("화요일", "http://live.hanindisk.com/tv_chart.php?week_day=3", "varietyCategories", '')
    addDir("수요일", "http://live.hanindisk.com/tv_chart.php?week_day=4", "varietyCategories", '')
    addDir("목요일", "http://live.hanindisk.com/tv_chart.php?week_day=5", "varietyCategories", '')
    addDir("금요일", "http://live.hanindisk.com/tv_chart.php?week_day=6", "varietyCategories", '')
    addDir("토요일", "http://live.hanindisk.com/tv_chart.php?week_day=7", "varietyCategories", '')
    addDir("일요일", "http://live.hanindisk.com/tv_chart.php?week_day=1", "varietyCategories", '')

def listdocuDate():
    addDir("최근 방영", "http://live.hanindisk.com/tv_list.php?cate=3", "RecentCategories2", '') 
    addDir("월요일", "http://live.hanindisk.com/tv_chart.php?week_day=2", "docuCategories", '')  
    addDir("화요일", "http://live.hanindisk.com/tv_chart.php?week_day=3", "docuCategories", '')
    addDir("수요일", "http://live.hanindisk.com/tv_chart.php?week_day=4", "docuCategories", '')
    addDir("목요일", "http://live.hanindisk.com/tv_chart.php?week_day=5", "docuCategories", '')
    addDir("금요일", "http://live.hanindisk.com/tv_chart.php?week_day=6", "docuCategories", '')
    addDir("토요일", "http://live.hanindisk.com/tv_chart.php?week_day=7", "docuCategories", '')
    addDir("일요일", "http://live.hanindisk.com/tv_chart.php?week_day=1", "docuCategories", '')

def listsportsDate():
    addDir("최근 방영", "http://live.hanindisk.com/tv_list.php?cate=6", "RecentCategories2", '') 
    addDir("월요일", "http://live.hanindisk.com/tv_chart.php?week_day=2", "sportsCategories", '')  
    addDir("화요일", "http://live.hanindisk.com/tv_chart.php?week_day=3", "sportsCategories", '')
    addDir("수요일", "http://live.hanindisk.com/tv_chart.php?week_day=4", "sportsCategories", '')
    addDir("목요일", "http://live.hanindisk.com/tv_chart.php?week_day=5", "sportsCategories", '')
    addDir("금요일", "http://live.hanindisk.com/tv_chart.php?week_day=6", "sportsCategories", '')
    addDir("토요일", "http://live.hanindisk.com/tv_chart.php?week_day=7", "sportsCategories", '')
    addDir("일요일", "http://live.hanindisk.com/tv_chart.php?week_day=1", "sportsCategories", '')

def listnewsDate():
    addDir("최근 방영", "http://live.hanindisk.com/tv_list.php?cate=4", "RecentCategories2", '') 
    addDir("월요일", "http://live.hanindisk.com/tv_chart.php?week_day=2", "newsCategories", '')  
    addDir("화요일", "http://live.hanindisk.com/tv_chart.php?week_day=3", "newsCategories", '')
    addDir("수요일", "http://live.hanindisk.com/tv_chart.php?week_day=4", "newsCategories", '')
    addDir("목요일", "http://live.hanindisk.com/tv_chart.php?week_day=5", "newsCategories", '')
    addDir("금요일", "http://live.hanindisk.com/tv_chart.php?week_day=5", "newsCategories", '')
    addDir("토요일", "http://live.hanindisk.com/tv_chart.php?week_day=6", "newsCategories", '')
    addDir("일요일", "http://live.hanindisk.com/tv_chart.php?week_day=7", "newsCategories", '')

def listcableDate():
    addDir("최근 방영", "http://live.hanindisk.com/tv_list.php?cate=5", "RecentCategories2", '') 
    addDir("월요일", "http://live.hanindisk.com/tv_chart.php?week_day=2", "cableCategories", '')  
    addDir("화요일", "http://live.hanindisk.com/tv_chart.php?week_day=3", "cableCategories", '')
    addDir("수요일", "http://live.hanindisk.com/tv_chart.php?week_day=4", "cableCategories", '')
    addDir("목요일", "http://live.hanindisk.com/tv_chart.php?week_day=5", "cableCategories", '')
    addDir("금요일", "http://live.hanindisk.com/tv_chart.php?week_day=6", "cableCategories", '')
    addDir("토요일", "http://live.hanindisk.com/tv_chart.php?week_day=7", "cableCategories", '')
    addDir("일요일", "http://live.hanindisk.com/tv_chart.php?week_day=1", "cableCategories", '')



def resolveAndPlayVideo(url):
    try:
        resp = opener.open(url)
        link = resp.read()
        resp.close()
        
        match=re.compile('http://haninlive.com/weblink/\'\+m_type\+\'/(.*?)\'').search(link).group(1)
##        match2=re.compile('576').findall(link)
##        if match2:
##            url='http://haninlive.com/weblink/576/' +match
##        else:
##            url='http://haninlive.com/weblink/352/' + match
        url='http://haninlive.com/moblink/' + match
        url2=url.replace('flv','mp4')
        
        listItem = xbmcgui.ListItem(path=str(url2))
        listItem.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)

    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
        
def listvideoInCategory(url):
    try:
        resp = opener.open(url)
        link = resp.read()
        resp.close()
        
        match=re.compile('<A href="./(.*?)"><.*? src=".*?"></A>\r\n\t\t\t\t\t\t\t<H3><A href=".*?">(.*?)</A> <span class=\'numb\'>(.*?)</span></H3>\r\n\t\t\t\t\t\t\t<P>.*?</P>\r\n\t\t\t\t\t\t\t<P>\xb9\xe6\xbf\xb5\xc0\xcf\xc0\xda : (.*?) </P>').findall(link)
   
        for i in range(len(match)):
            dramaurl = 'http://live.hanindisk.com/' + match[i][0]
            title = unicode(match[i][1], 'euc-kr') + ' : ' + unicode(match[i][2], 'euc-kr') + ' - ' + unicode(match[i][3], 'euc-kr')
            match[i] = (title, dramaurl)
    
        for title, url, in match:
            addLink(title, url, 'resolveAndPlayVideo', '')

        match2=re.compile('<a href=\'(.*?)\' class=\'page_link\'><SPAN class=\'on\'>(.*?)</SPAN>').findall(link)

        if match2:
            for i in range(len(match2)):
                Pgurl = 'http://live.hanindisk.com/' + match2[i][0]
                Pgname = match2[i][1] + ' 페이지'
                match2[i] = (Pgurl, Pgname)
                
            for url, name in match2:
                addDir(name, url, 'videoCategoryContent', '')


    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def listvideoInCategory2(url):
    try:
        resp = opener.open(url)
        link = resp.read()
        resp.close()
        
        match=re.compile('<A href="./(.*?)"><.*? src=".*?"></A>\r\n\t\t\t\t\t\t\t<H3><A href=".*?">(.*?)</A> <span class=\'numb\'>.*?</span></H3>\r\n\t\t\t\t\t\t\t<P>.*?</P>\r\n\t\t\t\t\t\t\t<P>\xb9\xe6\xbf\xb5\xc0\xcf\xc0\xda : (.*?) </P>').findall(link)
   
        for i in range(len(match)):
            dramaurl = 'http://live.hanindisk.com/' + match[i][0]
            title = unicode(match[i][1], 'euc-kr') + ' - ' + unicode(match[i][2], 'euc-kr')
            match[i] = (title, dramaurl)
    
        for title, url, in match:
            addLink(title, url, 'resolveAndPlayVideo', '')

        match2=re.compile('<a href=\'(.*?)\' class=\'page_link\'><SPAN class=\'on\'>(.*?)</SPAN>').findall(link)

        if match2:
            for i in range(len(match2)):
                Pgurl = 'http://live.hanindisk.com/' + match2[i][0]
                Pgname = match2[i][1] + ' 페이지'
                match2[i] = (Pgurl, Pgname)
                
            for url, name in match2:
                addDir(name, url, 'videoCategoryContent2', '')


    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
        
def listdramaCategories(url):
    try:
        resp = opener.open(url)
        link = resp.read()
        resp.close()
        soup=BeautifulSoup(link)
        
        table = soup.findAll('table')
        video = table[0]
        match=re.compile('<a href="./(.*?)">(.*?)</a>(.*?)<span>(.*?)</span>').findall(str(video))
             
        for i in range(len(match)):
	    videourl = 'http://live.hanindisk.com/' + match[i][0]
	    title = unicode(match[i][1], 'utf-8') + unicode(match[i][2], 'utf-8') + unicode(match[i][3], 'utf-8')
            match[i] = (title, videourl)
        
        for name, url in match:
            addDir(name, url, 'videoCategoryContent', '')
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
        

   
def listvarietyCategories(url):
    try:
        resp = opener.open(url)
        link = resp.read()
        resp.close()
        soup=BeautifulSoup(link)
        
        table = soup.findAll('table')
        video = table[1]
        match=re.compile('<a href="./(.*?)">(.*?)</a>(.*?)<span>(.*?)</span>').findall(str(video))
             
        for i in range(len(match)):
	    videourl = 'http://live.hanindisk.com/' + match[i][0]
	    title = unicode(match[i][1], 'utf-8') + unicode(match[i][2], 'utf-8') + unicode(match[i][3], 'utf-8')
            match[i] = (title, videourl)
        
        for name, url in match:
            addDir(name, url, 'videoCategoryContent2', '')
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
        
def listdocuCategories(url):
    try:
        resp = opener.open(url)
        link = resp.read()
        resp.close()
        soup=BeautifulSoup(link)
        
        table = soup.findAll('table')
        video = table[2]
        match=re.compile('<a href="./(.*?)">(.*?)</a>(.*?)<span>(.*?)</span>').findall(str(video))
             
        for i in range(len(match)):
	    videourl = 'http://live.hanindisk.com/' + match[i][0]
	    title = unicode(match[i][1], 'utf-8') + unicode(match[i][2], 'utf-8') + unicode(match[i][3], 'utf-8')
            match[i] = (title, videourl)
        
        for name, url in match:
            addDir(name, url, 'videoCategoryContent2', '')
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
        
def listnewsCategories(url):
    try:
        resp = opener.open(url)
        link = resp.read()
        resp.close()
        soup=BeautifulSoup(link)
        
        table = soup.findAll('table')
        video = table[3]
        match=re.compile('<a href="./(.*?)">(.*?)</a>(.*?)<span>(.*?)</span>').findall(str(video))
             
        for i in range(len(match)):
	    videourl = 'http://live.hanindisk.com/' + match[i][0]
	    title = unicode(match[i][1], 'utf-8') + unicode(match[i][2], 'utf-8') + unicode(match[i][3], 'utf-8')
            match[i] = (title, videourl)
        
        for name, url in match:
            addDir(name, url, 'videoCategoryContent2', '')
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def listsportsCategories(url):
    try:
        resp = opener.open(url)
        link = resp.read()
        resp.close()
        soup=BeautifulSoup(link)
        
        table = soup.findAll('table')
        video = table[5]
        match=re.compile('<a href="./(.*?)">(.*?)</a>(.*?)<span>(.*?)</span>').findall(str(video))
             
        for i in range(len(match)):
	    videourl = 'http://live.hanindisk.com/' + match[i][0]
	    title = unicode(match[i][1], 'utf-8') + unicode(match[i][2], 'utf-8') + unicode(match[i][3], 'utf-8')
            match[i] = (title, videourl)
        
        for name, url in match:
            addDir(name, url, 'videoCategoryContent2', '')
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def listcableCategories(url):
    try:
        resp = opener.open(url)
        link = resp.read()
        resp.close()
        soup=BeautifulSoup(link)
        
        table = soup.findAll('table')
        video = table[4]
        match=re.compile('<a href="./(.*?)">(.*?)</a>(.*?)<span>(.*?)</span>').findall(str(video))
             
        for i in range(len(match)):
	    videourl = 'http://live.hanindisk.com/' + match[i][0]
	    title = unicode(match[i][1], 'utf-8') + unicode(match[i][2], 'utf-8') + unicode(match[i][3], 'utf-8')
            match[i] = (title, videourl)
        
        for name, url in match:
            addDir(name, url, 'videoCategoryContent2', '')
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
    elif params["mode"] == 'videoCategoryContent':
        listvideoInCategory(urlUnquoted)
    elif params["mode"] == 'videoCategoryContent2':
        listvideoInCategory2(urlUnquoted)
    elif params["mode"] == 'resolveAndPlayVideo':
        resolveAndPlayVideo(urlUnquoted)

    elif params["mode"] == 'dramaDate':
        listdramaDate()  
    elif params["mode"] == 'varietyDate':
        listvarietyDate()
    elif params["mode"] == 'docuDate':
        listdocuDate()
    elif params["mode"] == 'newsDate':
        listnewsDate()
    elif params["mode"] == 'cableDate':
        listcableDate()
    elif params["mode"] == 'sportsDate':
        listsportsDate()
        
    elif params["mode"] == 'dramaCategories':
        listdramaCategories(urlUnquoted)   
    elif params["mode"] == 'varietyCategories':
        listvarietyCategories(urlUnquoted)
    elif params["mode"] == 'docuCategories':
        listdocuCategories(urlUnquoted)
    elif params["mode"] == 'sportsCategories':
        listsportsCategories(urlUnquoted)
    elif params["mode"] == 'newsCategories':
        listnewsCategories(urlUnquoted)
    elif params["mode"] == 'cableCategories':
        listcableCategories(urlUnquoted)
    elif params["mode"] == 'RecentCategories':
        listRecentCategories(urlUnquoted)
    elif params["mode"] == 'RecentCategories2':
        listRecentCategories2(urlUnquoted)
        
xbmcplugin.endOfDirectory(_thisPlugin)        
