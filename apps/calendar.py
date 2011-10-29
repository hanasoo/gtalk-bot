# -*- coding:utf-8 -*-

import gdata.gauth
import gdata.calendar.client
import atom
import atom.data

import logging, datetime, os
import settings

client = gdata.calendar.client.CalendarClient(source = settings.app_name)

class BotCalendarClient():
	def __init__(self, guser):
		logging.info('--- BotCalendarClient.__init__(%s)' % guser)
		self.guser = guser
		self.client = gdata.calendar.client.CalendarClient(source = settings.app_name)
		if guser.token:
			self.client.auth_token = guser.token
		else:
			self.client.ClientLogin(settings.reg_email, settings.reg_pass, settings.app_name)
			
	def addEvent(self, title, start, end, rid):
		logging.info('--- BotCalendarClient.addEvent(%s, %s, %s, %s)' % (title, start, end, rid))
		
		event = gdata.calendar.data.CalendarEventEntry()
		event.title = atom.data.Title(text = title)
		
		today = datetime.datetime.today()
		start_time = '%4d-%02d-%02dT%02d:00:00.000+09:00' % (today.year, today.month, today.day, start)
		end_time = '%4d-%02d-%02dT%02d:00:00.000+09:00' % (today.year, today.month, today.day, end)
		event.when.append(gdata.data.When(start = start_time, end = end_time))
		
		status = gdata.data.AttendeeStatus()
		status.value = 'ACCEPTED'
		who = gdata.calendar.data.EventWho(
			email = self.guser.email,
			attendee_status = status)
		event.who.append(who)
		
		if rid:
			who = gdata.calendar.data.EventWho(email = rid)
			event.who.append(who)
		
		event.guests_can_modify = gdata.calendar.data.GuestsCanModifyProperty(value='true')
		event.guests_can_see_guests = gdata.calendar.data.GuestsCanSeeGuestsProperty(value='true')
		event.guests_can_invite_others = gdata.calendar.data.GuestsCanInviteOthersProperty(value='true')
		anyone_can_add_self = atom.data.ExtensionElement(tag='anyoneCanAddSelf')
		anyone_can_add_self.attributes['value'] = 'true'
		event.extension_elements.append(anyone_can_add_self)
		
		try:
			new_event = self.client.InsertEvent(event)
		except Exception, e:
			logging.info(e.args)
			return False
		else:
			logging.info(new_event)
			return True
		
	def getEvents(self, cid, start, end):
		logging.info('--- BotCalendarClient.getEvent(%s, %s, %s)' % (rid, start, end))
		feeduri = "https://www.google.com/calendar/feeds/default/freebusy/busy-times/%s" % rid
		query = gdata.calendar.client.CalendarEventQuery(feeduri)
		
		today = datetime.datetime.today()
		start_time = '%4d-%02d-%02dT%02d:00:00.000+09:00' % (today.year, today.month, today.day, start)
		end_time = '%4d-%02d-%02dT%02d:00:00.000+09:00' % (today.year, today.month, today.day, end)
		query.start_min = start_time
		query.start_max = end_time
		query.singleevents = 'true'
		feed = self.client.GetCalendarEventFeed(q=query)
		return feed
