#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests, json, re, os, time

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
UNDERLINE = '\033[4m'
RUNDERLINE = '\033[24m'
GRAY = '\033[90m'

def Print_Logo():
	Logo = '''


	{Y} :'######::'##::::'##::::'###::::'##:::'##::::'###::::'##::: ##:
	{Y} '##... ##: ##:::: ##:::'## ##:::. ##:'##::::'## ##::: ###:: ##:
	{G}  ##:::..:: ##:::: ##::'##:. ##:::. ####::::'##:. ##:: ####: ##:
	{G} . ######:: #########:'##:::. ##:::. ##::::'##:::. ##: ## ## ##:
	{M} :..... ##: ##.... ##: #########:::: ##:::: #########: ##. ####:
	{M} '##::: ##: ##:::: ##: ##.... ##:::: ##:::: ##.... ##: ##:. ###:
	{C} . ######:: ##:::: ##: ##:::: ##:::: ##:::: ##:::: ##: ##::. ##:
	{C} :......:::..:::::..::..:::::..:::::..:::::..:::::..::..::::..::
							 	
		       {U}{Y}~ {G}User Grabber {M}- {G}By .::Shayan::. {Y}~{UR}\n\n'''.format(Y=YELLOW,M=MAGENTA,G=GREEN,GR=GRAY,C=CYAN,U=UNDERLINE,UR=RUNDERLINE)
	for Line in Logo.splitlines():
		time.sleep(0.05)
		print(Line)

def Clear():
	if os.name == 'nt':
		os.system('cls')
		os.system('title User Grabber - By .::Shayan::.')
	else:
		os.system('clear')

def Login(user,pas):
	payload = {
		'username': user,
		'password': pas
	}
	header,shit = login_headers()
	r = requests.post('https://www.instagram.com/accounts/login/ajax/',headers=header,data=payload)
	jr = json.loads(r.text)['authenticated']
	if str(jr) == 'False' or jr == False:
		return False
	else:
		return True

def login_headers():
	r = requests.get('https://www.instagram.com/accounts/login/').text
	r2 = requests.get('https://www.instagram.com/static/bundles/es6/ConsumerLibCommons.js/759be62fac48.js').text
	mid = requests.get('https://www.instagram.com/web/__mid/').text
	csrf = re.findall('{"csrf_token":"(.*)","viewer":', r)[0]
	app_id = re.findall("',e.instagramWebFBAppId='(.*)',e.instagramWebDesktopFBAppId='", r2)[0]
	ajax = re.findall('},"rollout_hash":"(.*)","bundle_variant":"', r)[0]
	header = {
		'accept': '*/*',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.9',
		'content-type': 'application/x-www-form-urlencoded',
		'cookie': 'ig_cb=1; csrftoken='+csrf+'; rur=FTW; mid='+mid,
		'origin': 'https://www.instagram.com',
		'referer': 'https://www.instagram.com/accounts/login/',
		'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36',
		'x-csrftoken': csrf,
		'x-ig-app-id': app_id,
		'x-instagram-ajax': ajax,
		'x-requested-with': 'XMLHttpRequest'
	}
	shit = re.findall("',e.instagramWebDesktopFBAppId='(.*)',e.igLiteAppId='", r2)[0]
	return header,shit

def userid(username):
	r =requests.get('https://instagram.com/'+username).text
	reg = re.findall(',"id":"(.*)","is_business_account":', r)[0]
	return reg

