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

img_base = "http://max.ondemandkorea.com/includes/timthumb.php?w=175&h=100&src="
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


@plugin.route('/')
def main_menu():
    #urls = scraper.parseTop()
    items = [
        {'label':'최신 영상', 'path':plugin.url_for('Recent')},
        {'label':'드라마', 'path':plugin.url_for('VOD', gid='2')},
        {'label':'예능', 'path':plugin.url_for('VOD', gid='6')},
        {'label':'시사/다큐', 'path':plugin.url_for('VOD', gid='450')},
        {'label':'음식/요리', 'path':plugin.url_for('VOD', gid='452')},
        {'label':'건강', 'path':plugin.url_for('VOD', gid='455')},
        {'label':'영화', 'path':plugin.url_for('VOD', gid='808')},
        {'label':'뉴스', 'path':plugin.url_for('VOD', gid='421')},
        {'label':'스포츠', 'path':plugin.url_for('VOD', gid='17')},
        #{'label':'뷰티/패션', 'path':plugin.url_for('VOD', gid='453')},
        #{'label':'종교', 'path':plugin.url_for('VOD', gid='75')},        
        #{'label':'어린이', 'path':plugin.url_for('VOD', gid='22')},
        #{'label':'교육', 'path':plugin.url_for('VOD', gid='1')},
        #{'label':'음악', 'path':plugin.url_for('VOD', gid='109')},
        #{'label':'경제', 'path':plugin.url_for('VOD', gid='180')}
    ]
    return items

@plugin.route('/Recent/')
def Recent():
    url='http://api.ondemandkorea.com/api3/home/index.php'
    data={'language': '0',
                   'adid': '4617319a-7b87-40fd-a62e-d0ae587da6cc',
                   'appShorterVersion':'1.8.26',
                   'idfv':'f94606748c42f360',
                   'screenid':'0',
                   'appBundleVersion':'1.8.26',
                   'accessToken': '432b1a3e19ba4d68d169d85a71de3a0ded683edfe0239f24fafd2db611f1e081',
          }
    headers={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}

    r = requests.post(url, data=data, headers=headers)
    print(r.status_code, r.reason)
    obj = json.loads(r.text)


    result = []
    for item in obj['data'][2]['data']:
        title=item['title']+' - '+item['broadcastDate']
        result.append({'label':title, 'path':plugin.url_for('resolveAndPlayVideo',title=title.encode('utf-8'), eid=item['id'], plus=item['plusOnly'],cat=item['slug']), 'thumbnail':item["thumbnailUrl"] })

    result.append({'label':'##예능##', 'path':'', 'thumbnail':''})
    
    for item in obj['data'][3]['data']:
        title=item['title']+' - '+item['broadcastDate']
        result.append({'label':title, 'path':plugin.url_for('resolveAndPlayVideo',title=title.encode('utf-8'), eid=item['id'], plus=item['plusOnly'],cat=item['slug']), 'thumbnail':item["thumbnailUrl"] })

    return plugin.finish(result, update_listing=False)

@plugin.route('/VOD/<gid>/')
def VOD(gid):
    url='http://api.ondemandkorea.com/api3/category/index.php'
    data={'language': '0',

                   'accessToken': token,
                   'id':gid
          }
    headers={
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'MMozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19',
            }
    r = requests.post(url, data=data, headers=headers)
    print(r.status_code, r.reason)
    obj = json.loads(r.text)


    result = []
    current = []
    past = []
    for item in obj['data']:
        result.append({'id':item['id'], 'title':item['title'], 'broad_date':item['latestDate'], 'thumbnail':item["posterUrl"],'stat':item['status'], 'new':item['new']})

    for i in range(len(result)):
        if result[i]['stat']=='current':
            if result[i]['new']=='true':
                title=result[i]['title']+' - NEW'
                current.append({'label': title, 'path':plugin.url_for('CategoryContent',cid=result[i]['id'],gid=gid), 'thumbnail':result[i]['thumbnail']})
            
            else:
                current.append({'label':result[i]['title'], 'path':plugin.url_for('CategoryContent',cid=result[i]['id'],gid=gid), 'thumbnail':result[i]['thumbnail']})
        
            
        else:
            past.append({'label':result[i]['title'], 'path':plugin.url_for('CategoryContent',cid=result[i]['id'],gid=gid), 'thumbnail':result[i]['thumbnail']})

    current=sorted(current)
    current.append({'label':'##이하 종영방송##', 'path':'', 'thumbnail':''})
    current.extend(past)
    return plugin.finish(current, update_listing=False)
