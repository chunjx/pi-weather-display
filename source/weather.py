#!/usr/bin/env python
import sys, json, urllib, time, io
import pygame 
from pygame.locals import *

#Initialize variables
quit = False

#Get API Key
apikey_data = json.loads(open('config.json').read())
api_key = apikey_data["api-key"]

def getSwipeType():
	x,y=pygame.mouse.get_rel()
	if abs(x)<=minSwipe:
		if abs(y)<=minSwipe:
			if abs(x) < maxClick and abs(y)< maxClick:
				return 0
			else:
				return -1
		elif y>minSwipe:
			return 3
		elif y<-minSwipe:
			return 4
	elif abs(y)<=minSwipe:
		if x>minSwipe:
			return 1
		elif x<-minSwipe:
			return 2
	return 0


#Initialize Screen
pygame.init()
screen = pygame.display.set_mode((480, 320))
pygame.display.set_caption('Weather Station')

#Fill Background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

#Set font
base_font = pygame.font.Font(None, 36)
ctemp_font = pygame.font.Font(None, 48)

#Display city
def getcity():
    city = base_font.render("Deerfield", 1, (10, 10, 10))
    citypos = city.get_rect()
    citypos.centerx = background.get_rect().centerx*1.7
    citypos.centery = background.get_rect().centery/4
    background.blit(city, citypos)

#Display time
def gettime():
    currenttime = time.strftime("%I:%M %p")
    clock = base_font.render(currenttime, 1, (10, 10, 10))
    clockpos = clock.get_rect()
    clockpos.centerx = background.get_rect().centerx/3.9
    clockpos.centery = background.get_rect().centery/4
    background.blit(clock, clockpos)


#Get current conditions
def getcurrentconditionsdata():
    #Call Weather Underground conditions API
    conditionsurl = 'http://api.wunderground.com/api/'+api_key+'/conditions/q/zmw:60015.1.99999.json'
    wu = urllib.urlopen(conditionsurl)
    data = wu.read()
    #print 'Retrieved', len(data), 'characters'
    
    #Load JSON data from API call
    #try: js = json.loads(open('weathersample.json').read())
    try: js = json.loads(str(data))
    except: js = None
    if 'response' not in js: #or js['response'] != OK:
        print '==== Failure to Retrieve ===='  
    return js


def displayweather(jsondata):
    #Read weather condition
    weather_data = jsondata["current_observation"]["weather"]  
    weather = base_font.render(weather_data, 1, (10, 10, 10))
    weatherpos = weather.get_rect()
    weatherpos.centerx = background.get_rect().centerx
    weatherpos.centery = background.get_rect().centery-20
    background.blit(weather, weatherpos)

    #Display current weather icon
    icon_url = jsondata["current_observation"]["icon_url"]
    icon_str = urllib.urlopen(icon_url).read()
    icon_file = io.BytesIO(icon_str)
    icon_image = pygame.image.load(icon_file)
    icon_image = pygame.transform.scale(icon_image, (100,100))
    iconpos = icon_image.get_rect()
    iconpos.centerx = background.get_rect().centerx
    iconpos.centery = background.get_rect().centery-60
    background.blit(icon_image, iconpos)

    #Display current temp
    temp_data = str(jsondata["current_observation"]["temp_f"])+unichr(176)
    temp = ctemp_font.render(temp_data, 1, (10,10,10))
    temp_pos = temp.get_rect()
    temp_pos.centerx = background.get_rect().centerx/4
    temp_pos.centery = background.get_rect().centery
    background.blit(temp, temp_pos)


def getforecastdata():
    #Call Weather Underground forecast API
    forecasturl = 'http://api.wunderground.com/api/'+api_key+'/forecast/q/zmw:60015.1.99999.json'
    furl = urllib.urlopen(forecasturl)
    data = furl.read()
    #try: fjs = json.loads(open('forecast.json').read())
    try: fjs = json.loads(str(data))
    except: fjs = None
    if 'response' not in fjs: #or fjs['status'] != OK:
        print '==== Failure to Retrieve ===='
    return fjs
    
def displayforecast(f_json):
    #Read high temp and display the data
    hightemp_data = f_json["forecast"]["simpleforecast"]["forecastday"][0]["high"]["fahrenheit"]+unichr(176)
    hightemp = base_font.render(hightemp_data, 1, (10, 10, 10))
    hightemppos = hightemp.get_rect()
    hightemppos.centerx = background.get_rect().centerx*1.8
    hightemppos.centery = background.get_rect().centery/1.5
    background.blit(hightemp, hightemppos)
    #Read low temp and display the data
    lowtemp_data = f_json["forecast"]["simpleforecast"]["forecastday"][0]["low"]["fahrenheit"]+unichr(176)
    lowtemp = base_font.render(lowtemp_data, 1, (10, 10, 10))
    lowtemppos = lowtemp.get_rect()
    lowtemppos.centerx = background.get_rect().centerx*1.8
    lowtemppos.centery = background.get_rect().centery
    background.blit(lowtemp, lowtemppos) 

#Retrieve initial data 
jsoninfo = getcurrentconditionsdata()
jsonforecast = getforecastdata()

current_time = time.time()  

while not quit:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit = True

        # 'Q' to quit    
        if (event.type == pygame.KEYUP): 
            if (event.key == pygame.K_q):
                 quit = True

    gettime()
    getcity()
    displayweather(jsoninfo)
    displayforecast(jsonforecast)

    if time.time()-current_time > 30:
        print time.time()-current_time
        jsoninfo = getcurrentconditionsdata()
        jsonforecast = getforecastdata()
        current_time = time.time()

    screen.blit(background, (0, 0))
    pygame.display.flip()
    background.fill((250, 250, 250))

    