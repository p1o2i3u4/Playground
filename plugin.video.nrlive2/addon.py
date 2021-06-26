# -*- coding: utf-8 -*-
"""
    NR LIVE
"""
from xbmcswift2 import Plugin
from urllib2 import unquote
import os
import urllib2, urllib, re
import requests, json
import xbmc
import xbmcgui

plugin = Plugin()
_L = plugin.get_string
Protocol = plugin.get_setting('Protocol', str)

plugin_path = plugin.addon.getAddonInfo('path')
lib_path = os.path.join(plugin_path, 'resources', 'lib')
sys.path.append(lib_path)


@plugin.route('/')
def main_menu():
    a=plugin.get_setting('a', bool)
    b=plugin.get_setting('b', bool)
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
                cid=re.compile('CHANNEL_IMAGE/([0-9]+)/').findall(item["still_cut_image"])
                result.append([item['service_ch_name'],item['program_name'],item['still_cut_image'],int(cid[0]),item['type']])

        if a:
            if item['adult_yn']=='Y':
                cid=re.compile('CHANNEL_IMAGE/([0-9]+)/').findall(item["still_cut_image"])
                result.append([item['service_ch_name'],item['program_name'],item['still_cut_image'],int(cid[0]),item['type']])
##----------------------
####    result.append(['HD shop','','','10670'])
####    result.append(['NS Shop','','','10680'])
####    result.append(['V - music video','','','10690'])
####    result.append(['JTBC3 - Fox sports','','','10700'])
####    result.append(['SPOTV Games','','','10710'])
##    #result.append(['ENCODER_M?','','','10720'])
####    result.append(['Viki','','','10730'])
####    result.append(['adult1 prob midnight','','','10740'])
####    result.append(['error','','','10750'])
####    result.append(['Disney','','','10760'])
####    result.append(['tooniverse','','','10770'])
####    result.append(['JTBC2','','','10780'])
####    result.append(['China Channel','','','10790'])
####    result.append(['Dramax','','','10800'])
####    result.append(['home & shop','','','10810'])
####    result.append(['NS shop+','','','10820'])
####    result.append(['Shinsege shop','','','10830'])
####    result.append(['discovery','','','10840'])
####    result.append(['w channel','','','10850'])
####    result.append(['CJ mall','','','10860'])
####    result.append(['Playboy','','','10870'])
####    result.append(['Honey','','','10880'])
####

    #result.append(['tvn','','','11800'])
    #result.append(['tvn - broken','','','11790'])
    #result.append(['kids','','','11780'])
    #result.append(['error','','','11770'])
    #result.append(['Play web drama','','','11760'])
    #result.append(['Play well made drama','','','11750'])
    #result.append(['Play well made movie','','','11740'])
    
    #result.append(['GS SHOP','','','10560'])
    #result.append(['SBS Sprts','','','10490'])
    
    #result.append(['SBS Sprts covered logo','','','10420'])


    ##
    #result.append(['Sky ICT','','','10360'])
    #result.append(['KBS1','','','10170'])
    #result.append(['KBS1','','','11970'])
    #result.append(['KBS2','','','11980'])
    result.append(['KBS1','','',10170,''])
    result.append(['KBS2','','',10140,''])
        #result.append(['KBS2','','','10140'])
    result.append(['MBC','','',10540,''])
    result.append(['SBS','','',10550,''])
    result.append(['SkySports','','',10440,''])
    result.append(['KBS N SPORTS','','',10410,''])
    result.append(['MBC Sports','','',10430,''])
    result.append(['MBC Sports2','','',10490,''])
    result.append(['SBS Sports','','',10420,''])
    result.append(['XTM','','',10130,''])
    result.append(['SPOTV','','',10070,''])
    result.append(['SPOTV2','','',11990,''])
    result.append(['SPOTV','','','http://www.jnas.info:9999/command/api/execute?apikey=0220169BZA&id=2&mode=redirect&ch=spotv',''])
    result.append(['SPOTV 2','','','http://www.jnas.info:9999/command/api/execute?apikey=0220169BZA&id=2&mode=redirect&ch=spotv2',''])
    result.append(['xtvn','','','http://rominc.synology.me:9999/klive/api/url.m3u8?m=url&s=tving&i=C01141&q=default&apikey=DOR0RCDXSE',''])
    
    #result.append(['SPOTV On','','','http://www.jnas.info:9999/command/api/execute?apikey=0220169BZA&id=2&mode=redirect&ch=spotvnow1'])
    #result.append(['SPOTV On 2','','','http://www.jnas.info:9999/command/api/execute?apikey=0220169BZA&id=2&mode=redirect&ch=spotvnow2'])    
