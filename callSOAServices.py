def callSOAService(message):
    if 'intents' in message:
        print 'you called SOA Service'
        for x in message['intents']:
            if x['intent'] == 'statement':
                print 'Intent statement is found'
                if 'output' in message:
                    print 'output is found'
                break
    return message        
