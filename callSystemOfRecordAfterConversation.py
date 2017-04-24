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
    global accountNumber1,motherName1
    accountNumber1=None
    motherName1=None
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
                         
            if  accountNumber1 is not None:
                print("your account no is-->",accountNumber1);
                bankUrl = 'http://161.202.176.3:5000/api/alliance/info'
                #bankUrl =  bankUrl + '/'+ motherName1
                print 'Bank Url is '+' ' + bankUrl
                r = requests.get(bankUrl)
                results = r.json();
                print results['custname']
                print results['dob']
                soap_custName = results['custname']
                if soap_custName == accountNumber1:
                    print "account number match"
                    message['output']['text'][0] = 'your balance is' + ' ' + soap_custName + ' ' + 'dollars'
                    #message['context']['custname'] = soap_custName
                    message['context']['verified'] = 'yes'
                else:
                    print "Account number does not match"
                    message['output']['text'][0] = 'you input wrong account number.'
                    message['context']['verified'] = 'no'
                    
        #for x in message['intents']:
            #if x['intent'] == 'balance':
                #print 'Intent balance is found'
                #if 'accNumber' in message:
                    #print 'variable accountbal  is found'
                    #accountNumber1 = message['accNumber']
                    #if accountNumber1.strip():
                        #print accountNumber1
                        #r = requests.get('https://alliancebank.mybluemix.net/rbs/account/12345')
                    #results = r.json();
                    #print results['accbal']
                    #message['output']['text'][0] = 'your balance is' + ' ' + results['accbal']
                    
                #break
            
	return message

def postCallSystemOfRecordAfterConversation(message):
	return message

#------ End Check SOR After Conversation Methods ---------------