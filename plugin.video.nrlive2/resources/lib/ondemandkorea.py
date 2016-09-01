# -*- coding: utf-8 -*-
"""
    ondemandkorea.com

    /includes/latest.php?cat=<name>
    /includes/episode_page.php?cat=<name>&id=<num>&page=<num>
"""
import urllib, urllib2
import re
import json
from BeautifulSoup import BeautifulSoup
import xml.etree.ElementTree as etree
import random

root_url = "http://www.ondemandkorea.com"
img_base = "http://max.ondemandkorea.com/includes/timthumb.php?w=175&h=100&src="
# mimic iPad
default_hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Connection': 'keep-alive'}
tablet_UA = 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19'

eplist_url = "/includes/episode_page.php?cat={program:s}&id={videoid:s}&page={page:d}"

bitrate2resolution = {
    196:'180p',
    396:'240p',
    796:'300p',
    1296:'360p',
    1596:'480p',
    2296:'720p'
}

def parseTop(koPage=True):
    req  = urllib2.Request(page_url, headers=default_hdr)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)
    items = []
    for node in soup.find('div', {'id':'menu-category'}).findAll(lambda tag: tag.name=='a' and '.html' in tag['href']):
        items.append(node['href'])
    return items

def parseGenrePage(page_url, koPage=True):
    req  = urllib2.Request(page_url, headers=default_hdr)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)
    # soup.findAll('div', {'class':'genreSub'})
    items = []
    for node in soup.findAll('div', {'class':'ep_box'}):
        thumb = node.find('img', {'title':True})['src']
        items.append({'title':node.a['title'], 'url':root_url+'/'+node.a['href'], 'thumbnail':thumb})
    return items

def parseGenrePage2(page_url, koPage=True):
    req  = urllib2.Request(page_url, headers=default_hdr)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    html = urllib2.urlopen(req).read().decode("utf-8")
    items = []
    for part in html.split('<div class="ep_box"')[1:]:
        match = re.compile('<a href="([^"]*)" title="([^"]*)">.*<img src="([^"]*timthumb[^"]*)"', re.S).search(part)
        if match:
            items.append({'title':match.group(2), 'url':root_url+"/"+match.group(1), 'thumbnail':match.group(3)})
    return items

def parseEpisodePage(page_url, page=1, koPage=True):
    req  = urllib2.Request(page_url, headers=default_hdr)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)
    # soup.findAll('div', {'class':'genreSub'})
    result = {'episode':[]}
    for node in soup.findAll('div', {'class':re.compile('^(?:ep|ep_last)$')}):
        if not node.b:
            continue
        title = node.b.string.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>')
        thumb = node.find('img', {'title':True})['src']
        dt = node.b.findNextSibling(text=True)
        bdate = dt.string.split(':',1)[1].strip() if dt else ''
        result['episode'].append({'title':title, 'broad_date':bdate, 'url':root_url+node.a['href'], 'thumbnail':thumb})
    # no page navigation
    return result

def parseEpisodePage2(page_url, page=1, koPage=True):
    req  = urllib2.Request(page_url, headers=default_hdr)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    html = urllib2.urlopen(req).read().decode('utf-8')
    # 1. 
    #   $.getJSON( "/includes/episode_page.php", {cat: '<program>',id: <videoid>,page : pg)
    # 2. 
    #   "program" : "<program>",
    #   "videoid" : "<videoid>",
    match = re.compile("getJSON\( *\"/[^\"]*\", *{ *cat: *'([^']*)', *id: *(\d+)"). search(html)
    if match:
        program, videoid = match.group(1,2)
    else:
        program = re.compile('"program" *: *"(.*?)"').search(html).group(1)
        videoid = re.compile('"videoid" *: *(\d+)').search(html).group(1)
    list_url = root_url+eplist_url.format(program=program, videoid=videoid, page=page)

    req  = urllib2.Request(list_url, headers=default_hdr)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    req.add_header('Referer', page_url)
    jstr = urllib2.urlopen(req).read()
    obj = json.loads(jstr)

    result = {'episode':[]}
    for item in obj['list']:
        result['episode'].append({'title':item['title'], 'broad_date':item['on_air_date'], 'url':root_url+"/"+item['url'], 'thumbnail':img_base+item["thumbnail"]})
    if obj['cur_page'] > 1:
        result['prevpage'] = page-1
    if obj['cur_page'] < obj['num_pages']:
        result['nextpage'] = page+1
    return result