def Followers(target,username,password):
	print(YELLOW+'\n ['+MAGENTA+'*'+YELLOW+']'+GREEN+'Grabbing Followers From '+target+'....\n\n')
	payload = {
		'username': username,
		'password': password
	}
	header,shit = login_headers()
	r = requests.post('https://www.instagram.com/accounts/login/ajax/',headers=header,data=payload)
	counts = 0
	header2 = {
		'Host': 'www.instagram.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
		'Accept': '*/*',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate, br',
		'X-IG-App-ID': shit,
		'X-Requested-With': 'XMLHttpRequest',
		'Connection': 'keep-alive',
		'Referer': 'https://www.instagram.com/'+target+'/followers/',
		'TE': 'Trailers'
	}
	aaaaaa = 0
	idtar = userid(target)
	r2 = requests.get('https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"'+str(idtar)+'","include_reel":true,"fetch_mutual":true,"first":50}',headers=header2,cookies=r.cookies)
	while True:
		if '"has_next_page":false,' in r2.text:
			try:
				reg = json.loads(r2.text)['data']['user']['edge_followed_by']['edges']
				for iu in reg:
					counts += 1
					print(YELLOW+'  ['+MAGENTA+str(counts)+YELLOW+']'+GREEN+str(iu['node']['username']))
					open('Followers['+target+'].txt','a').write(iu['node']['username']+'\n')
				print(YELLOW+'\n\n ['+MAGENTA+'!'+YELLOW+']'+GREEN+'Finished.')					
				input('{Y}  [{M}!{Y}]{G}Press `{B}Enter{G}` To Continue...'.format(Y=YELLOW,M=MAGENTA,G=GREEN,B=BLUE))
				break
			except KeyboardInterrupt:
				print(YELLOW+'\n\n ['+MAGENTA+'!'+YELLOW+']'+GREEN+'Finished.')					
				input('{Y}  [{M}!{Y}]{G}Press `{B}Enter{G}` To Continue...'.format(Y=YELLOW,M=MAGENTA,G=GREEN,B=BLUE))
				break
		else:
			if aaaaaa != 0:
				try:
					end = re.findall(',"end_cursor":"(.*)"},"edges":', r2.text)
					r2 = requests.get('https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"'+str(idtar)+'","include_reel":true,"fetch_mutual":true,"first":50,"after":"'+end[0]+'"}',headers=header2,cookies=r.cookies)
					reg = json.loads(r2.text)['data']['user']['edge_followed_by']['edges']
					for iu in reg:
						counts += 1
						print(YELLOW+' ['+MAGENTA+str(counts)+YELLOW+']'+GREEN+str(iu['node']['username']))					
						open('Followers['+target+'].txt','a').write(iu['node']['username']+'\n')
				except KeyboardInterrupt:
					print(YELLOW+'\n\n ['+MAGENTA+'!'+YELLOW+']'+GREEN+'Finished.')					
					input('{Y}  [{M}!{Y}]{G}Press `{B}Enter{G}` To Continue...'.format(Y=YELLOW,M=MAGENTA,G=GREEN,B=BLUE))
					break
			else:
				try:
					reg = json.loads(r2.text)['data']['user']['edge_followed_by']['edges']
					for iu in reg:
						counts += 1
						print(YELLOW+' ['+MAGENTA+str(counts)+YELLOW+']'+GREEN+str(iu['node']['username']))
						open('Followers['+target+'].txt','a').write(iu['node']['username']+'\n')
				except KeyboardInterrupt:
					print(YELLOW+'\n\n ['+MAGENTA+'!'+YELLOW+']'+GREEN+'Finished.')					
					input('{Y}  [{M}!{Y}]{G}Press `{B}Enter{G}` To Continue...'.format(Y=YELLOW,M=MAGENTA,G=GREEN,B=BLUE))
					break
				aaaaaa += 1

