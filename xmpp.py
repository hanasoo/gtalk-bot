# -*- coding:utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.api import xmpp
from wsgiref.handlers import CGIHandler

#import gdata.calendar
#import gdata.calendar.client
#import atom
#import atom.data

import datetime, logging, re, md5, random

from models.guser import GUser
from apps.calendar import BotCalendarClient
import settings, lang

class XMPPHandler(webapp.RequestHandler):
		
	def post(self):
		message = xmpp.Message(self.request.POST)
		from_params = self.request.get('from')
		from_user = from_params.split('/')[0] if '/' in from_params else from_params
		guser = GUser.get_or_insert(from_user)
		self.replyMessage(message, guser)
	
	def replyMessage(self, message, guser):
		logging.info('--- recieved: %s' % guser.email)
		logging.info('--- message: %s' % message.body)
		mbody = message.body.encode('utf-8')
		num = len(lang.TRIGGERS)
		act = self.greet
		for i in range(num):
			match = lang.TRIGGERS[i].search(mbody)
			if match:
				action_name = lang.TRIGGER_ACTION[i]
				self.actions[action_name](self, message, mbody, guser, match)
				break
		else:
			self.greet(message, mbody, guser)
	
	def sendMessage(self, message, mbody):
		message.reply(mbody)
		logging.info('--- response: %s' % mbody)
	
	#--------------------
	# reactions
	#--------------------
	
	def addEvent(self, message, mbody, guser, match=None):
		is_gigei = guser.email.endswith('@gigei.jp')
		dic = match.groupdict()
		start, end, resource, title = (int(dic['s']), int(dic['e']), dic['r'], dic['t'])
		client = BotCalendarClient(guser)
		
		if guser.token and is_gigei and resource and resource.lower() in settings.resource.keys():
			self.sendMessage(message, lang.MESSAGE['EVENT']['CHECK_AVAIL'])
			rid = settings.resource[resource.lower()]
			feed = client.getEvents(rid, start, end)
			logging.info(feed)
			if False:
				self.sendMessage(message, lang.MESSAGE['EVENT']['RESOURCE_BUSY'])
			return 0
		else:
			rid = None
			
		self.sendMessage(message, lang.MESSAGE['EVENT']['TRY'])
		if client.addEvent(title, start, end, rid):
			self.sendMessage(
				message,
				lang.MESSAGE['EVENT']['SUCCESS'] % (start, end, title.decode('utf-8')))
		else:
			self.sendMessage(message, lang.MESSAGE['EVENT']['FAILED'])
	
	def tellEvent(self, message, mbody, guser, match=None):
		rname = match.group()
		rid = settings.resource[rname.lower()]
		self.sendMessage(message, rid)
	
	def tellEventHelp(self, message, mbody, guser, match=None):
		self.sendMessage(message, lang.MESSAGE['EVENT']['NOIDEA'])

	def tellFortune(self, message, mbody, guser, match=None):
		h = int(md5.new(guser.email).hexdigest()[0:5], 16)
		h = h + datetime.datetime.today().day
		rbody = lang.MESSAGE['FORTUNE'][h % len(lang.MESSAGE['FORTUNE'])]
		self.sendMessage(message, rbody)

	def gatt(self, message, mbody, guser, match=None):
		self.sendMessage(message, lang.MESSAGE['NULL_POINTER'])

	def greet(self, message, mbody, guser, match=None):
		if match:
			self.sendMessage(
				message,
				u'%s %sさん！' % (match.group().decode('utf-8'), guser.nickname))
		else:
			if random.random() < 0.2:
				rbody = lang.MESSAGE['RANDOM'][random.randint(0, len(lang.MESSAGE['RANDOM'])-1)]
				self.sendMessage(message, rbody)
			else:
				rbody = lang.MESSAGE['GREET'][random.randint(0, len(lang.MESSAGE['GREET'])-1)]
				self.sendMessage(
					message,
					rbody % guser.nickname)

	actions = {
		'ADD_EVENT': addEvent,
		'TELL_EVENT': tellEvent,
		'TELL_EVENT_HELP': tellEventHelp,
		'GREET': greet,
		'TELL_FORTUNE': tellFortune,
		'NULL_POINTER': gatt}
		

"""
class XmppSend(webapp.RequestHandler):
	def get(self):
		to_address = setting.email #送信先のGmailアドレスをここに入力
		chat_message_sent = False

		xmpp.send_invite(to_address) #招待されてる、されていないにかかわらず送信先ユーザに招待状を送る

		if xmpp.get_presence(to_address): #送信先がオンラインの場合
			msg = "I'm Google Talk bot!"
			status_code = xmpp.send_message(to_address, msg)
			chat_message_sent = (status_code == xmpp.NO_ERROR)
		else:
			logging.info("送信先は現在オフラインです。")
			

		if chat_message_sent:
			self.response.out.write("正常に送信出来ました。");
		else:
			self.response.out.write("送信に失敗しました。");
"""

def main():
	application = webapp.WSGIApplication([
		('/_ah/xmpp/message/chat/', XMPPHandler)],
		debug=True)
	CGIHandler().run(application)

if __name__ == "__main__":
	main()

