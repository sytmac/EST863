#! /usr/bin/env python
#coding=utf-8
from config.url import urls
import web
import sys
from controllers.InputProcessing import Files
from controllers.InputProcessing import Cas
from controllers.InputProcessing import Smile

render = web.template.render('templates/')
class index(object):
    def GET(self):
        return render.upload()
app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()


