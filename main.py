import json
import Skype4Py
import web

urls = (
    '/api/(.*)', 'resolve'
)

instance = Skype4Py.Skype()
instance.Attach()

def writeToLog(skype, instance=instance):
	instance.Client.OpenUserInfoDialog(skype)
	instance.Hide()
	instance.Focus()
	return True

class resolve:
    def GET(self, skype):
        return writeToLog(skype)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
