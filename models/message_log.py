# -*- coding:utf-8 -*-

class MessageLog(db.Model):
  guser_email = db.EmailProperty()
  recieve_message = db.TextProperty()
  reply_message = db.TextProperty()
  updated = db.DateTimeProperty(auto_now = True)
  created = db.DateTimeProperty(auto_now_add = True)
