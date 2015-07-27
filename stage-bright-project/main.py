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
import webapp2
import jinja2
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class User(ndb.Model):
    name = ndb.StringProperty()

class Speech(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    user_key = ndb.KeyProperty()
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
        speeches = Speech.query().fetch()
        speeches.sort(key=lambda x: x.date, reverse=True)
        template = env.get_template('account.html')
        variables = {'speeches': speeches}
        self.response.write(template.render(variables))

class ResourcesHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('resources.html')
        self.response.write(template.render())

class PrepHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('prep.html')
        self.response.write(template.render())

class PracticeHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('practice.html')
        self.response.write(template.render())

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('about.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/account', AccountHandler),
    ('/resources', ResourcesHandler),
    ('/prep', PrepHandler),
    ('/about', AboutHandler)
], debug=True)
