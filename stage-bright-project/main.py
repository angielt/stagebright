#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import time
import webapp2
import jinja2
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class Speech(ndb.Model):
    user_email = ndb.StringProperty()
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    date = ndb.DateTimeProperty(required=True, auto_now=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is None: #the user is not logged in
            login_url = users.create_login_url('/')
            self.response.write('<a href="%s">Log In</a>' % login_url)
        else: #the user is logged in
            logout_url = users.create_logout_url('/')
            self.response.write('Hello, %s!' % user.email())
            self.response.write('<a href="%s"> Log Out</a>' % logout_url)
        template = env.get_template('main.html')
        variables = {'user': user}
        self.response.write(template.render(variables))

class AccountHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        login_url = users.create_login_url('/')
        if user is None:
            self.redirect("%s" % login_url)
        else:
            logout_url = users.create_logout_url('/')
            self.response.write('Hello, %s!' % user.email())
            self.response.write('<a href="%s"> Log Out </a>' % logout_url)
            speeches = Speech.query(Speech.user_email == users.get_current_user().email()).fetch()
            speeches.sort(key=lambda x: x.date, reverse=True)
            template = env.get_template('account.html')
            variables = {'speeches': speeches}
            self.response.write(template.render(variables))
    def post(self):
        content = self.request.get('content')
        title = self.request.get('title')
        speech = Speech(user_email=users.get_current_user().email(),
                        title=title,
                        content=content,
                        date=datetime.datetime.now())
        speech.put()
        time.sleep(1)
        return self.redirect("/account")

# class TeleprompterHandler(webapp2.RequestHandler):
#     def get(self):

class PrepHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('prep.html')
        self.response.write(template.render())

class PracticeHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('practice.html')
        self.response.write(template.render())

class VideosHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('videos.html')
        self.response.write(template.render())

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('about.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/account', AccountHandler),
    # ('/prep', PrepHandler),
    # ('/practice', PracticeHandler)
    # ('/teleprompter', TeleprompterHandler),
    ('/videos', VideosHandler),
    # ('/articles', ArticlesHandler),
    # ('/tips', TipsHandler),
    ('/about', AboutHandler),
], debug=True)
