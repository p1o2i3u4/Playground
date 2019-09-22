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
from datetime import date

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

img_base = "https://sp.ondemandkorea.com/includes/timthumb.php?w=175&h=100&src="
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
##    tokenurl='https://api.ondemandkorea.com/api3/device/'
##    data={'language': '0',
##                   'adid': 'a36f8a5d-edae-44b7-b88d-ff0981008535',
##                   'appShorterVersion':'1.8.93',
##                   'idfv':'ef4212b0a9778005',
##                   'screenid':'0',
##                   'appBundleVersion':'1.8.93'
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
    addDir("종영 드라마", "2", "VideoCategoriesPast", '')
    addDir("예능/오락", "6", "videoCategories", '')
    addDir("종영 예능/오락", "6", "VideoCategoriesPast", '')
    addDir("시사/다큐", "450", "videoCategories", '')
    addDir("음식/요리", "452", "videoCategories", '')
    #addDir("화제영상", "39", "videoCategories", '')
    addDir("뷰티/패션", "453", "videoCategories", '')
    #addDir("여성", root_url+"women", "videoCategories", '')
    addDir("건강", "455", "videoCategories", '')
    #addDir("교육", "1", "videoCategories", '')        
    #addDir("스포츠", "17", "videoCategories", '')    
    #addDir("경제", ""180, "videoCategories", '')    
    #addDir("종교", "75", "videoCategories", '')    
    #addDir("음악", "109", "videoCategories", '')
    #addDir("게임", root_url+"games", "videoCategories", '')
    #addDir("웹 드라마", '2730', "videoCategories", '')
    #addDir("웹 예능", '2731', "videoCategories", '')
    addDir("한국 영화", '808', "videoCategories", '')
    addDir("어린이", "22", "videoCategories", '')  



def listRecentCategories(url):
    url='https://api.ondemandkorea.com/api3/home2/'
    data={'language': '0',
                   'adid': 'a36f8a5d-edae-44b7-b88d-ff0981008535',
                   'appShorterVersion':'1.8.93',
                   'idfv':'ef4212b0a9778005',
                   'screenid':'0',
                   'appBundleVersion':'1.8.93',
                   'accessToken': token,
          }
    headers={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}

    r = requests.post(url, data=data, headers=headers)
    print(r.status_code, r.reason)
    obj = json.loads(r.text)

    #print "testingx"
    #print obj
    result = []
    for item in obj['data'][2]['data']:
        title=item['title']+' - '+item['broadcastDate']
        thumb1=item["thumbnailUrl"]
        thumb=thumb1.replace('https://sp.ondemandkorea.com/includes/timthumb.php?w=424&h=239&src=','').replace('https://sp.ondemandkorea.com/includes/timthumb.php?src=','https://sp.ondemandkorea.com').replace('&w=424&h=239','').replace('&w=320&h=468','')
        rootch=re.compile('ondemandkorea.com').search(thumb)
        if rootch:
            thumb=thumb
        else:
            thumb='https://sp.ondemandkorea.com'+thumb
        
        #if item['plusOnly']=='0':
        eid=item['id']+'^'+item['plusOnly']+'^'+item['slug']+'^'+item['categoryId']+'^'+item['broadcastDate']
        result.append([title, eid, thumb])

    result.append(['##예능##', '', ''])
    
    for item in obj['data'][3]['data']:
        title=item['title']+' - '+item['broadcastDate']
        thumb1=item["thumbnailUrl"]
        thumb=thumb1.replace('https://sp.ondemandkorea.com/includes/timthumb.php?w=424&h=239&src=','').replace('https://sp.ondemandkorea.com/includes/timthumb.php?src=','https://sp.ondemandkorea.com').replace('&w=424&h=239','').replace('&w=320&h=468','')
        rootch=re.compile('ondemandkorea.com').search(thumb)
        if rootch:
            thumb=thumb
        else:
            thumb='https://sp.ondemandkorea.com'+thumb
        #if item['plusOnly']=='0':   
        eid=item['id']+'^'+item['plusOnly']+'^'+item['slug']+'^'+item['categoryId']+'^'+item['broadcastDate']
        result.append([title, eid, thumb])
                              
    for name, url2, thumbnail in result:
        addLink(name, url2, 'resolveAndPlayVideoRecent', thumbnail)
    
