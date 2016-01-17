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

##채널 이름##
ad=['','','KBS N Sorts','SBS Sports','MBC Sports+','','','','','','','','','','','','','','','','']

def listMainCategories():
    addDir("하이라이트", " ", "vod", '')
    addDir("생방송", " ", "live", '')

def vod():
    url='http://sports.media.daum.net/rf/534b6e671652d99818d84ad0.json?callback=LegoLeagueInfoCallback'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    league=re.compile('"userId" : "(.*?)" , "userName" : "(.*?)"').findall(link)

    for i in range(len(league)):
        url='http://sports.media.daum.net/ronaldo/gallery/list.json?callback=VideoCallback&category-code='+league[i][0]
        league[i] = (league[i][1], url)
        
    for name, url in league:
        addDir(name, url, 'league', '')

def live():
    addDir("고화질", " ", "High", '')  
    addDir("중화질", " ", "Med", '')
    addDir("저화질", " ", "Low", '')
    addDir("티비", " ", "livetv", '')
    
def livetv():
    addLink('SBS', 'rtmp://rtmpplay3.idol001.com/live/korea_sbs', 'livetvplay', '')
    addLink('MBC', 'rtmp://rtmpplay2.idol001.com/live/korea_mbc', 'livetvplay', '')
    addLink('KBS1', 'rtmp://rtmpplay3.idol001.com/live/korea_kbs1', 'livetvplay', '')
    addLink('KBS2', 'rtmp://rtmpplay3.idol001.com/live/korea_kbs2', 'livetvplay', '')
    addLink('JTBC', 'rtmp://rtmpplay3.idol001.com/live/korea_jtbc', 'livetvplay', '')
    addLink('ONSTYLE', 'rtmp://rtmpplay3.idol001.com/live/korea_onstyle', 'livetvplay', '')
    addLink('MBC MUSIC', 'rtmp://rtmpplay3.idol001.com/live/korea_mbcmusic', 'livetvplay', '')
    addLink('Mnet', 'rtmp://rtmpplay3.idol001.com/live/korea_mnet', 'livetvplay', '')
    addLink('TVN', 'rtmp://rtmpplay3.idol001.com/live/korea_tvn', 'livetvplay', '')
    addLink('arirang', 'rtmp://rtmpplay3.idol001.com/live/korea_arirang', 'livetvplay', '')
    addLink('SBS MTV', 'rtmp://rtmpplay3.idol001.com/live/korea_sbsmtv', 'livetvplay', '')
    addLink('MBC everyone', 'rtmp://rtmpplay3.idol001.com/live/korea_mbcevery1', 'livetvplay', '')

