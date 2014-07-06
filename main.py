import json
import Skype4Py
import web
import time
import re
import glob


urls = (
    '/api/(.*)', 'resolve',
    '/bypass/(.*)', 'bypass',
)

instance = Skype4Py.Skype()
instance.Attach()

def findIpAddresses(skype):
	ipAddresses = []
	logs = glob.glob('debug-*.log')
	print(logs)
	for log in logs:
		lol = re.findall(r".*PresenceManager:.*%s.*"%skype, open(log, 'r').read())
		for ip in lol:
			try:
				ip = ip.split('-r')[1].split('-l')[0]
				if ip not in ipAddresses:
					if ip not in ipAddresses and "10042" not in ip and "40031" not in ip and "33033" not in ip:
						ipAddresses.append(ip)
			except:
				continue
	return ipAddresses

def writeToLog(skype, instance=instance):
	instance.Client.OpenUserInfoDialog(skype)
	instance.Client.Focus()
	instance.Client.Minimize()
	instance.Client.Focus()
	instance.Client.Minimize()
	return True

def emailToSkype(skype):
	return

def blacklist(skype):
	blackListedSkypes = ['live:doxing_3']
	if skype in blackListedSkypes:
		return True
	else:
		return False

class resolve:
	def GET(self, skype):
		web.header('Content-Type', 'application/json')
		if blacklist(skype):
			return json.dumps({'error': 'blacklist', 'success': False})
		try:
			ipDict = {'public': [], 'error': None, 'success': True}
			writeToLog(skype)
			time.sleep(2)
			ips = findIpAddresses(skype)
			print ips
			for ip in ips:
				ipDict['public'].append(ip)
			if len(ipDict['public']) > 0:
				print(ipDict)
				return json.dumps(ipDict)
			else:
				return json.dumps({'error': 'not found', 'success': False})
		except:
			return json.dumps({'error': 'fail', 'success': False})


def writeBypassToLog(skype, instance=instance):
	for i in range(3):
		xd = instance.PlaceCall(skype)
		time.sleep(2)
		xd.Finish()
	return True

def findBypassIpAddresses(skype):
	ipAddresses = []
	logs = glob.glob('debug-*.log')
	for log in logs:
		lel = re.findall(r"withUser = %s .*\n.*#.*.*\n"%skype, open(log, 'r').read())
		for ip in lel:
			ip = re.findall(r"\b[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}\b", ip)
			for wot in ip:
				if wot.count('.') < 3 or wot in ipAddresses:
					continue
				if " " in wot:
					wot = wot.split(" ")[1]
				ipAddresses.append(wot.strip().rstrip())
	return ipAddresses

class bypass:
	def GET(self, skype):
		web.header('Content-Type', 'application/json')
		try:
			ipDict = {'public': [], 'error': None, 'success': True}
			writeBypassToLog(skype)
			ips = findBypassIpAddresses(skype)
			for ip in ips:
				ipDict['public'].append(ip)
			if len(ipDict['public']) > 0:
				return json.dumps(ipDict)
			else:
				return json.dumps({'error': 'not found', 'success': False})
		except:
			return json.dumps({'error': 'fail', 'success': False})

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
