import datetime
from typing import List, Any

from am_auth_functions.context import am_auth_context
from lstools import utcnow
from pydantic import BaseModel


class TLockRequest(BaseModel):
	resource: List[Any]
	account_id: str | None = None
	expires: int | None = None
	include_org_id: bool | None = True
	force: bool | None = False


class TLock(BaseModel):
	resource: List[Any]
	account_id: str
	expires: datetime.datetime | None = None

	@property
	def resource_str(self):
		return "_".join(map(str, self.resource))

