# /usr/bin/python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import os
import urllib

version = 'REV 2' #Global version number

config_path = os.path.expanduser('~') + '/.pitube'
config_file = config_path + '/pitube.cfg'

def load_config():
	'''Try to load the config-file from [~/.pitube].
	
		If not possible create a new file at this possition.'''
	
	if not os.path.exists(config_path):
		os.makedirs(config_path)
		print 'Made directory'
		
	HDMI_audio_mode = False
	max_quality = 18
		
	if os.path.exists(config_file):
	
		f = file(config_file, 'r')
		while True:
			line = f.readline()
			
			if len(line) == 0:
				break
			
			exec(line)
		
		print 'Written Config-File'

	else:
		f =	file(config_file, 'w')
		write_string = '#Audio-Output over HDMI\nHDMI_audio_mode = True\n#Max. Video Quality. Visit "http://en.wikipedia.org/wiki/Youtube#Quality_and_codecs" for more infos.\nmax_quality = 18'
		f.write(write_string)
		print 'Written Config-File'
	f.close()
	
	configs = {'HDMI' : HDMI_audio_mode , 'QUALITY' : max_quality}
	
	return configs

def search_input():
	'''Empties the screen and take a string to search for, returns the Youtube-URL for the results.'''
	
	for i in range (0, 90):
		print ''
		
	print 'PiTUBE - YouTube-Client for the Raspberry Pi				V - %s' % (version)
	
	for i in range (0,9):
		print ''
		
	user_input = raw_input('Search: ')
	
	user_input = user_input.lower()
	
	user_input = str.replace(user_input, ' ' , '+')
	
	youtube_url = 'https://www.youtube.com/results?search_query=' + user_input

	return youtube_url
	
def read_urls(query, main_search = False):
	'''Take a string fron search_input() and returns a Dictionary with URLs, Names and lengths of the videos.
	
		btw this clears the screan and prints "Searching..."'''
	for i in range (0,90):
		print ''
	
	print 'Searching...'
	
	site = urllib.urlopen(query)
	contend = site.read()
	site.close()
	soup = BeautifulSoup(contend)
	
	links = []
	length =[]
	names = []
	
	number = 0
	
	for j in soup.findAll('a', href = True):
		
		check_vid = j['href'].find('/watch?v=') #if this element is a video-url check_vid should be != -1
		check_list = j['href'].find('&list=') # if this link is no playlist check_list should be == -1
		check_comment = j.text.find('http://www.youtube.com/watch?v=') # if the link isnt part of a comment check_comment schould be == -1
		if main_search == True:
			if check_vid != -1 and check_list == -1 and check_comment == -1 and number == 0:
					length.append(j.text)
					links.append('http://www.youtube.com' + j['href'])
					number = 1
			elif check_vid != -1 and check_list == -1 and check_comment == -1 and number == 1:
					names.append(j.text)
					number = 0
		else:
			if check_vid != -1 and check_list == -1 and check_comment == -1:
				names.append(j.text)
				links.append('http://www.youtube.com' + j['href'])
	result = {}
			
	result['URL'] = links[:]
	result['Name'] = names[:]
	result['Length'] = length[:]
		
	return result

def print_results(results, configs, main_search = False):
	
	'''Print the results and takes input from user.'''
	
	running = True
	vid_num = 0
	user_input = ''
	
	while running:
		
		for i in range (0,90):
			print ''
		
		if main_search == False:
			print 'Recommented Videos:'
			
		print 'Video %d of %d' % (vid_num + 1, len(results['URL'])-1)
		
		for i in range (0,6):
			print ''
		
		print results['Name'][vid_num].encode('utf8')
		print ''
		
		if main_search == True:
			print 'Video length:' , results['Length'][vid_num]
		else:
			print ''
		
		for i in range (0,6):
			print ''
			
		print '[n] Next Video [p] Previous Video [w] Watch Video [s] New Search [r] Recommented Videos [q] Quit'
		
		user_input = raw_input()
		
		if user_input.lower() == 'n':
			
			vid_num += 1
			
			if vid_num == len(results['URL'])-1:
				
				vid_num = 0
		
		if user_input.lower() == 'p':
			
			vid_num -= 1
			
			if vid_num < 0:
				
				vid_num = len(results['URL'])-2
				
		if user_input.lower() == 'w':
			
			for i in range (0,90):
				print ''
			
			print 'Connecting to Video... Please hold on.'
			
			youtubedl_command = 'youtube-dl --max-quality=' + str(configs['QUALITY']) + ' -g ' + results['URL'][vid_num]
			
			if configs['HDMI'] == False:
				hdmi = ' '
			else:
				hdmi = ' -o hdmi '
				
			player_command = 'omxplayer' + hdmi + '$(' + youtubedl_command + ') >> /dev/null'
			#player_command = 'mplayer -fs $(' + youtubedl_command + ') >> /dev/null'
			#^^^ This line above was just added to test this script on a Linux-PC 
			os.system(player_command)
			
		if user_input.lower() == 's':
			
			running = False
			print_results(read_urls(search_input(), True), load_config(), True)
		
		if user_input.lower() == 'r':
			
			running = False
			print_results(read_urls(results['URL'][vid_num]), load_config())
		
		if user_input.lower() == 'q':
			
			for i in range (0,90):
				print ''
			
			running = False

print_results(read_urls(search_input(), True), load_config(), True)
