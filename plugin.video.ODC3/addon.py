# -*- coding: utf-8 -*-
"""
    Ondemand Korea
"""
from xbmcswift2 import Plugin
import os
import json
import requests
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

##Play vid for plus
tablet_UA = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19"
root_url = "http://www.ondemandkorea.com/"

img_base = "http://sp.ondemandkorea.com/includes/timthumb.php?w=175&h=100&src="
eplist_url = "includes/episode_page.php?cat={program:s}&id={videoid:s}&page={page:d}"

default_hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Connection': 'keep-alive'}
##


## Get token
##try:
##    tokenurl='http://api.ondemandkorea.com/api3/device/index.php'
##    data={'language': '0',
##                   'adid': '4617319a-7b87-40fd-a62e-d0ae587da6cc',
##                   'appShorterVersion':'1.8.26',
##                   'idfv':'f94606748c42f360',
##                   'screenid':'0',
##                   'appBundleVersion':'1.8.26'
##          }
##    headers={
##        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
##        'User-Agent': 'MMozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19',
##            }
##
##    r = requests.post(tokenurl, data=data, headers=headers)
##    obj = json.loads(r.text)
##
##    token=obj['accessToken']
##except:
token='432b1a3e19ba4d68d169d85a71de3a0ded683edfe0239f24fafd2db611f1e081'

def listMainCategories():
    addDir("최근 방영", '0', "RecentCategories", '')  
    addDir("드라마", "2", "videoCategories", '')
    addDir("예능/오락", "6", "videoCategories", '')
    addDir("시사/다큐", "450", "videoCategories", '')
    addDir("음식/요리", "452", "videoCategories", '')
    addDir("뷰티/패션", "453", "videoCategories", '')
    #addDir("여성", root_url+"women", "videoCategories", '')
    addDir("건강", "455", "videoCategories", '')
    #addDir("교육", "1", "videoCategories", '')  
    #addDir("어린이", "22", "videoCategories", '')          
    #addDir("스포츠", "17", "videoCategories", '')    
    #addDir("경제", ""180, "videoCategories", '')    
    #addDir("종교", "75", "videoCategories", '')    
    #addDir("음악", "109", "videoCategories", '')
    #addDir("게임", root_url+"games", "videoCategories", '')
    addDir("한국 영화", '808', "videoCategories", '')



def listRecentCategories(url):
    url='http://api.ondemandkorea.com/api3/home/index.php'
    data={'language': '0',
                   'adid': '4617319a-7b87-40fd-a62e-d0ae587da6cc',
                   'appShorterVersion':'1.8.26',
                   'idfv':'f94606748c42f360',
                   'screenid':'0',
                   'appBundleVersion':'1.8.26',
                   'accessToken': token,
          }
    headers={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}

    r = requests.post(url, data=data, headers=headers)
    print(r.status_code, r.reason)
    obj = json.loads(r.text)


    result = []
    for item in obj['data'][2]['data']:
        title=item['title']+' - '+item['broadcastDate']
        thumb1=item["thumbnailUrl"]
        thumb=thumb1.replace('http://sp.ondemandkorea.com/includes/timthumb.php?w=424&h=239&src=','').replace('http://sp.ondemandkorea.com/includes/timthumb.php?src=','http://sp.ondemandkorea.com').replace('&w=424&h=239','').replace('&w=320&h=468','')
        rootch=re.compile('ondemandkorea.com').search(thumb)
        if rootch:
            thumb=thumb
        else:
            thumb='http://sp.ondemandkorea.com'+thumb
        
        #if item['plusOnly']=='0':
        eid=item['id']+'^'+item['plusOnly']+'^'+item['slug']
        result.append([title, eid, thumb])

    result.append(['##예능##', '', ''])
    
    for item in obj['data'][3]['data']:
        title=item['title']+' - '+item['broadcastDate']
        thumb1=item["thumbnailUrl"]
        thumb=thumb1.replace('http://sp.ondemandkorea.com/includes/timthumb.php?w=424&h=239&src=','').replace('http://sp.ondemandkorea.com/includes/timthumb.php?src=','http://sp.ondemandkorea.com').replace('&w=424&h=239','').replace('&w=320&h=468','')
        rootch=re.compile('ondemandkorea.com').search(thumb)
        if rootch:
            thumb=thumb
        else:
            thumb='http://sp.ondemandkorea.com'+thumb
        #if item['plusOnly']=='0':   
        eid=item['id']+'^'+item['plusOnly']+'^'+item['slug']
        result.append([title, eid, thumb])
                              
    for name, url2, thumbnail in result:
        addLink(name, url2, 'resolveAndPlayVideo', thumbnail)
    
