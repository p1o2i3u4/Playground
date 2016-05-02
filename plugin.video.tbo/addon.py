# -*- coding: utf-8 -*-
"""
    Ondemand Korea
"""
from xbmcswift2 import Plugin
import os
import xbmcplugin, xbmcgui, sys
import urllib2, urllib, re, cookielib
from BeautifulSoup import BeautifulSoup

username = 'anonymous'
password = 'anonymous'

plugin = Plugin()

# magic; id of this plugin's instance - cast to integer
_pluginName = (sys.argv[0])
_thisPlugin = int(sys.argv[1])
_connectionTimeout = 20
UserAgent = "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"
tablet_UA = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19"


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent',
    ('Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'))
]
login_data = urllib.urlencode({'pg_mode' : 'login_proc', 'userid' : username, 'userpw' : password})
opener.open('https://www.tbogo.com/member/', login_data)
        
def listMainCategories():
    #addDir("최근 방영", "http://www.ondemandkorea.com/", "RecentCategories", '')  
    addDir("드라마", "B01,onair", "dramaCategories", '')
    addDir("예능/오락", "B02,onair", "videoCategories", '')
    addDir("시사/다큐", "B03,onair", "videoCategories", '')
    #addDir("유아", "B05,onair", "videoCategories", '')
    addDir("영화", "M", "MovieCategories", '')
    #addDir("케이블", "B04,onair", "videoCategories", '')
    addDir("기분 좋은 날", "238", "dramaCategoryContent", '')
    addLink("##이후 종영 방송##", "", "", '')
    addDir("종영 드라마", "B01,offair", "dramaCategories", '')
    addDir("종영 예능/오락", "B02,offair", "videoCategories", '')
    addDir("종영 시사/다큐", "B03,offair", "videoCategories", '')

def listMovieCategories(url):
    #try:
    day2=[]
    g=[]
    for n in range(0,220,18):
        url2='https://www.tbogo.com/media/?&pg_mode=xml&start='+str(n)+'&code='+url
        req = urllib2.Request(url2)
        req.add_header('User-Agent', UserAgent)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

        try:

            day=re.compile('<info><\!\[CDATA\[(.*?) \|.*?([0-9][0-9][0-9][0-9])').findall(link)
            if day:
                
                day2.extend(day)
                l=re.compile('<a href=".*?([0-9]+)" title="(.*?)"').findall(link)

                ## remove duplicates from l
                seen = set()
                l2=[[y for y in x if y not in seen and not seen.add(y)] for x in l]
                l3=[x for x in l2 if x]

                img=re.compile('img src="(.*?)" width="([0-9]+)" height="([0-9]+)"').findall(link)

                ##combine two lists, first convert tuple to list (img)
                match3=[(x+y) for x,y in zip(l3,map(list,img))]
                g.extend(match3)
                
            else:
                print "no more episodes"
                break
        except:
            print 'error'
            break

    for i in range(len(g)):
        playVideoUrl = g[i][0]
        title = re.sub("&amp;","&", re.sub(r"E\d+","", g[i][1])) + '   -   ('+ day2[i][1]+')'
        g[i] = (day2[i][1], title, playVideoUrl, g[i][2])

    g.sort(reverse=True)
    
    for date, name, url, thumbnail in g:
        addLink(name, url, 'resolveAndPlayMovie', thumbnail)
                
##    except urllib2.URLError:
##        addLink("성용이를 불러주세용.", '', '', '')
        
