# -*- coding:utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app, login_required
from wsgiref.handlers import CGIHandler
from google.appengine.api import oauth
from google.appengine.api import users

import gdata.gauth
import gdata.calendar.client

import logging, os
import settings

client = gdata.calendar.client.CalendarClient(source = settings.app_name)

class MainHandler(webapp.RequestHandler):
	@login_required
	def get(self):
		current_user = users.get_current_user()
		access_token_key = 'access_token_%s' % current_user.email()
		access_token = gdata.gauth.ae_load(access_token_key)
		params = {'app_id': os.environ['APPLICATION_ID']}
		if access_token:
			params['login'] = True
		else:
			params['login'] = False

		fpath = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
		html = template.render(fpath, params)
		self.response.out.write(html)
	
class Fetcher(webapp.RequestHandler):
	
	@login_required
	def get(self):
		current_user = users.get_current_user()
		request_token = client.get_oauth_token(
			settings.scopes,
			'http://%s/step2' % self.request.host,
			settings.consumer_key,
			settings.consumer_secret)
		request_token_key = 'request_token_%s' % current_user.email()
		gdata.gauth.ae_save(request_token, request_token_key)
		approval_page_url = request_token.generate_authorization_url()
		self.redirect(str(approval_page_url))
		
class RequestTokenCallback(webapp.RequestHandler):
	@login_required
	def get(self):
		current_user = users.get_current_user()
		request_token_key = 'request_token_%s' % current_user.email()
		request_token = gdata.gauth.ae_load(request_token_key)
		gdata.gauth.authorize_request_token(request_token, self.request.uri)
		client.auth_token = client.get_access_token(request_token)
		access_token_key = 'access_token_%s' % current_user.email()
		gdata.gauth.ae_save(request_token, access_token_key)
		self.redirect('/')

class LogoutHandler(webapp.RequestHandler):
	def get(self):
		logout_url = users.create_logout_url('/')
		self.redirect(logout_url)
					
def main():
	application = webapp.WSGIApplication([
		('/step2', RequestTokenCallback),
		('/step1', Fetcher),
		('/logout', LogoutHandler),
		('/*', MainHandler)],
		debug=True)
	CGIHandler().run(application)

if __name__ == "__main__":
	main()

