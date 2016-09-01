# -*- coding: utf-8 -*-
"""
    Ondemand Korea
"""
from xbmcswift2 import Plugin
from urllib2 import unquote
import os
import urllib2, urllib, re
import requests, json
from BeautifulSoup import BeautifulSoup

plugin = Plugin()
_L = plugin.get_string
Protocol = plugin.get_setting('Protocol', str)

plugin_path = plugin.addon.getAddonInfo('path')
lib_path = os.path.join(plugin_path, 'resources', 'lib')
sys.path.append(lib_path)


@plugin.route('/')
def main_menu():
    #urls = scraper.parseTop()
    items = [
        {'label':'하이라이트', 'path':plugin.url_for('VOD')},
        {'label':'생방송', 'path':plugin.url_for('live')},
    ]
    return items

@plugin.route('/VOD/')
def VOD():
    url='http://sports.media.daum.net/rf/534b6e671652d99818d84ad0.json?callback=LegoLeagueInfoCallback'

    headers={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
             'Content-Type':'application/x-www-form-urlencoded'}
    r = requests.post(url, '', headers=headers)
    print(r.status_code, r.reason)
    t=r.text[23:-2]
    obj = json.loads(t)
    ##print obj

    result=[]


    for item in obj['component']['data'][0]['component']['data']:
        result.append({'league_id':item['component']['userId'], 'title':item['component']['userName']})

    items=[]
    items = [{'label':item['title'], 'path':plugin.url_for('league', league_id=item['league_id'], league=item['title'].encode('utf8')), 'thumbnail':''} for item in result]
    items.pop(0)
    return plugin.finish(items, update_listing=False)

    

@plugin.route('/VOD/<league>/<league_id>/')
def league(league_id, league):
    url='http://sports.media.daum.net/ronaldo/gallery/list.json?callback=VideoCallback&category-code='+league_id

    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    result=[]
    t=link[16:-3]
    obj = json.loads(t)
    try:
        for item in obj['data']['galleryList']:
            l = str(item['fieldValues']['game_time'])
            date=l[:4]+'/'+ l[4:6]+'/'+l[6:8]
            title=item['fieldValues']['home_team_name']+' vs. '+item['fieldValues']['away_team_name'] + ' - ' +date     
            result.append({'title':title, 'vid':item['fieldValues']['game_id'], 'vtype':'sport'})
        items=[]
        items = [{'label':item['title'], 'path':plugin.url_for('VODlist', league=league, vid=item['vid'],vtype=item['vtype']), 'thumbnail':''} for item in result]
        return plugin.finish(items, update_listing=False)
    except:
        for item in obj['data']['galleryList']:
            l = str(item['fieldValues']['game_start_time'])
            date=l[:4]+'/'+ l[4:6]+'/'+l[6:8]
            title=item['fieldValues']['home_team_name']+' vs. '+item['fieldValues']['away_team_name'] + ' - ' +date     
            result.append({'title':title, 'vid':item['fieldValues']['game_id'], 'vtype':'sport'})
        items=[]
        items = [{'label':item['title'], 'path':plugin.url_for('VODlist', league=league, vid=item['vid'],vtype=item['vtype']), 'thumbnail':''} for item in result]
        return plugin.finish(items, update_listing=False)

@plugin.route('/VOD/<league>/<vtype>/<vid>/')
def VODlist(vid,vtype,league):
##    if vtype=='sport':
    url='http://sports.media.daum.net/proxy/ronaldo/gallery/view.json?game-id='+vid
##    else:
##    url='http://sports.media.daum.net/ronaldo/gallery/view.json?callback=videoGalleryCallback&id='+vid

    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    obj = json.loads(link)
    items=[]

            
    for item in obj['data']['gallery']['mediaRelations']:
        items.append({'title':item['media']['fieldValues']['MEDIATYPE_tvpot']['title'], 'vodID':item['media']['fieldValues']['MEDIATYPE_tvpot']['vid'], 'thumbnail':item['media']['fieldValues']['MEDIATYPE_tvpot']['thumbnailUrl']})
        
    
    items2 = [{'label':item['title'], 'path':plugin.url_for('VODPlay', title=item['title'].encode('utf8'), league=league, vid=vid,vtype=vtype, vodID=item['vodID']), 'thumbnail':item['thumbnail']} for item in items]
    items2.sort()
    return plugin.finish(items2, update_listing=False)
    