def listVideoCategories(url):
    url2='http://api.ondemandkorea.com/api3/category/index.php'
    data={'language': '0',

                   'accessToken': token,
                   'id':url
          }
    headers={
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'MMozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19',
            }
    r = requests.post(url2, data=data, headers=headers)
    print(r.status_code, r.reason)
    obj = json.loads(r.text)


    result = []
    current = []
    past = []
    for item in obj['data']:
        #if item['odkPlus']=='0':
        thumb1=item["posterUrl"]
        thumb=thumb1.replace('http://sp.ondemandkorea.com/includes/timthumb.php?w=424&h=239&src=','http://sp.ondemandkorea.com').replace('http://sp.ondemandkorea.com/includes/timthumb.php?src=','http://sp.ondemandkorea.com').replace('&w=424&h=239','').replace('&w=320&h=468','')
        rootch=re.compile('ondemandkorea.com').search(thumb)
        if rootch:
            thumb=thumb
        else:
            thumb='http://sp.ondemandkorea.com'+thumb

        result.append({'id':item['id'], 'title':item['title'], 'broad_date':item['latestDate'], 'thumbnail':thumb,'stat':item['status'], 'new':item['new']})

    for i in range(len(result)):
        if result[i]['stat']=='current':
            if result[i]['new']=='true':
                title=result[i]['title']+' - NEW'
                current.append([title, result[i]['id'], result[i]['thumbnail']])
            
            else:
                current.append([result[i]['title'], result[i]['id'], result[i]['thumbnail']])
        
            
        else:
            past.append([result[i]['title'], result[i]['id'], result[i]['thumbnail']])

    current=sorted(current)
    current.append(['## ## ## ## ##이하 종영방송## ## ## ## ##','', ''])
    current.extend(past)

    for name, url2, thumbnail in current:
        addDir(name, url2, 'dramaCategoryContent', thumbnail)


def listdramaInCategory(url):
    url2='http://api.ondemandkorea.com/api3/program/index.php'
    data={'language': '0',
                   'adid': '4617319a-7b87-40fd-a62e-d0ae587da6cc',
                   'appShorterVersion':'1.8.26',
                   'idfv':'f94606748c42f360',
                   'screenid':'0',
                   'appBundleVersion':'1.8.26',
                   'accessToken': token,
                  'id': url,
                  'size':'300',
                  'from':'0'
          }
    headers={
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'MMozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19',
            }
    r = requests.post(url2, data=data, headers=headers)
    print(r.status_code, r.reason)
    obj = json.loads(r.text)


    result = []
    for item in obj['data']:
        title=item['title']+' - '+item['broadcastDate']
        thumb1=item["thumbnailUrl"]
        thumb=thumb1.replace('http://sp.ondemandkorea.com/includes/timthumb.php?w=424&h=239&&src=','http://sp.ondemandkorea.com').replace('http://sp.ondemandkorea.com/includes/timthumb.php?src=','http://sp.ondemandkorea.com').replace('&w=424&h=239','').replace('&w=320&h=468','')
        rootch=re.compile('ondemandkorea.com').search(thumb)
        if rootch:
            thumb=thumb
        else:
            thumb='http://sp.ondemandkorea.com'+thumb
        eid=item['id']+'^'+item['plusOnly']+'^'+item['slug']
        result.append([title, eid,thumb ])

    for name, url2, thumbnail in result:
        addLink(name, url2, 'resolveAndPlayVideo', thumbnail)

def resolveAndPlayVideo(url):
    url=url.split('%5E')
    plus=0
    if plus==0:
        url2='http://api.ondemandkorea.com/api3/episode/index.php'
        data={'language': '0',
                       'adid': '4617319a-7b87-40fd-a62e-d0ae587da6cc',
                       'appShorterVersion':'1.8.26',
                       'idfv':'f94606748c42f360',
                       'screenid':'0',
                       'appBundleVersion':'1.8.26',
                       'accessToken': token,
                       'id':url[0]
              }
        headers={
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'MMozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19',
                }
        r = requests.post(url2, data=data, headers=headers)
        obj = json.loads(r.text)


        use_mp4_url = plugin.get_setting('mp4_url', bool)
        quality = plugin.get_setting("quality", str)
        if use_mp4_url:
            if quality == '1':
                listItem = xbmcgui.ListItem(path=obj['episode']['mp4Src'][1]['src'])
                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
            
            else:
                try:
                    f = urllib2.Request(obj['episode']['mp4Src'][0]['src'])
                    f.add_header('User-Agent', default_hdr)
                    f=urllib2.urlopen(f)    
                    dead = False
                except:
                    dead = True
           
                if dead==False:
                    listItem = xbmcgui.ListItem(path=obj['episode']['mp4Src'][0]['src'])
                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                else:
                    add=re.compile('/v1/[0-9]+/').search(obj['episode']['videoSrc']).group()
                    url=obj['episode']['mp4Src'][0]['src']
                    url=url.replace('ondemandkorea.com/','ondemandkorea.com/'+add)
                    listItem = xbmcgui.ListItem(path=url)
                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
        else:
##            if quality == '1':
##                vurl1=obj['episode']['videoSrc']
##                vurl=vurl1.replace('1080','720')
##                plugin.play_video( {'label': title, 'path':vurl} )
##            else:
            listItem = xbmcgui.ListItem(path=obj['episode']['videoSrc'])
            xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
    
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
        listVideoCategories(url)
##    elif params["mode"] == 'videoCategoryContent':
##        listVideosInCategory(urlUnquoted)
        
    elif params["mode"] == 'resolveAndPlayVideo':
        resolveAndPlayVideo(url)
##    elif params["mode"] == 'resolveAndPlayMovie':
##        resolveAndPlayMovie(urlUnquoted)
##
##    elif params["mode"] == 'dramafever':
##        listdramafever(urlUnquoted)
##    elif params["mode"] == 'dramafeverPlay':
##        dramafeverPlay(urlUnquoted)
        
##    elif params["mode"] == 'dramaCategories':
##        listdramaCategories(urlUnquoted)   
    elif params["mode"] == 'dramaCategoryContent':
        listdramaInCategory(url)


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
        listRecentCategories(url)
##    elif params["mode"] == 'MovieCategories':
##        listMovieCategories(urlUnquoted)
##    elif params["mode"] == 'resolveAndPlayMovie':
##        resolveAndPlayMovie(urlUnquoted)
        
xbmcplugin.endOfDirectory(_thisPlugin)        

