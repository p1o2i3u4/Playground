# -*- coding: utf-8 -*-
"""
    Ondemand Korea
"""
from xbmcswift2 import Plugin
import os
import xbmcplugin, xbmcgui, sys
import urllib2, urllib, re
from BeautifulSoup import BeautifulSoup

plugin = Plugin()

# magic; id of this plugin's instance - cast to integer
_pluginName = (sys.argv[0])
_thisPlugin = int(sys.argv[1])
_connectionTimeout = 20
_header = "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"
tablet_UA = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19"
root_url = "http://www.ondemandkorea.com/"

def listMainCategories():
    addDir("최근 방영", "http://www.ondemandkorea.com/", "RecentCategories", '')  
    addDir("드라마", "http://www.ondemandkorea.com/drama", "videoCategories", '')
    addDir("예능/오락", "http://www.ondemandkorea.com/variety", "videoCategories", '')
    addDir("시사/다큐", "http://www.ondemandkorea.com/documentary", "videoCategories", '')
    addDir("음식/요리", "http://www.ondemandkorea.com/food", "videoCategories", '')
    addDir("뷰티/패션", "http://www.ondemandkorea.com/beauty", "videoCategories", '')
    #addDir("여성", "http://www.ondemandkorea.com/women", "videoCategories", '')
    addDir("건강", "http://www.ondemandkorea.com/health", "videoCategories", '')

        
    #addDir("스포츠", "http://www.ondemandkorea.com/sports", "videoCategories", '')    
    #addDir("경제", "http://www.ondemandkorea.com/economy", "videoCategories", '')    
    #addDir("종교", "http://www.ondemandkorea.com/religion", "videoCategories", '')    
    #addDir("음악", "http://www.ondemandkorea.com/kmuze", "videoCategories", '')
    #addDir("게임", "http://www.ondemandkorea.com/games", "videoCategories", '')
    addDir("한국 영화", "http://www.ondemandkorea.com/movie", "MovieCategories", '')
    #addDir("드라마 (저화질)", "http://www.ondemandkorea.com/drama", "videoCategoriesLow", '')
    #addDir("예능/오락 (저화질)", "http://www.ondemandkorea.com/variety", "videoCategoriesLow", '')
    #addDir("시사/다큐 (저화질)", "http://www.ondemandkorea.com/documentary", "videoCategoriesLow", '')
                
