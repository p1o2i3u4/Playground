# -*- coding: utf-8 -*-
"""
    Ondemand Korea
"""
from xbmcswift2 import Plugin
import os
import json
import xbmcplugin, xbmcgui, sys
import urllib2, urllib, re
from BeautifulSoup import BeautifulSoup

plugin = Plugin()

# maxcdn-origin.ondemandkorea.com, max.ondemandkorea.com, max2.ondemandkorea.com
# magic; id of this plugin's instance - cast to integer
_pluginName = (sys.argv[0])
_thisPlugin = int(sys.argv[1])
_connectionTimeout = 40
#UserAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
tablet_UA = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19"
root_url = "http://www.ondemandkorea.com/"

img_base = "http://max.ondemandkorea.com/includes/timthumb.php?w=175&h=100&src="
eplist_url = "includes/episode_page.php?cat={program:s}&id={videoid:s}&page={page:d}"

default_hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Connection': 'keep-alive'}

def listMainCategories():
    addDir("최근 방영", root_url, "RecentCategories", '')  
    addDir("드라마", root_url+"drama", "videoCategories", '')
    addDir("예능/오락", root_url+"variety", "videoCategories", '')
    addDir("시사/다큐", root_url+"documentary", "videoCategories", '')
    addDir("음식/요리", root_url+"food", "videoCategories", '')
    addDir("뷰티/패션", root_url+"beauty", "videoCategories", '')
    #addDir("여성", root_url+"women", "videoCategories", '')
    addDir("건강", root_url+"health", "videoCategories", '')

        
    #addDir("스포츠", root_url+"sports", "videoCategories", '')    
    #addDir("경제", root_url+"economy", "videoCategories", '')    
    #addDir("종교", root_url+"religion", "videoCategories", '')    
    #addDir("음악", root_url+"kmuze", "videoCategories", '')
    #addDir("게임", root_url+"games", "videoCategories", '')
    addDir("한국 영화", root_url+"movie", "MovieCategories", '')
    #addDir("드라마 (저화질)", root_url+"drama", "videoCategoriesLow", '')
    #addDir("예능/오락 (저화질)", root_url+"variety", "videoCategoriesLow", '')
    #addDir("시사/다큐 (저화질)", root_url+"documentary", "videoCategoriesLow", '')
                