@plugin.route('/VOD/<league>/<vtype>/<vid>/<vodID>/<title>/')
def VODPlay(vodID,league, vid,vtype,title):
        url='http://videofarm.daum.net/controller/api/open/v1_5/MovieLocation.apixml?vid='+vodID+'&profile=HIGH'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

        match=re.compile('<url><\!\[CDATA\[(.*?)\]\]></url>').search(link).group(1)
        print match
        plugin.play_video( {'label': title, 'path':match} )
        return plugin.finish(None, succeeded=False)

@plugin.route('/live/')
def live():
    items = [
        {'label':'티비', 'path':plugin.url_for('LiveTV')},
        {'label':'고화질', 'path':plugin.url_for('High_list')},
        {'label':'중화질', 'path':plugin.url_for('Med_list')},
        {'label':'저화질', 'path':plugin.url_for('Low_list')},
    ]
    return plugin.finish(items, view_mode='list')

@plugin.route('/live/LiveTV/')
def LiveTV():
    a=plugin.get_setting('a', bool)
    url='http://menu.megatvdnp.co.kr:38080/app5/0/api/epg_chlist?istest=0&category_id=1'

    headers={'User-Agent': 'OMS(compatible;ServiceType/OTN;DeviceType/Android;DeviceModel/LG-D852G;OSType/Android;OSVersion/5.0;AppVersion/5.0.32)',
             'Content-Type':'text/plain;charset=UTF-8'}
    r = requests.post(url, '', headers=headers)
    print(r.status_code, r.reason)
    obj = json.loads(r.text)
    ##print obj

    result=[]


    ##result = obj['data']['live_url']

    for item in obj['data']['list'][0]['list_channel']:
        if item['type']=='EPG':
            if item['adult_yn']=='N':
                result.append({'chname':item['service_ch_name'], 'title':item['program_name'], 'ch_img':item['ch_image_detail'], 'thumbnail':item["still_cut_image"],'type':item['type']})
        if a:
            if item['adult_yn']=='Y':
                result.append({'chname':item['service_ch_name'], 'title':item['program_name'], 'ch_img':item['ch_image_detail'], 'thumbnail':item["still_cut_image"],'type':item['type']})

    print'done'
    result2=[]
    for i in range(len(result)):
        s=result[i]['title'].encode('latin1')
        unquoted = unquote(s)
        d=unquoted.decode('utf8').replace('+',' ')
        title=result[i]['chname']+' - ' + d
        a=result[i]['thumbnail']
        b=unquote(a)
        b=b.decode('utf8')
        c=result[i]['chname']
        d=c.encode('utf8')
        result2.append({'title':title,'thumbnail':b,'channel':d})
     
    items2 = [{'label':item['title'], 'path':plugin.url_for('LiveTVplay', title=item['title'].encode('utf-8'),url=item['thumbnail']), 'thumbnail':item['thumbnail']} for item in result2]
    return plugin.finish(items2, update_listing=False)

@plugin.route('/live/LiveTV/<url>/<title>/')
def LiveTVplay(url,title):
    cid=re.compile('CHANNEL_IMAGE/([0-9]+)/').findall(url)
    quality=plugin.get_setting('1080P', bool)
    print quality
    if quality:
        print '1080p'
        cid=int(cid[0])+1
    else:
        print 'SD'
        cid=int(cid[0])+2
    print cid
    url2='http://menu.megatvdnp.co.kr:38080/app5/0/api/epg_play?istest=1&ch_no=404&bit_rate=S&bit_rate_option=1000&user_model=LG-D852G&user_os=5.0.1&user_type=Android&user_net=WIFI'
    #url='http://menu.megatvdnp.co.kr:38080/app5/0/api/epg_proglist?istext=1&ch_no=404'
  
    headers={'User-Agent': 'OMS(compatible;ServiceType/OTN;DeviceType/Android;DeviceModel/LG-D852G;OSType/Android;OSVersion/5.0;AppVersion/5.0.32)',
             'Content-Type':'text/plain;charset=UTF-8'}
    r = requests.post(url2, '', headers=headers)
    print(r.status_code, r.reason)
    obj = json.loads(r.text)

    result = obj['data']['live_url']

    print result
    result=result.replace('10452',str(cid))
    print result

    req = urllib2.Request(result,'', headers)
    res = urllib2.urlopen(req)
    finalurl = res.geturl()
    
    plugin.play_video( {'label': title, 'path':finalurl} )
    return plugin.finish(None, succeeded=False)