##   
##    for name, url2, thumbnail in sorted(current):
##        addDir(name, url2, 'dramaCategoryContent', thumbnail)
##

##    addLink("## 이하 종영방송##", '', '', '')
##    for name, url2, thumbnail in sorted(past):
##        addDir(name, url2, 'dramaCategoryContent', thumbnail)    
   

@plugin.route('/VOD/<gid>/<cid>/')
def CategoryContent(gid,cid):    
    url='http://api.ondemandkorea.com/api3/program/index.php'
    data={'language': '0',
                   'adid': '4617319a-7b87-40fd-a62e-d0ae587da6cc',
                   'appShorterVersion':'1.8.26',
                   'idfv':'f94606748c42f360',
                   'screenid':'0',
                   'appBundleVersion':'1.8.26',
                   'accessToken': token,
                  'id': cid,
                  'size':'300',
                  'from':'0'
          }
    headers={
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'MMozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19',
            }
    r = requests.post(url, data=data, headers=headers)
    print(r.status_code, r.reason)
    obj = json.loads(r.text)


    result = []
    for item in obj['data']:
        title=item['title']+' - '+item['broadcastDate']
        result.append({'label':title, 'path':plugin.url_for('resolveAndPlayVideo',title=title.encode('utf-8'), eid=item['id'], plus=item['plusOnly'],cat=item['slug']), 'thumbnail':item["thumbnailUrl"] })


    return plugin.finish(result, update_listing=False)