def listVideoCategories(url):
    try:
        day2=[]
        g=[]
        url=url.split(',')
        
        for n in range(0,220,15):
            url2='https://www.tbogo.com/media/?&pg_mode=xml&start='+str(n)+'&code='+url[0]+'&type='+url[1]
            req = urllib2.Request(url2)
            req.add_header('User-Agent', UserAgent)
            req.add_header('Accept-Langauge', 'ko')
            req.add_header('Cookie', 'language=kr')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()

            try:

                day=re.compile('<info><\!\[CDATA\[(.*?) \|.*?([0-9]+-[0-9]+-[0-9]+)').findall(link)
                if day:
                    
                    day2.extend(day)
                    l=re.compile('<a href=".*?([0-9]+)" title="(.*?)"').findall(link)

                    ## remove duplicates from l
                    seen = set()
                    l2=[[y for y in x if y not in seen and not seen.add(y)] for x in l]
                    l3=[x for x in l2 if x]

                    img=re.compile('img src="(.*?)" width="([0-9]+)" height="([0-9]+)"').findall(link)

                    ##combine two lists, first convert tuple to list (img)
                    match3=[(x+y) for x,y in zip(l3,map(list,img))]
                    g.extend(match3)
                    
                else:
                    print "no more episodes"
                    break
            except:
                print 'error'
                break

        for i in range(len(g)):
            playVideoUrl = g[i][0]
            title = re.sub("&amp;","&", re.sub(r"E\d+","", g[i][1])) + '      ('+ day2[i][1]+')'
            g[i] = (title, playVideoUrl, g[i][2])

        g.sort()
           
        for name, url, thumbnail in g:
            addDir(name, url, 'dramaCategoryContent', thumbnail)
                
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def listdramaCategories(url):
    try:
        day2=[]
        g=[]
        url=url.split(',')
        for n in range(0,220,15):
            url2='https://www.tbogo.com/media/?&pg_mode=xml&start='+str(n)+'&code='+url[0]+'&type='+url[1]
            req = urllib2.Request(url2)
            req.add_header('User-Agent', UserAgent)
            req.add_header('Accept-Langauge', 'ko')
            req.add_header('Cookie', 'language=kr')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()

            try:

                day=re.compile('<info><\!\[CDATA\[(.*?) \|.*?([0-9]+-[0-9]+-[0-9]+)').findall(link)
                if day:
                    
                    day2.extend(day)
                    l=re.compile('<a href=".*?([0-9]+)" title="(.*?)"').findall(link)

                    ## remove duplicates from l
                    seen = set()
                    l2=[[y for y in x if y not in seen and not seen.add(y)] for x in l]
                    l3=[x for x in l2 if x]

                    img=re.compile('img src="(.*?)" width="([0-9]+)" height="([0-9]+)"').findall(link)

                    ##combine two lists, first convert tuple to list (img)
                    match3=[(x+y) for x,y in zip(l3,map(list,img))]
                    g.extend(match3)
              
                else:
                    print "no more episodes"
                    break
            except:
                print 'error'
                break

        for i in range(len(g)):
            playVideoUrl = g[i][0]
            ##re.sub(r"E\d+","", g[i][1]) is for replacing episode. http://stackoverflow.com/questions/5658369/how-to-input-a-regex-in-string-replace-in-python
            title = day2[i][0]+': ' + re.sub("&amp;","&", re.sub(r"E\d+","", g[i][1])) + '      ('+ day2[i][1]+')'
            g[i] = (title, playVideoUrl, g[i][2])

        g.sort()
           
        for name, url, thumbnail in g:
            addDir(name, url, 'dramaCategoryContent', thumbnail)
                
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
        
        
##def listVideoCategories(url):
##    try:
##        req = urllib2.Request(url)
##        req.add_header('User-Agent', UserAgent)
##        req.add_header('Accept-Langauge', 'ko')
##        req.add_header('Cookie', 'language=kr')
##        response = urllib2.urlopen(req, timeout = _connectionTimeout)
##        link=response.read()
##        response.close()
##        
##        day=re.compile('<info><\!\[CDATA\[(.*?) \|.*?([0-9]+-[0-9]+-[0-9]+)').findall(link)
##        l=re.compile('<a href=".*?([0-9]+)" title="(.*?) E').findall(link)
##
##        ## remove duplicates from l
##        seen = set()
##        l2=[[y for y in x if y not in seen and not seen.add(y)] for x in l]
##        l3=[x for x in l2 if x]
##
##        img=re.compile('img src="(.*?)" width="([0-9]+)" height="([0-9]+)"').findall(link)
##
##        ##combine two lists, first convert tuple to list (img)
##        match3=[(x+y) for x,y in zip(l3,map(list,img))]
##
##
##        ###Page 2
##        url2= 'https://www.tbogo.com/media/?&pg_mode=xml&start=15&code=B01&type=onair'
##        req = urllib2.Request(url2)
##        req.add_header('User-Agent', UserAgent)
##        req.add_header('Accept-Langauge', 'ko')
##        req.add_header('Cookie', 'language=kr')
##        response = urllib2.urlopen(req)
##        link=response.read()
##        response.close()
##
##        day2=re.compile('<info><\!\[CDATA\[(.*?) \|.*?([0-9]+-[0-9]+-[0-9]+)').findall(link)
##        ##combine two days
##        day.extend(day2)
##        l=re.compile('<a href=".*?([0-9]+)" title="(.*?) E').findall(link)
##
##        ## remove duplicates from l
##        seen = set()
##        l2=[[y for y in x if y not in seen and not seen.add(y)] for x in l]
##        l3=[x for x in l2 if x]
##
##        img=re.compile('img src="(.*?)" width="([0-9]+)" height="([0-9]+)"').findall(link)
##
##        ##combine two lists, first convert tuple to list (img)
##        match4=[(x+y) for x,y in zip(l3,map(list,img))]
##
##        match3.extend(match4)
##        for i in range(len(match3)):
##            playVideoUrl = match3[i][0]
##            title = day[i][0]+': ' + match3[i][1] + '      ('+ day[i][1]+')'
##            match3[i] = (title, playVideoUrl, match3[i][2])
##
##        match3.sort()
##        for name, url, thumbnail in match3:
##            addDir(name, url, 'dramaCategoryContent', thumbnail)
##                
##    except urllib2.URLError:
##        addLink("성용이를 불러주세용.", '', '', '')

