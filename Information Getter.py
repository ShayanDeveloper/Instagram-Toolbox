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
							 	
		     {U}{Y}~ {G}Information Getter {M}- {G}By .::Shayan::. {Y}~{UR}'''.format(Y=YELLOW,M=MAGENTA,G=GREEN,GR=GRAY,C=CYAN,U=UNDERLINE,UR=RUNDERLINE)
	for Line in Logo.splitlines():
		time.sleep(0.05)
		print(Line)

def Clear():
	if os.name == 'nt':
		os.system('cls')
		os.system('title User Grabber - By .::Shayan::.')
	else:
		os.system('clear')

def short(link):
    r = requests.get('http://api.yon.ir/?url='+link).text
    js = json.loads(r)['output']
    return 'http://yon.ir/'+str(js)

def Decoder(txt):
    a = '{"a":"'+txt+'"}'
    return str(json.loads(a)['a'])

def Get(user):
    ret = {}
    r = requests.get('https://instagram.com/'+user).text
    All = re.findall('<meta property="og:description" content="(.*) Followers, (.*) Following, (.*) Posts',r)
    Username = RED+str(user)
    ret[YELLOW+'['+MAGENTA+'#'+YELLOW+']'+GREEN+'Username'+BLUE+': '] = Username
    follower = re.findall('"edge_followed_by":{"count":(.*)},',r)
    if 'k' in str(All[0][0]) or 'm' in str(All[0][0]):
        Followers = RED+str(All[0][0])+BLUE+' - '+RED+str(follower[0].split('}')[0])
    else:
        Followers = RED+str(All[0][0])
    ret[YELLOW+'['+MAGENTA+'#'+YELLOW+']'+GREEN+'Followers'+BLUE+': '] = Followers
    followin = re.findall(',"edge_follow":{"count":(.*)},"',r)
    if 'k' in str(All[0][1]) or 'm' in str(All[0][1]):
        Following = RED+str(All[0][1])+BLUE+' - '+RED+str(followin[0])
    else:
        Following = RED+str(All[0][1])
    ret[YELLOW+'['+MAGENTA+'#'+YELLOW+']'+GREEN+'Following'+BLUE+': '] = Following
    Posts = ''
    if 'k' in str(All[0][2]) or 'm' in str(All[0][2]):
        post = re.findall(',"edge_owner_to_timeline_media":{"count":(.*),"',r)
        Posts = RED+str(All[0][2])+BLUE+' - '+RED+str(post[0])
    else:
        Posts = RED+str(All[0][2])
    ret[YELLOW+'['+MAGENTA+'#'+YELLOW+']'+GREEN+'Posts'+BLUE+': '] = Posts
    shit = {}
    shit['t'] = str(re.findall('","@type":"(.*)","name":"',r)[0]) if '","@type":"' in r else '-'
    shit['n'] = str(re.findall(',"full_name":"(.*)","has_channel":',r)[0])
    shit['d'] = str(re.findall(',"graphql":{"user":{"biography":"(.*)","blocked_by_viewer":',r)[0])
    shit['u'] = str(re.findall(',"external_url":"(.*)","external_url_linkshimmed":"',r)[0])
    al = json.loads(json.dumps(shit))
    Type = RED+str(al['t'])
    ret[YELLOW+'['+MAGENTA+'#'+YELLOW+']'+GREEN+'Type'+BLUE+': '] = Type
    Name = RED+Decoder(str(al['n']))
    ret[YELLOW+'['+MAGENTA+'#'+YELLOW+']'+GREEN+'Name'+BLUE+': '] = Name
    Des = RED+Decoder(str(al['d']))
    ret[YELLOW+'['+MAGENTA+'#'+YELLOW+']'+GREEN+'Description'+BLUE+': '] = Des
    Url = RED+Decoder(str(al['u']).split('"')[0])
    ret[YELLOW+'['+MAGENTA+'#'+YELLOW+']'+GREEN+'Url'+BLUE+': '] = Url
    User_id = RED+str(re.findall('"profilePage_(.*)"',r)[0]).split('"')[0]
    ret[YELLOW+'['+MAGENTA+'#'+YELLOW+']'+GREEN+'User ID'+BLUE+': '] = User_id
    All3 = re.findall(
        '"is_business_account":(.*),"is_joined_recently":(.*),"business_category_name":(.*),"is_private":(.*),"is_verified":(.*),',
        r
    )
    Business_Account = RED+str(All3[0][0]).replace('false','False').replace('true','True')
    ret[YELLOW+'['+MAGENTA+'#'+YELLOW+']'+GREEN+'Business Account'+BLUE+': '] = Business_Account
    Joined_Recently = RED+str(All3[0][1]).replace('false','False').replace('true','True')
    ret[YELLOW+'['+MAGENTA+'#'+YELLOW+']'+GREEN+'Joined Recently'+BLUE+': '] = Joined_Recently
    Private = RED+str(All3[0][3]).replace('false','False').replace('true','True')
    ret[YELLOW+'['+MAGENTA+'#'+YELLOW+']'+GREEN+'Private Account'+BLUE+': '] = Private
    Verified = RED+str(All3[0][4]).replace('false','False').replace('true','True').split(',')[0]
    ret[YELLOW+'['+MAGENTA+'#'+YELLOW+']'+GREEN+'Verified'+BLUE+': '] = Verified
    Pic = RED+short(str(re.findall('<meta property="og:image" content="(.*)" />',r)[0]))
    ret[YELLOW+'['+MAGENTA+'#'+YELLOW+']'+GREEN+'Picture Url'+BLUE+': '] = Pic
    return ret

def Main():
	Clear()
	Print_Logo()
	print(YELLOW+' ['+MAGENTA+'*'+YELLOW+']'+GREEN+'Enter Target Username')
	user = input(YELLOW+'  > '+GREEN)
	Clear()
	Print_Logo()
	print('\n')
	print(YELLOW+'\n  ['+MAGENTA+'+'+YELLOW+']'+GREEN+'Getting Informations....\n\n')
	info = Get(user)
	for l in info:
		print('    '+l+info[l])
	print(YELLOW+'\n\n ['+MAGENTA+'!'+YELLOW+']'+GREEN+'Finished.')					
	input('{Y}  [{M}!{Y}]{G}Press `{B}Enter{G}` To Continue...'.format(Y=YELLOW,M=MAGENTA,G=GREEN,B=BLUE))

while True:
	Main()