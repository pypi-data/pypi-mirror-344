from http import HTTPStatus
from typing import List, Any

from webexception.webexception import WebException

from lslock.pydantic_models.TLock import TLock


class LsLockResourceAlreadyLocked(WebException):
	status_code = HTTPStatus.LOCKED

	def __init__(self, resource: List[Any], account_id: str, existing_account_id: str, **kwargs) -> None:
		super().__init__(
			f"{resource} Locked already by {existing_account_id}.",
			resource=resource,
			account_id=account_id,
			existing_account_id=existing_account_id,
			**kwargs
		)


class LsLockResourceNotOwned(WebException):
	status_code = HTTPStatus.FORBIDDEN

	def __init__(self, lock: TLock, existing_lock: TLock, **kwargs) -> None:
		super().__init__(
			f"Resource {lock.resource} owned by {existing_lock.account_id}.",
			resource_str=lock.resource_str,
			account_id=lock.account_id,
			existing_account_id=existing_lock.account_id,
			**kwargs
		)