def league(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    match=re.compile('"home_team_name":"(.*?)","away_team_name":"(.*?)".*?"game_time":"([0-9]+)".*?"game_id":"(.*?)"').findall(link)

    for i in range(len(match)):
        l = str(match[i][2])
        date=l[:4]+'/'+ l[4:6]+'/'+l[6:8]
        title=match[i][0]+' vs. '+match[i][1] + ' - ' +date
        url='http://sports.media.daum.net/proxy/ronaldo/gallery/view.json?game-id='+match[i][3]
        match[i] = (unicode(title, 'utf-8'), url)


    for name, url in match:
        addDir(name, url, 'vodlist', '')

    if len(match)<1:
        match=re.compile('galleryList":\[{"id":"(.*?)"').search(link).group(1)
        match2=re.compile('game_id":"1"}},{"id":"(.*?)"').findall(link)

        a=list(match2)
        a.insert(0,match)

        b=re.compile('"game_name":"(.*?)"').findall(link)
        d=re.compile('game_start_time":"([0-9]+)"').findall(link)

        c=zip(b, a, d)

        for i in range(len(c)):
            l= str(c[i][2])[:4]+'/'+ str(c[i][2])[4:6]+'/'+str(c[i][2])[6:8]
            title=c[i][0]+' - '+l
            url='http://sports.media.daum.net/ronaldo/gallery/view.json?callback=videoGalleryCallback&id='+c[i][1]
            c[i] = (unicode(title, 'utf-8'), url)

        for name, url in c:
            addDir(name, url, 'vodlist', '')
 
def vodlist(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    match=re.compile('"vid":"(.*?)","title":"(.*?)","thumbnailUrl":"(.*?)"').findall(link)

    for i in range(len(match)):
        url='http://videofarm.daum.net/controller/api/open/v1_5/MovieLocation.apixml?vid='+match[i][0]+'&profile=HIGH'
        match[i] = (unicode(match[i][1], 'utf-8'), url, match[i][2])
        
    match.sort()
    
    for name, url,thumbnail in match:
        addLink(name, url, 'resolveAndPlayVod', thumbnail)


def resolveAndPlayVod(url):
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

        match=re.compile('<url><\!\[CDATA\[(.*?)\]\]></url>').search(link).group(1)
    
        listItem = xbmcgui.ListItem(path=str(match))
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
            
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
    
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
            
        addDir('네이버 생방송 목록',' ','High_Live', '')
        addLink('##이하 다음 생중계##',' ','', '')
        
        ## daum ##
        url='http://live.tvpot.daum.net/potplayer/service/LiveTimeTable.do'
        req = urllib2.Request(url)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        link = urllib2.urlopen(req).read()
        soup=BeautifulSoup(link)
        
        items = []
        for node in soup.findAll('li', {'class':'on'}):
            if not node.span:
                continue
            time=node.span.string
            title = node.find('a', {'class': 'link_live cast_title'}).string.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&#039;','\'')
            liveid = node.a['href']
            liveid=int(re.search(r'\d+', liveid).group())
            url='http://videofarm.daum.net/controller/api/open/v1_0/BroadcastStreams.action?broadcastId='+str(liveid)+'&profile=HIGH'
            items.append({'title':title, 'broad_date':time, 'url':url, 'thumbnail':''})
            items.sort(reverse=True)

        for i in range(len(items)):
            items[i] = (items[i]['title'], items[i]['url'])
              

        for name, url in items:
            addLink(name, url, 'resolveAndPlayVideoDaum', '')

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
            
        addDir('네이버 생방송 목록',' ','Med_Live', '')
        addLink('##이하 다음 생중계##',' ','', '')
        
        ## daum ##
        url='http://live.tvpot.daum.net/potplayer/service/LiveTimeTable.do'
        req = urllib2.Request(url)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        link = urllib2.urlopen(req).read()
        soup=BeautifulSoup(link)
        
        items = []
        for node in soup.findAll('li', {'class':'on'}):
            if not node.span:
                continue
            time=node.span.string
            title = node.find('a', {'class': 'link_live cast_title'}).string.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&#039;','\'')
            liveid = node.a['href']
            liveid=int(re.search(r'\d+', liveid).group())
            url='http://videofarm.daum.net/controller/api/open/v1_0/BroadcastStreams.action?broadcastId='+str(liveid)+'&profile=MAIN'
            items.append({'title':title, 'broad_date':time, 'url':url, 'thumbnail':''})
            items.sort(reverse=True)

        for i in range(len(items)):
            items[i] = (items[i]['title'], items[i]['url'])
              

        for name, url in items:
            addLink(name, url, 'resolveAndPlayVideoDaum', '')

        
            
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

        addDir('네이버 생방송 목록',' ','Low_Live', '')
        addLink('##이하 다음 생중계##',' ','', '')
        
        ## daum ##
        url='http://live.tvpot.daum.net/potplayer/service/LiveTimeTable.do'
        req = urllib2.Request(url)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        link = urllib2.urlopen(req).read()
        soup=BeautifulSoup(link)
        
        items = []
        for node in soup.findAll('li', {'class':'on'}):
            if not node.span:
                continue
            time=node.span.string
            title = node.find('a', {'class': 'link_live cast_title'}).string.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&#039;','\'')
            liveid = node.a['href']
            liveid=int(re.search(r'\d+', liveid).group())
            url='http://videofarm.daum.net/controller/api/open/v1_0/BroadcastStreams.action?broadcastId='+str(liveid)+'&profile=BASE'
            items.append({'title':title, 'broad_date':time, 'url':url, 'thumbnail':''})
            items.sort(reverse=True)

        for i in range(len(items)):
            items[i] = (items[i]['title'], items[i]['url'])
              

        for name, url in items:
            addLink(name, url, 'resolveAndPlayVideoDaum', '')

        
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def resolveAndPlayVideoDaum(url):
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        
        #match=re.compile('"rtsp":"(.*?)"').search(link).group(1)
        match=re.compile('"rtmp":"(.*?)"').search(link).group(1)
        listItem = xbmcgui.ListItem(path=str(match))
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
        
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
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
        
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def resolveAndPlayVideoLive(url):
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        
        listItem = xbmcgui.ListItem(path=str(link))
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
        
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
    

def livetvplay(url):
    try:
        listItem = xbmcgui.ListItem(path=str(url))
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
        
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
            if match == 'on':
                name='채널 '+str(i)
                link='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_2000.stream%2Fplaylist.m3u8'
                addLink(name, link, 'resolveAndPlayVideoLive', '')
                
        f=range(100,102)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highch'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)
            if match == 'on':
                name='채널 '+str(i)
                link='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_2000.stream%2Fplaylist.m3u8'
                addLink(name, link, 'resolveAndPlayVideoLive', '')

        f=range(200,212)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highch'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)
            
            if match == 'on':
                name='채널 '+str(i)
                link='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_2000.stream%2Fplaylist.m3u8'
                addLink(name, link, 'resolveAndPlayVideoLive', '')
                
        f=range(1,15)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highad'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)
                       
            if match == 'on':
                
                name='ad채널 '+str(i) +' '+ad[i]
                link='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad'+str(i)+'%2F_definst_%2Fad'+str(i)+'_2000.stream%2Fplaylist.m3u8'
                addLink(name, link, 'resolveAndPlayVideoLive', '')
      
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

            if match == 'on':
                name='채널 '+str(i)
                link='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_800.stream%2Fplaylist.m3u8'
                addLink(name, link, 'resolveAndPlayVideoLive', '')
                
        f=range(100,102)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highch'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)

            if match == 'on':
                name='채널 '+str(i)
                link='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_800.stream%2Fplaylist.m3u8'
                addLink(name, link, 'resolveAndPlayVideoLive', '')

        f=range(200,212)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highch'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)

            if match == 'on':
                name='채널 '+str(i)
                link='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_800.stream%2Fplaylist.m3u8'
                addLink(name, link, 'resolveAndPlayVideoLive', '')
                
        f=range(1,15)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highad'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)

            
            if match == 'on':
                name='ad채널 '+str(i) +' '+ad[i]
                link='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad'+str(i)+'%2F_definst_%2Fad'+str(i)+'_800.stream%2Fplaylist.m3u8'
                addLink(name, link, 'resolveAndPlayVideoLive', '')
      
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

            if match == 'on':
                link='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_300.stream%2Fplaylist.m3u8'
                name='채널 '+str(i)
                addLink(name, link, 'resolveAndPlayVideoLive', '')
                
        f=range(100,102)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highch'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)

            if match == 'on':
                link='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_300.stream%2Fplaylist.m3u8'
                name='채널 '+str(i)
                addLink(name, link, 'resolveAndPlayVideoLive', '')

        f=range(200,212)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highch'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)

          
            if match == 'on':
                link='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fch'+str(i)+'%2F_definst_%2Fch'+str(i)+'_300.stream%2Fplaylist.m3u8'
                name='채널 '+str(i)
                addLink(name, link, 'resolveAndPlayVideoLive', '')
                
        f=range(1,15)
        for i in f:
            url='http://cvapi.ncast.nhncorp.com/chStatus.nhn?chid=highad'+str(i)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('"status":"(.*?)"').search(link).group(1)

            
            if match == 'on':
                link='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2Fad'+str(i)+'%2F_definst_%2Fad'+str(i)+'_300.stream%2Fplaylist.m3u8'
                name='ad채널 '+str(i)  +' '+ad[i]
                addLink(name, link, 'resolveAndPlayVideoLive', '')
      
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
    if params["mode"] == 'vod':
        vod()
    elif params["mode"] == 'live':
        live()
    elif params["mode"] == 'livetv':
        livetv()        
    elif params["mode"] == 'High':
        High_list(urlUnquoted)
    elif params["mode"] == 'Med':
        Med_list(urlUnquoted)
    elif params["mode"] == 'Low':
        Low_list(urlUnquoted)
    elif params["mode"] == 'livetv':
        livetv()



    elif params["mode"] == 'league':
        league(urlUnquoted)
    elif params["mode"] == 'vodlist':
        vodlist(urlUnquoted)
    elif params["mode"] == 'resolveAndPlayVod':
        resolveAndPlayVod(urlUnquoted)

        

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
    elif params["mode"] == 'resolveAndPlayVideoDaum':
        resolveAndPlayVideoDaum(urlUnquoted)
    elif params["mode"] == 'resolveAndPlayVideoLive':
        resolveAndPlayVideoLive(urlUnquoted)
    elif params["mode"] == 'livetvplay':
        livetvplay(urlUnquoted)

xbmcplugin.endOfDirectory(_thisPlugin)        
