# -*- coding: utf-8 -*-
import os
import urllib
import xbmcplugin, xbmcgui, xbmcaddon
from urlparse import parse_qs

__addon__ = xbmcaddon.Addon()
__language__  = __addon__.getLocalizedString
sys.path.append(os.path.join( xbmc.translatePath( __addon__.getAddonInfo('path') ), 'resources', 'lib' ))
from oksusu import *

def Main():
	message = DoStartLoginCheck()
	message = 'Ver : ' + VERSION + ' - ' + message
	
	if GetLoginStatus() is not 'SUCCESS':
		dialog = xbmcgui.Dialog()
		ret = dialog.yesno(__addon__.getAddonInfo('name'), __language__(30201).encode('utf8'), __language__(30202).encode('utf8'))
		if ret == True:
			__addon__.openSettings()
			sys.exit()
		else:
			addDir(message, None, None, True, None, None, None, None)
	else:
		for menu in TOP_MENU_LIST:
			tmp = menu.split(':')
			if tmp[2] == 'M':
				addDir(tmp[0], None, None, True, 'Menu', tmp[1], None, None)
			else:
				addDir(tmp[0], None, None, True, 'ContentList', tmp[1], tmp[2], 1)
				
		addDir(message, None, None, True, None, None, None, None)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Menu(p):
	for item in MENU_LIST:
		tmp = item.split(':')
		if p['param'] == tmp[0]:
			addDir(tmp[1], None, None, True, 'ContentList', tmp[2], tmp[3], 1)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def ContentList(p):
	#LOG('CONTENTLIST : %s' % p)
	type = p['param']
	param = None
	if 'param2' in p and p['param2'] != 'None': param = p['param2']
	pageNo = p['pageNo']

	has_more, items = GetList(type, param, pageNo)
	for item in items:
		if type == 'LIVE':
			title2 = item['channel_title']
			infoLabels = {"mediatype":"episode","label":item['channel_title'] ,"title":item['channel_title'],"plot":item['episode_title']}
			save_param = '|'.join( [type, item['id'], urllib.quote(item['channel_title'].encode('utf-8')), item['img'] ])
			addDir(title2, item['img'], infoLabels, False, 'PlayVideo', item['id'], save_param, None)
		elif type == 'CH' and param == 'C':
			title2 = item['channel_title']
			infoLabels = {"mediatype":"episode","label":item['channel_title'] ,"title":item['channel_title'],"plot":item['episode_title']}
			addDir(title2, item['img'], infoLabels, True, 'ContentList', 'CH', item['id'], 1)
		elif type == 'CH' and param is not None:
			infoLabels = {"mediatype":"episode","label":item['episode_title'] ,"title":item['episode_title'],"plot":item['episode_title']}
			save_param = '|'.join( [type, item['ch_id'], urllib.quote(item['ch_title'].encode('utf-8')), item['img'] ])
			addDir(item['episode_title'], item['img'], infoLabels, False, 'PlayVideo', 'CH', save_param, item['url'])
		elif type == 'CLIP':
			infoLabels = {"mediatype":"episode","label":item['title'] ,"title":item['title'],"plot":item['summary']}
			addDir(item['title'], item['img'], infoLabels, True, 'ContentList', item['id'], 'P', 1)
		elif param == 'P':
			infoLabels = {"mediatype":"episode","label":item['title'] ,"title":item['title'],"plot":item['summary']}
			#save_param = '|'.join( ['P', item['id'], urllib.quote(item['title'].encode('utf-8')), item['img'] ])
			#addDir(item['title'], item['img'], infoLabels, False, 'PlayVideo', item['id'], save_param, None)
			addDir(item['title'], item['img'], infoLabels, False, 'PlayVideo', item['id'], None, None)
		elif param == 'C':
			infoLabels = {"mediatype":"episode","label":item['title'] ,"title":item['title'],"plot":item['summary']}
			addDir(item['title'], item['img'], infoLabels, True, 'ContentList', item['series_id'], 'E', 1)
		elif param == 'E':
			title2 = item['no'] + '회 '.decode('utf8') + '(' + item['title'] + ') ' #+ item['summary'][0:50]
			infoLabels = {"mediatype":"episode","label":item['title'] ,"title":item['title'],"plot":item['summary']}
			save_param = '|'.join( ['C', item['series_id'], urllib.quote(item['program_title'].encode('utf-8')), item['img'] ])
			addDir(title2, item['img'], infoLabels, False, 'PlayVideo', item['id'], save_param, None)
		elif type == 'Watched':
			infoLabels = {"mediatype":"episode","label":item['title'] ,"title":item['title'],"plot":item['title']}
			if item['type'] == 'LIVE' or item['type'] == 'P':
				save_param = '|'.join( [item['type'], item['id'], urllib.quote(item['title'].encode('utf-8')), item['img'] ])
				addDir(item['title'], item['img'], infoLabels, False, 'PlayVideo', item['id'], save_param, None)
			elif item['type'] == 'CH':
				addDir(item['title'], item['img'], infoLabels, True, 'ContentList', 'CH', item['id'], 1)
			elif item['type'] == 'C':
				addDir(item['title'], item['img'], infoLabels, True, 'ContentList', item['id'], 'E', 1)
	if pageNo != '1':
		addDir('<< ' + __language__(30002).encode('utf8'), None, None, True, 'ContentList', p['param'], p['param2'], str(int(pageNo)-1))

	if has_more == 'Y':
		addDir(__language__(30003).encode('utf8') + ' >>', None, None, True, 'ContentList', p['param'], p['param2'], str(int(pageNo)+1))
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
def PlayVideo( p ):
	#LOG('PLAYVIDEO: %s' % p)
	if p['param'] == 'CH':
		item = xbmcgui.ListItem(path=p['pageNo']) 
	else:
		quality = GetQuality()
		if quality is None: return

		code = p['param']
		url = GetURL(code)
		if url is None:
			addon_noti( __language__(30001).encode('utf8') )
			return
		#if quality == 'FHD' and 'PCFHD' in url:
		#	quality = 'PCFHD'
		if quality == 'FHD' and url[quality] is None:
			quality = 'HD'
		if quality == 'HD' and url[quality] is None:
			quality = 'SD'
		if url[quality] is None and 'AUTO' in url:
			quality = 'AUTO'
		if url[quality] is None:
			addon_noti( __language__(30001).encode('utf8') )
			return			
		item = xbmcgui.ListItem(path=url[quality])
	if 'param2' in p and p['param2'] != 'None':
		tmps = p['param2'].split('|')
		data = '|'.join([tmps[0], tmps[1], urllib.unquote(tmps[2].encode('utf-8')), tmps[3]])
		SaveWatchedList(data)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

