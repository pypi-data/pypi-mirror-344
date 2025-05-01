import time
from typing import List, Any

import logging

from lsidentity.contexts import LsiOrgId, LsiAccountId
from lslock.exceptions import LsLockResourceAlreadyLocked
from lslock.functions.LsLockClient import LsLockClient
from lslock.pydantic_models.TLock import TLock, TLockRequest

log = logging.getLogger(__name__)


class LsLockLoggerAdapter(logging.LoggerAdapter):
	def __init__(self, logger):
		super(LsLockLoggerAdapter, self).__init__(logger, {})

	def process(self, msg, kwargs):
		return '[LsLock] %s' % msg, kwargs


log = LsLockLoggerAdapter(log)


class LsLock(object):
	def __init__(
		self,
		resource: List[Any],
		include_org_id: bool | None = True,
		expires: int | None = 300,
		blocking: bool | None = True,
		interval: float | None = 2,
		max_retries: int | None = None
	):
		self._resource = resource
		self.include_org_id = include_org_id
		self.locked = False
		self.created = False
		self.expires = expires
		self.blocking = blocking
		self.interval = interval
		self.retries = max_retries
		self.retry = 0

	@property
	def resource(self):
		if self.include_org_id:
			org_id = LsiOrgId().get()
			resource = [org_id, *self._resource] if org_id is not None else self._resource
		else:
			resource = self._resource

		return resource

	def acquire(self) -> bool:

		lock_request = TLockRequest(
			resource=self.resource,
			account_id=LsiAccountId().get(),
			org_id=LsiOrgId().get(),
			expires=self.expires,
			include_org_id=self.include_org_id,
		)
		while not self.locked and self.blocking and (self.retries is None or self.retry <= self.retries):
			try:
				created = LsLockClient.acquire(lock_request)
				self.locked = True
				if created:
					self.created = True
					log.debug(f"{self.resource} Locked.")
				else:
					log.debug(f"{self.resource} Updated.")

			except LsLockResourceAlreadyLocked as e:
				time.sleep(self.interval)
				self.retry += 1
				continue
			except Exception as e:
				raise e

		return self.locked

	def release(self, force: bool | None = None):
		force = False if force is None else force
		if self.locked and self.created:
			lock_request = TLockRequest(
				resource=self.resource,
				account_id=LsiAccountId().get(),
				org_id=LsiOrgId().get(),
				force=force,
				include_org_id=self.include_org_id,
			)
			LsLockClient.release(lock_request)
		log.debug(f"{self.resource} Released")
		self.locked = False
		self.retry = 0

	__enter__ = acquire

	def __exit__(self, t, v, tb):
		self.release()

	def status(self):
		return self.locked
