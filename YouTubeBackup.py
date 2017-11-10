# -*- coding: utf-8 -*-

import os
import time
import pickle

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow



delayPeriod = 2 # Seconds


clientSecretsFile = "Google_secret.json"
scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
apiServiceName = 'youtube'
apiVersion = 'v3'


def get_authenticated_service():
	flow = InstalledAppFlow.from_client_secrets_file(clientSecretsFile, scopes)

	if os.path.isfile("Google_credentials.obj"):
		# Read the credentials back out
		file = open("Google_credentials.obj",'rb')
		credentials = pickle.load(file)
	else:
		# Request and save the credentials
		credentials = flow.run_console()
		file = open("Google_credentials.obj","wb")
		pickle.dump(credentials,file)

	file.close()

	return build(apiServiceName, apiVersion, credentials = credentials)

	
def subscriptions_list_my_subscriptions(client, **kwargs):

	response = client.subscriptions().list(
	**kwargs
	).execute()

	return response	
	
	
def playlists_list_mine(client, **kwargs):

	response = client.playlists().list(
	**kwargs
	).execute()

	return response
  
  
def playlist_items_list_by_playlist_id(client, **kwargs):

	response = client.playlistItems().list(
	**kwargs
	).execute()

	return response

	
# Used by playlist() to get the videos from each playlist
def playlist_Items(iL,maxR,filePIL,playList):

	# Write playlist name to file.
	filePIL.write(playList['items'][iL]['snippet']['title']+"\n")
	filePIL.write("-----------------------------"+"\n")
	
	firstPIL = 1
	playItemNum = 1

	while True:
		if firstPIL:	# First request
			playItemsList = playlist_items_list_by_playlist_id(client,
													part='snippet,contentDetails',
													maxResults=maxR,
													playlistId=playList['items'][iL]['id'])
			filePIL.write("Number of playlist items: "+str(playItemsList['pageInfo']['totalResults'])+"\n\n")
			firstPIL = 0
		else:	# Every other request
			playItemsList = playlist_items_list_by_playlist_id(client,
													part='snippet,contentDetails',
													maxResults=maxR,
													pageToken=PILnPToken,
													playlistId=playList['items'][iL]['id'])
	
		# Write playlist videos to file.
		for iPIL in range(0,len(playItemsList['items'])):
			filePIL.write(str(playItemNum)+":\t"+str(playItemsList['items'][iPIL]['snippet']['title'])+"\t"+"https://www.youtube.com/watch?v="+str(playItemsList['items'][iPIL]['snippet']['resourceId']['videoId'])+"\n")
			playItemNum += 1
		
		
		try:	# Is this the last request? Yes = continue. No = Make another request			
			PILnPToken = playItemsList['nextPageToken']
			time.sleep(delayPeriod) # Small delay to avoid suspension/ban *See note at the bottom.
		except BaseException as e:
			filePIL.write("\n\n\n")
			break
	
	return
	
	
# Backup the playlist of the channel to a csv file.
def playlist():

	maxR = 50 # Max number of results per request. 50 Max.
	firstPL = 1 # First run through flag.
	playNum = 1	 # Playlist count.
	
	print("Collecting playlists")
	print("--------------------")
	print(" ")
	
	filePL = open("YouTube Playlists.csv","w+", encoding='utf-8')
	filePL.write("Playlists"+"\n")
	filePL.write("-----------------------"+"\n")
	

	while True:
		if firstPL:	# First request
			playList = playlists_list_mine(client,
										part='snippet,contentDetails',
										maxResults=maxR,
										mine=True)
			filePL.write("Number of playlist: "+str(playList['pageInfo']['totalResults'])+"\n\n\n\n\n")
			firstPL = 0
		else:	# Every other request
			playList = playlists_list_mine(client,
										part='snippet,contentDetails',
										maxResults=maxR,
										pageToken=PLnPToken,
										mine=True)

		# Get the videos in each playlist
		for iPL in range(0,len(playList['items'])):
			playlist_Items(iPL,maxR,filePL,playList)		
			playNum += 1
		
		
		try:	# Is this the last request? Yes = continue. No = Make another request
			print("Playlists retrieved so far...",playNum)
			PLnPToken = playList['nextPageToken']
			time.sleep(delayPeriod) # Small delay to avoid suspension/ban *See note at the bottom.
		except BaseException as e:
			print("Playlists Complete")
			break

	filePL.close()
	
	return
	

# Backup the subscribed channels to a csv file.
def subscription():

	maxR = 50 # Max number of results per request. 50 Max.
	firstS = 1	# First run through flag.
	subRequest	= 1 # Request count.
	subNum = 1 # Subscription count.
	
	print("Collecting subscriptions")
	print("------------------------")
	print(" ")

	fileS = open("YouTube Subscriptions.csv","w+", encoding='utf-8')		
	fileS.write("Subscriptions"+"\n")
	fileS.write("-------------"+"\n")

	while True:
		if firstS:	# First request
			subList = subscriptions_list_my_subscriptions(client,
											part='snippet,contentDetails',
											maxResults=maxR,
											order='alphabetical',
											mine=True)
			fileS.write("Number of subscriptions: "+str(subList['pageInfo']['totalResults'])+"\n\n")
			firstS = 0
		else:	# Every other request
			subList = subscriptions_list_my_subscriptions(client,
											part='snippet,contentDetails',
											maxResults=maxR,
											pageToken=SnPToken,
											order='alphabetical',
											mine=True)	
			subRequest += 1
		
		# Write channel subscriptions to file.
		for iS in range(0,len(subList['items'])):		
			fileS.write(str(subNum)+":\t"+subList['items'][iS]['snippet']['title']+"\t"+"https://www.youtube.com/channel/"+subList['items'][iS]['snippet']['resourceId']['channelId']+"\n")
			subNum += 1
		
		try: # Is this the last request? Yes = continue. No = Make another request
			print("Subscriptions retrieved so far...",subNum)
			SnPToken = subList['nextPageToken']
			time.sleep(delayPeriod) # Small delay to avoid suspension/ban *See note at the bottom.
		except BaseException as e:
			print("Subscriptions Complete")
			print(" ")
			print(" ")
			break
	
	fileS.close() 
	
	return



  
if __name__ == '__main__':
	os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
	client = get_authenticated_service()
	

	subscription()	
	playlist()
	
	print("Done")
	
	
	
	# YouTube's ToS 4H 
	# "You agree not to use or launch any automated system, including without limitation, "robots," "spiders," or "offline readers," that accesses the Service in a manner that sends more request messages to the YouTube servers in a given period of time than a human can reasonably produce in the same period by using a conventional on-line web browser."
	#
	# This means that we can't do this as quickly as we can process the data. Google/YouTube.... really? Scared of a DDOS? So i've added a small delay between each request so that Google/YouTube doesn't suspend/ban the account.
	
	
	
	
	
	
	
	
	