def listVideoCategories(url):
    url2='https://api.ondemandkorea.com/api3/category/'
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
        thumb=thumb1.replace('https://sp.ondemandkorea.com/includes/timthumb.php?w=424&h=239&src=','https://sp.ondemandkorea.com').replace('https://sp.ondemandkorea.com/includes/timthumb.php?src=','https://sp.ondemandkorea.com').replace('&w=424&h=239','').replace('&w=320&h=468','')
        rootch=re.compile('ondemandkorea.com').search(thumb)
        if rootch:
            thumb=thumb
        else:
            thumb='https://sp.ondemandkorea.com'+thumb

        result.append({'id':item['id'], 'title':item['title'], 'broad_date':item['latestDate'], 'thumbnail':thumb,'stat':item['status'], 'new':item['new']})

    for i in range(len(result)):
        if result[i]['stat']=='current':
            if result[i]['new']=='true':
                title=result[i]['title']+' - NEW'
                current.append([title, result[i]['id'], result[i]['thumbnail']])
            
            else:
                current.append([result[i]['title'], result[i]['id'], result[i]['thumbnail']])
        
            
##        else:
##            past.append([result[i]['title'], result[i]['id'], result[i]['thumbnail']])

    current=sorted(current)
##    current.append(['## ## ## ## ##이하 종영방송## ## ## ## ##','', ''])
##    current.extend(past)

    for name, url2, thumbnail in current:
        addDir(name, url2, 'dramaCategoryContent', thumbnail)


def listVideoCategoriesPast(url):
    url2='https://api.ondemandkorea.com/api3/category/'
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
        thumb=thumb1.replace('https://sp.ondemandkorea.com/includes/timthumb.php?w=424&h=239&src=','https://sp.ondemandkorea.com').replace('https://sp.ondemandkorea.com/includes/timthumb.php?src=','https://sp.ondemandkorea.com').replace('&w=424&h=239','').replace('&w=320&h=468','')
        rootch=re.compile('ondemandkorea.com').search(thumb)
        if rootch:
            thumb=thumb
        else:
            thumb='https://sp.ondemandkorea.com'+thumb

        result.append({'id':item['id'], 'title':item['title'], 'broad_date':item['latestDate'], 'thumbnail':thumb,'stat':item['status'], 'new':item['new']})

    for i in range(len(result)):
        if result[i]['stat']=='current':
            pass
        else:
            past.append([result[i]['title'], result[i]['id'], result[i]['thumbnail']])

    past=sorted(past)

    for name, url2, thumbnail in past:
        addDir(name, url2, 'dramaCategoryContent', thumbnail)
        