#    result.append(['SPOTV NBA TV','','','http://www.jnas.info:9999/command/api/execute?apikey=0220169BZA&id=2&mode=redirect&ch=nbatv',''])
#    result.append(['SPOTV Golf and Health','','','http://www.jnas.info:9999/command/api/execute?apikey=0220169BZA&id=2&mode=redirect&ch=spotvplus',''])    

##    if b:
##        result.append(['SPOTV1','','','http://152.67.192.55:9999/command/api/execute?apikey=19F1AQDMIL&id=2&mode=redirect&ch=evt_football01',''])
##        result.append(['SPOTV7','','','http://152.67.192.55:9999/command/api/execute?apikey=19F1AQDMIL&id=2&mode=redirect&ch=evt_football07',''])
##        result.append(['SPOTV8','','','http://152.67.192.55:9999/command/api/execute?apikey=19F1AQDMIL&id=2&mode=redirect&ch=evt_football08',''])
##        result.append(['SPOTV09','','','http://152.67.192.55:9999/command/api/execute?apikey=19F1AQDMIL&id=2&mode=redirect&ch=evt_football09',''])
##        result.append(['SPOTV10','','','http://152.67.192.55:9999/command/api/execute?apikey=19F1AQDMIL&id=2&mode=redirect&ch=evt_football10',''])
##        result.append(['SPOTV31','','','http://152.67.192.55:9999/command/api/execute?apikey=19F1AQDMIL&id=2&mode=redirect&ch=evt_football31',''])              
#    result.append(['SPOTV GAMES','','','10710'])  
##    #result.append(['Mnet','','','10150'])
##    #result.append(['K shopping','','','11526'])
####    result.append(['SPOTV 2','','','11990'])
####    result.append(['EBS e','','','11910'])
####    result.append(['EBS +2','','','11900'])
####    result.append(['EBS +1','','','11890'])
####    result.append(['YTN weather','','','11880'])
####    result.append(['Tomayotv','','','11860'])
####    result.append(['k baduk','','','11850'])
####    result.append(['(i)Kids TalkTalk','','','11830'])
####    result.append(['Dae','','','11820'])
####    result.append(['Olleh tv','','','11790'])
####    result.append(['Disney Jr','','','11780'])
####    result.append(['?','','','11770'])    
####    result.append(['Play web drama','','','11760'])
####    result.append(['Playy premium movie','','','11750'])    
####    result.append(['Playy well made movie','','','11740'])
####    result.append(['?','','','11730'])    
####    result.append(['error','','','11030'])
####    result.append(['error','','','11020'])    
####    result.append(['error','','','11010'])
####    result.append(['shopping1','','','10570'])  
####    result.append(['GSShop','','','10560']) 
####    result.append(['sbssports','','','10490'])
####    result.append(['skysports','','','10440'])
####    result.append(['skysports2','','','10420'])
####    result.append(['skypetpark','','','10310'])
####    result.append(['7','','','10240'])
####    result.append(['kbs1','','','10170'])
####    result.append(['billiards tv','','','10080'])
    
    result2=[]
    #print result
    for i in range(len(result)):
        s=result[i][1].encode('latin1')
        unquoted = unquote(s)
        d=unquoted.decode('utf8').replace('+',' ')
        title=result[i][0]+' - ' + d
        a=result[i][2]
        e=unquote(a)
        e=e.decode('utf8')
    ##        c=result[i][0]
    ##        e=c.encode('utf8')
        result2.append({'title':title,'thumbnail':e,'ch_no':result[i][3]})
     
    items2 = [{'label':item['title'], 'path':plugin.url_for('LiveTVplay', title=item['title'].encode('utf-8'),cid=item['ch_no']), 'thumbnail':item['thumbnail']} for item in result2]
    p='SPOTV 채널입력'
    if b:
        try:
            q=requests.get('http://152.67.192.55:9999/mod/api/spotv/m3u?apikey=19F1AQDMIL')
            #q=requests.get('http://www.jnas.info:9999/command/api/execute?apikey=V0CCW24DIT&id=4&mode=return&get=m3u')
            #a=re.compile('tvg-name="([^"]+)".*?\\n(http?\S+L)').findall(q.text)
            a=re.compile('tvg-name="([^"]+)".*?\\n(.*?)\\n').findall(q.text)
            
            for i in range(len(a)):
                items2.append({'label':a[i][0], 'path':plugin.url_for('LiveTVplay', title=a[i][0].encode('utf-8'),cid=a[i][1]), 'thumbnail':p})
        except:
            #q=requests.get('http://152.67.192.55:9999/command/api/execute?apikey=19F1AQDMIL&id=1&mode=return&get=m3u')
            q=requests.get('http://www.jnas.info:9999/command/api/execute?apikey=V0CCW24DIT&id=4&mode=return&get=m3u')
            #a=re.compile('tvg-name="([^"]+)".*?\\n(http?\S+L)').findall(q.text)
            a=re.compile('tvg-name="([^"]+)".*?\\n(.*?)\\n').findall(q.text)
            
            for i in range(len(a)):
                items2.append({'label':a[i][0], 'path':plugin.url_for('LiveTVplay', title=a[i][0].encode('utf-8'),cid=a[i][1]), 'thumbnail':p})
        #items2.append({'label':p, 'path':plugin.url_for('LiveSPOTV', title='SPOTV 채널입력',cid='a'), 'thumbnail':p})
