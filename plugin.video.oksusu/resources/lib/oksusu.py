# -*- coding: utf-8 -*-
import urllib, urllib2, cookielib
import os
import json
import re
import pickle
import ssl
from io import open

######################################## 
# KODI & PLEX
######################################## 
LOGINDATA = ''
try:
	import xbmc, xbmcaddon
	profile = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))
	LOCAL_PROGRAM_LIST = xbmc.translatePath(os.path.join( profile, 'programlist.txt'))
	LOGINDATA = xbmc.translatePath(os.path.join( profile, 'login2.dat'))
except:
	pass

try:
	if LOGINDATA is '':
		LOCAL_PROGRAM_LIST = os.path.join( os.getcwd(), 'programlist.txt')
		LOGINDATA = os.path.join( os.getcwd(), 'login2.dat')
except:
	pass

def LOG(str):
	try :
		import xbmc, xbmcaddon
		try:
			xbmc.log("[%s-%s]: %s" %(xbmcaddon.Addon().getAddonInfo('id'), xbmcaddon.Addon().getAddonInfo('version'), str), level=xbmc.LOGNOTICE)
			log_message = str.encode('utf-8', 'ignore')
		except:
			log_message = 'OKSUSU LOG Exception'
		xbmc.log("[%s-%s]: %s" %(xbmcaddon.Addon().getAddonInfo('id'), xbmcaddon.Addon().getAddonInfo('version'), log_message), level=xbmc.LOGNOTICE)
		return
	except:
		pass

	try:
		Log(str)
		return
	except:
		pass


def GetSetting(type):
	try:
		import xbmc, xbmcaddon
		ret = xbmcaddon.Addon().getSetting(type)
		return ret
	except:
		pass

	try:
		ret = Prefs[type]
		return ret
	except:
		pass

######################################## 
# 공통
######################################## 
VERSION = '0.2.0'
QUALITYS = ['FHD', 'HD', 'SD']
MENU_LIST = [
	'ALL:오리지널:9000002014:P',
	'ALL:방송 클립:9000001800:P',
	'ALL:스포츠:9000002016:P',
	'ALL:영화:9000002017:P',
	'ALL:키즈:8000000191:C',
#	'ALL:LIVE:9000001352:P',
	'ALL:인문/경영:9000001972:C',
	'SKT:영화:9000001405:P',
	'SKT:방송:9000001406:C',
	'BASIC:한국 영화:9000001403:P',
	'BASIC:해외 영화:9000001404:P',
	'BASIC:TV 종영작:9000001417:C',
	'BASIC:해외 시리즈:9000001751:C',
	'BASIC:다큐:9000001753:C',
	'BASIC:키즈:9000001752:C']
#TOP_MENU_LIST = ['LIVE:LIVE:P', 'ch.:CH:C', '전국민 무료:ALL:M','SKT 고객 전용관:SKT:M', '기본월정액 무료:BASIC:M', '오리지널:CLIP:C', 'Watched:Watched:W']
TOP_MENU_LIST = ['LIVE:LIVE:P', '전국민 무료:ALL:M','SKT 고객 전용관:SKT:M', '기본월정액 무료:BASIC:M', '오리지널:CLIP:C', 'Watched:Watched:W']

def DoStartLoginCheck():
	id = GetSetting('id')
	pw = GetSetting('pw')
	use_local_logindata = GetSetting('use_local_logindata')

	if id == '' : id = None
	if pw == '' : pw = None
	message = '['
	if id is None or pw is None:
		message += '아이디/암호 정보가 없습니다.'
	else:
		status = GetLoginStatus()
		if status == 'NOT_LOGIN_FILE' or status == 'LOGIN_FAIL' or use_local_logindata == False or use_local_logindata == 'false':
			isLogin = DoLogin(id, pw)
			status = GetLoginStatus()
			if status == 'SUCCESS': 
				message += '로그인 정보를 저장했습니다. '
				if str(use_local_logindata): message += '저장된 정보로 로그인합니다.'
				else: message += '매번 로그인합니다.'
			elif status == 'LOGIN_FAIL': message += '로그인에 실패하였습니다.'
		elif status == 'SUCCESS': message += '저장된 로그인 정보가 있습니다.' 
		elif status == 'LOGIN_FAIL': message += '로그인 파일은 있으나 유효하지 않습니다'
	message += ']'
	return message

def GetLoginStatus():
	if os.path.isfile(LOGINDATA):
		login_data = GetLoginData()
		if 't' in login_data: return 'SUCCESS'
		else: return 'LOGIN_FAIL'
	else:
		return 'NOT_LOGIN_FILE'