# m3u8
def extractStreamUrl(page_url, koPage=True, referer=None):
    req  = urllib2.Request(page_url, headers=default_hdr)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    if referer:
        req.add_header('Referer', referer)
    html = urllib2.urlopen(req).read().decode('utf-8')
    vid_title = re.compile('<div id="title">(.*?)</div>', re.S).search(html).group(1).strip()
    match = re.compile("""(http[^'"]*m3u8)""").search(html, re.I|re.U)
    if not match:
        return None
    vid_url = match.group(1)
    videos = dict()
    for bitrate, resolution in bitrate2resolution.iteritems():
        videos[resolution] = {'url':vid_url.replace('720p', resolution)}
    return {'title':vid_title, 'videos':videos}

# mp4
def extractVideoUrl(page_url, koPage=True, referer=None):
    req  = urllib2.Request(page_url)
    req.add_header('User-Agent', tablet_UA)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    if referer:
        req.add_header('Referer', referer)
    html = urllib2.urlopen(req).read().decode('utf-8')
    vid_title = re.compile('<div id="title">(.*?)</div>', re.S).search(html).group(1).strip()
    match = re.compile("""(http[^'"]*mp4)""").search(html)
    if not match:
        return None
    vid_url = match.group(1)
    videos = dict()
    for bitrate, resolution in bitrate2resolution.iteritems():
        videos[resolution] = {'url':vid_url.replace('360p.1296k', resolution+'.'+str(bitrate)+'k')}
    return {'title':vid_title, 'videos':videos}

def guessVideoUrl(page_url, genre='drama', koPage=True):
    hostname = "sjcstor%02d" % random.randint(1,8)
    if genre == "variety":
        genre = "variety2"

    req = urllib2.Request(page_url)
    req.add_header('User-Agent', tablet_UA)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    html = urllib2.urlopen(req).read().decode('utf-8')
    vid_title = re.compile('<div id="title">(.*?)</div>', re.S).search(html).group(1).strip()
    thumb = re.compile('<link rel="image_src" href="([^"]*)"').search(html).group(1)
    program, date = re.compile("/([^/_]*)_(\d+)").search(thumb).group(1,2)

    videos = dict()
    for bitrate, resolution in bitrate2resolution.iteritems():
        vid_url = "http://{hostname:s}.ondemandkorea.com/{genre:s}/{program:s}/{program:s}_{date:s}.{resolution:s}.{bitrate:s}.mp4".format(hostname=hostname, program=program, date=date, resolution=resolution, bitrate=str(bitrate)+'k', genre=genre)
        videos[resolution] = {'url':vid_url}
    return {'title':vid_title, 'videos':videos}

if __name__ == "__main__":
    #print parseTop()
    #print parseGenrePage( root_url+"/variety" )
    print parseGenrePage2( root_url+"/variety" )
    #print parseEpisodePage( root_url+"/infinite-challenge-e452.html" )
    print parseEpisodePage2( root_url+"/infinite-challenge-e452.html", page=2 )
    #print extractStreamUrl( root_url+"/infinite-challenge-e452.html" )
    #print extractVideoUrl( root_url+"/infinite-challenge-e452.html" )
    print parseEpisodePage2( root_url+"/mystery-music-show-mask-king-e31.html" )
    print extractVideoUrl( root_url+"/mystery-music-show-mask-king-e31.html" )
    print guessVideoUrl( root_url+"/mystery-music-show-mask-king-e31.html", genre='variety' )

# vim:sw=4:sts=4:et