##
##    result3=[]
##
##    fixed=[]
##    fixed.append(['SPOTV','','','http://www.jnas.info:9999/command/api/execute?apikey=0220169BZA&id=2&mode=redirect&ch=spotv'])
##    fixed.append(['SPOTV 2','','','http://www.jnas.info:9999/command/api/execute?apikey=0220169BZA&id=2&mode=redirect&ch=spotv2'])
##    fixed.append(['SPOTV On','','','http://www.jnas.info:9999/command/api/execute?apikey=0220169BZA&id=2&mode=redirect&ch=spotvnow1'])
##    fixed.append(['SPOTV On 2','','','http://www.jnas.info:9999/command/api/execute?apikey=0220169BZA&id=2&mode=redirect&ch=spotvno2'])
##
##    
##    if b:
##        items2.append({'label':fixed[0][0], 'path':plugin.url_for('LiveTVplayfixed', title='SPOTV',cid='http://www.jnas.info:9999/command/api/execute?apikey=0220169BZA&id=2&mode=redirect&ch=spotv'), 'thumbnail':fixed[0][1]})
##        items2.append({'label':fixed[1][0], 'path':plugin.url_for('LiveTVplayfixed', title='SPOTV2',cid='http://www.jnas.info:9999/command/api/execute?apikey=0220169BZA&id=2&mode=redirect&ch=spotv2'), 'thumbnail':fixed[1][1]})
##        items2.append({'label':fixed[2][0], 'path':plugin.url_for('LiveTVplayfixed', title='SPOTV On',cid='http://www.jnas.info:9999/command/api/execute?apikey=0220169BZA&id=2&mode=redirect&ch=spotvnow1'), 'thumbnail':fixed[2][1]})
##        items2.append({'label':fixed[3][0], 'path':plugin.url_for('LiveTVplayfixed', title='SPOTV On 2',cid='http://www.jnas.info:9999/command/api/execute?apikey=0220169BZA&id=2&mode=redirect&ch=spotvnow2'), 'thumbnail':fixed[3][1]})
##        
    return plugin.finish(items2, update_listing=False)