def listRecentCategories(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', default_hdr)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req)
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
            thumb1 = root_url+'wp-content'+thumb2[0]
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
            thumb1 = root_url+'wp-content'+thumb2[0]
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
        req.add_header('User-Agent', default_hdr)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

        items = []
        for part in link.split('<div class="ep_box"')[1:]:
            match = re.compile('<a href="([^"]*)" title="([^"]*)">.*<img src="([^"]*timthumb[^"]*)"', re.S).search(part)
            if match:
                thumb=match.group(3).replace(' ','%20')
                items.append({'title':match.group(2), 'url':root_url+match.group(1), 'thumbnail':thumb})
                
        for i in range(len(items)):
            items[i] = (items[i]['title'], items[i]['url'], items[i]['thumbnail'])
            
        for name, url, thumbnail in items:
            addDir(name, url, 'dramaCategoryContent', thumbnail)
            
##        match=re.compile('\n\t\t\t\t\t\t\t<img src=".*?src=(.+?)" style="(.*?)"').findall(link)
##        match1=re.compile('<div class="ep_box">\n\t\t\t<a href="(.*?)" title="(.*?)">').findall(link)
##        match3=[(x+y) for x,y in zip(match,match1)] #combine match and match2!
##
##        for i in range(len(match3)):
##            thumb1 = root_url + match3[i][0]
##            thumb = thumb1.replace(' ','%20')
##	    dramaurl = root_url+match3[i][2]
##            match3[i] = (unicode(match3[i][3], 'utf-8'), dramaurl, thumb)
##
##        for name, url, thumbnail in match3:
##            addDir(name, url, 'dramaCategoryContent', thumbnail)
##            
        if len(items)<1:
            soup=BeautifulSoup(link)
            items = []
            for node in soup.findAll('div', {'class':'ep_box'}):
                thumb2 = re.compile('img src=".*?/wp-content(.*?)"').findall(str(node))
                thumb1 = root_url+'wp-content'+thumb2[0]
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
##        req.add_header('User-Agent', UserAgent)
##        req.add_header('Accept-Langauge', 'ko')
##        req.add_header('Cookie', 'language=kr')
##        response = urllib2.urlopen(req)
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
        req.add_header('User-Agent', default_hdr)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup=BeautifulSoup(link)
        
        try:
            f=re.compile('file: "(.*?)"').findall(link)
            print 'Found original m3u8 ' + f[0]
            f2=str(f[0])+'|Referer=' + url + '&User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
            listItem = xbmcgui.ListItem(path=f2)
            xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
            
        except:
            title1=re.compile('<meta property="og:url" content="http://mondemandkorea.com/(.*?)-e').findall(link)
            if len(title1)<1:
                title1=re.compile('<meta property="og:url" content="http://ondemandkorea.com/(.*?)-[0-9][0-9][0-9][0-9][0-9][0-9]').findall(link)
            #title=re.compile('/uploads/thumbnail/(.*?)_([0-9]*)_').findall(link)
            title=re.compile(r'<link rel="image_src" href="http://(.*?)\.jpg').findall(link)
            title=title[0].split('/')
            title=title[len(title)-1:]
            title=title[0].split('_')
            title=title[0:2]
            
            title[1]=title[1].replace('480p','').replace('1596k','').replace('.','').replace('300p664k','')
            
            if len(title[1])==6:
                date='20'+title[1]
            else:
                date=title[1]

            print title
    

            ##Finding category
            cat=soup.find('td',{'class':'v-bar  active'}).a['href']
            if cat=='http://www.ondemandkorea.com/drama':
                cat='drama'
                print cat
                m=[
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',             
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8', 
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil1720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil1720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil11080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil11080p.smil/manifest.m3u8'
                ]
                


            elif cat=='http://www.ondemandkorea.com/documentary':
                cat='variety'
                print cat
                m=[
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',

##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
                
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
                ]

            else:
                cat='variety'
                print cat
                m=[
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
                
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
                ]                
##                
##                    
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080p/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080p/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080p/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080p/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080p/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080p/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080p/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080p/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080p/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080p/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080p/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080p/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+date[4:6]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+date[4:6]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+date[4:6]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+date[4:6]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+date[4:6]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+date[4:6]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+date[4:6]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+date[4:6]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##                'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+date[4:6]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8'
##                ]

            
            for i in range(len(m)):
                try:
                    f = urllib2.Request(m[i])
                    f.add_header('User-Agent', default_hdr)
                    f=urllib2.urlopen(f)    
                    dead = False
                    
                except:
                    dead = True
               
                if dead==False:
                    print "Correct m3u8 found = "+str(m[i])
                    listItem = xbmcgui.ListItem(path=str(m[i]))
                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                    break
                
                elif i ==len(m)-1:
                    print "No m3u8 found."
                    try: 
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', tablet_UA)
                        req.add_header('Accept-Langauge', 'ko')
                        req.add_header('Cookie', 'language=kr')
                        response = urllib2.urlopen(req)
                        link=response.read()
                        response.close()
                        soup=BeautifulSoup(link)
                        
                        match=re.compile('video.src = "(.*?)"').search(link).group(0).replace('360p.1296k','720p.2296k').replace('.480p.1596k','720p.2296k')
                        
                        print match
                        listItem = xbmcgui.ListItem(path=str(match[0]))
                        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                        break

                            
                    except:
            ##            Thumblink=re.compile('thumbnail/(.+?)_([0-9]+).*?.jpg"').search(link)
            ##            episode=Thumblink.group(1)
            ##            date=Thumblink.group(2)
            ##            
                        url=[
                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',                        
                        'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
                        'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
                        'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
                        'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
                        'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
                        'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',                         
##                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080p/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
##                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
##                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080p/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
##                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
##                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
##                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
##                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
##                        'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+date[4:6]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
                        ]

                        print m
                        for i in range(len(url)):
                            try:
                                f = urllib2.Request(url[i])
                                f.add_header('User-Agent', default_hdr)
                                f=urllib2.urlopen(f)    
                                dead = False
                                print i
                            except:
                                dead = True
                           
                            if dead==False:
                                print "Correct MP4 found = "+str(url[i])
                                listItem = xbmcgui.ListItem(path=str(url[i]))
                                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                                break
                            elif i ==len(url)-1:
                                print "No MP4 found."
                            

    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')


def resolveAndPlayMovie(url):
    try:
        quality = plugin.get_setting("quality", str)
        req = urllib2.Request(url)
        req.add_header('User-Agent', default_hdr)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup=BeautifulSoup(link)
                
        try:
            f=re.compile('file: "(.*?)"').findall(link)
            print 'Found original link ' + f[0]
            listItem = xbmcgui.ListItem(path=str(f[0]))
            xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
            
        except:
            title1=re.compile('<meta property="og:url" content="http://www.ondemandkorea.com/(.*?).html').findall(link)
            title=re.compile('/uploads/thumbnail/(.*?).[0-9]*p').findall(link)

            
            m=[
            'http://sjc55.ondemandkorea.com:1935/cache/_definst_/smil:gludisp/movies/'+title1[0]+'/'+title[0]+'-smil1080p.smil/playlist.m3u8',
            'http://sjc55.ondemandkorea.com:1935/cache/_definst_/smil:glucache/movies/'+title1[0]+'/'+title[0]+'-smil1080p.smil/playlist.m3u8',
            'http://sjc55.ondemandkorea.com:1935/cache/_definst_/smil:gludisp/movies/'+title1[0]+'/'+title[0]+'-smil720p.smil/playlist.m3u8',
            'http://sjc55.ondemandkorea.com:1935/cache/_definst_/smil:glucache/movies/'+title1[0]+'/'+title[0]+'-smil720p.smil/playlist.m3u8',
            'http://sjc55.ondemandkorea.com:1935/cache/_definst_/smil:gludisp/movies/'+title1[0]+'/'+title[0]+'-smil1080p.smil/playlist.m3u8',
            'http://sjc55.ondemandkorea.com:1935/cache/_definst_/smil:glucache/movies/'+title1[0]+'/'+title[0]+'-smil1080p.smil/playlist.m3u8',
            'http://sjc55.ondemandkorea.com:1935/cache/_definst_/smil:gludisp/movies/'+title1[0]+'/'+title[0]+'-smil720p.smil/playlist.m3u8',
            'http://sjc55.ondemandkorea.com:1935/cache/_definst_/smil:glucache/movies/'+title1[0]+'/'+title[0]+'-smil720p.smil/playlist.m3u8',
            'http://sjc55.ondemandkorea.com:1935/cache/_definst_/smil:gludisp/movies/'+title1[0]+'/'+title[0]+'-smil1080p.smil/playlist.m3u8',
            'http://sjc55.ondemandkorea.com:1935/cache/_definst_/smil:gludisp/movies/'+title1[0]+'/'+title[0]+'-smil480p.smil/playlist.m3u8',
            'http://sjc55.ondemandkorea.com:1935/cache/_definst_/smil:glucache/movies/'+title1[0]+'/'+title[0]+'-smil480p.smil/playlist.m3u8',
            'http://sjc55.ondemandkorea.com:1935/cache/_definst_/smil:gludisp/movies/'+title1[0]+'/'+title[0]+'-smil360p.smil/playlist.m3u8',
            'http://sjc55.ondemandkorea.com:1935/cache/_definst_/smil:glucache/movies/'+title1[0]+'/'+title[0]+'-smil360p.smil/playlist.m3u8',

            ]
       

            for i in range(len(m)):
                try:
                    f = urllib2.Request(m[i])
                    f.add_header('User-Agent', default_hdr)
                    f=urllib2.urlopen(f)    
                    dead = False
                    
                except:
                    dead = True
               
                if dead==False:
                    print "Correct m3u8 found = "+str(m[i])
                    listItem = xbmcgui.ListItem(path=str(m[i]))
                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                    break
                
                elif i ==len(m)-1:
                    print "No m3u8 found."
                    try: 
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', tablet_UA)
                        req.add_header('Accept-Langauge', 'ko')
                        req.add_header('Cookie', 'language=kr')
                        response = urllib2.urlopen(req)
                        link=response.read()
                        response.close()
                        soup=BeautifulSoup(link)
                        
                        match=re.compile('video.src = "(.*?)"').search(link).group(0).replace('360p.1296k','720p.2296k').replace('.480p.1596k','720p.2296k')
                        
                        print match
                        listItem = xbmcgui.ListItem(path=str(match[0]))
                        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                        break

                            
                    except:
            ##            Thumblink=re.compile('thumbnail/(.+?)_([0-9]+).*?.jpg"').search(link)
            ##            episode=Thumblink.group(1)
            ##            date=Thumblink.group(2)
            ##            
                        url=[
                        'http://sjcstor04.ondemandkorea.com/movies/'+title1[0]+'/'+title[0]+'.1080p.4896k.mp4',
                        'http://sjcdisp06.ondemandkorea.com/movies/'+title1[0]+'/'+title[0]+'.1080p.4896k.mp4',
                        'http://sjcstor04.ondemandkorea.com/movies/'+title1[0]+'/'+title[0]+'.720p.2296k.mp4',
                        'http://sjcdisp06.ondemandkorea.com/movies/'+title1[0]+'/'+title[0]+'.720p.2296k.mp4',
                        'http://sjcstor04.ondemandkorea.com/movies/'+title1[0]+'/'+title[0]+'.720p.1596k.mp4',
                        'http://sjcdisp06.ondemandkorea.com/movies/'+title1[0]+'/'+title[0]+'.720p.1596k.mp4',
                        'http://sjcstor04.ondemandkorea.com/movies/'+title1[0]+'/'+title[0]+'.480p.1596k.mp4',
                        'http://sjcdisp06.ondemandkorea.com/movies/'+title1[0]+'/'+title[0]+'.480p.1596k.mp4',
                        'http://sjcstor04.ondemandkorea.com/movies/'+title1[0]+'/'+title[0]+'.480p.2296k.mp4',
                        'http://sjcdisp06.ondemandkorea.com/movies/'+title1[0]+'/'+title[0]+'.480p.2296k.mp4',

                        ]
                        
                        for i in range(len(url)):
                            try:
                                f = urllib2.Request(url[i])
                                f.add_header('User-Agent', default_hdr)
                                f=urllib2.urlopen(f)    
                                dead = False
                                print i
                            except:
                                dead = True
                           
                            if dead==False:
                                print "Correct MP4 found = "+str(url[i])
                                listItem = xbmcgui.ListItem(path=str(url[i]))
                                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                                break
                            elif i ==len(url)-1:
                                print "No MP4 found."


                                

    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def listdramaInCategory(url):
    print url
    try:
        url=url.split(';')
        page=int(url[1])

    except:
        page=1
    req  = urllib2.Request(url[0], headers=default_hdr)
    req.add_header('Accept-Langauge', 'ko')
    req.add_header('Cookie', 'language=kr')
    html = urllib2.urlopen(req).read().decode('utf-8')

    match = re.compile("getJSON\( *\"/[^\"]*\", *{ *cat: *'([^']*)', *id: *(\d+)"). search(html)
    if match:
        program, videoid = match.group(1,2)
    else:
        program = re.compile('"program" *: *"(.*?)"').search(html).group(1)
        videoid = re.compile('"videoid" *: *(\d+)').search(html).group(1)
        
    list_url = root_url+eplist_url.format(program=program, videoid=videoid, page=page)
    print list_url

    req  = urllib2.Request(list_url, headers=default_hdr)
    req.add_header('Accept-Langauge', 'ko')
    req.add_header('Cookie', 'language=kr')
    req.add_header('Referer', url)
    jstr = urllib2.urlopen(req).read()
    obj = json.loads(jstr)

    result = []
    for item in obj['list']:
        result.append({'title':item['title'], 'broad_date':item['on_air_date'], 'url':root_url+"/"+item['url'], 'thumbnail':img_base+item["thumbnail"]})

    for i in range(len(result)):
        title=result[i]['title']+' - '+result[i]['broad_date']
        result[i] = (title, result[i]['url'], result[i]['thumbnail'])

    for name, url2, thumbnail in result:
        addLink(name, url2, 'resolveAndPlayVideo', thumbnail)

    if obj['cur_page'] > 1:
        page=obj['cur_page']-1
        url1=url[0]+';'+str(page)
        addDir('이전 페이지', url1, 'dramaCategoryContent', "")

    if obj['cur_page'] < obj['num_pages']:
        page=obj['cur_page']+1
        url1=url[0]+';'+str(page)
        addDir('다음 페이지', url1, 'dramaCategoryContent', "")
        
def listdramaInCategory2(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', tablet_UA)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

        

##        match2=[]
##        for i in match1:
##            if i not in match2:
##                match2.append(i)
##                
        match=re.compile('<div class="ep.*?">\n\t\t\t\t<a href="(.*?)" title="(.*?)">\n\t\t\t\t\t\n\t\t\t\t\t<img src=".*?src=(.*?)_(.*?)_(.*?)"').findall(link)
        
        for i in range(len(match)):
	    playVideoUrl = root_url + match[i][0]
	    poster1 = root_url + match[i][2] + '_'+ match[i][3] +'_' + match[i][4]
	    poster = poster1.replace(' ','%20')
	    title = unicode(match[i][1], 'utf-8')  + " - " + match[i][3]
	    title = title.replace('.480p.1596k','').replace('amp;','').replace('&#039;','\'').replace('&lt;','<').replace('&gt;','>').replace('360p.1296k','')
	    match[i] = (title, playVideoUrl, poster)

        for title, url, thumbnail, in match:
            addLink(title, url, 'resolveAndPlayVideo', thumbnail)

        
     #soup를 통한 리스팅...
        if len(match)<1:
            print 'failed to match. Using soup'
            soup=BeautifulSoup(link)
            items = []
            for node in soup.findAll('div', {'class':re.compile('^(?:ep|ep_last)$')}):
                if not node.b:
                    continue
                title2 = node.b.string.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&#039;','\'')
                thumb2 = re.compile('img src=".*?/wp-content(.*?)"').findall(str(node))
                thumb1 = root_url+'wp-content'+thumb2[0]
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
        page=root_url+'includes/episode_page.php?cat='+match1[0][0]+'&id=' +match1[0][1]+'&page=99'

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
                        Pgurl = root_url+'includes/episode_page.php?cat='+match1[0][0]+'&id=' +match1[0][1]+'&page='+str(i)
                        req = urllib2.Request(Pgurl)
                        response = urllib2.urlopen(req)
                        link=response.read()
                        match=re.compile('"url":"(.*?)"').search(link).group(1)
                        Pgurl=root_url+''+match
                        name=str(i) +' 페이지'
                        addDir(name, Pgurl, 'dramaCategoryContent', "")
      
        
           
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

##

def listMovieCategories(url):
    try:
        print "requesting url " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', default_hdr)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')  
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<dd class="thumb"><a href="(.*?)".*?><img src="(.+?)" alt="(.*?)">').findall(link)
        
        for i in range(len(match)):
            playVideoUrl = root_url+'' + match[i][0]
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
                thumb1 = root_url+'wp-content'+thumb2[0]
                thumb = thumb1.replace(' ','%20')
                dt = node.find("span", {"class":"thumb-date"}).find(text=True)
                title = title2 + ' - '+dt
                genre = node.find('dd', {"class":"info1"}).find(text=True)
                genre1 = genre.replace('\n\t\t\t\t\t\t    ','').replace('\t\t\t\t\t\t\t ','')
                genre2 = genre1.split('/')
                items.append({'title':title, 'year':dt, 'genre':genre2, 'url':root_url+node.a['href'], 'thumbnail':thumb})

           
            for i in range(len(items)):
                items[i] = (items[i]['title'], items[i]['url'], items[i]['thumbnail'])
                  
            
            for name, url, thumbnail in items:
                addLink(name, url, 'resolveAndPlayMovie', thumbnail)
                
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
    elif params["mode"] == 'resolveAndPlayMovie':
        resolveAndPlayMovie(urlUnquoted)
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
