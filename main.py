import json
import Skype4Py
import web

urls = (
    '/api/(.*)', 'resolve'
)

instance = Skype4Py.Skype()
instance.Attach()

def resolveIt(skype, instance=instance):
	instance.Client.OpenUserInfoDialog(skype)

class resolve:
    def GET(self, skype):
        return resolveIt(skype)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