@plugin.route('/live/sports/High/')
def High_list():

    url='http://sports.news.naver.com/tv/onairScheduleList.nhn?gameId=&isScoreOn=true'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link=response.read()
    soup=BeautifulSoup(link)

    items = []

    try:
        for node in soup.findAll('li', {'class':'ing'}):
            cat = re.compile('params1="(.*?)"').findall(str(node))
            cat = [element.upper() for element in cat]
            gid = re.compile('params2="(.*?)"').findall(str(node))
            if len(gid)==0:
                gid = re.compile('params1="(.*?)"').findall(str(node))
                cat = re.compile('params="(.*?)"').findall(str(node))
            s1 = node.find("span", {"class":"score_num"}).find(text=True)
            t1=re.compile('<strong>(.*?)</strong>').findall(str(node))
            s2 = node.find("span", {"class":"score_num b_num"}).find(text=True)
            info = node.find("span", {"class":"score_info"}).find(text=True)
            
            title = cat[0]+ ': ' + unicode(t1[0],'utf-8') + ' ' +s1+ ' vs. ' + unicode(t1[1],'utf-8') + ' ' +s2+ ' ' +info
            items.append({'title':title, 'vid':gid[0]})
            
    except:
        print "No sport streams"
        
    for node in soup.findAll('li', {'class':'normal_e'}):
        cat = re.compile('params1="(.*?)"').findall(str(node))
        cat = [element.upper() for element in cat]
        gid = re.compile('params2="(.*?)"').findall(str(node))
        if len(gid)==0:
            gid = re.compile('params1="(.*?)"').findall(str(node))
            cat = re.compile('params="(.*?)"').findall(str(node))
        t1=re.compile('<strong>(.*?)</strong>').findall(str(node))
        
        title = cat[0]+ ': ' + unicode(t1[0],'utf-8')

        items.append({'title':title, 'vid':gid[0]})


    items2=[]
    items2 = ({'label':item['title'], 'path':plugin.url_for('resolveAndPlayVideo', title=item['title'].encode('utf-8'), vid=item['vid'], quality='2000'), 'thumbnail':''} for item in items)
    items2=list(items2)
    items2.append({'label':'##이하 DAUM 중계##', 'path':plugin.url_for('High_list'), 'thumbnail':''})
    
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
    ####        if Protocol==0:
    ####            url='rtmp://203.133.176.170:1935/live/'+str(liveid)+'_1_2000'
    ####
    ####        elif Protocol==1:
    ####            url='rtsp://203.133.176.170:554/'+ str(liveid) +'_1_2000'
    ####        else:
    ####            url='http://cdn.live.daum.net/kakao_ch1/'+ str(liveid) +'_1_2000.m3u8?domain=cdn.live.daum.net&ch=35349604'
        #url='http://videofarm.daum.net/controller/api/open/v1_0/BroadcastStreams.action?broadcastId='+str(liveid)+'&profile=HIGH'
        items.append({'title':title, 'broad_date':time, 'liveid':liveid, 'thumbnail':''})
        items.sort(reverse=True)

    items3=({'label':item['title'], 'path':plugin.url_for('resolveAndPlayVideoDaum', title=item['title'].encode('utf-8'), liveid=item['liveid'], quality='2000'), 'thumbnail':''} for item in items)

    items2.extend(items3)
    return plugin.finish(items2, update_listing=False)

