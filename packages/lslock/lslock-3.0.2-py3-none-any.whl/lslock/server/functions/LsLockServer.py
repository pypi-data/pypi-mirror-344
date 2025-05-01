import threading
from typing import Dict

from lstools import utcnow

from lslock.exceptions import LsLockResourceAlreadyLocked, LsLockResourceNotOwned
from lslock.pydantic_models.TLock import TLock

import logging

log = logging.getLogger(__name__)


class LsLockServerLoggerAdapter(logging.LoggerAdapter):
	def __init__(self, logger):
		super(LsLockServerLoggerAdapter, self).__init__(logger, {})

	def process(self, msg, kwargs):
		return '[LsLockServer] %s' % (msg), kwargs


log = LsLockServerLoggerAdapter(log)


class LsLockServer(object):
	_locks: Dict[str, TLock] = {}
	_access_lock = threading.Lock()

	@classmethod
	def cleanup_expired_locks(cls):
		# log.debug("Cleaning up expired locks...")
		with cls._access_lock:
			expired_locks = [key for key, value in cls._locks.items() if value.expires and value.expires <= utcnow()]
			for key in expired_locks:
				log.debug(f"{cls._locks[key].resource} Released.")
				del cls._locks[key]

	@classmethod
	def acquire(cls, lock: TLock) -> bool:
		"""
		Acquires a lock on the server and stores it in memory.
		In case the resource is already locked, a error gets raised.

		:param lock:
		:return: bool - True if the lock was created, False if it was updated.
		"""
		cls.cleanup_expired_locks()
		log.debug(f"{lock.resource} Acquiring lock for {lock.account_id}")

		with cls._access_lock:
			if lock.resource_str in cls._locks:
				existing_lock = cls._locks[lock.resource_str]
				if existing_lock.account_id != lock.account_id:
					log.error(f"{lock.resource} Locked already by {existing_lock.account_id}.")
					raise LsLockResourceAlreadyLocked(lock.resource, lock.account_id, existing_lock.account_id)
				cls._locks[lock.resource_str] = lock
				log.debug(f"{lock.resource} Lock updated.")
				return False
			else:
				cls._locks[lock.resource_str] = lock
				log.debug(f"{lock.resource} Lock created.")
				return True

	@classmethod
	def release(cls, lock: TLock, force: bool = False) -> bool:
		cls.cleanup_expired_locks()

		log.debug(f"{lock.resource} Releasing lock.")
		with cls._access_lock:
			if lock.resource_str not in cls._locks:
				log.debug(f"{lock.resource} Not locked.")
				return False

			existing_lock = cls._locks[lock.resource_str]
			if existing_lock.account_id == lock.account_id or force:
				del cls._locks[lock.resource_str]
				log.debug(f"{lock.resource} Lock released.")
				return True
			else:
				log.error(f"{lock.resource} Lock owned by {existing_lock.account_id} and release not forced.")
				raise LsLockResourceNotOwned(lock, existing_lock)
