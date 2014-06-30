import json
import Skype4Py
import web
import time
import re
import glob

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
		lol = re.findall(r".*PresenceManager: .*%s.*-r.*-l"%skype, open(log, 'r').read())
		for ip in lol:
			ip = ip.split("-r")[1].split("-l")[0]
			if ip not in ipAddresses and "40031" not in ip and "10042" not in ip:
				ipAddresses.append(ip)

	return ipAddresses

def writeToLog(skype, instance=instance):
	instance.Client.OpenUserInfoDialog(skype)
	#So we can resolve more than once
	instance.Client.Focus()
	instance.Client.Minimize()
	return True

class resolve:
	def GET(self, skype):
		web.header('Content-Type', 'application/json')
		try:
			ipDict = {'public': [], 'error': None, 'success': True}
			writeToLog(skype)
			time.sleep(2)
			ips = findIpAddresses(skype)
			for ip in ips:
				ipDict['public'].append(ip)
			if len(ipDict['public']) > 0:
				return json.dumps(ipDict)
			else:
				return json.dumps({'error': 'fail', 'success': False})
		except:
			return json.dumps({'error': 'fail', 'success': False})

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