def DoLogin(user_id, user_pw ):
	e = 'Log'
	isLogin = False
	try:
		if os.path.isfile(LOGINDATA): os.remove(LOGINDATA)
		loginData = {}
		url = 'https://www.oksusu.com/user/login'
		params = { 'userId' : user_id,
			'password' : user_pw,
			'loginMode' : '1',
			'rw' : '/',
			'serviceProvide' : '',
			'accessToken' : '' }
		postdata = urllib.urlencode( params )
		request = urllib2.Request(url, postdata)
		request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
		#response = urllib2.urlopen(request)
		gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
		response = urllib2.urlopen(request, context=gcontext)
		cookie = response.info().getheader('Set-Cookie')
		for c in cookie.split(','):
			c = c.strip()
			if c.startswith('CORN_AC'):
				loginData['t'] = c.split(';')[0]
			
		file = open(LOGINDATA, 'wb')
		pickle.dump(loginData, file)
		file.close()
		isLogin = True
	except Exception as e:
		LOG('<<<Exception>>> DoLogin: %s' % e)
	return (isLogin, e)

def GetList( type, param, page ):
	#LOG('GETLIST PARAM type:%s param:%s page:%s' % (type, param, page ) )
	has_more = 'N'
	try:
		result = []
		if type == 'Watched':
			for line in LoadWatchedList():
				info = {}
				tmp = line.strip().split('|')
				info['type'] = tmp[0]
				info['id'] = tmp[1]
				info['title'] = tmp[2]
				info['img'] = tmp[3]
				result.append(info)
		elif type == 'LIVE' or (type == 'CH' and param == 'C'):
			url = 'https://www.oksusu.com/api/live/organization/list?genreCode=99&orgaPropCode=ALL'
			request = urllib2.Request(url)
			request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
			#response = urllib2.urlopen(request)
			response = urllib2.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
			data = json.load(response, encoding="utf-8")
			#LOG(data)
			for item in data["channels"]:
				try:
					info = {}
					if (type == 'LIVE' and item['hlsUrlPhoneAUTO'] is not None) or (type == 'CH' and item['hlsUrlPhoneAUTO'] is None):
						info['id'] = item['serviceId']
						info['channel_title'] = unicode(item['channelName'])
						info['episode_title'] = item['programs'][0]['programName']
						info['img'] = 'http://image.oksusu.com:8080/thumbnails/image/0_0_F20/live/logo/387/'+ item['channelImageName']
						#info['music_yn'] = 'item['music_yn']
						info['music_yn'] = 'N' if item['programs'][0]['subGenreCd'] != 'G006' else 'Y'
						result.append(info)
				except Exception as e:
					LOG(e)
					pass
		elif type == 'CH' and param is not None:
			data = GetURLJSON(param)
			for item in data['channel']['another_programs']:
				try:
					info = {}
					info['episode_title'] = item['programName']
					info['img'] = item['extr_posterUrl']
					info['ch_id'] = param
					info['ch_title'] = data['channel']['channelName']
					result.append(info)
				except:
					pass
			i = 0
			for item in data["streamUrl"]['nvodHlsUrlList']:
				try:
					result[i]['url'] = item['nvod_token']
					i = i+1
				except:	
					pass
		elif type == 'CLIP':
			url = 'http://www.oksusu.com/api/nav/menu/content/list?menuId=9000000702&pageNo=1&pageSize=30&sortMethod='
			request = urllib2.Request(url)
			request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
			response = urllib2.urlopen(request)
			data = json.load(response, encoding='utf-8')
			for item in data['grids']:
				try:
					info = {}
					#info['id'] = item['menu_id']
					tmp = item['call_object'].split('|')
					info['id'] = tmp[len(tmp)-1]
					info['title'] = item['card_headline']
					info['summary'] = item['card_title']
					info['img'] = item['grids'][0]['thum_info_high'][0]['1']
					result.append(info)
				except:
					pass
		elif param == 'P' or param == 'C':
			url = 'http://www.oksusu.com/api/nav/menu/content/list?menuId=%s&pageNo=%s&pageSize=30&sortMethod=6' % (type, page)
			request = urllib2.Request(url)
			request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
			response = urllib2.urlopen(request)
			data = json.load(response, encoding="utf-8")
			total_count = data['grids'][0]['total_grids_count']
			if int(total_count) > 30*int(page): has_more = 'Y'
			for item in data["grids"][0]["grids"]:
				try:
					info = {}
					if 'con_id' in item:
						info['id'] = item['con_id']
						info['title'] = item['title']
						info['summary'] = item['c_desc']
						info['img'] = item['poster_high']
						info['series_id'] = None
						if 'series_id' in item: info['series_id']= item['series_id']
					elif 'clip_id' in item:
						info['id'] = item['clip_id']
						info['title'] = '['+ item['clip_chnl_nm'] + '] '  + item['clip_title']
						info['summary'] = item['clip_chnl_nm']
						info['img'] = item['thum_info_high'][0]['1']
						info['series_id'] = None
						if 'obj_id' in item: info['series_id']= item['obj_id']
					result.append(info)
				except:
					pass
		elif param == 'E':
			url = 'http://www.oksusu.com/api/vod/season?seriesId=' + type
			request = urllib2.Request(url)
			request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
			response = urllib2.urlopen(request)
			data = json.load(response, encoding="utf-8")
			for item in data['content']['series']:
				try:
					info = {}
					info['id'] = item['con_id']
					info['no'] = item['seq_no']
					info['title'] = item['s_title']
					info['summary'] = item['story_mid']
					info['img'] = item['thum_path'].replace(':type', '560_320')
					info['program_title'] = item['title']
					info['series_id'] = type
					result.append(info)
				except:
					pass		
		
	except Exception as e:
		LOG('<<<Exception>>> GetList: %s' % e)
		result = []
	return has_more, result