@plugin.route('/<cid>/<title>/SPOTV/')
def LiveTVplay(cid,title):
    try:

        #cid=re.compile('CHANNEL_IMAGE/([0-9]+)/').findall(cid)
        quality = plugin.get_setting("quality", str)    
        #quality=plugin.get_setting('1080P', bool)
        if quality == '2':
            print '1080p'
            cid=int(cid)+1
        elif quality == '1':
            print 'HD'
            cid=int(cid)+2
        else:
            print 'SD'
            cid=int(cid)+3        

        url2='http://menu.megatvdnp.co.kr:38080/app5/0/api/epg_play?istest=1&ch_no=404&bit_rate=S&bit_rate_option=4000&user_model=LG-D852G&user_os=5.0.1&user_type=Android&user_net=WIFI'
        #url='http://menu.megatvdnp.co.kr:38080/app5/0/api/epg_proglist?istext=1&ch_no=404'
      
        headers={'User-Agent': 'OMS(compatible;ServiceType/OTN;DeviceType/Android;DeviceModel/LG-D852G;OSType/Android;OSVersion/5.0;AppVersion/5.0.32)',
                 'Content-Type':'text/plain;charset=UTF-8'}
        r = requests.post(url2, '', headers=headers)
        print(r.status_code, r.reason)
        obj = json.loads(r.text)

        result = obj['data']['live_url']

        chd = result.split('10451.m3u8')

        #result='http://121.156.46.112:80/'+str(cid)+'.m3u8'+chd[1]

        
    ##    #result=result.replace('10450',str(cid))
    ##    result=result.replace('10451',str(cid))
    ##    #result=result.replace('10452',str(cid))
    ##    #result=result.replace('10453',str(cid))
        serverfix = plugin.get_setting("Fixed Server", bool)
        server = plugin.get_setting("Servers", str)
        result='http://121.156.46.'+server+':80/'+str(cid)+'.m3u8'+chd[1]
        print result
    ##    if serverfix:
    ##        if server == '69':
    ##            result='http://121.156.46.69:80/'+str(cid)+'.m3u8'+chd[1]            
    ##        if server == '75':
    ##            result='http://121.156.46.75:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '76':
    ##            result='http://121.156.46.76:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '77':
    ##            result='http://121.156.46.77:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '79':
    ##            result='http://121.156.46.79:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '80':
    ##            result='http://121.156.46.80:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '81':
    ##            result='http://121.156.46.81:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '82':
    ##            result='http://121.156.46.82:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '83':
    ##            result='http://121.156.46.83:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '84':
    ##            result='http://121.156.46.84:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '85':
    ##            result='http://121.156.46.85:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '86':
    ##            result='http://121.156.46.86:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '87':
    ##            result='http://121.156.46.87:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '88':
    ##            result='http://121.156.46.88:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '89':
    ##            result='http://121.156.46.89:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '90':
    ##            result='http://121.156.46.90:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '91':
    ##            result='http://121.156.46.91:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '92':
    ##            result='http://121.156.46.92:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '93':
    ##            result='http://121.156.46.93:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '94':
    ##            result='http://121.156.46.94:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '95':
    ##            result='http://121.156.46.95:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '96':
    ##            result='http://121.156.46.96:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '97':
    ##            result='http://121.156.46.97:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '98':
    ##            result='http://121.156.46.98:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '99':
    ##            result='http://121.156.46.99:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '100':
    ##            result='http://121.156.46.100:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '101':
    ##            result='http://121.156.46.101:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '102':
    ##            result='http://121.156.46.102:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '103':
    ##            result='http://121.156.46.103:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '104':
    ##            result='http://121.156.46.104:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '105':
    ##            result='http://121.156.46.105:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '106':
    ##            result='http://121.156.46.106:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '107':
    ##            result='http://121.156.46.107:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '108':
    ##            result='http://121.156.46.108:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '109':
    ##            result='http://121.156.46.109:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '110':
    ##            result='http://121.156.46.110:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '111':
    ##            result='http://121.156.46.111:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '112':
    ##            result='http://121.156.46.112:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '113':
    ##            result='http://121.156.46.113:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '114':
    ##            result='http://121.156.46.114:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '115':
    ##            result='http://121.156.46.115:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '116':
    ##            result='http://121.156.46.116:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '117':
    ##            result='http://121.156.46.117:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '118':
    ##            result='http://121.156.46.118:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '119':
    ##            result='http://121.156.46.119:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '120':
    ##            result='http://121.156.46.120:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '121':
    ##            result='http://121.156.46.121:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '122':
    ##            result='http://121.156.46.122:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '123':
    ##            result='http://121.156.46.123:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '124':
    ##            result='http://121.156.46.124:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '125':
    ##            result='http://121.156.46.125:80/'+str(cid)+'.m3u8'+chd[1]
    ##        if server == '126':
    ##            result='http://121.156.46.126:80/'+str(cid)+'.m3u8'+chd[1]
    ##   
    ##        else:
    ##            result=chd[0]+str(cid)+'.m3u8'+chd[1]
    #    print 'no server selection ' + result

        req = urllib2.Request(result,'', headers)
        res = urllib2.urlopen(req)
        finalurl = res.geturl()
        
    except ValueError:
        finalurl = cid

    plugin.play_video( {'label': title, 'path':finalurl} )
    return plugin.finish(None, succeeded=False)

