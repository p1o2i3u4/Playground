# -*- coding: utf-8 -*-
__author__ = "Dong-gyun Ham"
__email__ = "irow14@gmail.com"


import os
import urllib
import xbmcplugin, xbmcgui, xbmcaddon
from urlparse import parse_qs


__addon__ = xbmcaddon.Addon()
__language__  = __addon__.getLocalizedString
__profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__version__ = __addon__.getAddonInfo('version')
__id__ = __addon__.getAddonInfo('id')
__name__ = __addon__.getAddonInfo('name')
__cwd__ = xbmc.translatePath( __addon__.getAddonInfo('path') )
__lib__ = os.path.join( __cwd__, 'resources', 'lib' )
sys.path.append(__lib__)

from pooqCore import *

SHOW_GRADE = __addon__.getSetting('show_grade')
ONLY_NINETEEN = __addon__.getSetting('show_only_over_19')

# root 
def dp_main():
	addon_log('Display main!')

	# login process
	(pooq_id, pooq_pw) = get_settings_login_info()

	if not (pooq_id and pooq_pw):
		dialog = xbmcgui.Dialog()
		ret = dialog.yesno(__name__, __language__(30201).encode('utf8'), __language__(30202).encode('utf8'))
		if ret == True:
			__addon__.openSettings()
			sys.exit()

	# check login
	if pooq_id and pooq_pw:
		if not Pooq().GetCredential( pooq_id, pooq_pw ):
			# login failed
			addon_noti( __language__(30203).encode('utf8') )

	items = [
			  {'title':__language__(30009).encode('utf8'), 'category':'Live'},
			  {'title':__language__(30004).encode('utf8'), 'category':'VOD'},
			  {'title':__language__(30011).encode('utf8'), 'category':'ProgramList'},
			  {'title':__language__(30005).encode('utf8'), 'category':'Movie'}
			]

	for item in items:
		title = item['title']
		cate = item['category']
		add_dir(title, '', '', '', '', cate, 0)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def dp_live_list( p ):
	addon_log('Display Live List!')
	index = int(p['index'])
	mode = p['mode']
	items = Pooq().GetLiveListGeneresort()
	addon_log(items, True)

	for lists in items:
		for item in lists['list']:
			info = getInfo(mode,item)
			add_dir(info['title'], info['subtitle'], info['id'], info['img'], info['quality'], 'play_live', (index + 1), info, False)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def play_live( p ):
	addon_log('Play Live!')
	surl = None
	success = False

	try:
		ch_id = p['c_id']
	except:
		ch_id = None
	if ch_id:
		# select quality
		qualityList = p['properties'].split('|')
		quality = choose_stream_quality( qualityList )

		# get stream url
		if quality: isPreview, surl = Pooq().GetLiveStreamUrl(ch_id, quality)
	else:
		addon_noti( __language__(30204).encode('utf-8') )
	if surl:
		addon_log(surl, True)
		success = True
		## by soju
		#if isPreview: addon_noti( __language__(30001).encode('utf-8') )
	else:
		surl = ''

	item = xbmcgui.ListItem(path=surl)
	#item.setInfo(type="Video", infoLabels={'title': ch_nm})
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), success, item)