def GetQuality():
	isManualQuality = __addon__.getSetting('manual_quality')
	quality = None
	if (isManualQuality == 'true'):
		choose_idx = xbmcgui.Dialog().select('Quality'.encode('utf-8'), QUALITYS)
		if choose_idx > -1: quality = QUALITYS[choose_idx]
		else: quality = None
		quality
	else:
		selected_quality = __addon__.getSetting('selected_quality')
		quality =  QUALITYS[int(selected_quality)]
	return quality

#########################
def addDir(title, img, infoLabels, isFolder, mode, param, param2, pageNo):
	params = {'mode': mode, 'param':param, 'param2':param2, 'pageNo':pageNo}
	url = '%s?%s' %(sys.argv[0], urllib.urlencode(params))
	listitem = xbmcgui.ListItem(title, thumbnailImage=img)
	if infoLabels: listitem.setInfo(type="Video", infoLabels=infoLabels)
	if not isFolder: listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, isFolder)

def addon_noti(sting):
	try:
		dialog = xbmcgui.Dialog()
		dialog.notification(__addon__.getAddonInfo('name'), sting)
	except:
		LOG('addonException: addon_noti')

def get_params():
	p = parse_qs(sys.argv[2][1:])
	for i in p.keys():
		p[i] = p[i][0]
	return p


params = get_params()
try:
	mode = params['mode']
except:
	mode = None
if mode == None: Main()
elif mode == 'Menu': Menu(params)
elif mode == 'ContentList': ContentList(params)
elif mode == 'PlayVideo': PlayVideo(params)
else: LOG('NOT FUNCTION!!')

