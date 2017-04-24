#####
import os, requests, json, string, datetime, logging, time
from os.path import join, dirname
import voiceProxySettings


MUSIC_HOLD_ENABLED = False
MUSIC_HOLD = "http://10.2.2.216:5000/static/hold_music_01.wav"




def earlyReturn(message):
	if 'cisContext' in message['context']:
		if 'earlyReturn' in message['context']['cisContext']:
			return message['context']['cisContext']['earlyReturn']
	
	return False;
	
def setEarlyReturn(message, logmessage):
	message['context']['cisContext']['earlyReturn'] = True
	message['context']['cisContext']['earlyReturnMsg'] = logmessage
	
	return message


def getCisAttribute(attrib, message):
	if attrib in message['context']['cisContext']:
		return message['context']['cisContext'][attrib]
	else:
		return None
		
def clearCisAttribute(attrib, message):
	del message['context']['cisContext'][attrib]
	return message

def removeEntities(message):
	if 'entities' in message:
		del message['entities']
	return message

def removeIntents(message):
	if 'intents' in message:
		del message['intents']
	return message
#-------------- Polling Helper Methods -----------------------

def inPollingState(message):
	if 'cisPolling' in message['context']['cisContext']:
		if message['context']['cisContext']['cisPolling']:
			logging.debug("In Polling State")
			return True

	return False

def pollingTimeLeft(message):
	if 'cisPollTimeStamp' in message['context']['cisContext']:
		ts  = message['context']['cisContext']['cisPollTimeStamp']
		now = time.time()
		if (now-ts) < voiceProxySettings.POLLING_SLEEP_TIME:
			return (voiceProxySettings.POLLING_SLEEP_TIME) - (now-ts)
		else:
			return 0
	return 0
	
def startPolling(message):
	message['context']['cgwForceNoInputTurn'] = 'Yes'
	message['context']['cisContext']['cisPollTimeStamp'] = time.time()
	message['context']['cisContext']['cisPolling'] = True
		
	if MUSIC_HOLD_ENABLED:
		message['context']['cgwMusicOnHoldURL'] = MUSIC_HOLD
	return message


	
def stopPolling(message):
	if 'context' in message:
		if 'cgwForceNoInputTurn' in message['context']:
			del message['context']['cgwForceNoInputTurn']
		if 'cgwPostResponseTimeout' in message['context']:
			del message['cgwPostResponseTimeout']
		if 'cisPollTimeStamp' in message['context']['cisContext']:
			message['context']['cisContext']['cisPollTimeStamp'] = 0.0
		if 'cisPolling' in message['context']['cisContext']:
			message['context']['cisContext']['cisPolling'] = False
			
	return message
	
#-------------- End Polling Helper Methods -------------------
	