def dp_vod_list( p ):
	addon_log('Display VOD List!')
	index = int(p['index'])
	mode = p['mode']
	pooq = Pooq()
	funcs_list = {
					'VOD':( pooq.GetVODGenres, pooq.GetVODList ),
					'Movie':( pooq.GetMovieGenres, pooq.GetMovieList )
				 }
	funcs = funcs_list[mode]

	if index == 0:
		items = { 'VOD' : [ [__language__(30006).encode('utf8'),'search','s'], 
				  			[__language__(30007).encode('utf8'),'all','d'], 
				  			[__language__(30008).encode('utf8'),'all','h'] ],#, ['다국어','l'] 
				  'Movie' : [ [__language__(30006).encode('utf8'),'search','s'], 
							  [__language__(30010).encode('utf8'),'recommend','d'], 
							  [__language__(30007).encode('utf8'),'all','r'], 
							  [__language__(30008).encode('utf8'),'all','h'],
							  ['PLAYY','playy','d'] ] }

		for item in items[mode]:
			title = item[0]
			genre = item[1]
			orderby = item[2]
			add_dir(title, '', genre, '', orderby, mode, (index + 1))

		getgenre_func = funcs[0]
		genres = getgenre_func()

		for item in genres:
			titme = ''
			if mode == 'VOD':
				title = item['genreTitle'].encode('utf-8')
			elif mode == 'Movie':
				title = item['genreName'].encode('utf-8')
			genre = item['genreCode']
			#by soju d->h
			orderby = 'h'
			add_dir(title, '', genre, '', orderby, mode, (index + 1))

	else:
		genre = p['c_id']
		items = []

		if genre == 'search':
			# search
			kwd = get_keyboard_input(__language__(30003).encode('utf-8'))
			if kwd:
				items = pooq.Search(mode, kwd, index)
			else:
				return
		else:
			orderby = p['properties']
			getlist_func = funcs[1]
			items = getlist_func(genre, orderby, index)

		addon_log(items, True)
		
		for item in items['list']:
			info = getInfo(mode,item)
			if mode == 'VOD':
				pgm_nm = info['tvshowtitle']
				freq = info['episode']
				if freq: title = '%s %s회' % (pgm_nm, freq)
				else: title = pgm_nm
				## by soju
				if item['isFree'] == 'Y': title = '[Free]'+title
				## by soju6jan 2018-01-28. quickvod patch
				#ids = '|'.join([info['id'],info['programId'],info['cornerId']])
				isQvod = 'N'
				if item.has_key('isQvod'): isQvod = item['isQvod']
				#ids = '|'.join([info['id'],info['programId'],info['cornerId'], isQvod ])
				#add_dir(title, '', ids, info['img'], '', 'play_vod', (index + 1), info, False)
				add_dir(title, '', info['programId'], info['img'], '', 'EpisodeList', 1)
			elif mode == 'Movie':
				title = info['title']
				ids = info['id']
				add_dir(title, '', ids, info['img'], '', 'play_vod', (index + 1), info, False)
		# more page
		if genre == 'search':
			if (len(items) == 30) and (len(items) != 0):
				add_dir('[B]%s >>[/B]' % __language__(30002).encode('utf-8'), '', genre, '', orderby, mode, (index + 1) )
		else:
			count = int(items['count'])
			has_more = 'Y' if count > 30 else 'N'
			if has_more == 'Y':
				add_dir('[B]%s >>[/B]' % __language__(30002).encode('utf-8'), '', genre, '', orderby, mode, (index + 1) )

	xbmcplugin.endOfDirectory(int(sys.argv[1]))

##by soju #################
def dp_program_list( p ):
	items = Pooq().LoadProgramList()
	for item in items:
		data = item.split('|')
		add_dir(data[2], '', data[0], '', data[1], 'EpisodeList', 1)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def dp_episode_list( p ):
	index = int(p['index'])
	mode = p['mode']
	programId = p['c_id']
	channelId = p['properties'] if 'properties' in p else None
	if channelId == None: 
		result = Pooq().GetProgramInfo(programId)
		channelId = result['channelId'] if result is not None and 'channelId' in result else programId
	items = Pooq().GetEpisodeList(channelId, programId, int(index))
	for item in items['list']:
		info = getInfo('VOD',item)
		pgm_nm = ' ' if item['episodeTitle'] is None else item['episodeTitle'].encode('utf-8')
		freq = info['episode']
		if freq: title = '%s회 %s' % (freq,pgm_nm)
		else: title = pgm_nm
		if item['isFree'] == 'Y': title = '[Free]'+title
		isQvod = 'N'
		if item.has_key('isQvod'): isQvod = item['isQvod']
		ids = '|'.join([info['id'],info['programId'],info['cornerId'], isQvod])
		add_dir(title, '', ids, info['img'], '', 'play_vod', (index + 1), info, False)
	count = int(items['count'])
	has_more = 'Y' if count > 30 else 'N'
	if has_more == 'Y':
		add_dir('[B]%s >>[/B]' % __language__(30002).encode('utf-8'), '', programId, '', channelId, mode, (index + 1) )
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
##by soju #################

