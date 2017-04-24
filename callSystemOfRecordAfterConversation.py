# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, logging, time
from os.path import join, dirname
from weblogger import addLogEntry
import voiceProxySettings
from voiceProxyUtilities import setEarlyReturn, earlyReturn

logging_comp_name = "callSystemOfRecordAfterConversation"



#------- Check SOR After Conversation Methods -----------------
def callSORAfterConv(message):

	message = preCallSystemOfRecordAfterConversation(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'preCallSystemOfRecordAfterConversation -> Returning to Gateway', message)
		return message

	message = callSystemOfRecordAfterConversation(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'callSystemOfRecordAfterConversation -> Returning to Gateway', message)
		return message
		
	message = postCallSystemOfRecordAfterConversation(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'postCallSystemOfRecordAfterConversation -> Returning to Gateway', message)
		return message
		
	return message	

def preCallSystemOfRecordAfterConversation(message):
	return message

def callSystemOfRecordAfterConversation(message):
    global accountNumber1,motherName1,watsonDob
    accountNumber1=None
    motherName1=None
    watsonDob=None
    if 'intents' in message:
        print message
        print 'you called SOA Service'
        if 'context' in message:
            print 'context  is found'
            if 'accNumber' in message['context']:
                print message['context']['accNumber']
                accountNumber1 = message['context']['accNumber']
                accountNumber1 = accountNumber1.replace(" ","")
                del message['context']['accNumber'];
                
            if 'dob' in message['context']:
                print message['context']['dob']
                watsonDob = message['context']['dob']
                watsonDob = watsonDob.replace(" ","")
                del message['context']['dob']
                         
            if  accountNumber1 is not None:
                print("your account no is-->",accountNumber1);
                bankUrl = 'http://161.202.176.3:5000/api/alliance/info'
                #bankUrl =  bankUrl + '/'+ motherName1
                print 'Bank Url is '+' ' + bankUrl
                r = requests.get(bankUrl)
                results = r.json();
                print results['custname']
                soap_custName = results['custname']
                if soap_custName == accountNumber1:
                    print "account number match"
                    message['output']['text'][0] = 'Your balance is' + ' ' + soap_custName + ' ' + 'Would you like help with something else?'
                    #message['context']['custname'] = soap_custName
                    message['context']['verified'] = 'yes'
                else:
                    print "Account number does not match"
                    message['output']['text'][0] = 'I am sorry, I could not find your account number. Can you please try again?'
                    message['context']['verified'] = 'no'
                    
            if  watsonDob is not None:
                print("your entered dob is-->",watsonDob);
                bankUrl = 'http://161.202.176.3:5000/api/alliance/info'
                #bankUrl =  bankUrl + '/'+ motherName1
                print 'Bank Url is '+' ' + bankUrl
                r = requests.get(bankUrl)
                results = r.json();
                print results['dob']
                soap_dob = results['dob']
                if soap_dob == watsonDob:
                    print "DOB match"
                    message['output']['text'][0] = 'thank you, your date of birth' + ' '  + soap_dob + ' ' +  'is correct. Would you like your statement for the last month or last two months?'
                    #message['context']['custname'] = soap_custName
                else:
                    print "DOB does not match"
                    message['output']['text'][0] = 'I am sorry your date of birth does not match our records. can you please try again?'
            
	return message

def postCallSystemOfRecordAfterConversation(message):
	return message

#------ End Check SOR After Conversation Methods ---------------