def listdramaInCategory(url):
    try:
        

        resp = opener.open('https://www.tbogo.com/media/?&pg_mode=xml_blist&idx='+url+'&start=0')
        link=resp.read()

        l=re.compile('stream\(\'(.*?) &lt;').findall(link)
        l2=re.compile('stream\(\'.*?,([0-9]+)').findall(link)
        l4=re.compile('img src="https://image.tbogo.com/(.*?)"').findall(link)
        date=re.compile('<span class="postDate">(.*?)</span>').findall(link)

        l3=re.compile('stream\(\'.*?E([0-9]+)').findall(link)
        l= [(a+' : '+b+'회'+' - '+c) for a,b,c in zip(l,l3,date)]

        for i in range(len(l4)):
            l4[i] = 'https://image.tbogo.com/'+l4[i]
            l2[i] = url+','+l2[i]
            
            
        l5=[(a,b,c) for a,b,c in zip(l,l2,l4)]
        
        for title, url2, thumbnail, in l5:
            addLink(title, url2, 'resolveAndPlayVideo', thumbnail)

        
        page='https://www.tbogo.com/media/?&pg_mode=xml_blist&idx='+url+'&start=15'
        resp = opener.open(page)
        link=resp.read()

        l=re.compile('stream\(\'(.*?) &lt;').findall(link)

        if l:
            addDir('다음 페이지', url+',0', 'NextPage', '')

    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def NextPage(url):
    try:
        url=url.split(',')
        p=int(url[1])+15
        
        resp = opener.open('https://www.tbogo.com/media/?&pg_mode=xml_blist&idx='+url[0]+'&start='+str(p))
        link=resp.read()

        l=re.compile('stream\(\'(.*?) &lt;').findall(link)
        l2=re.compile('stream\(\'.*?,([0-9]+)').findall(link)
        l4=re.compile('img src="https://image.tbogo.com/(.*?)"').findall(link)
        date=re.compile('<span class="postDate">(.*?)</span>').findall(link)

        l3=re.compile('stream\(\'.*?E([0-9]+)').findall(link)
        l= [(a+' : '+b+'회'+' - '+c) for a,b,c in zip(l,l3,date)]

        for i in range(len(l4)):
            l4[i] = 'https://image.tbogo.com/'+l4[i]
            l2[i] = url[0]+','+l2[i]
            
            
        l5=[(a,b,c) for a,b,c in zip(l,l2,l4)]
        
        for title, url2, thumbnail, in l5:
            addLink(title, url2, 'resolveAndPlayVideo', thumbnail)

        p=p+15
        page='https://www.tbogo.com/media/?&pg_mode=xml_blist&idx='+url[0]+'&start='+str(p)
        resp = opener.open(page)
        link=resp.read()

        l=re.compile('stream\(\'(.*?) &lt;').findall(link)

        if l:
            addDir('다음 페이지', url[0]+','+str(p), 'NextPage', '')

                
    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')
        