def listRecentCategories(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
##        match=re.compile('<div class="entry.*?">\n\t\t\t\t\t\t\t\t\t<a href="(.+?)" title="(.+?)">').findall(link)
##        match2=re.compile('<img src=".*?src=(.+?)">\n\t\t\t\t\t\t\t\t\t\t<div class="ep_title"><b>.+?</b></div>\n\t\t\t\t\t\t\t\t\t\t<div class="ep_date">(.+?)</div>').findall(link,0)
##        match3=[(x+y) for x,y in zip(match,match2)] #combine match and match2!
##        
##        for i in range(len(match3)):
##            thumb = "http://max.ondemandkorea.com" + match3[i][2]
##            playVideoUrl = 'http://www.ondemandkorea.com' + match3[i][0]
##            title = unicode(match3[i][1], 'utf-8')  + " - " + match3[i][3]
##            title = title.replace('.480p.1596k','').replace('amp;','').replace('&#039;','\'').replace('&lt;','<').replace('&gt;','>')
##            match3[i] = (playVideoUrl, title, thumb)
##
##        #match.sort(reverse=True)
##
##        
##        for url, title, thumbnail in match3:
##            addLink(title, url, 'resolveAndPlayVideo', thumbnail)
            
     #soup를 통한 리스팅...
        #if len(match)<1:
        soup=BeautifulSoup(link)
        
        items = []
        drama=soup.find('div', {'class':re.compile('^(?:iosSlider contents drama)$')})
        for node in drama.findAll('div', {'class':re.compile('^(?:entry |entry last)$')}):
            if not node.b:
                continue
            title2 = node.b.string.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&#039;','\'')
            #thumb = node.find('img', {'src':re.compile(r'(jpe?g)|(png32)$')})
            thumb2 = re.compile('img src=".*?/wp-content(.*?)"').findall(str(node))
            thumb1 = 'http://max.ondemandkorea.com/wp-content'+thumb2[0]
            thumb = thumb1.replace(' ','%20')   
            #dt = node.find("div", {"class":"ep_date"}).find(text=True)
            dt = re.compile('([0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9])').findall(str(node))
            title = title2 + ' - '+dt[0]
            items.append({'title':title, 'broad_date':dt, 'url':root_url+node.a['href'], 'thumbnail':thumb})
       
        for i in range(len(items)):
            items[i] = (items[i]['title'], items[i]['url'], items[i]['thumbnail'])
              

        for name, url, thumbnail in items:
            addLink(name, url, 'resolveAndPlayVideo', thumbnail)

        items2 = []
        variety=soup.find('div', {'class':re.compile('^(?:iosSlider contents variety)$')})
        for node in variety.findAll('div', {'class':re.compile('^(?:entry |entry last)$')}):
            if not node.b:
                continue
            title2 = node.b.string.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&#039;','\'')
            thumb2 = re.compile('img src=".*?/wp-content(.*?)"').findall(str(node))
            thumb1 = 'http://max.ondemandkorea.com/wp-content'+thumb2[0]
            thumb = thumb1.replace(' ','%20')   
            dt = node.find("div", {"class":"ep_date"}).find(text=True)
            title = title2 + ' - '+dt
            items2.append({'title':title, 'broad_date':dt, 'url':root_url+node.a['href'], 'thumbnail':thumb})
       
        for i in range(len(items2)):
            items2[i] = (items2[i]['title'], items2[i]['url'], items2[i]['thumbnail'])
              

        for name, url, thumbnail in items2:
            addLink(name, url, 'resolveAndPlayVideo', thumbnail)

                        
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
        
def listVideoCategories(url):
    try:
        print "requesting url " + url
        url2=url
        req = urllib2.Request(url)
        req.add_header('User-Agent', tablet_UA)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        
        
        match=re.compile('\n\t\t\t\t\t\t\t<img src=".*?src=(.+?)" style="(.*?)"').findall(link)
        match1=re.compile('<div class="ep_box">\n\t\t\t<a href="(.*?)" title="(.*?)">').findall(link)
        match3=[(x+y) for x,y in zip(match,match1)] #combine match and match2!

        for i in range(len(match3)):
            thumb1 = "http://max.ondemandkorea.com" + match3[i][0]
            thumb = thumb1.replace(' ','%20')
	    dramaurl = 'http://www.ondemandkorea.com/' + match3[i][2]
            match3[i] = (unicode(match3[i][3], 'utf-8'), dramaurl, thumb)

        for name, url, thumbnail in match3:
            addDir(name, url, 'dramaCategoryContent', thumbnail)
            
        if len(match3)<1:
            soup=BeautifulSoup(link)
            items = []
            for node in soup.findAll('div', {'class':'ep_box'}):
                thumb2 = re.compile('img src=".*?/wp-content(.*?)"').findall(str(node))
                thumb1 = 'http://max.ondemandkorea.com/wp-content'+thumb2[0]
                thumb = thumb1.replace(' ','%20')   

                items.append({'title':node.b.string, 'url':root_url+'/'+node.a['href'], 'thumbnail':thumb})

            for i in range(len(items)):
                items[i] = (items[i]['title'], items[i]['url'], items[i]['thumbnail'])
                  

            for name, url, thumbnail in items:
                addDir(name, url, 'dramaCategoryContent', thumbnail)
                
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

        
##def listVideosInCategory(url):
##    try:
##        req = urllib2.Request(url)
##        req.add_header('User-Agent', _header)
##        req.add_header('Accept-Langauge', 'ko')
##        req.add_header('Cookie', 'language=kr')
##        response = urllib2.urlopen(req, timeout = _connectionTimeout)
##        link=response.read()
##        response.close()
##        match=re.compile('<img src="(.+?)"[^>]*>\n\t\t\t\t</a>\n\t\t\t\t<a href="(.+?)"[^>]*>\n\t\t\t\t\t<b>(.+?)</b><br>.+? : (.+?)\t\t\t\t</a>').findall(link)
##
##        for i in range(len(match)):
##            playVideoUrl = 'http://www.ondemandkorea.com/' + match[i][1]
##	    title = unicode(match[i][2], 'utf-8')  + " - " + match[i][3]
##            match[i] = (playVideoUrl, title, match[i][0])
##    
##        for url, title, thumbnail, in match:
##            addLink(title, url, 'resolveAndPlayVideo', thumbnail)
##
## 
##    except urllib2.URLError:
##        addLink("성용이를 불러주세용.", '', '', '')
##   
def resolveAndPlayVideo(url):
    try:
        quality = plugin.get_setting("quality", str)
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        
        ## playlist.php 를 통해 정확한 파일명을 불러오기
        token=re.compile('cat: \'.*?\',id: (.*?),').findall(link)
        tokenurl='http://www.ondemandkorea.com/includes/playlist.php?token=' + token[0]
        req2 = urllib2.Request(tokenurl)
        req2.add_header('User-Agent', _header)
        response2 = urllib2.urlopen(req2, timeout = _connectionTimeout)
        link2=response2.read()
        response2.close()
        
        match=re.compile('src="(.*?).[0-9]*p.[0-9]*k.mp4"').findall(link2)
        #list replace
        match = [w.replace('mp4:', '').replace('http2/', '').replace('http/','') for w in match]
   
        if quality =='2':
            quality = '720p'
            qurl=match[0]
        elif quality =='1':
            quality = '480p'
            qurl=match[1]
        else:
            quality = '360p'
            qurl=match[2]
        
        #if plugin.get_setting("m3u8") == 'true':

        
##            Thumblink=re.compile('thumbnail/(.+?)_([0-9]+).*?.jpg"').search(link)
##            episode=Thumblink.group(1)
##            date=Thumblink.group(2)
        sr= re.compile('srcurl: "(.*?)",').findall(link)
        
            
##            url1='http://'+sr[0]+'.ondemandkorea.com:1935/cache/_definst_/smil:glucache/variety/'+ episode + '/' + episode + '_' + date + '-smil'+quality+'.smil/playlist.m3u8'
##            url2='http://'+sr[0]+'.ondemandkorea.com:1935/cache/_definst_/smil:glucache/variety2/'+ episode + '/' + episode + '_' + date + '-smil'+quality+'.smil/playlist.m3u8'
##            
##            url5='http://'+sr[0]+'.ondemandkorea.com:1935/cache/_definst_/smil:gludisp/variety2/'+ episode + '/' + episode + '_' + date + '-smil'+quality+'.smil/playlist.m3u8'
##            url6='http://'+sr[0]+'.ondemandkorea.com:1935/cache/_definst_/smil:gludisp/drama/'+ episode + '/' + episode + '_' + date + '-smil'+quality+'.smil/playlist.m3u8'

        url1='http://'+sr[0]+'.ondemandkorea.com:1935/cache/_definst_/smil:glucache/'+qurl+'-smil'+quality+'.smil/playlist.m3u8'
        url2='http://'+sr[0]+'.ondemandkorea.com:1935/cache/_definst_/smil:gludisp/'+qurl+'-smil'+quality+'.smil/playlist.m3u8'
        
        try:
            f = urllib2.urlopen(urllib2.Request(url1))
            deadLinkFound2 = False
        except:
            deadLinkFound2 = True
        try:
            f = urllib2.urlopen(urllib2.Request(url2))
            deadLinkFound3 = False
        except:
            deadLinkFound3 = True

##            try:
##                f = urllib2.urlopen(urllib2.Request(url3))
##                deadLinkFound4 = False
##            except:
##                deadLinkFound4 = True
##            try:
##                f = urllib2.urlopen(urllib2.Request(url4))
##                deadLinkFound5 = False
##            except:
##                deadLinkFound5 = True
##            try:
##                f = urllib2.urlopen(urllib2.Request(url5))
##                deadLinkFound6 = False
##            except:
##                deadLinkFound6 = True
        
        if deadLinkFound2==False:
            listItem = xbmcgui.ListItem(path=str(url1))
            xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
            
##            elif deadLinkFound3==False:
##                listItem = xbmcgui.ListItem(path=str(url2))
##                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##            
##            elif deadLinkFound4==False:
##                listItem = xbmcgui.ListItem(path=str(url3))
##                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##                
##            elif deadLinkFound5==False:
##                listItem = xbmcgui.ListItem(path=str(url4))
##                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##            elif deadLinkFound5==False:
##                listItem = xbmcgui.ListItem(path=str(url5))
##                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)  
        elif deadLinkFound3==False:
            listItem = xbmcgui.ListItem(path=str(url2))
            xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
            
        else:
            tablet_UA = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19"
            req = urllib2.Request(url)
            req.add_header('User-Agent', tablet_UA)
            req.add_header('Accept-Langauge', 'ko')
            req.add_header('Cookie', 'language=kr')
            response = urllib2.urlopen(req, timeout = _connectionTimeout)
            link=response.read()
            response.close()
            match1=re.compile('"http://(.*?).com/.*?.mp4"').search(link).group(1)
            print match1
            
            match=re.compile('src="(.*?)"').findall(link2)
             #list replace
            match = [w.replace('mp4:', '').replace('http2/', '').replace('http/','') for w in match]
            
            quality = plugin.get_setting("quality", str)
            if quality =='2':
                quality = '720p'
                qurl=match[0]
            elif quality =='1':
                quality = '480p'
                qurl=match[1]
            else:
                quality = '360p'
                qurl=match[2]
                
            if qurl:
                qurl2='http://'+match1+'.com/'+qurl
                listItem = xbmcgui.ListItem(path=str(qurl2))
                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##                match2=match.group(1)
##                urllow='http://' + match2 + '.mp4'
##                match3=match2.replace('480p','720p')
##                url0=match3.replace('1596k','2296k')
##                url1=url0.replace('360p','720p')
##                url2=url1.replace('1296k','2296k')
##                url= 'http://' + url2 + '.mp4'
##
##                url1=url0.replace('360p','480p')
##                url2=url1.replace('1296k','1596k')
##                url2= 'http://' + url2 + '.mp4'
##                
##                if quality =='720p':
##                    try:
##                        listItem = xbmcgui.ListItem(path=str(qurl))
##                        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##                    except:
##                        listItem = xbmcgui.ListItem(path=str(url2))
##                        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##                elif quality =='480p':
##                    try:
##                        listItem = xbmcgui.ListItem(path=str(url2))
##                        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##                
##                    except:
##                        listItem = xbmcgui.ListItem(path=str(urllow))
##                        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##
##                else:
##                    listItem = xbmcgui.ListItem(path=str(urllow))
##                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                    
            else:
                Thumblink=re.compile('thumbnail/(.+?)_([0-9]+).*?.jpg"').search(link)
                episode=Thumblink.group(1)
                date=Thumblink.group(2)
                
                #url = 'http://sjcssd2.ondemandkorea.com/variety2/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
    ##            postid=re.compile('.*?post_id=([0-9]*)\&').search(link).group(1)
    ##            
    ##            url='http://www.ondemandkorea.com/includes/playlist.php?token=' + postid
    ##            req = urllib2.Request(url)
    ##            response = urllib2.urlopen(req, timeout = _connectionTimeout)
    ##            link=response.read()
    ##            response.close()
    ##            
    ##            match=re.compile('src="(.*?)"').search(link).group(1)
    ##            match0=match.replace('mp4:','')
    ##            match1=match0.replace('http2/','')
    ##            match2=match1.replace('http/','')
    ##            match3=match2.replace('480p','720p')
    ##            url0=match3.replace('1596k','2296k')
    ##            url1= 'http://sjcssd2.ondemandkorea.com/variety/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
    ##            url2= 'http://sjcssd2.ondemandkorea.com/variety2/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
    ##            url3= 'http://sjcs1.ondemandkorea.com/variety/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
    ##            url4= 'http://sjcs1.ondemandkorea.com/variety2/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
    ##            url5= 'http://sjcglu1.ondemandkorea.com/variety2/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
    ##            url6= 'http://sjcglu1.ondemandkorea.com/variety/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
                url7= 'http://sjcdisp06.ondemandkorea.com/'+qurl
                url8= 'http://sjcdisp06.ondemandkorea.com/'+qurl
                #url9= 'http://sjcdisp01.ondemandkorea.com/'
                #url10= 'http://sjcdisp01.ondemandkorea.com/variety/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
    ##            url11= 'http://sjcstor05.ondemandkorea.com/variety/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
    ##            url12= 'http://sjcstor06.ondemandkorea.com/variety2/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
    ##            url13= 'http://sjcstor07.ondemandkorea.com/variety/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
    ##            url14= 'http://sjcstor08.ondemandkorea.com/variety2/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
    ##            url15= 'http://sjcstor09.ondemandkorea.com/variety/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
    ##            url16= 'http://sjcstor10.ondemandkorea.com/variety2/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'    

                
                #url5= 'http://sjcs3.ondemandkorea.com/' + url0
                #sjcglu4
    ##            try:
    ##              f = urllib2.urlopen(urllib2.Request(url1))
    ##              deadLinkFound1 = False
    ##            except:
    ##              deadLinkFound1 = True
    ##            try:
    ##              f = urllib2.urlopen(urllib2.Request(url2))
    ##              deadLinkFound2 = False
    ##            except:
    ##              deadLinkFound2 = True
    ##            try:
    ##              f = urllib2.urlopen(urllib2.Request(url3))
    ##              deadLinkFound3 = False
    ##            except:
    ##              deadLinkFound3 = True
    ##            try:
    ##              f = urllib2.urlopen(urllib2.Request(url4))
    ##              deadLinkFound4 = False
    ##            except:
    ##              deadLinkFound4 = True
    ##            try:
    ##              f = urllib2.urlopen(urllib2.Request(url5))
    ##              deadLinkFound5 = False
    ##            except:
    ##              deadLinkFound5 = True
    ##            try:
    ##              f = urllib2.urlopen(urllib2.Request(url6))
    ##              deadLinkFound6 = False
    ##            except:
    ##              deadLinkFound6 = True

                try:
                  f = urllib2.urlopen(urllib2.Request(url7))
                  deadLinkFound7 = False
                except:
                  deadLinkFound7 = True
                try:
                  f = urllib2.urlopen(urllib2.Request(url8))
                  deadLinkFound8 = False
                except:
                  deadLinkFound8 = True
##                try:
##                  f = urllib2.urlopen(urllib2.Request(url9))
##                  deadLinkFound9 = False
##                except:
##                  deadLinkFound9 = True
##
##                try:
##                  f = urllib2.urlopen(urllib2.Request(url10))
##                  deadLinkFound10 = False
##                except:
##                  deadLinkFound10 = True


    ##            if deadLinkFound1==False:
    ##                listItem = xbmcgui.ListItem(path=str(url1))
    ##                     
    ##                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
    ##
    ##
    ##            elif deadLinkFound2==False:
    ##                listItem = xbmcgui.ListItem(path=str(url2))
    ##                     
    ##                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
    ##                
    ##            elif deadLinkFound3==False:
    ##                listItem = xbmcgui.ListItem(path=str(url3))
    ##                     
    ##                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
    ##
    ##            elif deadLinkFound4==False:
    ##                listItem = xbmcgui.ListItem(path=str(url4))
    ##                     
    ##                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
    ##
    ##            elif deadLinkFound5==False:
    ##                listItem = xbmcgui.ListItem(path=str(url5))
    ##                     
    ##                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
    ##                
    ##            elif deadLinkFound6==False:
    ##                listItem = xbmcgui.ListItem(path=str(url6))
    ##                     
    ##                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)

                if deadLinkFound7==False:
                    listItem = xbmcgui.ListItem(path=str(url7))
                         
                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                    
##                elif deadLinkFound8==False:
##                    listItem = xbmcgui.ListItem(path=str(url8))
##                         
##                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##
##                elif deadLinkFound9==False:
##                    listItem = xbmcgui.ListItem(path=str(url9))
##                         
##                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##
##                elif deadLinkFound10==False:
##                    listItem = xbmcgui.ListItem(path=str(url10))
##                         
##                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##                    
            
                else:
                    listItem = xbmcgui.ListItem(path=str(url8))
                         
                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
    ##		url1= 'http://sjcssd2.ondemandkorea.com/drama/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
    ##		url3= 'http://sjcs1.ondemandkorea.com/drama/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
    ##		url4= 'http://sjcglu1.ondemandkorea.com/drama/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
##                    url5= 'http://sjcstor07.ondemandkorea.com/drama/' + episode + '/' + episode + '_' + date +'.720p.2296k.mp4'
                    
    ##                try:
    ##                  f = urllib2.urlopen(urllib2.Request(url1))
    ##                  dead = False
    ##                except:
    ##                  dead = True
    ##                try:
    ##                  f = urllib2.urlopen(urllib2.Request(url3))
    ##                  dead1 = False
    ##                except:
    ##                  dead1 = True
    ##                try:
    ##                  f = urllib2.urlopen(urllib2.Request(url4))
    ##                  dead2 = False
    ##                except:
    ##                  dead2 = True
##
##                    try:
##                      f = urllib2.urlopen(urllib2.Request(url5))
##                      dead2 = False
##                    except:
##                      dead2 = True
                                      
    ##                if dead==False:
    ##                    listItem = xbmcgui.ListItem(path=str(url1))
    ##                    listItem.setProperty('IsPlayable', 'true')
    ##                
    ##                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
    ##                if dead1==False:
    ##                    listItem = xbmcgui.ListItem(path=str(url3))
    ##                    listItem.setProperty('IsPlayable', 'true')
    ##                
    ##                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
    ##                if dead2==False:
    ##                    listItem = xbmcgui.ListItem(path=str(url4))
    ##                    listItem.setProperty('IsPlayable', 'true')
    ##                
    ##                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)

##                    if dead2==False:
##                        listItem = xbmcgui.ListItem(path=str(url5))
##                    
##                        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)

    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

##def listdramaCategories(url):
##    try:
##        print "requesting url " + url
##        url2=url
##        req = urllib2.Request(url)
##        req.add_header('User-Agent', tablet_UA)
##        req.add_header('Accept-Langauge', 'ko')
##        req.add_header('Cookie', 'language=kr')
##        response = urllib2.urlopen(req, timeout = _connectionTimeout)
##        link=response.read()
##        response.close()
##        
##        
####        match2=[]
####        for i in match1:
####            if i not in match2:
####                match2.append(i)
##        match=re.compile('\n\t\t\t\t\t\t\t<img src=".*?src=(.+?)" style="(.*?)"').findall(link)
##        match1=re.compile('<div class="ep_box">\n\t\t\t<a href="(.*?)" title="(.*?)">').findall(link)
##        match3=[(x+y) for x,y in zip(match,match1)] #combine match and match2!
##
##        for i in range(len(match3)):
##            thumb1 = "http://max.ondemandkorea.com" + match3[i][0]
##            thumb = thumb1.replace(' ','%20')
##	    dramaurl = 'http://www.ondemandkorea.com/' + match3[i][2]
##            match3[i] = (unicode(match3[i][3], 'utf-8'), dramaurl, thumb)
##
##        for name, url, thumbnail in match3:
##            addDir(name, url, 'dramaCategoryContent', thumbnail)
##
##        addDir('아무것도 없으면 여길 누르세요', url2, 'listVideoCategoriesSoup', '')
##        
##    except urllib2.URLError:
##        addLink("성용이를 불러주세용.", '', '', '')
        
def listdramaInCategory(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', tablet_UA)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()

        

##        match2=[]
##        for i in match1:
##            if i not in match2:
##                match2.append(i)
##                
        match=re.compile('<div class="ep.*?">\n\t\t\t\t<a href="(.*?)" title="(.*?)">\n\t\t\t\t\t\n\t\t\t\t\t<img src=".*?src=(.*?)_(.*?)_(.*?)"').findall(link)
        
        for i in range(len(match)):
	    playVideoUrl = 'http://www.ondemandkorea.com/' + match[i][0]
	    poster1 = 'http://max.ondemandkorea.com/' + match[i][2] + '_'+ match[i][3] +'_' + match[i][4]
	    poster = poster1.replace(' ','%20')
	    title = unicode(match[i][1], 'utf-8')  + " - " + match[i][3]
	    title = title.replace('.480p.1596k','').replace('amp;','').replace('&#039;','\'').replace('&lt;','<').replace('&gt;','>').replace('360p.1296k','')
	    match[i] = (title, playVideoUrl, poster)

        for title, url, thumbnail, in match:
            addLink(title, url, 'resolveAndPlayVideo', thumbnail)
        
     #soup를 통한 리스팅...
        if len(match)<1:
            soup=BeautifulSoup(link)
            items = []
            for node in soup.findAll('div', {'class':re.compile('^(?:ep|ep_last)$')}):
                if not node.b:
                    continue
                title2 = node.b.string.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&#039;','\'')
                thumb2 = re.compile('img src=".*?/wp-content(.*?)"').findall(str(node))
                thumb1 = 'http://max.ondemandkorea.com/wp-content'+thumb2[0]
                thumb = thumb1.replace(' ','%20')   
                try:
                    #dt = node.find("div", {"class":"ep_date"}).find(text=True)
                    dt = re.compile('([0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9])').findall(str(node))
                    print node
                except:
                    dt = ""
                title = title2 + ' - '+dt[0]
                items.append({'title':title, 'broad_date':dt, 'url':root_url+node.a['href'], 'thumbnail':thumb})
           
            for i in range(len(items)):
                items[i] = (items[i]['title'], items[i]['url'], items[i]['thumbnail'])
                  

            for name, url, thumbnail in items:
                addLink(name, url, 'resolveAndPlayVideo', thumbnail)
        
        #페이지 추가
        match1=re.compile('cat: \'(.*?)\',id: (.*?),').findall(link)
        page='http://www.ondemandkorea.com/includes/episode_page.php?cat='+match1[0][0]+'&id=' +match1[0][1]+'&page=99'

        #페이지 수 확인
        req = urllib2.Request(page)
        response = urllib2.urlopen(req)
        link=response.read()

        match2=re.compile('"num_pages":([1-9]+),').findall(link)
        if match2:
            if int(match2[0])>1:
                pg=int(match2[0])+1
                for i in range(1,pg): 
                    if i<5: #너무 오래 걸려서 4페이지까지 제한... 
                        Pgurl = 'http://www.ondemandkorea.com/includes/episode_page.php?cat='+match1[0][0]+'&id=' +match1[0][1]+'&page='+str(i)
                        req = urllib2.Request(Pgurl)
                        response = urllib2.urlopen(req)
                        link=response.read()
                        match=re.compile('"url":"(.*?)"').search(link).group(1)
                        Pgurl='http://www.ondemandkorea.com/'+match
                        name=str(i) +' 페이지'
                        addDir(name, Pgurl, 'dramaCategoryContent', "")
      
        
           
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')


def listMovieCategories(url):
    try:
        print "requesting url " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')  
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        match=re.compile('<dd class="thumb"><a href="(.*?)".*?><img src="(.+?)" alt="(.*?)">').findall(link)
        
        for i in range(len(match)):
            playVideoUrl = 'http://www.ondemandkorea.com/' + match[i][0]
	    title = unicode(match[i][2], 'utf-8')
            match[i] = (playVideoUrl, title, match[i][1])
            

        for url, name, thumbnail in match:
            addLink(name, url, 'resolveAndPlayMovie', thumbnail)
            
        if len(match)<1:
            soup=BeautifulSoup(link)

            items = []
            for node in soup.findAll('dl'):
                title2 = node.a.string.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&#039;','\'')
                thumb2 = re.compile('src=/wp-content(.*?)"').findall(str(node))
                thumb1 = 'http://max.ondemandkorea.com/wp-content'+thumb2[0]
                thumb = thumb1.replace(' ','%20')
                dt = node.find("span", {"class":"thumb-date"}).find(text=True)
                title = title2 + ' - '+dt
                genre = node.find('dd', {"class":"info1"}).find(text=True)
                genre1 = genre.replace('\n\t\t\t\t\t\t    ','').replace('\t\t\t\t\t\t\t ','')
                genre2 = genre1.split('/')
                items.append({'title':title, 'year':dt, 'genre':genre2, 'url':root_url+node.a['href'], 'thumbnail':thumb})

           
            for i in range(len(items)):
                items[i] = (items[i]['title'], items[i]['url'], items[i]['thumbnail'])
                  
            print items
            
            for name, url, thumbnail in items:
                addLink(name, url, 'resolveAndPlayVideo', thumbnail)
                
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

##playVideo 로 통일 
def resolveAndPlayMovie(url):
    try:
        tablet_UA = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19"

        
        #m3u8 = plugin.get_setting('m3u8', bool)

        #if plugin.get_setting("Mm3u8") == 'true':
        
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()

        title=re.compile('content="http://www.ondemandkorea.com/(.*?).html"').findall(link)
        
        episode=re.compile('thumbnail/(.*?).[0-9]+p').findall(link)
        
        
        sr= re.compile('srcurl: "(.*?)",').findall(link)
        #url1='http://'+sr[0]+'.ondemandkorea.com:1935/cache/_definst_/smil:glucache/movies/'+ title[0] + '/' + episode[0] + '-smil1080p.smil/playlist.m3u8'
        url1='http://'+sr[0]+'.ondemandkorea.com:1935/cache/_definst_/smil:gludisp/movies/'+ title[0] + '/' + episode[0] + '-smil1080p.smil/playlist.m3u8'
        url2='http://'+sr[0]+'.ondemandkorea.com:1935/cache/_definst_/smil:gludisp/movies/'+ title[0] + '/' + episode[0] + '-smil720p.smil/playlist.m3u8'
        url3='http://'+sr[0]+'.ondemandkorea.com:1935/cache/_definst_/smil:gludisp/movies/'+ title[0] + '/' + episode[0] + '-smil480p.smil/playlist.m3u8'
        url4='http://'+sr[0]+'.ondemandkorea.com:1935/cache/_definst_/smil:gludisp/movies/'+ title[0] + '/' + episode[0] + '-smil360p.smil/playlist.m3u8'

        try:
            f = urllib2.urlopen(urllib2.Request(url1))
            deadLinkFound2 = False
        except:
            deadLinkFound2 = True
        try:
            f = urllib2.urlopen(urllib2.Request(url2))
            deadLinkFound3 = False
        except:
            deadLinkFound3 = True
        try:
            f = urllib2.urlopen(urllib2.Request(url3))
            deadLinkFound4 = False
        except:
            deadLinkFound4 = True
        try:
            f = urllib2.urlopen(urllib2.Request(url4))
            deadLinkFound5 = False
        except:
            deadLinkFound5 = True
            
        if deadLinkFound2==False:
            listItem = xbmcgui.ListItem(path=str(url1))
            xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
            
        elif deadLinkFound3==False:
            listItem = xbmcgui.ListItem(path=str(url2))
            xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
            
        elif deadLinkFound4==False:
            listItem = xbmcgui.ListItem(path=str(url3))
            xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
             
        elif deadLinkFound5==False:
            listItem = xbmcgui.ListItem(path=str(url4))
            xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
        else:
        
            req = urllib2.Request(url)
            req.add_header('User-Agent', tablet_UA)
            req.add_header('Accept-Langauge', 'ko')
            req.add_header('Cookie', 'language=kr')
                
            response = urllib2.urlopen(req, timeout = _connectionTimeout)
            link=response.read()
            response.close()
            match=re.compile('cat: \'.*?\',id: (.*?),').findall(link)
            url='http://www.ondemandkorea.com/includes/playlist.php?token=' + match[0]
            req = urllib2.Request(url)
            response = urllib2.urlopen(req, timeout = _connectionTimeout)
            link=response.read()
            response.close()
            
            match=re.compile('src="(.*?)"').findall(link)
            match0=match[0].replace('mp4:','')
            match1=match0.replace('http2/','')
            url0=match1.replace('http/','')

            url1= 'http://sjcstor05.ondemandkorea.com/' + url0
            url2= 'http://sjcdisp04.ondemandkorea.com/' + url0
            
            try:
              f = urllib2.urlopen(urllib2.Request(url1))
              deadLinkFound1 = False
            except:
              deadLinkFound1 = True
    ##
    ##        try:
    ##          f = urllib2.urlopen(urllib2.Request(url2))
    ##          deadLinkFound2 = False
    ##        except:
    ##          deadLinkFound2 = True

            if deadLinkFound1==False:
                listItem = xbmcgui.ListItem(path=str(url1))   
                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                
            else:
                listItem = xbmcgui.ListItem(path=str(url2))
                     
                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)  

    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
    
def addLink(name,url,mode,iconimage):
    u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    
    liz.setProperty("IsPlayable","true")
    xbmcplugin.addDirectoryItem(handle=_thisPlugin,url=u,listitem=liz,isFolder=False)
    

def addDir(name,url,mode,iconimage):
    u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)#+"&name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    xbmcplugin.addDirectoryItem(handle=_thisPlugin,url=u,listitem=liz,isFolder=True)
    

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
##
##    elif params["mode"] == 'dramafever':
##        listdramafever(urlUnquoted)
##    elif params["mode"] == 'dramafeverPlay':
##        dramafeverPlay(urlUnquoted)
        
    elif params["mode"] == 'dramaCategories':
        listdramaCategories(urlUnquoted)   
    elif params["mode"] == 'dramaCategoryContent':
        listdramaInCategory(urlUnquoted)


##    elif params["mode"] == 'varietyCategories':
##        listvarietyCategories(urlUnquoted)    
##    elif params["mode"] == 'varietyCategoryContent':
##        listvarietyInCategory(urlUnquoted)
##
##    elif params["mode"] == 'videoCategoriesLow':
##        listVideoCategoriesLow(urlUnquoted)
##    elif params["mode"] == 'videoCategoryContentLow':
##        listVideosInCategoryLow(urlUnquoted)
##    elif params["mode"] == 'resolveAndPlayVideoLow':
##        resolveAndPlayVideoLow(urlUnquoted)
        
    elif params["mode"] == 'RecentCategories':
        listRecentCategories(urlUnquoted)
    elif params["mode"] == 'MovieCategories':
        listMovieCategories(urlUnquoted)
    elif params["mode"] == 'resolveAndPlayMovie':
        resolveAndPlayMovie(urlUnquoted)
        
xbmcplugin.endOfDirectory(_thisPlugin)        
