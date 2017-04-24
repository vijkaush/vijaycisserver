# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, logging, time
from os.path import join, dirname
from weblogger import addLogEntry
from checkDTMF import handleDTMFTimeout, DTMFwaitState
from voiceProxyUtilities import setEarlyReturn, inPollingState, startPolling, pollingTimeLeft, earlyReturn

import voiceProxySettings

logging_comp_name = 'checkGatewaySignal'

#------- Check Input From Gateway Methods -----------------


def signals(message):
	message = preCheckGatewaySignal(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'preCheckGatewaySignal -> Returning to Gateway', message)
		return message
	
	message = checkGatewaySignal(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'checkGatewaySignal -> Returning to Gateway', message)
		return message
	
	message = postCheckGatewaySignal(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'postCheckGatewaySignal -> Returning to Gateway', message)
		return message
	
	return message




def preCheckGatewaySignal(message):
	
	return message

def checkGatewaySignal(message):
	
	if check_cgwPostResponseTimeout(message):
		logging.debug("RespTimeout")
		if inPollingState(message):
			logging.info("in Polling State with RespTimeout Message")
			#message = startPolling(message)
			message = setEarlyReturn(message,'In Polling State and Gateway Signals ResTimeout -> Returning to Gateway')
			return message
		
		if DTMFwaitState(message):
			logging.info("Timeout while in DTMF WaitState")
			message = handleDTMFTimeout(message)
			message = setEarlyReturn(message,'Gateway Signals RespTimeout in DTMF Waitstate -> Returning to Gateway')
			return message

		
		message = setEarlyReturn(message,'Returning from RespTimeout')
		return message

	if check_cgwNoInputTurn(message) and inPollingState(message):
		logging.info("NoInputTurn")
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'Gateway Signals NoInputTurn and in Polling WaitState', message)
		time.sleep(pollingTimeLeft(message))
		return message
	
	if check_cgwHangUp(message):
		logging.info("Hangup")
		message = setEarlyReturn(message,'Gateway Signals Hangup -> Returning to Gateway')
		return message
		
	return message
	
	
def postCheckGatewaySignal(message):
	return message


#------ EndCheck Input From Gateway Methods ---------------






#--------------- Signals from the SIP Gateway --------------	
def check_cgwPostResponseTimeout(message):
	return check_cgwSignal(message,'cgwPostResponseTimeout')

def check_cgwNoInputTurn(message):
	return check_cgwSignalInString(message,'cgwNoInputTurn')

def check_cgwHangUp(message):
	return check_cgwSignal(message,'cgwHangUp')
	
def check_cgwSignal(message, signal):
	if 'input' in message:
		if 'text' in message['input']:
			if message['input']['text'] == signal:
				return True
	
	return False

def check_cgwSignalInString(message, signal):
	if 'input' in message:
		if 'text' in message['input']:
			if signal in message['input']['text']:
				return True
	
	return False
#------------- End Signals from Help Gateway -----------------