def getInfo( c_type, i ):
	import re
	info = {}

	#common
	ageRestriction = i['ageRestriction'].encode('utf8')
	if ageRestriction in ['12','15', '18']: info['mpaa'] = '%s세 관람가' % ageRestriction
	else: info['mpaa'] = '전체 관람가'

	try:
		description = i['description'].encode('utf8').replace('<br>','').replace('</br>','').replace('<b>','[B]').replace('</b>','[/B]')
		info['plot'] = description
		info['plotoutline'] = description
	except:
		pass

	info['id'] = i['id']

	# individual
	if c_type == 'Live':
		info['subtitle'] = i['title'].encode('utf8')
		info['title'] = i['channelTitle'].encode('utf8')
		info['img'] = i['image']
		info['isRadio'] = i['isRadio']
		if i['isLicenceAvaliable'] == 'X': info['id'] = ''
		info['quality'] = "|".join(i['qualityList'][0]['quality'])
		info['programId'] = i['programId']

	elif c_type == 'VOD':
		info['tvshowtitle'] = i['title'].encode('utf8')
		try:
			info['title'] = i['episodeTitle'].encode('utf8')
		except:
			info['title'] = info['tvshowtitle']
		info['img'] = i['image'].replace('.jpg','_11.jpg')
		info['aired'] = i['airDate']
		info['programId'] = i['programId']
		info['cornerId'] = i['cornerId']
		try:
			info['cast'] = i['starling'].split(',')
		except:
			pass
		try:
			info['episode'] = int(i['episodeNo'])
		except:
			info['episode'] = None

	elif c_type == 'Movie':
		info['programId'] = ''
		title = i['title'].encode('utf8')
		info['title'] = re.sub(r'\[.*\] ?', '', title)
		info['img'] = i['image'].replace('.jpg','_210.jpg')
		try:
			info['genre'] = i['genere']
			info['cast'] = i['starling'].split(', ')
		except:
			pass

	return info


def play_vod( p ):
	addon_log('Play VOD!')
	success = False
	surl = None
	item_cd = p['c_id']

	try:
		## by soju6jan 2018-01-28. quickvod patch
		#item_id, program_id, corner_id = item_cd.split('|')
		item_id, program_id, corner_id, is_qvod = item_cd.split('|')
	except:
		item_id = item_cd
		program_id = None
		corner_id = '1'
	pooq = Pooq()

	if program_id:
		vod_info = pooq.GetVODInfo( program_id, item_id, corner_id)
		vod_type = 'vod'
		## by soju6jan 2018-01-28. quickvod patch
		if is_qvod == 'Y': vod_type = 'qvod'
	else:
		vod_info = pooq.GetMovieInfo( item_id )
		vod_type = 'movie'

	if vod_info:
		addon_log(vod_info, True)

		# select quality
		qualityList = vod_info['resolutions'][0]['resolution']
		quality = choose_stream_quality( qualityList )

		# get stream url
		if quality: isPreview, surl = pooq.GetVODStreamUrl( vod_type, item_id, corner_id, quality )

		if surl:
			addon_log(surl, True)
			success = True
			if isPreview: addon_noti( __language__(30001).encode('utf-8') )
		else:
			surl = ''
		item = xbmcgui.ListItem(path=surl)
		#item.setInfo(type="Video", infoLabels={'title': title})
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), success, item)
		
		##by soju
		try:
			result = pooq.GetProgramInfo(program_id)
			data = '|'.join([program_id, result['channelId'], unicode(result['programTitle']), result['imageUrl']])
			pooq.SaveProgramList(data)
		except Exception as e:
			pass


def get_settings_login_info():
	# 설정에서 id, pwd 가져오기
	uid = __addon__.getSetting( 'id' )
	pwd = __addon__.getSetting( 'pwd' )
	return (uid, pwd)


