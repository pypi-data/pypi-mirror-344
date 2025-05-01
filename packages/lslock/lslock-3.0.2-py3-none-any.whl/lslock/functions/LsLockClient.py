import lstools
from lsrestclient import LsRestClient
from pydantic_settings import BaseSettings
import logging

from lslock.exceptions import LsLockResourceAlreadyLocked
from lslock.pydantic_models.TLock import TLock, TLockRequest

log = logging.getLogger(__name__)


class LsLockClientSettings(BaseSettings):
	lslock_api_url: str


class LsLockClient(object):
	client_instance: LsRestClient | None = None

	@classmethod
	def init(cls):
		cls.client_instance = LsRestClient(name="lslock", base_url=LsLockClientSettings().lslock_api_url)

	@classmethod
	def client(cls):
		if LsLockClient.client_instance is None:
			cls.init()
		return cls.client_instance

	@classmethod
	def acquire(cls, lock: TLockRequest):
		client = cls.client()
		r = client.post("/lock/acquire", json=lock.model_dump())

		if r.status_code == 201:
			return True
		elif r.status_code == 200:
			return False
		elif r.status_code == 423:
			json = r.json()
			# print(json)
			payload = lstools.get(json, ['detail', 'error_payload'])
			raise LsLockResourceAlreadyLocked(lock.resource, lock.account_id, payload["existing_account_id"])
		else:
			raise Exception("Return code not processable.")


	@classmethod
	def reset(cls):
		cls.client_instance = None

	@classmethod
	def release(cls, lock: TLockRequest):
		client = cls.client()
		r = client.put("/lock/release", json=lock.model_dump())

		if r.status_code == 200:
			return True
		else:
			raise Exception("Return code not processable.")

