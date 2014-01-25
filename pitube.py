# /usr/bin/python
# -*- coding: utf-8 -*-
############################################Import##################################
from BeautifulSoup import BeautifulSoup
import os
import urllib
import tty
import termios
import sys
import cPickle
import time
###########################################Classes##################################
class yt_options():
	
	def __init__(self):
		
		config_path = os.path.expanduser('~') + '/.pitube'
		config_file = config_path + '/pitube.cfg'
		
		if not os.path.exists(config_path):
			os.makedirs(config_path)
			print 'Made directory'
			
		HDMI_audio_mode = True
		max_quality = 18
		
		if os.path.exists(config_file):
	
			f = file(config_file, 'r')
			while True:
				line = f.readline()
			
				if len(line) == 0:
					break
			
				exec(line)

		else:
			f =	file(config_file, 'w')
			write_string = '#Audio-Output over HDMI\nHDMI_audio_mode = True\n#Max. Video Quality. Visit "http://en.wikipedia.org/wiki/Youtube#Quality_and_codecs" for more infos.\nmax_quality = 18'
			f.write(write_string)
			print 'Written Config-File'
			
		f.close()
		if HDMI_audio_mode == True:	
			self.HDMI = ' -o hdmi '
		else:
			self.HDMI = ' '
		self.quality = max_quality
		
	def set_them(self):
		
		os.system('clear')
		looping = True
		hdmi = True
		quality = 18
		
		while looping:
			print 'Play audio over HDMI? (y/n)'
			key = getkey()
			
			if key.lower()=='y':
				hdmi = True
				looping = False
			elif key.lower()=='n':
				hdmi = False
				looping = False
				
		
		looping =  True
		
		while looping:
			print 'Maximum Quality. [h]igh [m]edium [l]ow'
			key = getkey()
			
			if key.lower()=='h':
				quality=22
				looping = False
			elif key.lower()=='m':
				quality=18
				looping = False
			elif key.lower()=='l':
				quality=17
				looping = False
				
		path = os.path.expanduser('~') + '/.pitube/pitube.cfg'
			
		try:
			os.remove(path)
		except:
			None
		
		f =	file(path, 'w')
		write_string = '#Audio-Output over HDMI\nHDMI_audio_mode = %s\n#Max. Video Quality. Visit "http://en.wikipedia.org/wiki/Youtube#Quality_and_codecs" for more infos.\nmax_quality = %s' % (hdmi,quality)
		f.write(write_string)
		print 'Written Config-File'
		
		self.__init__
		
		print 'Done...'
		time.sleep(1)

class yt_video():
	
	def __init__(self,name='NA',link='NA',length='NA'):
		
		self.name = name
		self.length = length
		self.url = link
		
	def play(self,options):
		
		youtubedl_command = 'youtube-dl --max-quality=' + str(options.quality) + ' -g ' + self.url
		player_command = 'omxplayer' + options.HDMI + '$(' + youtubedl_command + ') >> /dev/null'
		os.system(player_command)
		
	def save(self):
		
		path = os.path.expanduser('~') + '/.pitube/bookmark.data'
		
		save = [self.name,self.length,self.url]
		return save
		
	def load(self,save):
		
		self.name = save[0]
		self.length = save[1]
		self.url = save[2]
		

class yt_list():
	
		def __init__(self):
			
			self.vid_list = []
			self.url ='NA'
			self.query = ''
			
		def find_vids(self,query,page=1):
			
			self.query = query
			query = query.lower()
			query = str.replace(query, ' ' , '+')
			youtube_url = 'https://www.youtube.com/results?search_query=' + query + '&page=' + str(page)
			self.url = youtube_url
			
			self.get_data(True)
			
		def url_set(self,url):
			
			self.url = url
	
	
		def get_data(self,main_search=False):
			
			self.vid_list = []
			
			site = urllib.urlopen(self.url)
			contend = site.read()
			site.close()
			soup = BeautifulSoup(contend)
			
			number = 0
			
			urls = []
			names = []
			lengths = []
			
			for j in soup.findAll('a', href = True):
				
				check_vid = j['href'].find('/watch?v=') #if this element is a video-url check_vid should be != -1
				check_list = j['href'].find('&list=') # if this link is no playlist check_list should be == -1
				check_comment = j.text.find('http://www.youtube.com/watch?v=') # if the link isnt part of a comment check_comment schould be == -1
				
	
				
				if main_search == True:
				
					if check_vid != -1 and check_list == -1 and check_comment == -1 and number == 0:
						lengths.append(j.text)
						urls.append('http://www.youtube.com' + j['href'])
						number = 1
						
					elif check_vid != -1 and check_list == -1 and check_comment == -1 and number == 1:
						names.append(j.text)
						number = 0
				else:
					if check_vid != -1 and check_list == -1 and check_comment == -1:
						names.append(j.text)
						urls.append('http://www.youtube.com' + j['href'])
						lengths.append('NA')					
			
			for k in range (0, len(names)-1):
						
				vid = yt_video(names[k],urls[k],lengths[k])
				
				if vid.name != 'NA':
					self.vid_list.append(vid)
					
		def save(self, num):
			
			path = os.path.expanduser('~') + '/.pitube/bookmark.data'
			
			try:
				f = file(path,'r')
				sav_list = cPickle.load(f)
				f.close()
			except:
				sav_list = []
				print 'Made Bookmark...'
				time.sleep(1)
			
			sav = self.vid_list[num].save()
			sav_list.append(sav)
				
			f = file(path,'w')
			cPickle.dump(sav_list,f)
			f.close()
			
		def load(self):
			
			path = os.path.expanduser('~') + '/.pitube/bookmark.data'
			
			f = file(path, 'r')
			load_list = cPickle.load(f)
			f.close()
			
			for a in load_list:
				b = yt_video()
				b.load(a)
				self.vid_list.append(b)
			