def listdramaInCategory(url):
    url2='https://api.ondemandkorea.com/api3/program/'
    data={'language': '0',
                   'adid': 'a36f8a5d-edae-44b7-b88d-ff0981008535',
                   'appShorterVersion':'1.8.93',
                   'idfv':'ef4212b0a9778005',
                   'screenid':'0',
                   'appBundleVersion':'1.8.93',
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

    #print obj
    src=obj['program']['topEpisode']['videoSrc']
    
    result = []
    for item in obj['data']:
        title=item['title']+' - '+item['broadcastDate']
        thumb1=item["thumbnailUrl"]
        thumb=thumb1.replace('https://sp.ondemandkorea.com/includes/timthumb.php?w=424&h=239&&src=','https://sp.ondemandkorea.com').replace('https://sp.ondemandkorea.com/includes/timthumb.php?src=','https://sp.ondemandkorea.com').replace('&w=424&h=239','').replace('&w=320&h=468','')
        rootch=re.compile('ondemandkorea.com').search(thumb)
        if rootch:
            thumb=thumb
        else:
            thumb='https://sp.ondemandkorea.com'+thumb

                            
        inds= [i for i,c in enumerate(src) if c=='/']
        src2= src.replace(src[inds[-2]+1:inds[-1]], item['slug'])

        inds= [i for i,c in enumerate(src2) if c=='/']
        src3=src2.replace(src2[inds[4]+1:inds[5]], item['broadcastDate'][-4]+item['broadcastDate'][-3]+item['broadcastDate'][-2]+item['broadcastDate'][-1]+item['broadcastDate'][0]+item['broadcastDate'][1])
            
        eid=item['id']+'^'+item['plusOnly']+'^'+item['slug']+'^'+src3
        result.append([title, eid,thumb ])

    for name, url2, thumbnail in result:
        addLink(name, url2, 'resolveAndPlayVideo', thumbnail)

def resolveAndPlayVideo(url):
    url=url.split('%5E')
    plus=0
    today = date.today()

    print url
    if plus==0:
        url2='https://api.ondemandkorea.com/api3/episode/'
        data={'language': '0',
                       'adid': 'a36f8a5d-edae-44b7-b88d-ff0981008535',
                       'appShorterVersion':'1.8.93',
                       'idfv':'ef4212b0a9778005',
                       'screenid':'0',
                       'appBundleVersion':'1.8.93',
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
        prefix = plugin.get_setting("prefix", str)
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

      
            try:
                #print "testingx"
                if quality == '1':
                    url[3]=url[3].replace('%3A',':').replace('%2F','/')

                    
                    print url[3]
                    listItem = xbmcgui.ListItem(path=url[3])
                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                    
                else:
                    url[3]=url[3].replace('%3A',':').replace('%2F','/')
                    url[3]=url[3].replace('720','1080')
                    
                    print url[3]
                    listItem = xbmcgui.ListItem(path=url[3])
                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
            except:
                print obj['episode']['videoSrc']
                listItem = xbmcgui.ListItem(path=obj['episode']['videoSrc'])
                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)


def resolveAndPlayVideoRecent(url):
    url=url.split('%5E')
    plus=0
    today = date.today()

    print url
    if plus==0:
        url2='https://api.ondemandkorea.com/api3/episode/'
        data={'language': '0',
                       'adid': 'a36f8a5d-edae-44b7-b88d-ff0981008535',
                       'appShorterVersion':'1.8.93',
                       'idfv':'ef4212b0a9778005',
                       'screenid':'0',
                       'appBundleVersion':'1.8.93',
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
        prefix = plugin.get_setting("prefix", str)

        try:
            name=re.findall(".*?-e[0-9]",url[2])[0]
        except:
            name2=re.findall(".*?-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]",url[2])[0]

        try:
            name
        except NameError:
            if url[3]=="2":
                base_url = "http://odk-hls.akamaized.net/"+prefix+"/v1/"+url[4][-4]+url[4][-3]+url[4][-2]+url[4][-1]+url[4][0]+url[4][1]+"/drama/"+ name2[:-9] +"/"+url[2]+"/playlist_720.m3u8"
            else:
                base_url = "http://odk-hls.akamaized.net/"+prefix+"/v1/"+url[4][-4]+url[4][-3]+url[4][-2]+url[4][-1]+url[4][0]+url[4][1]+"/variety/"+ name2[:-9] +"/"+url[2]+"/playlist_720.m3u8"
        else:
            if url[3]=="2":
                base_url = "http://odk-hls.akamaized.net/"+prefix+"/v1/"+url[4][-4]+url[4][-3]+url[4][-2]+url[4][-1]+url[4][0]+url[4][1]+"/drama/"+ name[:-3] +"/"+url[2]+"/playlist_720.m3u8"
            else:
                base_url = "http://odk-hls.akamaized.net/"+prefix+"/v1/"+url[4][-4]+url[4][-3]+url[4][-2]+url[4][-1]+url[4][0]+url[4][1]+"/variety/"+ name[:-3] +"/"+url[2]+"/playlist_720.m3u8"
        
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

      
            try:
                #print "testingx"
                if quality == '1':
                   
                    #print base_url
                    listItem = xbmcgui.ListItem(path=base_url)
                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                    
                else:
                    base_url=base_url.replace('720','1080')
                    
                    print base_url
                    listItem = xbmcgui.ListItem(path=base_url)
                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
            except:
                print obj['episode']['videoSrc']
                listItem = xbmcgui.ListItem(path=obj['episode']['videoSrc'])
                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)

                
def addLink(name,url,mode,iconimage):
    u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )    
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
    elif params["mode"] == 'VideoCategoriesPast':
        listVideoCategoriesPast(url)    
##    elif params["mode"] == 'videoCategoryContent':
##        listVideosInCategory(urlUnquoted)
        
    elif params["mode"] == 'resolveAndPlayVideo':
        resolveAndPlayVideo(url)
    elif params["mode"] == 'resolveAndPlayVideoRecent':
        resolveAndPlayVideoRecent(url)
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

