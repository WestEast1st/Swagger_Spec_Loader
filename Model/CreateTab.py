from burp import IBurpExtenderCallbacks

def sendToIntruder (callbacks, host, req, name) :
    IBurpExtenderCallbacks.sendToIntruder(callbacks,host,443,True,req)

def sendToRepeater (callbacks, host, req, name) :
    IBurpExtenderCallbacks.sendToRepeater(callbacks,host,443,True,req,name)