def GetURLJSON(code):
	try:
		login = GetLoginData()
		# 2018-03-29 영화, 방송은 https / 클립 http
		data = None
		try:
			url = 'https://www.oksusu.com/v/' + code
			request = urllib2.Request(url)
			request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
			if login is not None and 't' in login:
				request.add_header('cookie', login['t'])
			response = urllib2.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
			data = response.read()
		except: 
			pass
		if data == None:
			url = 'http://www.oksusu.com/v/' + code
			request = urllib2.Request(url)
			request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
			if login is not None and 't' in login:
				request.add_header('cookie', login['t'])
			response = urllib2.urlopen(request)
			data = response.read()
		
		idx1 = data.find('contentsInfo:') +14
		idx2 = data.find('|| {}')-1
		data = data[idx1:idx2]
		js = json.loads(data)
		return js
	except Exception as e:
		LOG('<<<Exception>>> GetURLJSON: %s' % e)
	return

def GetURL(code):
	try:
		js = GetURLJSON(code)
		info = {}
		info['FHD'] = js['streamUrl']['urlFHD'] if 'urlFHD' in js['streamUrl'] else None
		info['HD'] = js['streamUrl']['urlHD'] if 'urlHD' in js['streamUrl'] else None
		info['SD'] = js['streamUrl']['urlSD'] if 'urlSD' in js['streamUrl'] else None
		info['AUTO'] = js['streamUrl']['urlAUTO'] if 'urlAUTO' in js['streamUrl'] else None
		#info['PCFHD'] = js['streamUrl']['hlsUrlPcFHDAuto'] if 'hlsUrlPcFHDAuto' in js['streamUrl'] else None
		if 'nvodHlsUrlList' in js['streamUrl'] and js['streamUrl']['nvodHlsUrlList'] is not None:
			vods = js['streamUrl']['nvodHlsUrlList']
			if len(vods) > 0:
				#for i in range(0, len(vods)-1):
				#	info['VOD'][i] = vods['nvod_token']
				info['VOD'] = vods[0]['nvod_token']
		return info
	except Exception as e:
		LOG('<<<Exception>>> GetURL: %s' % e)
	return

def LoadWatchedList():
	try:
		f = open(LOCAL_PROGRAM_LIST, 'r', encoding='utf-8')
		result = f.readlines()
		f.close()
		return result
	except Exception as e:
		LOG('<<<Exception>>> LoadWatchedList: %s' % e)
		result = []
	return result

def SaveWatchedList( data ):
	try:
		result = LoadWatchedList()
		with open(LOCAL_PROGRAM_LIST, 'w', encoding='utf-8') as fw:
			#data = unicode(data + '\n')
			data = (data + '\n').decode('utf8')
			fw.write(data)
			num = 1
			for line in result:
				if line.find(data.split('|')[1]) == -1: 
					fw.write(line)
					num += 1
				if num == 100: break
	except Exception as e:
		LOG('<<<Exception>>> SaveWatchedList: %s' % e)
	return

def GetLoginData():
	try:
		file = open(LOGINDATA, 'rb')
		login = pickle.load(file)
		file.close()
	except Exception, e:
		LOG('<<<Exception>>> GetLoginData: %s' % e)
		login = []
	return login
