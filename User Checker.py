#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests, re, os, time, random, datetime, threading

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
header = {
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'en-US,en;q=0.9',
	'upgrade-insecure-requests': '1',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

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
							 	
		       {U}{Y}~ {G}User Checker {M}- {G}By .::Shayan::. {Y}~{UR}\n\n'''.format(Y=YELLOW,M=MAGENTA,G=GREEN,GR=GRAY,C=CYAN,U=UNDERLINE,UR=RUNDERLINE)
	for Line in Logo.splitlines():
		time.sleep(0.05)
		print(Line)

def Clear():
	if os.name == 'nt':
		os.system('cls')
		os.system('title User Grabber - By .::Shayan::.')
	else:
		os.system('clear')

def Check(username,less,more):
	try:
		r = requests.get('https://instagram.com/'+username,headers=header).text
		followers = int(re.findall(',"edge_followed_by":{"count":(.*)},"followed_by_viewer":', r)[0])
		following = int(re.findall(',"edge_follow":{"count":(.*)},"follows_viewer":', r)[0])
		if followers >= more and following <= less:
			print(YELLOW+' ['+MAGENTA+'+'+YELLOW+']'+GREEN+username+WHITE+' -> '+GREEN+'That\'s It !')
			print(YELLOW+'   ['+MAGENTA+'#'+YELLOW+']'+GREEN+'Followers'+WHITE+': '+GREEN+str(followers))
			print(YELLOW+'   ['+MAGENTA+'#'+YELLOW+']'+GREEN+'Following'+WHITE+': '+GREEN+str(following))
			open('Goods.txt','a').write(username+'\n')
		else:
			print(YELLOW+' ['+MAGENTA+'~'+YELLOW+']'+GREEN+username+WHITE+' ->'+YELLOW+' :((')
			print(YELLOW+'   ['+MAGENTA+'#'+YELLOW+']'+GREEN+'Followers'+WHITE+': '+YELLOW+str(followers))
			print(YELLOW+'   ['+MAGENTA+'#'+YELLOW+']'+GREEN+'Following'+WHITE+': '+YELLOW+str(following))
			open('Bads.txt','a').write(username+'\n')

	except:
		print(YELLOW+'  ['+MAGENTA+'-'+YELLOW+']'+GREEN+username+WHITE+' ->'+RED+' User Is Not Available!')	

def Main():
	Clear()
	Print_Logo()
	print(YELLOW+' ['+MAGENTA+'*'+YELLOW+']'+GREEN+'Enter Username List Path')
	userlist = input(YELLOW+'  > '+GREEN)
	userlist = open(userlist,'r').read().splitlines()
	print(YELLOW+'\n ['+MAGENTA+'*'+YELLOW+']'+GREEN+'Followers More Than')
	followers = int(input(YELLOW+'  > '+GREEN))
	print(YELLOW+'\n ['+MAGENTA+'*'+YELLOW+']'+GREEN+'Following Less Than')
	following = int(input(YELLOW+'  > '+GREEN))
	Clear()
	Print_Logo()
	print(YELLOW+'\n ['+MAGENTA+'!'+YELLOW+']'+GREEN+'Checking Users...')
	for u in userlist:
		Check(u,following,followers)
Main()