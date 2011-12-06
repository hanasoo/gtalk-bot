# -*- coding:utf-8 -*-

from google.appengine.api import capabilities

class StatusFetcher():

	def __init__(self):
		target = {
			'blobstore': 'blobstore',
			'datastore-read': ('datastore_v3', ['read']),
			'datastore-write': ('datastore_v3', ['write']),
			'image': 'images',
			'mail': 'mail',
			'memcache-set': ('memcache', [], ['set']),
			'memcache-get': ('memcache', [], ['get']),
			'taskqueue': 'taskqueue',
			'urlFetch': 'urlfetch',
			'xmpp': 'xmpp'
		}
		self.status = {}
		for k, v in target.items():
			if isinstance(v, tuple):
				cap = capabilities.CapabilitySet(*v)
			else:
				cap = capabilities.CapabilitySet(v)
			self.status[k] = {
				'enabled': cap.is_enabled(),
				'will_remain': cap.will_remain_enabled_for()
			}
			
	def get(self):
		return self.status