def get_keyboard_input( heading, hidden=False ):
	input_text = None
	kb = xbmc.Keyboard()
	kb.setHeading( heading )
	if hidden: kb.setHiddenInput( hidden )
	xbmc.sleep(1000)
	kb.doModal()
	if (kb.isConfirmed()):
		input_text = kb.getText()
	return input_text


def choose_stream_quality( quality_list ):
	isManualQuality = __addon__.getSetting('manual_quality')
	quality = None

	if (isManualQuality == 'true'):
		quality = item_selecting( quality_list )
	else:
		def_quality_list = [ "5000", "2000", "1000", "500", "0" ]
		sel_quality_idx = int(__addon__.getSetting('selected_quality'))
		sel_quality = def_quality_list[sel_quality_idx]
		if sel_quality in quality_list:
			quality = sel_quality
		else:
			def_quality_list_new = def_quality_list[:sel_quality_idx+2]
			for i in reversed(range(0,len(quality_list))):
				for j in reversed(range(0,len(def_quality_list_new))):
					try:
						addon_log( "%s <= %s < %s" % (def_quality_list_new[j], quality_list[i], def_quality_list_new[j-1]), True )
						if int(def_quality_list_new[j]) > int(quality_list[i]):
							break
						elif int(def_quality_list_new[j]) <= int(quality_list[i]) < int(def_quality_list_new[j-1]):
							quality = quality_list[i]
							break
					except:
						pass
				if quality: break
			if not quality: quality = quality_list[0]
	return quality



def item_selecting( items ):
	choose_idx = xbmcgui.Dialog().select(__language__(30205).encode('utf-8'), items)
	if choose_idx > -1: sel_item = items[choose_idx]
	else: sel_item = None
	return sel_item


def add_grade( t, mpaa ):
	if SHOW_GRADE == 'true':
		if ONLY_NINETEEN == 'true' : 
			if (mpaa == "18세 관람가") : t = "[COLOR FFFF0000]⑲[/COLOR] " + t
		else:
			if (mpaa == "전체 관람가") : t = "[COLOR FF00FF00]◯[/COLOR] " + t
			elif (mpaa == "12세 관람가") : t = "[COLOR FF0000FF]⑫[/COLOR] " + t
			elif (mpaa == "15세 관람가") : t = "[COLOR FFFFFF00]⑮[/COLOR] " + t
			elif (mpaa == "18세 관람가") : t = "[COLOR FFFF0000]⑲[/COLOR] " + t
	return t



def addon_noti(sting):
	try:
		dialog = xbmcgui.Dialog()
		dialog.notification(__name__, sting)
	except:
		addon_log('addonException: addon_noti')


def addon_log(string, isDebug=False):
	try:
		log_message = string.encode('utf-8', 'ignore')
	except:
		log_message = 'addonException: addon_log'
	if isDebug: level = xbmc.LOGDEBUG
	else: level = xbmc.LOGNOTICE
	xbmc.log("[%s-%s]: %s" %(__id__, __version__, log_message), level=level)


def add_dir(label, sublabel, c_id, img, properties, mode, index, infoLabels=None, isfolder=True):
	params = {'c_id': c_id, 'mode': mode, 'index':index, 'properties':properties}
	url = '%s?%s' %(sys.argv[0], urllib.urlencode(params))
	if not img: img = 'DefaultFolder.png'
	if sublabel:
		title = '%s < %s >' % (label, sublabel)
	else:
		title = label

	if infoLabels: title = add_grade( title, infoLabels['mpaa'] )

	listitem = xbmcgui.ListItem(title, thumbnailImage=img)
	if infoLabels: listitem.setInfo(type="Video", infoLabels=infoLabels)
	if not isfolder: listitem.setProperty('IsPlayable', 'true')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, isfolder)


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

if mode == None:
	dp_main()

elif mode == 'Live':
	dp_live_list( params )

elif mode == 'play_live':
	play_live( params )

elif mode in ['VOD', 'Movie']:
	dp_vod_list( params )

elif mode == 'play_vod':
	play_vod( params )

elif mode == 'ProgramList':
	dp_program_list( params )

elif mode == 'EpisodeList':
	dp_episode_list( params )

else:
	addon_log('################### funcs not define ###################')

