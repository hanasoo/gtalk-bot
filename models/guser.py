# -*- coding:utf-8 -*-

from google.appengine.ext import db
from google.appengine.api import users

import gdata.gauth

class GUser(db.Model):
	domain = db.StringProperty()
	nickname = db.StringProperty()
	user = db.UserProperty(auto_current_user_add = True)
 	updated = db.DateTimeProperty(auto_now = True)
	created = db.DateTimeProperty(auto_now_add = True)

	def put(self, **kwds):
		email = self.key().name()
		self.nickname, self.domain = email.split('@')
		return super(self.__class__, self).put(**kwds)
		
	@property
	def email(self):
		return str(self.key().name())
	
	@property
	def token(self):
		token_key = 'access_token_%s' % self.email
		token = gdata.gauth.ae_load(token_key)
		return token if token else False
	