def resolveAndPlayVideo(url):
    quality = plugin.get_setting("quality", str)
    if quality =='2':
        quality = '720P'

    elif quality =='1':
        quality = '450P'
        
    else:
        quality = 'MP4'
        
    url=url.split(',')
    try:
        for n in range(181,192):
            url1='http://s'+str(n)+'.tbogo.com/play_link/'+url[0]+'_'+url[1]+'_'+quality+'.mp4'
            print url1
            try:
              f = urllib2.Request(url1)
              f.add_header('User-Agent', UserAgent)
              f2= urllib2.urlopen(f)
              deadLinkFound = False
            except:
              deadLinkFound = True

            if deadLinkFound==False:
                print 'Correct url found = '+url1                
                listItem = xbmcgui.ListItem(path=str(url1))
                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                break
            elif n==191:
                
                print "No 720P Found, Looking for 450P"
                for n in range(181,192):
                    url1='http://s'+str(n)+'.tbogo.com/play_link/'+url[0]+'_'+url[1]+'_450P.mp4'

                    try:
                      f = urllib2.Request(url1)
                      f.add_header('User-Agent', UserAgent)
                      f2= urllib2.urlopen(f)
                      deadLinkFound = False
                    except:
                      deadLinkFound = True

                    if deadLinkFound==False:
                        print 'Correct url found = '+url1                
                        listItem = xbmcgui.ListItem(path=str(url1))
                        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                        break
   

    except urllib2.URLError:
        addLink("성용이를 불러주세용.", '', '', '')

def resolveAndPlayMovie(url):

    quality = plugin.get_setting("quality", str)
    if quality =='2':
        quality = '720P'

    elif quality =='1':
        quality = '450P'
        
    else:
        quality = 'MP4'
        
    

    resp = opener.open('https://www.tbogo.com/media/?&pg_mode=xml_blist&idx='+url+'&start=0')
    link=resp.read()

    l2=re.compile('stream\(\'.*?,([0-9]+)').findall(link)

    
    url=url.split(',')
    try:
        for n in range(181,192):
            url1='http://s'+str(n)+'.tbogo.com/play_link/'+str(url[0])+'_'+str(l2[0])+'_'+quality+'.mp4'
            try:
              f = urllib2.Request(url1)
              f.add_header('User-Agent', UserAgent)
              f2= urllib2.urlopen(f)
              deadLinkFound = False
            except:
              deadLinkFound = True

            if deadLinkFound==False:
                print 'Correct url found = '+url1                
                listItem = xbmcgui.ListItem(path=str(url1))
                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                break
            elif n==191:
              

                print "No 720P Found, Looking for 450P"
                for n in range(181,192):
                    url1='http://s'+str(n)+'.tbogo.com/play_link/'+str(url[0])+'_'+str(l2[0])+'_450P.mp4'

                    try:
                      f = urllib2.Request(url1)
                      f.add_header('User-Agent', UserAgent)
                      f2= urllib2.urlopen(f)
                      deadLinkFound = False
                    except:
                      deadLinkFound = True

                    if deadLinkFound==False:
                        print 'Correct url found = '+url1                
                        listItem = xbmcgui.ListItem(path=str(url1))
                        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                        break


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
    elif params["mode"] == 'resolveAndPlayVideo':
        resolveAndPlayVideo(urlUnquoted)

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
        
    elif params["mode"] == 'NextPage':
        NextPage(urlUnquoted)
    elif params["mode"] == 'MovieCategories':
        listMovieCategories(urlUnquoted)
    elif params["mode"] == 'resolveAndPlayMovie':
        resolveAndPlayMovie(urlUnquoted)
        
xbmcplugin.endOfDirectory(_thisPlugin)        