@plugin.route('/<cid>/<title>/')
def LiveSPOTV(cid,title):
    kb = xbmc.Keyboard('', '01 부터 31까지')
    kb.doModal()
    if kb.isConfirmed():
        enteredvalue = kb.getText()
    finalurl='http://152.67.192.55:9999/command/api/execute?apikey=19F1AQDMIL&id=2&mode=redirect&ch=evt_football'+enteredvalue
    
    plugin.play_video( {'label': title, 'path':finalurl} )
    return plugin.finish(None, succeeded=False)

##@plugin.route('/live/sports/High/')
##def High_list():
##
##    url='http://sports.news.naver.com/tv/onairScheduleList.nhn?gameId=&isScoreOn=true'
##    req = urllib2.Request(url)
##    response = urllib2.urlopen(req)
##    link=response.read()
##    soup=BeautifulSoup(link)
##
##    items = []
##
##    try:
##        for node in soup.findAll('li', {'class':''}):
##            cat = re.compile('params1="(.*?)"').findall(str(node))
##            cat = [element.upper() for element in cat]
##            gid = re.compile('params2="(.*?)"').findall(str(node))
##            if len(gid)==0:
##                gid = re.compile('params1="(.*?)"').findall(str(node))
##                cat = re.compile('params="(.*?)"').findall(str(node))
##            s1 = node.find("span", {"class":"score_num"}).find(text=True)
##            t1=re.compile('<strong>(.*?)</strong>').findall(str(node))
##            s2 = node.find("span", {"class":"score_num b_num"}).find(text=True)
##            info = node.find("span", {"class":"score_info"}).find(text=True)
##            
##            title = cat[0]+ ': ' + unicode(t1[0],'utf-8') + ' ' +s1+ ' vs. ' + unicode(t1[1],'utf-8') + ' ' +s2+ ' ' +info
##            items.append({'title':title, 'vid':gid[0]})
##            
##    except:
##        print "No sport streams"
##        
##    for node in soup.findAll('li', {'class':''}):
##        cat = re.compile('params1="(.*?)"').findall(str(node))
##        cat = [element.upper() for element in cat]
##        gid = re.compile('params2="(.*?)"').findall(str(node))
##        if len(gid)==0:
##            gid = re.compile('params1="(.*?)"').findall(str(node))
##            cat = re.compile('params="(.*?)"').findall(str(node))
##        t1=re.compile('<strong>(.*?)</strong>').findall(str(node))
##        
##        title = cat[0]+ ': ' + unicode(t1[0],'utf-8')
##
##        items.append({'title':title, 'vid':gid[0]})
##
##
##    items2=[]
##    items2 = ({'label':item['title'], 'path':plugin.url_for('resolveAndPlayVideo', title=item['title'].encode('utf-8'), vid=item['vid'], quality='2000'), 'thumbnail':''} for item in items)
##    items2=list(items2)
##    items2.append({'label':'##이하 DAUM 중계##', 'path':plugin.url_for('High_list'), 'thumbnail':''})
##    
##    url='http://live.tvpot.daum.net/potplayer/service/LiveTimeTable.do'
##    req = urllib2.Request(url)
##    req.add_header('Accept-Langauge', 'ko')
##    req.add_header('Cookie', 'language=kr')
##    link = urllib2.urlopen(req).read()
##    soup=BeautifulSoup(link)
##
##    items = []
##    for node in soup.findAll('li', {'class':'on'}):
##        if not node.span:
##            continue
##        time=node.span.string
##        title = node.find('a', {'class': 'link_live cast_title'}).string.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&#039;','\'')
##        liveid = node.a['href']
##        liveid=int(re.search(r'\d+', liveid).group())
##    ####        if Protocol==0:
##    ####            url='rtmp://203.133.176.170:1935/live/'+str(liveid)+'_1_2000'
##    ####
##    ####        elif Protocol==1:
##    ####            url='rtsp://203.133.176.170:554/'+ str(liveid) +'_1_2000'
##    ####        else:
##    ####            url='http://cdn.live.daum.net/kakao_ch1/'+ str(liveid) +'_1_2000.m3u8?domain=cdn.live.daum.net&ch=35349604'
##        #url='http://videofarm.daum.net/controller/api/open/v1_0/BroadcastStreams.action?broadcastId='+str(liveid)+'&profile=HIGH'
##        items.append({'title':title, 'broad_date':time, 'liveid':liveid, 'thumbnail':''})
##        items.sort(reverse=True)
##
##    items3=({'label':item['title'], 'path':plugin.url_for('resolveAndPlayVideoDaum', title=item['title'].encode('utf-8'), liveid=item['liveid'], quality='2000'), 'thumbnail':''} for item in items)
##
##    items2.extend(items3)
##    return plugin.finish(items2, update_listing=False)
##
##@plugin.route('/live/sports/Med/')
##def Med_list():
##
##    url='http://sports.news.naver.com/tv/onairScheduleList.nhn?gameId=&isScoreOn=true'
##    req = urllib2.Request(url)
##    response = urllib2.urlopen(req)
##    link=response.read()
##    soup=BeautifulSoup(link)
##
##    items = []
##
##    try:
##        for node in soup.findAll('li', {'class':''}):
##            cat = re.compile('params1="(.*?)"').findall(str(node))
##            cat = [element.upper() for element in cat]
##            gid = re.compile('params2="(.*?)"').findall(str(node))
##            if len(gid)==0:
##                gid = re.compile('params1="(.*?)"').findall(str(node))
##                cat = re.compile('params="(.*?)"').findall(str(node))
##            s1 = node.find("span", {"class":"score_num"}).find(text=True)
##            t1=re.compile('<strong>(.*?)</strong>').findall(str(node))
##            s2 = node.find("span", {"class":"score_num b_num"}).find(text=True)
##            info = node.find("span", {"class":"score_info"}).find(text=True)
##            
##            title = cat[0]+ ': ' + unicode(t1[0],'utf-8') + ' ' +s1+ ' vs. ' + unicode(t1[1],'utf-8') + ' ' +s2+ ' ' +info
##            items.append({'title':title, 'vid':gid[0]})
##            
##    except:
##        print "No sport streams"
##        
##    for node in soup.findAll('li', {'class':''}):
##        cat = re.compile('params1="(.*?)"').findall(str(node))
##        cat = [element.upper() for element in cat]
##        gid = re.compile('params2="(.*?)"').findall(str(node))
##        if len(gid)==0:
##            gid = re.compile('params1="(.*?)"').findall(str(node))
##            cat = re.compile('params="(.*?)"').findall(str(node))
##        t1=re.compile('<strong>(.*?)</strong>').findall(str(node))
##        
##        title = cat[0]+ ': ' + unicode(t1[0],'utf-8')
##
##        items.append({'title':title, 'vid':gid[0]})
##
##
##    items2=[]
##    items2 = ({'label':item['title'], 'path':plugin.url_for('resolveAndPlayVideo', title=item['title'].encode('utf-8'), vid=item['vid'], quality='800'), 'thumbnail':''} for item in items)
##    items2=list(items2)
##    items2.append({'label':'##이하 DAUM 중계##', 'path':plugin.url_for('High_list'), 'thumbnail':''})
##    
##    url='http://live.tvpot.daum.net/potplayer/service/LiveTimeTable.do'
##    req = urllib2.Request(url)
##    req.add_header('Accept-Langauge', 'ko')
##    req.add_header('Cookie', 'language=kr')
##    link = urllib2.urlopen(req).read()
##    soup=BeautifulSoup(link)
##
##    items = []
##    for node in soup.findAll('li', {'class':'on'}):
##        if not node.span:
##            continue
##        time=node.span.string
##        title = node.find('a', {'class': 'link_live cast_title'}).string.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&#039;','\'')
##        liveid = node.a['href']
##        liveid=int(re.search(r'\d+', liveid).group())
##    ####        if Protocol==0:
##    ####            url='rtmp://203.133.176.170:1935/live/'+str(liveid)+'_1_2000'
##    ####
##    ####        elif Protocol==1:
##    ####            url='rtsp://203.133.176.170:554/'+ str(liveid) +'_1_2000'
##    ####        else:
##    ####            url='http://cdn.live.daum.net/kakao_ch1/'+ str(liveid) +'_1_2000.m3u8?domain=cdn.live.daum.net&ch=35349604'
##        #url='http://videofarm.daum.net/controller/api/open/v1_0/BroadcastStreams.action?broadcastId='+str(liveid)+'&profile=HIGH'
##        items.append({'title':title, 'broad_date':time, 'liveid':liveid, 'thumbnail':''})
##        items.sort(reverse=True)
##
##    items3=({'label':item['title'], 'path':plugin.url_for('resolveAndPlayVideoDaum', title=item['title'].encode('utf-8'), liveid=item['liveid'], quality='1000'), 'thumbnail':''} for item in items)
##
##    items2.extend(items3)
##    return plugin.finish(items2, update_listing=False)
##
##
##@plugin.route('/live/sports/Low/')
##def Low_list():
##
##    url='http://sports.news.naver.com/tv/onairScheduleList.nhn?gameId=&isScoreOn=true'
##    req = urllib2.Request(url)
##    response = urllib2.urlopen(req)
##    link=response.read()
##    soup=BeautifulSoup(link)
##
##    items = []
####
####    try:
####        for node in soup.findAll('li', {'class':''}):
####            cat = re.compile('params1="(.*?)"').findall(str(node))
####            cat = [element.upper() for element in cat]
####            gid = re.compile('params2="(.*?)"').findall(str(node))
####            if len(gid)==0:
####                gid = re.compile('params1="(.*?)"').findall(str(node))
####                cat = re.compile('params="(.*?)"').findall(str(node))
####            s1 = node.find("span", {"class":"score_num"}).find(text=True)
####            t1=re.compile('<strong>(.*?)</strong>').findall(str(node))
####            s2 = node.find("span", {"class":"score_num b_num"}).find(text=True)
####            info = node.find("span", {"class":"score_info"}).find(text=True)
####            
####            title = cat[0]+ ': ' + unicode(t1[0],'utf-8') + ' ' +s1+ ' vs. ' + unicode(t1[1],'utf-8') + ' ' +s2+ ' ' +info
####            items.append({'title':title, 'vid':gid[0]})
####            
####    except:
####        print "No sport streams"
##        
##    for node in soup.findAll('li', {'class':''}):
##        cat = re.compile('params1="(.*?)"').findall(str(node))
##        cat = [element.upper() for element in cat]
##        gid = re.compile('params2="(.*?)"').findall(str(node))
##        if len(gid)==0:
##            gid = re.compile('params1="(.*?)"').findall(str(node))
##            cat = re.compile('params="(.*?)"').findall(str(node))
##        t1=re.compile('<strong>(.*?)</strong>').findall(str(node))
##        
##        title = cat[0]+ ': ' + unicode(t1[0],'utf-8')
##
##        items.append({'title':title, 'vid':gid[0]})
##
##
##    items2=[]
##    items2 = ({'label':item['title'], 'path':plugin.url_for('resolveAndPlayVideo', title=item['title'].encode('utf-8'), vid=item['vid'], quality='300'), 'thumbnail':''} for item in items)
##    items2=list(items2)
##    items2.append({'label':'##이하 DAUM 중계##', 'path':plugin.url_for('High_list'), 'thumbnail':''})
##    
##    url='http://live.tvpot.daum.net/potplayer/service/LiveTimeTable.do'
##    req = urllib2.Request(url)
##    req.add_header('Accept-Langauge', 'ko')
##    req.add_header('Cookie', 'language=kr')
##    link = urllib2.urlopen(req).read()
##    soup=BeautifulSoup(link)
##
##    items = []
##    for node in soup.findAll('li', {'class':'on'}):
##        if not node.span:
##            continue
##        time=node.span.string
##        title = node.find('a', {'class': 'link_live cast_title'}).string.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&#039;','\'')
##        liveid = node.a['href']
##        liveid=int(re.search(r'\d+', liveid).group())
##    ####        if Protocol==0:
##    ####            url='rtmp://203.133.176.170:1935/live/'+str(liveid)+'_1_2000'
##    ####
##    ####        elif Protocol==1:
##    ####            url='rtsp://203.133.176.170:554/'+ str(liveid) +'_1_2000'
##    ####        else:
##    ####            url='http://cdn.live.daum.net/kakao_ch1/'+ str(liveid) +'_1_2000.m3u8?domain=cdn.live.daum.net&ch=35349604'
##        #url='http://videofarm.daum.net/controller/api/open/v1_0/BroadcastStreams.action?broadcastId='+str(liveid)+'&profile=HIGH'
##        items.append({'title':title, 'broad_date':time, 'liveid':liveid, 'thumbnail':''})
##        items.sort(reverse=True)
##
##    items3=({'label':item['title'], 'path':plugin.url_for('resolveAndPlayVideoDaum', title=item['title'].encode('utf-8'), liveid=item['liveid'], quality='500'), 'thumbnail':''} for item in items)
##
##    items2.extend(items3)
##    return plugin.finish(items2, update_listing=False)
##
##
##@plugin.route('/live/sports/<quality>/<liveid>/daum/<title>')
##def resolveAndPlayVideoDaum(liveid,quality,title):
##    if Protocol==0:
##        url='rtmp://203.133.176.170:1935/live/'+liveid+'_1_'+quality
##
##    elif Protocol==1:
##        url='rtsp://203.133.176.170:554/'+ liveid +'_1_'+quality
##    else:
##        url='http://cdn.live.daum.net/kakao_ch1/'+ liveid +'_1_'+quality+'.m3u8?domain=cdn.live.daum.net&ch=35349604'  
####    listItem = xbmcgui.ListItem(path=str(url))
####    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
####
####    
##    plugin.play_video( {'label': title, 'path':url} )
##    return plugin.finish(None, succeeded=False)
##
##@plugin.route('/live/sports/<quality>/<vid>/<title>')
##def resolveAndPlayVideo(vid,quality,title):
##    url2='http://sports.news.naver.com/tv/index.nhn?gameId=' + vid
##    req = urllib2.Request(url2)
##    response = urllib2.urlopen(req)
##    link=response.read()
##    response.close()
##    
##    ch=re.compile('"channelID":"high(.*?)"').search(link).group(1)
##
##    if quality=='2000':
##        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2F'+ch+'%2F_definst_%2F'+ch+'_2000.stream%2Fplaylist.m3u8'
##    elif quality=='800':
##        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2F'+ch+'%2F_definst_%2F'+ch+'_800.stream%2Fplaylist.m3u8'
##    else:
##        url='http://surl.ncast.nhncorp.com/secUrl.nhn?orgUrl=http%3A%2F%2Fhls.live.m.nhn.gscdn.com%2F'+ch+'%2F_definst_%2F'+ch+'_300.stream%2Fplaylist.m3u8'
##        
##    req = urllib2.Request(url)
##    response = urllib2.urlopen(req)
##    link=response.read()
##    response.close()
##
##    plugin.play_video( {'label': title, 'path':link} )
##    return plugin.finish(None, succeeded=False)

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