@plugin.route('/live/sports/Med/')
def Med_list():

    url='http://sports.news.naver.com/tv/onairScheduleList.nhn?gameId=&isScoreOn=true'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link=response.read()
    soup=BeautifulSoup(link)

    items = []

    try:
        for node in soup.findAll('li', {'class':'ing'}):
            cat = re.compile('params1="(.*?)"').findall(str(node))
            cat = [element.upper() for element in cat]
            gid = re.compile('params2="(.*?)"').findall(str(node))
            if len(gid)==0:
                gid = re.compile('params1="(.*?)"').findall(str(node))
                cat = re.compile('params="(.*?)"').findall(str(node))
            s1 = node.find("span", {"class":"score_num"}).find(text=True)
            t1=re.compile('<strong>(.*?)</strong>').findall(str(node))
            s2 = node.find("span", {"class":"score_num b_num"}).find(text=True)
            info = node.find("span", {"class":"score_info"}).find(text=True)
            
            title = cat[0]+ ': ' + unicode(t1[0],'utf-8') + ' ' +s1+ ' vs. ' + unicode(t1[1],'utf-8') + ' ' +s2+ ' ' +info
            items.append({'title':title, 'vid':gid[0]})
            
    except:
        print "No sport streams"
        
    for node in soup.findAll('li', {'class':'normal_e'}):
        cat = re.compile('params1="(.*?)"').findall(str(node))
        cat = [element.upper() for element in cat]
        gid = re.compile('params2="(.*?)"').findall(str(node))
        if len(gid)==0:
            gid = re.compile('params1="(.*?)"').findall(str(node))
            cat = re.compile('params="(.*?)"').findall(str(node))
        t1=re.compile('<strong>(.*?)</strong>').findall(str(node))
        
        title = cat[0]+ ': ' + unicode(t1[0],'utf-8')

        items.append({'title':title, 'vid':gid[0]})


    items2=[]
    items2 = ({'label':item['title'], 'path':plugin.url_for('resolveAndPlayVideo', title=item['title'].encode('utf-8'), vid=item['vid'], quality='800'), 'thumbnail':''} for item in items)
    items2=list(items2)
    items2.append({'label':'##이하 DAUM 중계##', 'path':plugin.url_for('High_list'), 'thumbnail':''})
    
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
    ####        if Protocol==0:
    ####            url='rtmp://203.133.176.170:1935/live/'+str(liveid)+'_1_2000'
    ####
    ####        elif Protocol==1:
    ####            url='rtsp://203.133.176.170:554/'+ str(liveid) +'_1_2000'
    ####        else:
    ####            url='http://cdn.live.daum.net/kakao_ch1/'+ str(liveid) +'_1_2000.m3u8?domain=cdn.live.daum.net&ch=35349604'
        #url='http://videofarm.daum.net/controller/api/open/v1_0/BroadcastStreams.action?broadcastId='+str(liveid)+'&profile=HIGH'
        items.append({'title':title, 'broad_date':time, 'liveid':liveid, 'thumbnail':''})
        items.sort(reverse=True)

    items3=({'label':item['title'], 'path':plugin.url_for('resolveAndPlayVideoDaum', title=item['title'].encode('utf-8'), liveid=item['liveid'], quality='1000'), 'thumbnail':''} for item in items)

    items2.extend(items3)
    return plugin.finish(items2, update_listing=False)


@plugin.route('/live/sports/Low/')
def Low_list():

    url='http://sports.news.naver.com/tv/onairScheduleList.nhn?gameId=&isScoreOn=true'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link=response.read()
    soup=BeautifulSoup(link)

    items = []

    try:
        for node in soup.findAll('li', {'class':'ing'}):
            cat = re.compile('params1="(.*?)"').findall(str(node))
            cat = [element.upper() for element in cat]
            gid = re.compile('params2="(.*?)"').findall(str(node))
            if len(gid)==0:
                gid = re.compile('params1="(.*?)"').findall(str(node))
                cat = re.compile('params="(.*?)"').findall(str(node))
            s1 = node.find("span", {"class":"score_num"}).find(text=True)
            t1=re.compile('<strong>(.*?)</strong>').findall(str(node))
            s2 = node.find("span", {"class":"score_num b_num"}).find(text=True)
            info = node.find("span", {"class":"score_info"}).find(text=True)
            
            title = cat[0]+ ': ' + unicode(t1[0],'utf-8') + ' ' +s1+ ' vs. ' + unicode(t1[1],'utf-8') + ' ' +s2+ ' ' +info
            items.append({'title':title, 'vid':gid[0]})
            
    except:
        print "No sport streams"
        
    for node in soup.findAll('li', {'class':'normal_e'}):
        cat = re.compile('params1="(.*?)"').findall(str(node))
        cat = [element.upper() for element in cat]
        gid = re.compile('params2="(.*?)"').findall(str(node))
        if len(gid)==0:
            gid = re.compile('params1="(.*?)"').findall(str(node))
            cat = re.compile('params="(.*?)"').findall(str(node))
        t1=re.compile('<strong>(.*?)</strong>').findall(str(node))
        
        title = cat[0]+ ': ' + unicode(t1[0],'utf-8')

        items.append({'title':title, 'vid':gid[0]})


    items2=[]
    items2 = ({'label':item['title'], 'path':plugin.url_for('resolveAndPlayVideo', title=item['title'].encode('utf-8'), vid=item['vid'], quality='300'), 'thumbnail':''} for item in items)
    items2=list(items2)
    items2.append({'label':'##이하 DAUM 중계##', 'path':plugin.url_for('High_list'), 'thumbnail':''})
    
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
    ####        if Protocol==0:
    ####            url='rtmp://203.133.176.170:1935/live/'+str(liveid)+'_1_2000'
    ####
    ####        elif Protocol==1:
    ####            url='rtsp://203.133.176.170:554/'+ str(liveid) +'_1_2000'
    ####        else:
    ####            url='http://cdn.live.daum.net/kakao_ch1/'+ str(liveid) +'_1_2000.m3u8?domain=cdn.live.daum.net&ch=35349604'
        #url='http://videofarm.daum.net/controller/api/open/v1_0/BroadcastStreams.action?broadcastId='+str(liveid)+'&profile=HIGH'
        items.append({'title':title, 'broad_date':time, 'liveid':liveid, 'thumbnail':''})
        items.sort(reverse=True)

    items3=({'label':item['title'], 'path':plugin.url_for('resolveAndPlayVideoDaum', title=item['title'].encode('utf-8'), liveid=item['liveid'], quality='500'), 'thumbnail':''} for item in items)

    items2.extend(items3)
    return plugin.finish(items2, update_listing=False)