def Following(target,username,password):
	print(YELLOW+'\n ['+MAGENTA+'*'+YELLOW+']'+GREEN+'Grabbing Following From '+target+'....\n\n')
	payload = {
		'username': username,
		'password': password
	}
	header,shit = login_headers()
	r = requests.post('https://www.instagram.com/accounts/login/ajax/',headers=header,data=payload)
	counts = 0
	header2 = {
		'Host': 'www.instagram.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
		'Accept': '*/*',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate, br',
		'X-IG-App-ID': shit,
		'X-Requested-With': 'XMLHttpRequest',
		'Connection': 'keep-alive',
		'Referer': 'https://www.instagram.com/'+target+'/following/',
		'TE': 'Trailers'
	}
	aaaaaa = 0
	idtar = userid(target)
	r2 = requests.get('https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={"id":"'+str(idtar)+'","include_reel":true,"fetch_mutual":false,"first":50}',headers=header2,cookies=r.cookies)
	while True:
		if '"has_next_page":false,' in r2.text:
			try:
				reg = json.loads(r2.text)['data']['user']['edge_follow']['edges']
				for iu in reg:
					counts += 1
					print(YELLOW+'  ['+MAGENTA+str(counts)+YELLOW+']'+GREEN+str(iu['node']['username']))
					open('Following['+target+'].txt','a').write(iu['node']['username']+'\n')
				print(YELLOW+'\n\n ['+MAGENTA+'!'+YELLOW+']'+GREEN+'Finished.')					
				input('{Y}  [{M}!{Y}]{G}Press `{B}Enter{G}` To Continue...'.format(Y=YELLOW,M=MAGENTA,G=GREEN,B=BLUE))
				break
			except KeyboardInterrupt:
				print(YELLOW+'\n\n ['+MAGENTA+'!'+YELLOW+']'+GREEN+'Finished.')					
				input('{Y}  [{M}!{Y}]{G}Press `{B}Enter{G}` To Continue...'.format(Y=YELLOW,M=MAGENTA,G=GREEN,B=BLUE))
				break
		else:
			if aaaaaa != 0:
				try:
					end = re.findall(',"end_cursor":"(.*)"},"edges":', r2.text)
					r2 = requests.get('https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={"id":"'+str(idtar)+'","include_reel":true,"fetch_mutual":false,"first":50,"after":"'+end[0]+'"}',headers=header2,cookies=r.cookies)
					reg = json.loads(r2.text)['data']['user']['edge_follow']['edges']
					for iu in reg:
						counts += 1
						print(YELLOW+' ['+MAGENTA+str(counts)+YELLOW+']'+GREEN+str(iu['node']['username']))					
						open('Following['+target+'].txt','a').write(iu['node']['username']+'\n')
				except KeyboardInterrupt:
					print(YELLOW+'\n\n ['+MAGENTA+'!'+YELLOW+']'+GREEN+'Finished.')					
					input('{Y}  [{M}!{Y}]{G}Press `{B}Enter{G}` To Continue...'.format(Y=YELLOW,M=MAGENTA,G=GREEN,B=BLUE))
					break
			else:
				try:
					reg = json.loads(r2.text)['data']['user']['edge_follow']['edges']
					for iu in reg:
						counts += 1
						print(YELLOW+' ['+MAGENTA+str(counts)+YELLOW+']'+GREEN+str(iu['node']['username']))
						open('Following['+target+'].txt','a').write(iu['node']['username']+'\n')
				except KeyboardInterrupt:
					print(YELLOW+'\n\n ['+MAGENTA+'!'+YELLOW+']'+GREEN+'Finished.')					
					input('{Y}  [{M}!{Y}]{G}Press `{B}Enter{G}` To Continue...'.format(Y=YELLOW,M=MAGENTA,G=GREEN,B=BLUE))
					break
				aaaaaa += 1

def Main():
	Clear()
	Print_Logo()
	print(YELLOW+' ['+MAGENTA+'*'+YELLOW+']'+GREEN+'Enter Your Username')
	user = input(YELLOW+'  > '+GREEN)
	print(YELLOW+'\n ['+MAGENTA+'*'+YELLOW+']'+GREEN+'Enter Your Password')
	paas = input(YELLOW+'  > '+GREEN)
	log = Login(user, paas)
	if not log is True:
		input(YELLOW+'\n ['+MAGENTA+'!'+YELLOW+']'+GREEN+'Username Or/And Password Is Wrong.')
		Main()
	print(YELLOW+'\n ['+MAGENTA+'*'+YELLOW+']'+GREEN+'Enter Target Page For Grab')
	target = input(YELLOW+'  > '+GREEN)
	print(YELLOW+'\n ['+MAGENTA+'*'+YELLOW+']'+GREEN+'Grab From:')
	print(YELLOW+'  ['+MAGENTA+'1'+YELLOW+']'+GREEN+'Followers')
	print(YELLOW+'  ['+MAGENTA+'2'+YELLOW+']'+GREEN+'Following')
	typ = input(YELLOW+'  > '+GREEN)
	if typ == '1':
		Clear()
		Print_Logo()
		Followers(target,user,paas)
	elif typ == '2':
		Clear()
		Print_Logo()
		Following(target,user,paas)
	else:
		Main()

while True:
	Main()