###################################Functions##########################################

def getkey():
	
	a = sys.stdin.fileno()
	old = termios.tcgetattr(a)
	
	try:
		tty.setraw(a)
		char = sys.stdin.read(1)
	finally:
		termios.tcsetattr(a, termios.TCSADRAIN, old)
		
	return char
					
def user_input():
		
	user_input = raw_input('Search: ')
	print 'Searching... Please hold on.'
	return  user_input

def print_results(vid_list, search_title = 'Video Search'):
	
	'''Print the results and takes input from user.'''
	
	options = yt_options()
	
	running = True
	vid_num = 0
	user_input = ''
	page = 1
	
	while running:
		
		os.system('clear')
		
		
		print search_title , '(Page: ' + str(page) +')'
			
		print 'Video %d of %d' % (vid_num +1, len(vid_list.vid_list))
		
		for i in range (0,6):
			print ''
		
		print vid_list.vid_list[vid_num].name.encode('utf8')
		print ''
		
		print 'Video length:' , vid_list.vid_list[vid_num].length.encode('utf8')
		
		print 'Video URL:' , vid_list.vid_list[vid_num].url.encode('utf8')
		
		for i in range (0,6):
			print ''
			
		print '[n] Next Video [p] Previous Video [u] Page Up [d] Page down'
		print '[w] Watch Video [s] New Search' 
		if search_title != 'Bookmarks':
			print '[r] Recommended Videos [b] Bookmark Video'
		else:
			print '[r] Recommended Videos [b] Remove bookmark'
		print '[q] Quit to title'
		
		user_input = getkey()
		
		if user_input.lower() == 'n':
			
			vid_num += 1
			
			if vid_num == len(vid_list.vid_list):
				
				vid_num = 0
		
		if user_input.lower() == 'p':
			
			vid_num -= 1
			
			if vid_num < 0:
				
				vid_num = len(vid_list.vid_list)-1
				
		if user_input.lower() == 'u':
			
			if search_title != 'Bookmarks': 
				page += 1
				vid_num = 0
				print 'Getting Page %d ... Please hold on.' % (page)
				vid_list.find_vids(vid_list.query, page)
				
			else:
				print 'Not here...'
				time.sleep(1)
		
		if user_input.lower() == 'd':
			
			if search_title != 'Bookmarks':
				if page > 1:
					page -= 1
					vid_num = 0
					print 'Getting Page %d ... Please hold on.' % (page)
					vid_list.find_vids(vid_list.query, page)
				
				else:
					print 'There are no negative Sites'
					
			else:
				print 'Not here...'
				time.sleep(1)
					
		if user_input.lower() == 'w':
			
			os.system('clear')
						
			print 'Connecting to Video... Please hold on.'
			
			vid_list.vid_list[vid_num].play(options)
			
		if user_input.lower() == 's':
			
			print ''
			q = raw_input('>>>New Search: ')
			print 'Searching... Please hold on'
			vid_list.find_vids(q)
		
		if user_input.lower() == 'r':
			
			print 'Getting recommended Videos...	Please hold on'
			vid_list.url_set(vid_list.vid_list[vid_num].url)
			vid_list.get_data(False)
		
		if user_input.lower() == 'q':
			
			os.system('clear')
			
			running = False
			
		if user_input.lower() == 'b':
			
			if search_title != 'Bookmarks':
			
				vid_list.save(vid_num)
				print 'Made bookmark...'
				time.sleep(1)
			
			else:
				
				print 'Really remove this bookmark?(y/n)'
				
				yn = getkey()
				
				if yn == 'y':
					
					print 'Removed bookmark...'
				
					path = os.path.expanduser('~') + '/.pitube/bookmark.data'
					try:
						os.remove(path)
					except:
						print 'Made new bookmark file...'
				
					vid_list.vid_list.pop(vid_num)
				
					for c in range (0,len(vid_list.vid_list)):
						vid_list.save(c)
				
					if len(vid_list.vid_list) == 0:
			
						running == False
						break 
					
					vid_num = 0
					
					time.sleep(1)
			
def main_menue(version):
		
	mainrun = True
		
	while mainrun:
			
		os.system('clear')
		
		print 'PiTUBE - YouTube-Client for the Raspberry Pi	[V: %s]' % (version)
		
		print '\n[1] Search videos\n\n[2] Show bookmarks\n\n[3] Configurations\n\n[4] Quit'
		
		uinput = getkey()
			
		if uinput == '1':
				
			a = yt_list()
			a.find_vids(user_input())
			print_results(a)
				
		if uinput == '2':
			
			path = os.path.expanduser('~') + '/.pitube/bookmark.data'
			
			if os.path.exists(path):
				
				b = yt_list()
				b.load()
				print_results(b,'Bookmarks')
				
			else:
				
				print 'No Bookmarks...'
				time.sleep(1)
			
		if uinput == '3':
			
			o = yt_options()
			o.set_them()
			
		if uinput == '4':
			os.system('clear')
			print 'You want to leave?\n\n[1] Back to shell\n\n[2] Shutdown\n\n[3] Do not leave'
			key=getkey()
			
			if key.lower()=='1':
				mainrun = False
				
			if key.lower()=='2':
				mainrun = False
				os.system('sudo shutdown -h now')
				
######################################Programm###########################################
version = 'Rev-3.1.0'

if __name__ == '__main__':
	main_menue(version)