@plugin.route('/VOD/Play/<eid>/<plus>/<cat>/<title>/')
def resolveAndPlayVideo(eid,plus,cat,title):
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
                       'id':eid
              }
        headers={
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'MMozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19',
                }
        r = requests.post(url2, data=data, headers=headers)
        obj = json.loads(r.text)


        use_mp4_url = plugin.get_setting('mp4_url', bool)
        if use_mp4_url:
            plugin.play_video( {'label': title, 'path':obj['episode']['mp4Src'][0]['src']} )
            return plugin.finish(None, succeeded=False)
        else:
            plugin.play_video( {'label': title, 'path':obj['episode']['videoSrc']} )
            return plugin.finish(None, succeeded=False)
    else:
        html='http://www.ondemandkorea.com/'+cat+'.html'
        req = urllib2.Request(html)
        req.add_header('User-Agent', default_hdr)
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup=BeautifulSoup(link)
        
        title1=re.compile('<meta property="og:url" content="http://www.ondemandkorea.com/(.*?)-e').findall(link)
        if len(title1)<1:
            title1=re.compile('<meta property="og:url" content="http://www.ondemandkorea.com/(.*?)-[0-9][0-9][0-9][0-9][0-9][0-9]').findall(link)
        print title1
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
            ]
            


        elif cat=='http://www.ondemandkorea.com/documentary':
            cat='variety'
            print cat
            m=[
            'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
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
                plugin.play_video( {'label': 'test', 'path':m[i]} )
                return plugin.finish(None, succeeded=False)
##                listItem = xbmcgui.ListItem(path=str(m[i]))
##                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
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
                    plugin.play_video( {'label': 'test', 'path':match[0]} )
                    return plugin.finish(None, succeeded=False)
##                    listItem = xbmcgui.ListItem(path=str(match[0]))
##                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                    break

                        
                except:

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
                            plugin.play_video( {'label': 'test', 'path':url[i]} )
                            return plugin.finish(None, succeeded=False)
##                            listItem = xbmcgui.ListItem(path=str(url[i]))
##                            xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
                            break
                        elif i ==len(url)-1:
                            print "No MP4 found."

if __name__ == "__main__":
    plugin.run()

    
##
##
##def listMainCategories():
##    addDir("최근 방영", '0', "RecentCategories", '')  
##    addDir("드라마", "2", "videoCategories", '')
##    addDir("예능/오락", "6", "videoCategories", '')
##    addDir("시사/다큐", "450", "videoCategories", '')
##    addDir("음식/요리", "452", "videoCategories", '')
##    addDir("뷰티/패션", "453", "videoCategories", '')
##    #addDir("여성", root_url+"women", "videoCategories", '')
##    addDir("건강", "455", "videoCategories", '')
##    #addDir("교육", "1", "videoCategories", '')  
##    #addDir("어린이", "22", "videoCategories", '')          
##    #addDir("스포츠", "17", "videoCategories", '')    
##    #addDir("경제", ""180, "videoCategories", '')    
##    #addDir("종교", "75", "videoCategories", '')    
##    #addDir("음악", "109", "videoCategories", '')
##    #addDir("게임", root_url+"games", "videoCategories", '')
##    #addDir("한국 영화", '808', "videoCategories", '')
##
##
##
##def listRecentCategories(url):
##    url2='http://api.ondemandkorea.com/api3/home/index.php'
##    data={'language': '0',
##                   'adid': '4617319a-7b87-40fd-a62e-d0ae587da6cc',
##                   'appShorterVersion':'1.8.26',
##                   'idfv':'f94606748c42f360',
##                   'screenid':'0',
##                   'appBundleVersion':'1.8.26',
##                   'accessToken': token
##          }
##    headers={
##        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
##        'User-Agent': 'MMozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19',
##            }
##    r = requests.post(url2, data=data, headers=headers)
##    print(r.status_code, r.reason)
##    obj = json.loads(r.text)
##
##
##    result = []
##    
##    today=obj['data'][2]['data'][0]['broadcastDate']
##    print today
##    for item in obj['data'][2]['data']:
##        result.append({'id':item['id'], 'title':item['title'], 'broad_date':item['broadcastDate'], 'thumbnail':item["thumbnailUrl"], 'plusOnly':item['plusOnly'], 'cat':item['slug']})
##
##    for item in obj['data'][3]['data']:
##        result.append({'id':item['id'], 'title':item['title'], 'broad_date':item['broadcastDate'], 'thumbnail':item["thumbnailUrl"], 'plusOnly':item['plusOnly'], 'cat':item['slug']})
##
##
##
##    result2=[]
##    
##            
##    for i in range(len(result)):
##        if result[i]['broad_date']==today:
###            print 'today'
##            title=result[i]['title']+' - '+result[i]['broad_date']
##            eid=result[i]['id']+'^'+result[i]['plusOnly']+'^'+result[i]['cat']
##            result2.append([title, eid, result[i]['thumbnail']])
##            
##
##
##    for name, url2, thumbnail in result2:
##        addLink(name, url2, 'resolveAndPlayVideo', thumbnail)
##    
##def listVideoCategories(url):
##    url2='http://api.ondemandkorea.com/api3/category/index.php'
##    data={'language': '0',
##
##                   'accessToken': token,
##                   'id':url
##          }
##    headers={
##        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
##        'User-Agent': 'MMozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19',
##            }
##    r = requests.post(url2, data=data, headers=headers)
##    print(r.status_code, r.reason)
##    obj = json.loads(r.text)
##
##
##    result = []
##    current = []
##    past = []
##    for item in obj['data']:
##        result.append({'id':item['id'], 'title':item['title'], 'broad_date':item['latestDate'], 'thumbnail':item["posterUrl"],'stat':item['status'], 'new':item['new']})
##
##    for i in range(len(result)):
##        if result[i]['stat']=='current':
##            if result[i]['new']=='true':
##                title=result[i]['title']+' - NEW'
##                current.append([title, result[i]['id'], result[i]['thumbnail']])
##            
##            else:
##                current.append([result[i]['title'], result[i]['id'], result[i]['thumbnail']])
##        
##            
##        else:
##            past.append([result[i]['title'], result[i]['id'], result[i]['thumbnail']])
##    print current
##    for name, url2, thumbnail in sorted(current):
##        addDir(name, url2, 'dramaCategoryContent', thumbnail)
##    
##    addLink("## 이하 종영방송##", '', '', '')
##    for name, url2, thumbnail in sorted(past):
##        addDir(name, url2, 'dramaCategoryContent', thumbnail)    
##
##def listdramaInCategory(url):    
##    url2='http://api.ondemandkorea.com/api3/program/index.php'
##    data={'language': '0',
##                   'adid': '4617319a-7b87-40fd-a62e-d0ae587da6cc',
##                   'appShorterVersion':'1.8.26',
##                   'idfv':'f94606748c42f360',
##                   'screenid':'0',
##                   'appBundleVersion':'1.8.26',
##                   'accessToken': token,
##                  'id': url,
##                  'size':'300',
##                  'from':'0'
##          }
##    headers={
##        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
##        'User-Agent': 'MMozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19',
##            }
##    r = requests.post(url2, data=data, headers=headers)
##    print(r.status_code, r.reason)
##    obj = json.loads(r.text)
##
##
##    result = []
##    for item in obj['data']:
##        result.append({'id':item['id'], 'title':item['title'], 'broad_date':item['broadcastDate'], 'thumbnail':item["thumbnailUrl"], 'plusOnly':item['plusOnly'], 'cat':item['slug']})
##
##    for i in range(len(result)):
##        title=result[i]['title']+' - '+result[i]['broad_date']
##        eid=result[i]['id']+'^'+result[i]['plusOnly']+'^'+result[i]['cat']
##        result[i] = (title, eid, result[i]['thumbnail'])
##
##    for name, url2, thumbnail in result:
##        addLink(name, url2, 'resolveAndPlayVideo', thumbnail)
##
##def resolveAndPlayVideo(url):
##    url=url.split('%5E')
##    print url
##    if url[1]=='0':
##        url2='http://api.ondemandkorea.com/api3/episode/index.php'
##        data={'language': '0',
##                       'adid': '4617319a-7b87-40fd-a62e-d0ae587da6cc',
##                       'appShorterVersion':'1.8.26',
##                       'idfv':'f94606748c42f360',
##                       'screenid':'0',
##                       'appBundleVersion':'1.8.26',
##                       'accessToken': token,
##                       'id':url[0]
##              }
##        headers={
##            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
##            'User-Agent': 'MMozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19',
##                }
##        r = requests.post(url2, data=data, headers=headers)
##        obj = json.loads(r.text)
##
##
##        use_mp4_url = plugin.get_setting('mp4_url', bool)
##        if use_mp4_url:
##            listItem = xbmcgui.ListItem(path=obj['episode']['mp4Src'][0]['src'])
##            xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem) 
##        else:
##            listItem = xbmcgui.ListItem(path=obj['episode']['videoSrc'])
##            xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##    else:
##        html='http://www.ondemandkorea.com/'+url[2]+'.html'
##        req = urllib2.Request(html)
##        req.add_header('User-Agent', default_hdr)
##        req.add_header('Accept-Langauge', 'ko')
##        req.add_header('Cookie', 'language=kr')
##        response = urllib2.urlopen(req)
##        link=response.read()
##        response.close()
##        soup=BeautifulSoup(link)
##        
##        title1=re.compile('<meta property="og:url" content="http://www.ondemandkorea.com/(.*?)-e').findall(link)
##        if len(title1)<1:
##            title1=re.compile('<meta property="og:url" content="http://www.ondemandkorea.com/(.*?)-[0-9][0-9][0-9][0-9][0-9][0-9]').findall(link)
##        print title1
##        #title=re.compile('/uploads/thumbnail/(.*?)_([0-9]*)_').findall(link)
##        title=re.compile(r'<link rel="image_src" href="http://(.*?)\.jpg').findall(link)
##        title=title[0].split('/')
##        title=title[len(title)-1:]
##        title=title[0].split('_')
##        title=title[0:2]
##        
##        title[1]=title[1].replace('480p','').replace('1596k','').replace('.','').replace('300p664k','')
##        
##        if len(title[1])==6:
##            date='20'+title[1]
##        else:
##            date=title[1]
##
##        print title
##
##
##        ##Finding category
##        cat=soup.find('td',{'class':'v-bar  active'}).a['href']
##        if cat=='http://www.ondemandkorea.com/drama':
##            cat='drama'
##            print cat
##            m=[
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',             
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8', 
##            ]
##            
##
##
##        elif cat=='http://www.ondemandkorea.com/documentary':
##            cat='variety'
##            print cat
##            m=[
##            'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            ]
##
##        else:
##            cat='variety'
##            print cat
##            m=[
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p_'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p-'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil1080p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-smil720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'_720p.smil/manifest.m3u8',
##            'http://lime1.ondemandkorea.com/'+cat+'2/'+title1[0]+'/1080/'+title[0]+'_'+title[1]+'-1-smil720p.smil/manifest.m3u8',
##            ]                
##
##        
##        for i in range(len(m)):
##            try:
##                f = urllib2.Request(m[i])
##                f.add_header('User-Agent', default_hdr)
##                f=urllib2.urlopen(f)    
##                dead = False
##                
##            except:
##                dead = True
##           
##            if dead==False:
##                print "Correct m3u8 found = "+str(m[i])
##                listItem = xbmcgui.ListItem(path=str(m[i]))
##                xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##                break
##            
##            elif i ==len(m)-1:
##                print "No m3u8 found."
##                try: 
##                    req = urllib2.Request(url)
##                    req.add_header('User-Agent', tablet_UA)
##                    req.add_header('Accept-Langauge', 'ko')
##                    req.add_header('Cookie', 'language=kr')
##                    response = urllib2.urlopen(req)
##                    link=response.read()
##                    response.close()
##                    soup=BeautifulSoup(link)
##                    
##                    match=re.compile('video.src = "(.*?)"').search(link).group(0).replace('360p.1296k','720p.2296k').replace('.480p.1596k','720p.2296k')
##                    
##                    print match
##                    listItem = xbmcgui.ListItem(path=str(match[0]))
##                    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##                    break
##
##                        
##                except:
##
##                    url=[
##                    'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/'+cat+'2/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',                        
##                    'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
##                    'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
##                    'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
##                    'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p_'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'_720p.mp4',
##                    'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'.720p.2296k.mp4',
##                    'http://lime2.ondemandkorea.com/documentary/'+title1[0]+'/'+date[0:4]+'/1080p-'+title1[0]+'/'+title[0]+'_'+title[1]+'-1.720p.2296k.mp4',                         
##                    ]
##
##                
##                    for i in range(len(url)):
##                        try:
##                            f = urllib2.Request(url[i])
##                            f.add_header('User-Agent', default_hdr)
##                            f=urllib2.urlopen(f)    
##                            dead = False
##                            print i
##                        except:
##                            dead = True
##                       
##                        if dead==False:
##                            print "Correct MP4 found = "+str(url[i])
##                            listItem = xbmcgui.ListItem(path=str(url[i]))
##                            xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##                            break
##                        elif i ==len(url)-1:
##                            print "No MP4 found."
##
##    
##def addLink(name,url,mode,iconimage):
##    u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
##    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
##    
##    liz.setProperty("IsPlayable","true")
##    xbmcplugin.addDirectoryItem(handle=_thisPlugin,url=u,listitem=liz,isFolder=False)
##    
##
##def addDir(name,url,mode,iconimage):
##    u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)#+"&name="+urllib.quote_plus(name)
##    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
##    liz.setInfo( type="Video", infoLabels={ "Title": name } )
##    xbmcplugin.addDirectoryItem(handle=_thisPlugin,url=u,listitem=liz,isFolder=True)
##
##def getparams():
##    """
##    Pick up parameters sent in via command line
##    @return dict list of parameters
##    @thanks Team XBM - I lifted this straight out of the
##    shoutcast addon
##    """
##    param=[]
##    paramstring=sys.argv[2]
##    if len(paramstring)>=2:
##        params=sys.argv[2]
##        cleanedparams=params.replace('?','')
##        if (params[len(params)-1]=='/'):
##            params=params[0:len(params)-2]
##        pairsofparams=cleanedparams.split('&')
##        param={}
##        for i in range(len(pairsofparams)):
##            splitparams={}
##            splitparams=pairsofparams[i].split('=')
##            if (len(splitparams))==2:
##                param[splitparams[0]]=splitparams[1]
##    return param
##
##params = getparams()
##
##try:
##    url = params["url"]
##    urlUnquoted = urllib.unquote_plus(url)
##except:
##    url = None
##  
##if url == None:
##    #do listing
##    listMainCategories()
##else:
##    if params["mode"] == 'videoCategories':
##        listVideoCategories(url)
####    elif params["mode"] == 'videoCategoryContent':
####        listVideosInCategory(urlUnquoted)
##        
##    elif params["mode"] == 'resolveAndPlayVideo':
##        resolveAndPlayVideo(url)
####    elif params["mode"] == 'resolveAndPlayMovie':
####        resolveAndPlayMovie(urlUnquoted)
####
####    elif params["mode"] == 'dramafever':
####        listdramafever(urlUnquoted)
####    elif params["mode"] == 'dramafeverPlay':
####        dramafeverPlay(urlUnquoted)
##        
####    elif params["mode"] == 'dramaCategories':
####        listdramaCategories(urlUnquoted)   
##    elif params["mode"] == 'dramaCategoryContent':
##        listdramaInCategory(url)
##
##
####    elif params["mode"] == 'varietyCategories':
####        listvarietyCategories(urlUnquoted)    
####    elif params["mode"] == 'varietyCategoryContent':
####        listvarietyInCategory(urlUnquoted)
####
####    elif params["mode"] == 'videoCategoriesLow':
####        listVideoCategoriesLow(urlUnquoted)
####    elif params["mode"] == 'videoCategoryContentLow':
####        listVideosInCategoryLow(urlUnquoted)
####    elif params["mode"] == 'resolveAndPlayVideoLow':
####        resolveAndPlayVideoLow(urlUnquoted)
##        
##    elif params["mode"] == 'RecentCategories':
##        listRecentCategories(url)
####    elif params["mode"] == 'MovieCategories':
####        listMovieCategories(urlUnquoted)
####    elif params["mode"] == 'resolveAndPlayMovie':
####        resolveAndPlayMovie(urlUnquoted)
##        
##xbmcplugin.endOfDirectory(_thisPlugin)        
##