@plugin.route('/live/sports/<quality>/<liveid>/daum/<title>')
def resolveAndPlayVideoDaum(liveid,quality,title):
    if Protocol==0:
        url='rtmp://203.133.176.170:1935/live/'+liveid+'_1_'+quality

    elif Protocol==1:
        url='rtsp://203.133.176.170:554/'+ liveid +'_1_'+quality
    else:
        url='http://cdn.live.daum.net/kakao_ch1/'+ liveid +'_1_'+quality+'.m3u8?domain=cdn.live.daum.net&ch=35349604'  
##    listItem = xbmcgui.ListItem(path=str(url))
##    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
##
##    
    plugin.play_video( {'label': title, 'path':url} )
    return plugin.finish(None, succeeded=False)

@plugin.route('/live/sports/<quality>/<vid>/<title>')
def resolveAndPlayVideo(vid,quality,title):
    url2='http://sports.news.naver.com/tv/index.nhn?gameId=' + vid
    req = urllib2.Request(url2)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    
    ch=re.compile('"channelID":"high(.*?)"').search(link).group(1)

    if quality=='2000':
        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2F'+ch+'%2F_definst_%2F'+ch+'_2000.stream%2Fplaylist.m3u8'
    elif quality=='800':
        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2F'+ch+'%2F_definst_%2F'+ch+'_800.stream%2Fplaylist.m3u8'
    else:
        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2F'+ch+'%2F_definst_%2F'+ch+'_300.stream%2Fplaylist.m3u8'
        
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    plugin.play_video( {'label': title, 'path':link} )
    return plugin.finish(None, succeeded=False)

##
##@plugin.route('/episode/<genre>/<page>/<url>')
##def episode_view(url, page, genre):
##    plugin.log.debug(url)
##    koPage = plugin.get_setting('koPage', bool)
##    info = scraper.parseEpisodePage2(url, page=int(page), koPage=koPage)
##    items = [{'label':item['title'], 'label2':item['broad_date'], 'path':plugin.url_for('play_episode', url=item['url'], genre=genre), 'thumbnail':item['thumbnail']} for item in info['episode']]
##    # navigation
##    if 'prevpage' in info:
##        items.append({'label':tPrevPage, 'path':plugin.url_for('episode_view', url=url, page=info['prevpage'], genre=genre)})
##    if 'nextpage' in info:
##        items.append({'label':tNextPage, 'path':plugin.url_for('episode_view', url=url, page=info['nextpage'], genre=genre)})
##    return plugin.finish(items, update_listing=False)
##
##@plugin.route('/play/<genre>/<url>')
##def play_episode(url, genre):
##    global quality_tbl
##    plugin.log.debug(url)
##    resolution = quality_tbl[ plugin.get_setting('quality', int) ]
##    use_mp4_url = plugin.get_setting('mp4_url', bool)
##
##    if use_mp4_url:
##        info = scraper.extractVideoUrl(url, referer=url)
##        if info is None:
##            info = scraper.guessVideoUrl(url, genre=genre)
##            plugin.log.info("use guessed url")
##    else:
##        info = scraper.extractStreamUrl(url, referer=url)
##
##    plugin.log.debug("resolution: "+resolution)
##    avail_resolutions = info['videos'].keys()
##    if not resolution in avail_resolutions:
##        resolution = avail_resolutions[0]
##    video = info['videos'][resolution]
##
##    plugin.play_video( {'label':info['title'], 'path':video['url']} )
##
##    return plugin.finish(None, succeeded=False)

if __name__ == "__main__":
    plugin.run()

# vim:sw=4:sts=4:et
